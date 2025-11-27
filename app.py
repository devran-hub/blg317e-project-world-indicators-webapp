from flask import Flask, render_template, request, redirect, url_for, flash
import os
import db_utils

from db_utils import (
    # Regions
    get_all_regions, add_region, delete_region,
    # Sources
    get_all_sources, add_source, delete_source,
    # Categories
    get_all_categories, add_category, delete_category,
    # Countries
    get_all_countries, add_country, get_country_by_code, update_country, delete_country,
    # Indicators
    get_all_indicators, add_indicator, delete_indicator,
    # Indicator Data
    get_data_by_country, add_indicator_data, delete_indicator_data
)

app = Flask(__name__)
app.secret_key = os.urandom(24)

# -----------------------------------------------------------
# Main Page
# -----------------------------------------------------------
@app.route('/')
def index():
    return render_template('index.html')

# -----------------------------------------------------------
# Regions
# -----------------------------------------------------------
@app.route('/regions')
def regions():
    all_regions = get_all_regions()
    return render_template('regions.html', regions=all_regions)

@app.route('/regions/add', methods=['POST'])
def add_region_route():
    name = request.form.get('region_name')
    code = request.form.get('region_code')
    if add_region(name, code):
        flash('Bölge eklendi.', 'success')
    else:
        flash('Hata oluştu.', 'danger')
    return redirect(url_for('regions'))

@app.route('/regions/delete/<int:id>', methods=['POST'])
def delete_region_route(id):
    if delete_region(id):
        flash('Bölge silindi.', 'success')
    else:
        flash('Silinemedi. Bu bölgeye bağlı ülkeler olabilir.', 'danger')
    return redirect(url_for('regions'))

# -----------------------------------------------------------
# Sources
# -----------------------------------------------------------
@app.route('/sources')
def sources():
    all_sources = get_all_sources()
    return render_template('sources.html', sources=all_sources)

@app.route('/sources/add', methods=['GET', 'POST'])
def add_source_route():
    if request.method == 'POST':
        name = request.form.get('source_name')
        org = request.form.get('source_organization')
        url = request.form.get('source_url')
        desc = request.form.get('description')

        if add_source(name, org, url, desc):
            flash('Kaynak eklendi.', 'success')
            return redirect(url_for('sources'))
        else:
            flash('Hata oluştu.', 'danger')

    return render_template('source_form.html', action="Ekle")

@app.route('/sources/delete/<int:id>', methods=['POST'])
def delete_source_route(id):
    if delete_source(id):
        flash('Kaynak silindi.', 'success')
    else:
        flash('Silinemedi. Bu kaynağa bağlı göstergeler olabilir.', 'danger')
    return redirect(url_for('sources'))

# -----------------------------------------------------------
# Indicator Categories
# -----------------------------------------------------------
@app.route('/categories')
def categories():
    cats = get_all_categories()
    return render_template('categories.html', categories=cats)

@app.route('/categories/add', methods=['POST'])
def add_category_route():
    name = request.form.get('category_name')
    desc = request.form.get('description')
    if add_category(name, desc):
        flash('Kategori eklendi.', 'success')
    else:
        flash('Hata oluştu.', 'danger')
    return redirect(url_for('categories'))

@app.route('/categories/delete/<int:id>', methods=['POST'])
def delete_category_route(id):
    if delete_category(id):
        flash('Kategori silindi.', 'success')
    else:
        flash('Silinemedi. Bu kategoriye bağlı göstergeler olabilir.', 'danger')
    return redirect(url_for('categories'))

# -----------------------------------------------------------
# Countries
# -----------------------------------------------------------
@app.route('/countries')
def countries():
    all_countries = get_all_countries()
    return render_template('countries.html', countries=all_countries)

@app.route('/countries/add', methods=['GET', 'POST'])
def add_country_route():
    if request.method == 'POST':
        code = request.form.get('country_code')
        name = request.form.get('country_name')
        capital = request.form.get('capital_city')
        region_id = request.form.get('region_id')
        income = request.form.get('income_level')

        if add_country(code, name, capital, region_id, income):
            flash(f'{name} eklendi.', 'success')
            return redirect(url_for('countries'))
        else:
            flash('Hata: Kod benzersiz olmalı.', 'danger')

    regions = get_all_regions()
    return render_template('country_form.html', regions=regions, action="Ekle")

