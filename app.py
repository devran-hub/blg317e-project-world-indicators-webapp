from flask import Flask, render_template
import db_utils  

# Flask uygulamasını başlat
app = Flask(__name__)

@app.route('/')
def index():
    """Ana Sayfa: Bölgeleri listeler."""
    
    sql = "SELECT region_name, income_group FROM Regions ORDER BY region_name;"
    
    regions_data = db_utils.execute_query(sql, fetch=True)
    
    return render_template('index.html', regions=regions_data)

@app.route('/indicators')
def indicators_page():
    """Göstergeler için örnek sayfa"""
    
    sql = "SELECT indicator_name, unit_of_measure FROM Indicators LIMIT 10;"
    indicator_list = db_utils.execute_query(sql, fetch=True)
    
    return render_template('indicators.html', indicators=indicator_list)


if __name__ == '__main__':
    app.run(debug=True)