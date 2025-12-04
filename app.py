from flask import Flask, render_template, request, redirect, url_for, flash
from db_utils import (
    get_all_regions, add_region,
    get_all_sources, add_source,
    get_all_categories, add_category,
    get_all_countries, add_country, update_country, get_country_by_code,
    get_all_indicators, add_indicator,
    get_data_by_country, add_indicator_data,
    get_yearly_indicator_average,
    get_global_population,
    get_global_gdp,
    get_global_life_expectancy,
    get_latest_population_by_country,
    get_indicators_by_category_name,
    execute,
    get_health_indicators,
    get_economy_indicators,
    get_education_indicators,
    get_indicators_by_category_id,
    get_indicators_with_data,
    get_countries_with_data
)
import db_utils
import pending_utils
import auth

app = Flask(__name__)
app.secret_key = 'your-secret-key-here-change-in-production'

@app.route('/search')
def search():
    """Global search across all tables"""
    query = request.args.get('q', '')
    
    if not query:
        return redirect(url_for('index'))
    
    results = {
        'countries': execute(
            "SELECT * FROM Countries WHERE country_name LIKE %s OR country_code LIKE %s LIMIT 20",
            (f"%{query}%", f"%{query}%"),
            fetch=True
        ),
        'indicators': execute(
            "SELECT * FROM Indicators WHERE indicator_name LIKE %s OR indicator_code LIKE %s LIMIT 20",
            (f"%{query}%", f"%{query}%"),
            fetch=True
        ),
        'regions': execute(
            "SELECT * FROM Regions WHERE region_name LIKE %s LIMIT 20",
            (f"%{query}%",),
            fetch=True
        ),
        'sources': execute(
            "SELECT * FROM Sources WHERE source_name LIKE %s LIMIT 20",
            (f"%{query}%",),
            fetch=True
        )
    }
    
    return render_template('search.html', query=query, results=results)

@app.route('/')
def index():
    """Dashboard with stats and charts"""
    # Regions and Sources return just the list
    regions = db_utils.get_all_regions()
    sources = db_utils.get_all_sources()
    total_regions = len(regions)
    total_sources = len(sources)

    # Countries and Indicators return (items, count)
    _, total_countries = db_utils.get_all_countries()
    _, total_indicators = db_utils.get_all_indicators()
    
    # Get chart data
    population_data = db_utils.get_global_population()
    gdp_data = db_utils.get_global_gdp()
    life_expectancy_data = db_utils.get_global_life_expectancy()
    country_populations = db_utils.get_latest_population_by_country()
    recent_activity = db_utils.get_recent_activity()
    
    return render_template('index.html',
                         total_regions=total_regions,
                         total_countries=total_countries,
                         total_indicators=total_indicators,
                         total_sources=total_sources,
                         population_data=population_data,
                         gdp_data=gdp_data,
                         life_expectancy_data=life_expectancy_data,
                         country_populations=country_populations,
                         recent_activity=recent_activity)

@app.route('/regions')
def regions():
    """List all regions"""
    search = request.args.get('search')
    all_regions = db_utils.get_all_regions(search_query=search)
    return render_template('regions.html', regions=all_regions, search=search)

@app.route('/regions/add', methods=['GET', 'POST'])
def add_region_route():
    """Add a new region"""
    if request.method == 'POST':
        name = request.form.get('region_name')
        code = request.form.get('region_code')
        
        if name:
            data = {'region_name': name, 'region_code': code}
            pending_utils.submit_change('Regions', 'INSERT', data)
            flash(f'Region "{name}" submitted for approval!', 'info')
            return redirect(url_for('regions'))
            
    return render_template('region_form.html', action="Add")

@app.route('/regions/edit/<int:id>', methods=['GET', 'POST'])
def edit_region(id):
    """Edit a region"""
    if request.method == 'POST':
        name = request.form.get('region_name')
        code = request.form.get('region_code')
        
        if name:
            data = {'region_name': name, 'region_code': code}
            pending_utils.submit_change('Regions', 'UPDATE', data, record_id=id)
            flash(f'Changes for "{name}" submitted for approval!', 'info')
            return redirect(url_for('regions'))
            
    region = db_utils.get_region_by_id(id)
    return render_template('region_form.html', action="Edit", region=region)

