import pandas as pd
from io import BytesIO
from flask import send_file
from datetime import datetime

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
import auth

app = Flask(__name__)
app.secret_key = 'your-secret-key-here-change-in-production'

@app.context_processor
def inject_auth():
    return dict(auth_module=auth)

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
    country_gdp = db_utils.get_latest_gdp_by_country()
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
                         country_gdp=country_gdp,
                         recent_activity=recent_activity)

@app.route('/regions')
def regions():
    """List all regions"""
    search = request.args.get('search')
    all_regions = db_utils.get_all_regions(search_query=search)
    return render_template('regions.html', regions=all_regions, search=search)

@app.route('/regions/add', methods=['GET', 'POST'])
@auth.login_required
def add_region_route():
    """Add a new region"""
    if request.method == 'POST':
        name = request.form.get('region_name')
        code = request.form.get('region_code')
        
        if name:
            db_utils.add_region(name, code)
            flash(f'Region "{name}" added successfully!', 'success')
            return redirect(url_for('regions'))
            
    return render_template('region_form.html', action="Add")

@app.route('/regions/edit/<int:id>', methods=['GET', 'POST'])
@auth.login_required
def edit_region(id):
    """Edit a region"""
    if request.method == 'POST':
        name = request.form.get('region_name')
        code = request.form.get('region_code')
        
        if name:
            db_utils.update_region(id, name, code)
            flash(f'Region "{name}" updated successfully!', 'success')
            return redirect(url_for('regions'))
            
    region = db_utils.get_region_by_id(id)
    return render_template('region_form.html', action="Edit", region=region)

@app.route('/regions/delete/<int:id>')
@auth.login_required
def delete_region_route(id):
    """Delete a region"""
    region = db_utils.get_region_by_id(id)
    if region:
        db_utils.delete_region(id)
        flash(f'Region "{region["region_name"]}" deleted successfully!', 'success')
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
@auth.login_required
def add_country_route():
    """Add a new country"""
    if request.method == 'POST':
        code = request.form.get('country_code')
        name = request.form.get('country_name')
        capital = request.form.get('capital_city')
        region_id = request.form.get('region_id')
        income_level = request.form.get('income_level')
        
        if code and name and region_id and income_level:
            db_utils.add_country(code, name, capital, region_id, income_level)
            flash(f'Country "{name}" added successfully!', 'success')
            return redirect(url_for('countries'))
            
    # GET request: Show form
    all_regions = db_utils.get_all_regions()
    return render_template('country_form.html', action="Add", regions=all_regions)

@app.route('/countries/edit/<code>', methods=['GET', 'POST'])
@auth.login_required
def edit_country(code):
    """Edit a country"""
    if request.method == 'POST':
        new_code = request.form.get('country_code')
        name = request.form.get('country_name')
        capital = request.form.get('capital_city')
        region_id = request.form.get('region_id')
        income_level = request.form.get('income_level')
        
        if name and region_id and income_level:
            db_utils.update_country(code, name, capital, region_id, income_level)
            flash(f'Country "{name}" updated successfully!', 'success')
            return redirect(url_for('countries'))
    
    country = get_country_by_code(code)
    all_regions = db_utils.get_all_regions()
    return render_template('country_form.html', action="Edit", country=country, regions=all_regions)

@app.route('/countries/delete/<code>')
@auth.login_required
def delete_country_route(code):
    """Delete a country"""
    country = get_country_by_code(code)
    if country:
        db_utils.delete_country(code)
        flash(f'Country "{country["country_name"]}" deleted successfully!', 'success')
    return redirect(url_for('countries'))

@app.route('/sources')
def sources():
    """List all sources"""
    search = request.args.get('search')
    all_sources = db_utils.get_all_sources(search_query=search)
    return render_template('sources.html', sources=all_sources, search=search)

@app.route('/sources/add', methods=['GET', 'POST'])
@auth.login_required
def add_source_route():
    """Add a new source"""
    if request.method == 'POST':
        name = request.form.get('source_name')
        org = request.form.get('source_organization')
        url = request.form.get('source_url')
        desc = request.form.get('description')
        
        if name:
            db_utils.add_source(name, org, url, desc)
            flash(f'Source "{name}" added successfully!', 'success')
            return redirect(url_for('sources'))
            
    return render_template('source_form.html', action="Add")

