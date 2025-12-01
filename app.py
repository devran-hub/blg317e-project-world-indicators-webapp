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
    get_indicators_by_category_name
)

app = Flask(__name__)
app.secret_key = 'your-secret-key-here-change-in-production'

@app.route('/')
def index():
    """Dashboard with stats and charts"""
    regions = get_all_regions()
    countries = get_all_countries()
    indicators = get_all_indicators()
    sources = get_all_sources()
    
    # Get chart data
    population_data = get_global_population()
    gdp_data = get_global_gdp()
    life_expectancy_data = get_global_life_expectancy()
    country_populations = get_latest_population_by_country()
    
    return render_template('index.html',
                         total_regions=len(regions),
                         total_countries=len(countries),
                         total_indicators=len(indicators),
                         total_sources=len(sources),
                         population_data=population_data,
                         gdp_data=gdp_data,
                         life_expectancy_data=life_expectancy_data,
                         country_populations=country_populations)

@app.route('/regions')
def regions():
    """List all regions"""
    all_regions = get_all_regions()
    return render_template('regions.html', regions=all_regions)

@app.route('/regions/add', methods=['POST'])
def add_region_route():
    """Add a new region"""
    name = request.form.get('name')
    if name:
        add_region(name)
        flash(f'Region "{name}" added successfully!', 'success')
    return redirect(url_for('regions'))

@app.route('/countries')
def countries():
    """List all countries"""
    all_countries = get_all_countries()
    all_regions = get_all_regions()
    return render_template('countries.html', countries=all_countries, regions=all_regions)

@app.route('/countries/add', methods=['POST'])
def add_country_route():
    """Add a new country"""
    code = request.form.get('code')
    name = request.form.get('name')
    region_id = request.form.get('region_id')
    income_group = request.form.get('income_group')
    
    if code and name and region_id:
        add_country(code, name, region_id, income_group)
        flash(f'Country "{name}" added successfully!', 'success')
    return redirect(url_for('countries'))

@app.route('/countries/edit/<code>', methods=['GET', 'POST'])
def edit_country(code):
    """Edit a country"""
    if request.method == 'POST':
        name = request.form.get('name')
        region_id = request.form.get('region_id')
        income_group = request.form.get('income_group')
        
        if name and region_id:
            update_country(code, name, region_id, income_group)
            flash(f'Country "{name}" updated successfully!', 'success')
        return redirect(url_for('countries'))
    
    country = get_country_by_code(code)
    all_regions = get_all_regions()
    return render_template('country_form.html', country=country, regions=all_regions)

@app.route('/sources')
def sources():
    """List all sources"""
    all_sources = get_all_sources()
    return render_template('sources.html', sources=all_sources)

@app.route('/sources/add', methods=['POST'])
def add_source_route():
    """Add a new source"""
    name = request.form.get('name')
    description = request.form.get('description')
    
    if name:
        add_source(name, description)
        flash(f'Source "{name}" added successfully!', 'success')
    return redirect(url_for('sources'))

@app.route('/indicators')
def indicators():
    """List all indicators"""
    all_indicators = get_all_indicators()
    all_categories = get_all_categories()
    all_sources = get_all_sources()
    return render_template('indicators.html', 
                         indicators=all_indicators,
                         categories=all_categories,
                         sources=all_sources)

@app.route('/health')
def health():
    """Health indicators"""
    indicators = get_indicators_by_category_name('Health')
    # Fallback if 'Health' category doesn't exist yet, try 'Life Expectancy' or similar if needed
    # For now, we rely on the LIKE query in db_utils
    return render_template('category_indicators.html', 
                         title='Health Indicators',
                         indicators=indicators,
                         active_page='health')

@app.route('/education')
def education():
    """Education indicators"""
    indicators = get_indicators_by_category_name('Education')
    return render_template('category_indicators.html', 
                         title='Education Indicators',
                         indicators=indicators,
                         active_page='education')

@app.route('/economy')
def economy():
    """Economy indicators"""
    # Mapping 'Economy' to 'Economy & Growth' via the LIKE query
    indicators = get_indicators_by_category_name('Economy')
    return render_template('category_indicators.html', 
                         title='Economy Indicators',
                         indicators=indicators,
                         active_page='economy')

@app.route('/indicators/add', methods=['POST'])
def add_indicator_route():
    """Add a new indicator"""
    code = request.form.get('code')
    name = request.form.get('name')
    category_id = request.form.get('category_id')
    source_id = request.form.get('source_id')
    unit = request.form.get('unit')
    
    if code and name and category_id and source_id:
        add_indicator(code, name, category_id, source_id, unit)
        flash(f'Indicator "{name}" added successfully!', 'success')
    return redirect(url_for('indicators'))

@app.route('/categories/add', methods=['POST'])
def add_category_route():
    """Add a new category"""
    name = request.form.get('name')
    if name:
        add_category(name)
        flash(f'Category "{name}" added successfully!', 'success')
    return redirect(url_for('indicators'))

@app.route('/indicator-data/<country_code>')
def indicator_data(country_code):
    """View indicator data for a specific country"""
    country = get_country_by_code(country_code)
    data = get_data_by_country(country_code)
    all_indicators = get_all_indicators()
    
    return render_template('indicator_data.html',
                         country=country,
                         data=data,
                         indicators=all_indicators)

@app.route('/indicator-data/add', methods=['POST'])
def add_indicator_data_route():
    """Add indicator data for a country"""
    country_code = request.form.get('country_code')
    indicator_code = request.form.get('indicator_code')
    year = request.form.get('year')
    value = request.form.get('value')
    
    if country_code and indicator_code and year and value:
        add_indicator_data(country_code, indicator_code, year, value)
        flash('Indicator data added successfully!', 'success')
        return redirect(url_for('indicator_data', country_code=country_code))
    
    return redirect(url_for('countries'))

if __name__ == '__main__':
    app.run(debug=True, port=5001)