@app.route('/regions/delete/<int:id>')
def delete_region_route(id):
    """Delete a region"""
    region = db_utils.get_region_by_id(id)
    if region:
        pending_utils.submit_change('Regions', 'DELETE', {}, record_id=id)
        flash(f'Deletion request for "{region["region_name"]}" submitted for approval!', 'info')
    return redirect(url_for('regions'))

@app.route('/countries')
def countries():
    """List all countries"""
    search = request.args.get('search')
    page = request.args.get('page', 1, type=int)
    per_page = 1000
    
    all_countries, total_count = get_all_countries(page=page, per_page=per_page, search_query=search)
    total_pages = (total_count + per_page - 1) // per_page
    
    return render_template('countries.html', 
                         countries=all_countries, 
                         page=page, 
                         total_pages=total_pages,
                         search=search)

@app.route('/countries/add', methods=['GET', 'POST'])
def add_country_route():
    """Add a new country"""
    if request.method == 'POST':
        code = request.form.get('country_code')
        name = request.form.get('country_name')
        capital = request.form.get('capital_city')
        region_id = request.form.get('region_id')
        income_level = request.form.get('income_level')
        
        if code and name and region_id and income_level:
            # Submit to pending changes instead of direct add
            data = {
                'country_code': code,
                'country_name': name,
                'capital_city': capital,
                'region_id': region_id,
                'income_level': income_level
            }
            pending_utils.submit_change('Countries', 'INSERT', data)
            flash(f'Country "{name}" submitted for approval!', 'info')
            return redirect(url_for('countries'))
            
    # GET request: Show form
    all_regions = db_utils.get_all_regions()
    return render_template('country_form.html', action="Add", regions=all_regions)

@app.route('/countries/edit/<code>', methods=['GET', 'POST'])
def edit_country(code):
    """Edit a country"""
    if request.method == 'POST':
        new_code = request.form.get('country_code')
        name = request.form.get('country_name')
        capital = request.form.get('capital_city')
        region_id = request.form.get('region_id')
        income_level = request.form.get('income_level')
        
        if new_code and name and region_id and income_level:
            data = {
                'country_code': new_code,
                'country_name': name,
                'capital_city': capital,
                'region_id': region_id,
                'income_level': income_level
            }
            # For update, we pass the original code as record_id
            pending_utils.submit_change('Countries', 'UPDATE', data, record_id=code)
            flash(f'Changes for "{name}" submitted for approval!', 'info')
            return redirect(url_for('countries'))
    
    country = get_country_by_code(code)
    all_regions = db_utils.get_all_regions()
    return render_template('country_form.html', action="Edit", country=country, regions=all_regions)

@app.route('/countries/delete/<code>')
def delete_country_route(code):
    """Delete a country"""
    country = get_country_by_code(code)
    if country:
        pending_utils.submit_change('Countries', 'DELETE', {}, record_id=code)
        flash(f'Deletion request for "{country["country_name"]}" submitted for approval!', 'info')
    return redirect(url_for('countries'))

@app.route('/sources')
def sources():
    """List all sources"""
    search = request.args.get('search')
    all_sources = db_utils.get_all_sources(search_query=search)
    return render_template('sources.html', sources=all_sources, search=search)

@app.route('/sources/add', methods=['GET', 'POST'])
def add_source_route():
    """Add a new source"""
    if request.method == 'POST':
        name = request.form.get('source_name')
        org = request.form.get('source_organization')
        url = request.form.get('source_url')
        desc = request.form.get('description')
        
        if name:
            data = {
                'source_name': name,
                'source_organization': org,
                'source_url': url,
                'description': desc
            }
            pending_utils.submit_change('Sources', 'INSERT', data)
            flash(f'Source "{name}" submitted for approval!', 'info')
            return redirect(url_for('sources'))
            
    return render_template('source_form.html', action="Add")