@app.route('/sources/edit/<int:id>', methods=['GET', 'POST'])
@auth.login_required
def edit_source(id):
    """Edit a source"""
    if request.method == 'POST':
        name = request.form.get('source_name')
        org = request.form.get('source_organization')
        url = request.form.get('source_url')
        desc = request.form.get('description')
        
        if name:
            db_utils.update_source(id, name, org, url, desc)
            flash(f'Source "{name}" updated successfully!', 'success')
            return redirect(url_for('sources'))
            
    source = db_utils.get_source_by_id(id)
    return render_template('source_form.html', action="Edit", source=source)

@app.route('/sources/delete/<int:id>')
@auth.login_required
def delete_source_route(id):
    """Delete a source"""
    source = db_utils.get_source_by_id(id)
    if source:
        db_utils.delete_source(id)
        flash(f'Source "{source["source_name"]}" deleted successfully!', 'success')
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
@auth.login_required
def add_category_route():
    """Add a new category"""
    if request.method == 'POST':
        name = request.form.get('category_name')
        description = request.form.get('description')
        
        if name:
            db_utils.add_category(name, description)
            flash(f'Category "{name}" added successfully!', 'success')
            return redirect(url_for('categories'))
            
    return render_template('category_form.html', action="Add")

@app.route('/categories/edit/<int:id>', methods=['GET', 'POST'])
@auth.login_required
def edit_category(id):
    """Edit a category"""
    if request.method == 'POST':
        name = request.form.get('category_name')
        description = request.form.get('description')
        
        if name:
            db_utils.update_category(id, name, description)
            flash(f'Category "{name}" updated successfully!', 'success')
            return redirect(url_for('categories'))
            
    category = db_utils.get_category_by_id(id)
    return render_template('category_form.html', action="Edit", category=category)

@app.route('/categories/delete/<int:id>')
@auth.login_required
def delete_category_route(id):
    """Delete a category"""
    category = db_utils.get_category_by_id(id)
    if category:
        db_utils.delete_category(id)
        flash(f'Category "{category["category_name"]}" deleted successfully!', 'success')
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
@auth.login_required
def add_indicator_route():
    """Add a new indicator"""
    if request.method == 'POST':
        code = request.form.get('indicator_code')
        name = request.form.get('indicator_name')
        source_id = request.form.get('source_id')
        category_id = request.form.get('category_id')
        definition = request.form.get('long_definition')
        
        if code and name and source_id and category_id:
            db_utils.add_indicator(code, name, source_id, category_id, definition)
            flash(f'Indicator "{name}" added successfully!', 'success')
            return redirect(url_for('indicators'))
            
    all_sources = db_utils.get_all_sources()
    all_categories = db_utils.get_all_categories()
    return render_template('indicator_form.html', action="Add", sources=all_sources, categories=all_categories)

@app.route('/indicators/edit/<code>', methods=['GET', 'POST'])
@auth.login_required
def edit_indicator(code):
    """Edit an indicator"""
    if request.method == 'POST':
        new_code = request.form.get('indicator_code')
        name = request.form.get('indicator_name')
        source_id = request.form.get('source_id')
        category_id = request.form.get('category_id')
        definition = request.form.get('long_definition')
        
        if new_code and name and source_id and category_id:
            db_utils.update_indicator(new_code, name, source_id, category_id, definition)
            flash(f'Indicator "{name}" updated successfully!', 'success')
            return redirect(url_for('indicators'))
            
    indicator = db_utils.get_indicator_by_code(code)
    all_sources = db_utils.get_all_sources()
    all_categories = db_utils.get_all_categories()
    return render_template('indicator_form.html', action="Edit", indicator=indicator, sources=all_sources, categories=all_categories)