@app.route('/countries/edit/<string:code>', methods=['GET', 'POST'])
def edit_country_route(code):
    country = get_country_by_code(code)
    if not country:
        flash('Ülke bulunamadı.', 'warning')
        return redirect(url_for('countries'))

    if request.method == 'POST':
        new_code = request.form.get('country_code')
        name = request.form.get('country_name')
        capital = request.form.get('capital_city')
        region_id = request.form.get('region_id')
        income = request.form.get('income_level')

        if update_country(code, new_code, name, capital, region_id, income):
            flash('Ülke güncellendi.', 'success')
            return redirect(url_for('countries'))
        else:
            flash('Güncelleme hatası.', 'danger')

    regions = get_all_regions()
    return render_template('country_form.html', regions=regions, country=country, action="Güncelle")

@app.route('/countries/delete/<string:code>', methods=['POST'])
def delete_country_route(code):
    if delete_country(code):
        flash('Ülke silindi.', 'success')
    else:
        flash('Silinemedi. Verisi olabilir.', 'danger')
    return redirect(url_for('countries'))

# -----------------------------------------------------------
# Indicators
# -----------------------------------------------------------
@app.route('/indicators')
def indicators():
    all_indicators = get_all_indicators()
    return render_template('indicators.html', indicators=all_indicators)

@app.route('/indicators/add', methods=['GET', 'POST'])
def add_indicator_route():
    if request.method == 'POST':
        code = request.form.get('indicator_code')
        name = request.form.get('indicator_name')
        definition = request.form.get('long_definition')
        unit = request.form.get('unit_of_measure')
        cat_id = request.form.get('category_id')
        source_id = request.form.get('source_id')

        if add_indicator(code, name, definition, unit, cat_id, source_id):
            flash('Gösterge eklendi.', 'success')
            return redirect(url_for('indicators'))
        else:
            flash('Hata: Kod benzersiz olmalı.', 'danger')

    categories = get_all_categories()
    sources = get_all_sources()
    return render_template('indicator_form.html', categories=categories, sources=sources, action="Ekle")

@app.route('/indicators/delete/<string:code>', methods=['POST'])
def delete_indicator_route(code):
    if delete_indicator(code):
        flash('Gösterge silindi.', 'success')
    else:
        flash('Silinemedi. Verisi olabilir.', 'danger')
    return redirect(url_for('indicators'))

# -----------------------------------------------------------
# Indicator Data (Extended)
# -----------------------------------------------------------

# Full list view (all rows)
@app.route('/indicator-data')
def indicator_data_list():
    rows = db_utils.get_all_indicator_data()
    return render_template('indicator_data.html', rows=rows)

# Add new row
@app.route('/indicator-data/add', methods=['POST'])
def add_indicator_data_route():
    db_utils.add_indicator_data(
        request.form["country_code"],
        request.form["indicator_code"],
        request.form["year"],
        request.form["value"],
        request.form["footnote"]
    )
    return redirect(url_for('indicator_data_list'))

# Update an existing row
@app.route('/indicator-data/update/<int:id>', methods=['POST'])
def update_indicator_data_route(id):
    db_utils.update_indicator_data(id, request.form["value"], request.form["footnote"])
    return redirect(url_for('indicator_data_list'))

# Delete a row
@app.route('/indicator-data/delete/<int:id>')
def delete_indicator_data_route(id):
    db_utils.delete_indicator_data(id)
    return redirect(url_for('indicator_data_list'))

# Country-specific data view
@app.route('/data/country/<string:code>')
def country_data(code):
    country = get_country_by_code(code)
    data = get_data_by_country(code)
    return render_template('indicator_data.html', country=country, data=data)

# Add data (form)
@app.route('/data/add', methods=['GET', 'POST'])
def add_data_route():
    if request.method == 'POST':
        country_code = request.form.get('country_code')
        indicator_code = request.form.get('indicator_code')
        year = request.form.get('year')
        value = request.form.get('value')
        footnote = request.form.get('footnote')

        if add_indicator_data(country_code, indicator_code, year, value, footnote):
            flash('Veri başarıyla eklendi.', 'success')
            return redirect(url_for('country_data', code=country_code))
        else:
            flash('Hata oluştu. (Belki bu yıl için veri zaten var?)', 'danger')

    countries = get_all_countries()
    indicators = get_all_indicators()
    return render_template('data_form.html', countries=countries, indicators=indicators)

@app.route('/data/delete/<int:id>/<string:return_country_code>', methods=['POST'])
def delete_data_route(id, return_country_code):
    if delete_indicator_data(id):
        flash('Veri satırı silindi.', 'success')
    else:
        flash('Silinemedi.', 'danger')
    return redirect(url_for('country_data', code=return_country_code))


# -----------------------------------------------------------
# Run Flask
# -----------------------------------------------------------
if __name__ == '__main__':
    app.run(debug=True, port=5000)