@app.route('/sources/edit/<int:id>', methods=['GET', 'POST'])
def edit_source(id):
    """Edit a source"""
    if request.method == 'POST':
        name = request.form.get('source_name')
        org = request.form.get('source_organization')
        url = request.form.get('source_url')
        desc = request.form.get('description')
        
        if name:
            data = {
                'source_name': name,
                'source_organization': org,
                'source_url': url,
                'description': desc
            }
            pending_utils.submit_change('Sources', 'UPDATE', data, record_id=id)
            flash(f'Changes for "{name}" submitted for approval!', 'info')
            return redirect(url_for('sources'))
            
    source = db_utils.get_source_by_id(id)
    return render_template('source_form.html', action="Edit", source=source)

@app.route('/sources/delete/<int:id>')
def delete_source_route(id):
    """Delete a source"""
    source = db_utils.get_source_by_id(id)
    if source:
        pending_utils.submit_change('Sources', 'DELETE', {}, record_id=id)
        flash(f'Deletion request for "{source["source_name"]}" submitted for approval!', 'info')
    return redirect(url_for('sources'))

@app.route('/indicators')
def indicators():
    """List all indicators"""
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search')
    per_page = 1000
    
    all_indicators, total_count = db_utils.get_all_indicators(page=page, per_page=per_page, search_query=search)
    total_pages = (total_count + per_page - 1) // per_page
    
    return render_template('indicators.html', 
                         indicators=all_indicators, 
                         page=page, 
                         total_pages=total_pages,
                         endpoint='indicators',
                         search=search)

@app.route('/categories')
def categories():
    """List all categories"""
    search = request.args.get('search')
    page = request.args.get('page', 1, type=int)
    per_page = 1000
    
    all_categories, total_count = db_utils.get_all_categories(page=page, per_page=per_page, search_query=search)
    total_pages = (total_count + per_page - 1) // per_page
    
    return render_template('categories.html', 
                         categories=all_categories,
                         page=page,
                         total_pages=total_pages,
                         search=search)

@app.route('/categories/add', methods=['GET', 'POST'])
def add_category_route():
    """Add a new category"""
    if request.method == 'POST':
        name = request.form.get('category_name')
        description = request.form.get('description')
        
        if name:
            data = {'category_name': name, 'description': description}
            pending_utils.submit_change('IndicatorCategories', 'INSERT', data)
            flash(f'Category "{name}" submitted for approval!', 'info')
            return redirect(url_for('categories'))
            
    return render_template('category_form.html', action="Add")

@app.route('/categories/edit/<int:id>', methods=['GET', 'POST'])
def edit_category(id):
    """Edit a category"""
    if request.method == 'POST':
        name = request.form.get('category_name')
        description = request.form.get('description')
        
        if name:
            data = {'category_name': name, 'description': description}
            pending_utils.submit_change('IndicatorCategories', 'UPDATE', data, record_id=id)
            flash(f'Changes for "{name}" submitted for approval!', 'info')
            return redirect(url_for('categories'))
            
    category = db_utils.get_category_by_id(id)
    return render_template('category_form.html', action="Edit", category=category)

@app.route('/categories/delete/<int:id>')
def delete_category_route(id):
    """Delete a category"""
    category = db_utils.get_category_by_id(id)
    if category:
        pending_utils.submit_change('IndicatorCategories', 'DELETE', {}, record_id=id)
        flash(f'Deletion request for "{category["category_name"]}" submitted for approval!', 'info')
    return redirect(url_for('categories'))

@app.route('/categories/<int:category_id>')
def category_detail(category_id):
    """List indicators for a specific category"""
    page = request.args.get('page', 1, type=int)
    per_page = 1000
    
    # Get category name for title
    # Get category name for title
    category = db_utils.get_category_by_id(category_id)
    category_name = category['category_name'] if category else "Category Indicators"
            
    indicators, total_count = get_indicators_by_category_id(category_id, page, per_page)
    total_pages = (total_count + per_page - 1) // per_page
    
    return render_template('category_indicators.html', 
                         title=category_name, 
                         indicators=indicators,
                         page=page,
                         total_pages=total_pages,
                         endpoint='category_detail',
                         category_id=category_id)