@app.route('/indicators/delete/<code>')
@auth.login_required
def delete_indicator_route(code):
    """Delete an indicator"""
    indicator = db_utils.get_indicator_by_code(code)
    if indicator:
        db_utils.delete_indicator(code)
        flash(f'Indicator "{indicator["indicator_name"]}" deleted successfully!', 'success')
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
    selected_countries = []
    selected_indicator = None
    start_year = None
    end_year = None
    chart_title = ""
    
    if request.method == 'POST':
        # Get list of selected countries
        selected_countries = request.form.getlist('country_code')
        selected_indicator = request.form.get('indicator_code')
        start_year = request.form.get('start_year')
        end_year = request.form.get('end_year')
        
        if selected_countries and selected_indicator:
            raw_data = db_utils.get_chart_data(selected_countries, selected_indicator, start_year, end_year)
            
            if raw_data:
                # Process data for Chart.js
                # 1. Get all unique years and sort them
                years = sorted(list(set(d['year'] for d in raw_data)))
                
                # 2. Group data by country
                datasets = {}
                for entry in raw_data:
                    cc = entry['country_code']
                    if cc not in datasets:
                        datasets[cc] = {year: None for year in years}
                    datasets[cc][entry['year']] = entry['value']
                
                # 3. Format into a list of datasets
                final_datasets = []
                country_map = {c['country_code']: c['country_name'] for c in countries}
                
                # Simple color palette generator
                colors = [
                    '#4e79a7', '#f28e2b', '#e15759', '#76b7b2', '#59a14f', 
                    '#edc948', '#b07aa1', '#ff9da7', '#9c755f', '#bab0ac'
                ]
                
                for i, (cc, values_map) in enumerate(datasets.items()):
                    # Create data array matching the sorted years order, handle missing years
                    data_points = [values_map.get(year) for year in years]
                    
                    color = colors[i % len(colors)]
                    final_datasets.append({
                        'label': country_map.get(cc, cc),
                        'data': data_points,
                        'borderColor': color,
                        'backgroundColor': color,
                        'fill': False
                    })
                
                chart_data = {
                    'labels': years,
                    'datasets': final_datasets
                }
            
            # Get names for title
            indicator = db_utils.get_indicator_by_code(selected_indicator)
            
            if indicator:
                if len(selected_countries) == 1:
                    country_name = next((c['country_name'] for c in countries if c['country_code'] == selected_countries[0]), selected_countries[0])
                    chart_title = f"{indicator['indicator_name']} - {country_name}"
                else:
                    chart_title = f"{indicator['indicator_name']} - {len(selected_countries)} Countries Comparison"
    
    return render_template('analyze.html',
                         countries=countries,
                         indicators=indicators,
                         chart_data=chart_data,
                         selected_countries=selected_countries,
                         selected_indicator=selected_indicator,
                         start_year=start_year,
                         end_year=end_year,
                         chart_title=chart_title)

