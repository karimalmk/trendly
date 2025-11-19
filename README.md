# Trendly

Trendly is a lightweight portfolio analytics and watchlist application built on Django. It provides a structured backend for handling user authentication, watchlists, tickers, and real‑time or cached market data through a modular codebase.

---

## Overview

**Key Features**

* User authentication and session management
* Watchlist creation, editing, and deletion
* Ticker data retrieval (via yFinance or cached sources)
* Modular static assets (shared CSS variables, JS helpers)
* Responsive layout and clean UI

**Stack**

* **Backend:** Django, Django ORM
* **Database:** SQLite (development) — can be swapped for PostgreSQL in production
* **Frontend:** HTML templates, modular JS, shared design system
* **Environment:** Python 3.11+

---

## Installation

### 1. Clone the repository

```bash
git clone <REPO_URL>
cd trendly
```

---

## Python Environment and Requirements

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

## Django Setup

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

## Running the Server

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

---

## Project Structure (Simplified)

```
trendly/
│
├── manage.py
├── runserver.sh
├── requirements.txt
│
├── users/
├── analytics/
├── static/
│   ├── css/
│   └── js/
│
└── templates/
```

---

## Notes

* Ensure Redis is running if using cached endpoints.
* The shared static system allows you to reuse the same design set across multiple Django apps.
* Frontend JS modules (e.g., `helpers.js`, `watchlist_api.js`) should be imported through your templates.

---

If you want, I can add badges, images, a contribution guide, or expand the documentation for APIs, models, and JS architecture.
