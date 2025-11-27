🌍 World Development Indicators — Web Application

A Flask-based web dashboard for viewing and managing World Bank Development Indicators.
Supports regions, countries, indicators, indicator categories, sources, and time-series data visualization using Chart.js.

📌 Features
✅ Dashboard

Global statistics (total regions, countries, indicators, sources)

Line charts for:

Global Population (SP.POP.TOTL)

GDP (NY.GDP.MKTP.CD)

Life Expectancy (SP.DYN.LE00.IN)

✅ Regions

List all regions

Add new region

Delete region

✅ Countries

List all countries with region name

Add new country

Edit existing country

Delete country

View indicator data for each country

✅ Indicators

List indicators with category + source

Add new indicator

Delete indicator

✅ Indicator Categories

List categories

Add new category

Delete category

✅ Sources

List sources

Add new source

Delete source

✅ Indicator Data

List all data entries for a country

Add new indicator data

Delete data entries

🏛️ Technology Stack
Component	Technology
Backend	Flask (Python)
Database	MySQL
Frontend	Tailwind CSS, Chart.js, HTML/Jinja2
ORM/DB	mysql-connector-python
Structure	MVC-style Flask project
📂 Project Structure
blg317e-project-world-indicators-webapp/
│
├── app.py                      # Main Flask application
├── db_utils.py                 # All database functions
├── database/
│    └── db_connect.py          # MySQL connection setup
│
├── static/
│    ├── css/
│    │    └── style.css
│    └── ...
│
├── templates/
│    ├── base.html
│    ├── index.html
│    ├── regions.html
│    ├── countries.html
│    ├── indicators.html
│    ├── indicator_data.html
│    ├── sources.html
│    ├── categories.html
│    └── forms…
│
└── README.md

⚙️ Installation
1️⃣ Clone the Repository
git clone https://github.com/yourusername/world-indicators-webapp.git
cd world-indicators-webapp

2️⃣ Create Virtual Environment
python3 -m venv venv
source venv/bin/activate

3️⃣ Install Requirements
pip install -r requirements.txt

🛢️ Database Setup
1️⃣ Create MySQL Database
CREATE DATABASE wdi;
USE wdi;

2️⃣ Import Schema

Import the SQL file:

mysql -u root -p wdi < database/schema_only.sql

3️⃣ Configure Connection

Edit:

database/db_connect.py


Example:

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="YOUR_PASSWORD",
        database="wdi"
    )

🚀 Run the Application

After installing everything:

python app.py


Visit:

http://127.0.0.1:5000

📊 Preview

The app includes:

Modern responsive dashboard

Chart.js visualization

CRUD operations

Dynamic Jinja templates

(Screen-shots or GIF can be added here)

🧑‍💻 Developers

Ali Huseynov
Mehmet Fatih Kaya
Devrim Polat
Ahmet Yusuf Kurukız
Yunus Korkmaz

BLG317E — Database Systems
Istanbul Technical University

📄 License

This project is for academic use.
You may extend and modify it freely.