@app.route('/health')
def health():
    """List health indicators"""
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search')
    per_page = 1000
    
    indicators, total_count = db_utils.get_health_indicators(page, per_page, search_query=search)
    total_pages = (total_count + per_page - 1) // per_page
    
    return render_template('health_indicators.html', 
                         indicators=indicators,
                         page=page,
                         total_pages=total_pages,
                         endpoint='health',
                         search=search)

@app.route('/education')
def education():
    """List education indicators"""
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search')
    per_page = 1000
    
    indicators, total_count = db_utils.get_education_indicators(page, per_page, search_query=search)
    total_pages = (total_count + per_page - 1) // per_page
    
    return render_template('education_indicators.html', 
                         indicators=indicators,
                         page=page,
                         total_pages=total_pages,
                         endpoint='education',
                         search=search)

@app.route('/economy')
def economy():
    """List economy indicators"""
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search')
    per_page = 1000
    
    indicators, total_count = db_utils.get_economy_indicators(page, per_page, search_query=search)
    total_pages = (total_count + per_page - 1) // per_page
    
    return render_template('economy_indicators.html', 
                         indicators=indicators,
                         page=page,
                         total_pages=total_pages,
                         endpoint='economy',
                         search=search)

@app.route('/indicators/add', methods=['GET', 'POST'])
def add_indicator_route():
    """Add a new indicator"""
    if request.method == 'POST':
        code = request.form.get('indicator_code')
        name = request.form.get('indicator_name')
        source_id = request.form.get('source_id')
        category_id = request.form.get('category_id')
        definition = request.form.get('long_definition')
        
        if code and name and source_id and category_id:
            data = {
                'indicator_code': code,
                'indicator_name': name,
                'source_id': source_id,
                'category_id': category_id,
                'long_definition': definition
            }
            pending_utils.submit_change('Indicators', 'INSERT', data)
            flash(f'Indicator "{name}" submitted for approval!', 'info')
            return redirect(url_for('indicators'))
            
    all_sources = db_utils.get_all_sources()
    all_categories = db_utils.get_all_categories()
    return render_template('indicator_form.html', action="Add", sources=all_sources, categories=all_categories)

@app.route('/indicators/edit/<code>', methods=['GET', 'POST'])
def edit_indicator(code):
    """Edit an indicator"""
    if request.method == 'POST':
        new_code = request.form.get('indicator_code')
        name = request.form.get('indicator_name')
        source_id = request.form.get('source_id')
        category_id = request.form.get('category_id')
        definition = request.form.get('long_definition')
        
        if new_code and name and source_id and category_id:
            data = {
                'indicator_code': new_code,
                'indicator_name': name,
                'source_id': source_id,
                'category_id': category_id,
                'long_definition': definition
            }
            pending_utils.submit_change('Indicators', 'UPDATE', data, record_id=code)
            flash(f'Changes for "{name}" submitted for approval!', 'info')
            return redirect(url_for('indicators'))
            
    indicator = db_utils.get_indicator_by_code(code)
    all_sources = db_utils.get_all_sources()
    all_categories = db_utils.get_all_categories()
    return render_template('indicator_form.html', action="Edit", indicator=indicator, sources=all_sources, categories=all_categories)

@app.route('/indicators/delete/<code>')
def delete_indicator_route(code):
    """Delete an indicator"""
    indicator = db_utils.get_indicator_by_code(code)
    if indicator:
        pending_utils.submit_change('Indicators', 'DELETE', {}, record_id=code)
        flash(f'Deletion request for "{indicator["indicator_name"]}" submitted for approval!', 'info')
    return redirect(url_for('indicators'))

