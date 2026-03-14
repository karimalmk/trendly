# 📊 Trendly

Trendly is a lightweight, modular **portfolio analytics and watchlist platform** built with Django. It provides a clean backend architecture for **user accounts**, **watchlists**, **tickers**, and **market-data ingestion** — sourced from **30+ global exchanges** and normalized to USD. The aim is to deliver a fast, minimal, developer-friendly analytics tool that can later scale into a full investment dashboard.

## 🔎 Overview

### Key Features
- 📑 Watchlist management — create, edit, reorder, delete  
- 📈 Ticker ingestion pipeline using live yFinance queries (local caching optional)  
- 🌍 Global ticker normalization (all values converted to USD)  
- 📱 Responsive UI with minimal, fast-loading templates  

## Tech Stack
- **Backend:** Django, Django ORM  
- **Database:** SQLite
- **Frontend:** HTML templates, JavaScript, CSS
- **Environment:** Python 3.11+

## 🚀 Installation

### 1. Clone the repository
```bash
git clone <REPO_URL>
cd trendly
```

### 2. Create and activate a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## ⚙️ Django Setup

### 4. Apply migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create a superuser (optional)

```bash
python manage.py createsuperuser
```

---

## ▶️ Running the Server

### 6. Make the runscript executable

Ensure `runserver.sh` has execution permissions:

```bash
chmod +x runserver.sh
```

### 7. Run the development server

```bash
./runserver.sh
```

or directly via Django:

```bash
python manage.py runserver
```