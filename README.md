# 🌍 World Development Indicators — Web Application

A modern Flask-based web dashboard for viewing and managing World Bank Development Indicators.
Supports regions, countries, indicators, indicator categories, sources, and time-series data visualization using Chart.js.

## 📌 Features

### ✅ Dashboard
- Global statistics (total regions, countries, indicators, sources)
- Recent activity feed showing latest data entries
- Line charts for:
  - Global Population (SP.POP.TOTL)
  - GDP (NY.GDP.MKTP.CD)
  - Life Expectancy (SP.DYN.LE00.IN)
- Top 10 countries by population chart

### ✅ Data Analysis
- Custom chart builder with country and indicator selection
- **Smart filtering**: Only shows countries and indicators that have actual data
- Year range filtering (start/end year)
- Interactive Chart.js visualizations

### ✅ Category Pages
- **Health Indicators** - Health-related metrics and statistics
- **Education Indicators** - Education-related metrics
- **Economy Indicators** - Economic development indicators
- Each category shows indicators with data availability status

### ✅ Regions
- List all regions with search functionality
- Add, edit, and delete regions
- Pending changes approval system

### ✅ Countries
- List all countries with region information
- Add, edit, and delete countries
- View indicator data for each country
- Search functionality

### ✅ Indicators
- List indicators with category and source information
- Add, edit, and delete indicators
- Data availability status indicator

### ✅ Indicator Categories
- List, add, edit, and delete categories
- View indicators by category

### ✅ Sources
- List, add, edit, and delete data sources
- Source organization and URL tracking

### ✅ Indicator Data
- Browse all indicator data with pagination
- Filter by indicator code
- Search across countries, indicators, and years
- Add, edit, and delete data entries

### ✅ Admin Panel
- Secure login system
- Pending changes approval workflow
- Approve or reject submitted changes

### ✅ Global Search
- Search across countries, indicators, regions, and sources

## 🏛️ Technology Stack

| Component | Technology |
|-----------|------------|
| Backend | Flask (Python) |
| Database | MySQL |
| Frontend | Modern CSS, Chart.js, HTML/Jinja2 |
| DB Connector | mysql-connector-python |
| Design | Glassmorphism, Dark Theme, Responsive |

## 📂 Project Structure

```
blg317e-project-world-indicators-webapp/
│
├── app.py                      # Main Flask application
├── db_utils.py                 # All database functions
├── auth.py                     # Authentication utilities
├── pending_utils.py            # Pending changes management
│
├── database/
│    └── db_connect.py          # MySQL connection setup
│
├── static/
│    └── css/
│         └── style.css         # Custom styles
│
├── templates/
│    ├── base.html              # Base template with navigation
│    ├── index.html             # Dashboard
│    ├── analyze.html           # Data analysis page
│    ├── regions.html           # Regions list
│    ├── countries.html         # Countries list
│    ├── indicators.html        # Indicators list
│    ├── indicator_data.html    # Country indicator data
│    ├── indicator_data_list.html # All indicator data
│    ├── sources.html           # Sources list
│    ├── categories.html        # Categories list
│    ├── health_indicators.html # Health category
│    ├── education_indicators.html # Education category
│    ├── economy_indicators.html # Economy category
│    ├── search.html            # Search results
│    ├── login.html             # Admin login
│    ├── admin.html             # Admin panel
│    └── *_form.html            # Various form templates
│
└── README.md
```

## ⚙️ Installation

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/yourusername/world-indicators-webapp.git
cd world-indicators-webapp
```

### 2️⃣ Create Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3️⃣ Install Requirements
```bash
pip install -r requirements.txt
```

## 🛢️ Database Setup

### 1️⃣ Create MySQL Database
```sql
CREATE DATABASE wdi;
USE wdi;
```

### 2️⃣ Import Schema
```bash
mysql -u root -p wdi < database/schema_only.sql
```

### 3️⃣ Configure Connection

Edit `database/db_connect.py`:

```python
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="YOUR_PASSWORD",
        database="wdi"
    )
```

## 🚀 Run the Application

After installing everything:

```bash
python app.py
```

Visit: **http://127.0.0.1:5001**

## 📊 Key Features

- **Modern UI**: Dark theme with glassmorphism effects
- **Responsive Design**: Works on desktop and mobile
- **Chart.js Visualizations**: Interactive charts and graphs
- **Smart Data Filtering**: Analyze page only shows data that exists
- **Pending Changes System**: All modifications require admin approval
- **Search Functionality**: Global search across all tables

## 🧑‍💻 Developers

- Ali Huseynov
- Mehmet Fatih Kaya
- Devrim Polat
- Ahmet Yusuf Kurukız
- Yunus Korkmaz

**BLG317E — Database Systems**  
Istanbul Technical University

## 📄 License

This project is for academic use.
You may extend and modify it freely.