@app.route('/data')
def indicator_data_list():
    """List all indicator data with pagination"""
    page = request.args.get('page', 1, type=int)
    indicator_code = request.args.get('indicator_code')
    search = request.args.get('search')
    per_page = 1000
    offset = (page - 1) * per_page
    
    if indicator_code:
        # Get count
        count_query = "SELECT COUNT(*) as count FROM IndicatorData WHERE indicator_code = %s"
        count_res = execute(count_query, (indicator_code,), fetch=True)
        total_count = count_res[0]['count'] if count_res else 0
        
        # Get data
        data = execute("""
            SELECT 
                d.year, d.value, d.footnote,
                c.country_name, d.country_code,
                i.indicator_name, d.indicator_code
            FROM IndicatorData d
            JOIN Countries c ON d.country_code = c.country_code
            JOIN Indicators i ON d.indicator_code = i.indicator_code
            WHERE d.indicator_code = %s
            ORDER BY d.year DESC, c.country_name ASC
            LIMIT %s OFFSET %s
        """, (indicator_code, per_page, offset), fetch=True)
    elif search:
        # Search query
        search_term = f"%{search}%"
        count_query = """
            SELECT COUNT(*) as count 
            FROM IndicatorData d
            JOIN Countries c ON d.country_code = c.country_code
            JOIN Indicators i ON d.indicator_code = i.indicator_code
            WHERE c.country_name LIKE %s OR i.indicator_name LIKE %s OR d.year LIKE %s
        """
        count_res = execute(count_query, (search_term, search_term, search_term), fetch=True)
        total_count = count_res[0]['count'] if count_res else 0
        
        data = execute("""
            SELECT 
                d.year, d.value, d.footnote,
                c.country_name, d.country_code,
                i.indicator_name, d.indicator_code
            FROM IndicatorData d
            JOIN Countries c ON d.country_code = c.country_code
            JOIN Indicators i ON d.indicator_code = i.indicator_code
            WHERE c.country_name LIKE %s OR i.indicator_name LIKE %s OR d.year LIKE %s
            ORDER BY d.year DESC, c.country_name ASC
            LIMIT %s OFFSET %s
        """, (search_term, search_term, search_term, per_page, offset), fetch=True)
    else:
        # Get count
        count_res = execute("SELECT COUNT(*) as count FROM IndicatorData", fetch=True)
        total_count = count_res[0]['count'] if count_res else 0
        
        # Get data
        data = execute("""
            SELECT 
                d.year, d.value, d.footnote,
                c.country_name, d.country_code,
                i.indicator_name, d.indicator_code
            FROM IndicatorData d
            JOIN Countries c ON d.country_code = c.country_code
            JOIN Indicators i ON d.indicator_code = i.indicator_code
            ORDER BY d.year DESC, c.country_name ASC
            LIMIT %s OFFSET %s
        """, (per_page, offset), fetch=True)
    
    total_pages = (total_count + per_page - 1) // per_page
    
    return render_template('indicator_data_list.html', 
                         data=data,
                         page=page,
                         total_pages=total_pages,
                         indicator_code=indicator_code,
                         search=search)

@app.route('/analyze', methods=['GET', 'POST'])
def analyze():
    """Custom chart builder"""
    # Only get countries and indicators that have actual data
    countries = db_utils.get_countries_with_data()
    indicators = db_utils.get_indicators_with_data()
    
    chart_data = None
    selected_country = None
    selected_indicator = None
    start_year = None
    end_year = None
    chart_title = ""
    
    if request.method == 'POST':
        selected_country = request.form.get('country_code')
        selected_indicator = request.form.get('indicator_code')
        start_year = request.form.get('start_year')
        end_year = request.form.get('end_year')
        
        if selected_country and selected_indicator:
            chart_data = db_utils.get_chart_data(selected_country, selected_indicator, start_year, end_year)
            
            # Get names for title
            country = db_utils.get_country_by_code(selected_country)
            indicator = db_utils.get_indicator_by_code(selected_indicator)
            
            if country and indicator:
                chart_title = f"{indicator['indicator_name']} - {country['country_name']}"
    
    return render_template('analyze.html',
                         countries=countries,
                         indicators=indicators,
                         chart_data=chart_data,
                         selected_country=selected_country,
                         selected_indicator=selected_indicator,
                         start_year=start_year,
                         end_year=end_year,
                         chart_title=chart_title)