@app.route('/export', methods=['POST'])
def export_data():
    """Export analyzed data to Excel"""
    # 1. Formdan verileri al (Analyze ile aynı mantık)
    selected_countries = request.form.getlist('country_code') # Çoklu seçim
    # Eğer frontend'de 'country_code_2' ayrı bir input ise onu da listeye ekle:
    if request.form.get('country_code_2'):
        selected_countries.append(request.form.get('country_code_2'))
        
    selected_indicator = request.form.get('indicator_code')
    start_year = request.form.get('start_year')
    end_year = request.form.get('end_year')

    # 2. Veri yoksa geri gönder
    if not selected_countries or not selected_indicator:
        flash('Please select countries and an indicator to export.', 'warning')
        return redirect(url_for('analyze'))

    # 3. Veritabanından veriyi çek
    raw_data = db_utils.get_chart_data(selected_countries, selected_indicator, start_year, end_year)
    
    if not raw_data:
        flash('No data found to export.', 'warning')
        return redirect(url_for('analyze'))

    # 4. Pandas DataFrame oluştur (Veri manipülasyonu için)
    df = pd.DataFrame(raw_data)
    
    # 5. Veriyi daha okunabilir hale getir
    # Sütun isimlerini düzelt
    df = df.rename(columns={
        'country_code': 'Country Code',
        'year': 'Year', 
        'value': 'Value'
    })
    
    # İsteğe bağlı: Ülke isimlerini de ekleyebilirsin (db_utils'den çekip mergeleyerek)
    # Şimdilik ham veri yeterli.

    # 6. Excel dosyasını RAM'de (Memory) oluştur
    output = BytesIO()
    # ExcelWriter kullanarak meta data ve sheet ismi ayarla
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Data_Analysis')
        
    # Pointer'ı dosyanın başına al
    output.seek(0)
    
    # 7. Dosya ismi oluştur (Dinamik ve tarihli olsun)
    filename = f"export_{selected_indicator}_{datetime.now().strftime('%Y%m%d_%H%M')}.xlsx"

    # 8. İndirme işlemi başlat
    return send_file(
        output,
        download_name=filename,
        as_attachment=True,
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )

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
@auth.login_required
def add_data_route():
    """Add new indicator data"""
    if request.method == 'POST':
        country_code = request.form.get('country_code')
        indicator_code = request.form.get('indicator_code')
        year = request.form.get('year')
        value = request.form.get('value')
        
        if country_code and indicator_code and year and value:
            db_utils.add_indicator_data(country_code, indicator_code, year, value, None)
            flash('Data entry added successfully!', 'success')
            return redirect(url_for('indicator_data_list'))
            
    all_countries, _ = get_all_countries(per_page=1000)
    all_indicators, _ = db_utils.get_all_indicators(per_page=20000)
    return render_template('data_form.html', action="Add", countries=all_countries, indicators=all_indicators)

@app.route('/data/edit/<country_code>/<indicator_code>/<year>', methods=['GET', 'POST'])
@auth.login_required
def edit_data(country_code, indicator_code, year):
    """Edit indicator data"""
    if request.method == 'POST':
        value = request.form.get('value')
        
        if value:
            db_utils.update_indicator_data(country_code, indicator_code, year, value)
            flash('Data updated successfully!', 'success')
            return redirect(url_for('indicator_data_list'))
            
    data_entry = db_utils.get_data_by_composite_key(country_code, indicator_code, year)
    return render_template('data_form.html', action="Edit", data_entry=data_entry)

@app.route('/data/delete/<country_code>/<indicator_code>/<year>')
@auth.login_required
def delete_data_route(country_code, indicator_code, year):
    """Delete indicator data"""
    db_utils.delete_indicator_data(country_code, indicator_code, year)
    flash('Data entry deleted successfully!', 'success')
    return redirect(url_for('indicator_data_list'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Admin login page"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        success, message = auth.login_user(username, password)
        
        if success:
            flash(f'Welcome back, {username}!', 'success')
            return redirect(url_for('index'))
        else:
            flash(message, 'error')
            
    return render_template('login.html')

@app.route('/logout')
def logout():
    """Logout user"""
    auth.logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Handle user registration"""
    if auth.is_logged_in():
        return redirect(url_for('index'))
        
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        if password != confirm_password:
            flash('Passwords do not match', 'error')
            return render_template('register.html')
        
        success, message = auth.register_user(username, email, password)
        
        if success:
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('login'))
        else:
            flash(message, 'error')
            
    return render_template('register.html')

@app.route('/admin/users')
@auth.login_required
def admin_users():
    """Admin panel to view pending users"""
    pending_users = auth.get_pending_users()
    return render_template('admin_users.html', users=pending_users)

@app.route('/admin/approve/<username>')
@auth.login_required
def approve_user_route(username):
    """Approve a pending user"""
    success, message = auth.approve_user(username)
    if success:
        flash(f'User {username} approved!', 'success')
    else:
        flash(message, 'error')
    return redirect(url_for('admin_users'))

@app.route('/admin/reject/<username>')
@auth.login_required
def reject_user_route(username):
    """Reject a pending user"""
    success, message = auth.reject_user(username)
    if success:
        flash(f'User {username} rejected and removed.', 'info')
    else:
        flash(message, 'error')
    return redirect(url_for('admin_users'))



if __name__ == '__main__':
    app.run(debug=True, port=5001)