@app.route('/data/<country_code>')
def indicator_data(country_code):
    """View indicator data for a specific country"""
    country = get_country_by_code(country_code)
    data = db_utils.get_data_by_country(country_code)
    all_indicators, _ = db_utils.get_all_indicators(per_page=20000)
    
    return render_template('indicator_data.html',
                         country=country,
                         data=data,
                         indicators=all_indicators)

@app.route('/data/add', methods=['GET', 'POST'])
def add_data_route():
    """Add new indicator data"""
    if request.method == 'POST':
        country_code = request.form.get('country_code')
        indicator_code = request.form.get('indicator_code')
        year = request.form.get('year')
        value = request.form.get('value')
        
        if country_code and indicator_code and year and value:
            data = {
                'country_code': country_code,
                'indicator_code': indicator_code,
                'year': year,
                'value': value
            }
            pending_utils.submit_change('IndicatorData', 'INSERT', data)
            flash('Data entry submitted for approval!', 'info')
            return redirect(url_for('indicator_data_list'))
            
    all_countries, _ = get_all_countries(per_page=1000)
    all_indicators, _ = db_utils.get_all_indicators(per_page=20000)
    return render_template('data_form.html', action="Add", countries=all_countries, indicators=all_indicators)

@app.route('/data/edit/<country_code>/<indicator_code>/<year>', methods=['GET', 'POST'])
def edit_data(country_code, indicator_code, year):
    """Edit indicator data"""
    if request.method == 'POST':
        value = request.form.get('value')
        
        if value:
            data = {'value': value}
            # Composite key for record_id
            record_id = f"{country_code}|{indicator_code}|{year}"
            pending_utils.submit_change('IndicatorData', 'UPDATE', data, record_id=record_id)
            flash('Changes submitted for approval!', 'info')
            return redirect(url_for('indicator_data_list'))
            
    data_entry = db_utils.get_data_by_composite_key(country_code, indicator_code, year)
    return render_template('data_form.html', action="Edit", data_entry=data_entry)

@app.route('/data/delete/<country_code>/<indicator_code>/<year>')
def delete_data_route(country_code, indicator_code, year):
    """Delete indicator data"""
    record_id = f"{country_code}|{indicator_code}|{year}"
    pending_utils.submit_change('IndicatorData', 'DELETE', {}, record_id=record_id)
    flash('Deletion request submitted for approval!', 'info')
    return redirect(url_for('indicator_data_list'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Admin login page"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if auth.login_user(username, password):
            flash('Welcome back, Admin!', 'success')
            return redirect(url_for('admin_panel'))
        else:
            flash('Invalid username or password', 'error')
            
    return render_template('login.html')

@app.route('/logout')
def logout():
    """Logout user"""
    auth.logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

@app.route('/admin')
@auth.login_required
def admin_panel():
    """Admin panel to view pending changes"""
    pending_changes = pending_utils.get_pending_changes()
    return render_template('admin.html', changes=pending_changes)

@app.route('/admin/approve/<int:change_id>')
@auth.login_required
def approve_change_route(change_id):
    """Approve a pending change"""
    success, message = pending_utils.approve_change(change_id)
    if success:
        flash(message, 'success')
    else:
        flash(f'Error: {message}', 'error')
    return redirect(url_for('admin_panel'))

@app.route('/admin/reject/<int:change_id>')
@auth.login_required
def reject_change_route(change_id):
    """Reject a pending change"""
    pending_utils.reject_change(change_id)
    flash('Change rejected', 'info')
    return redirect(url_for('admin_panel'))

if __name__ == '__main__':
    app.run(debug=True, port=5001)