# PREMs HEI News Portal (Biblo)

A Django-based news and institution management portal for Don Bosco Higher Education Institutions under PREM's network.

## Features

- Role-based access control (Admin and Institution users)
- News management with approval workflow (Draft → Pending → Approved/Rejected)
- Institution profile and statistics dashboard
- UN SDG goal mapping for news and institutions
- REST API for news retrieval
- Responsive design with Bootstrap 5

## Prerequisites

- Python 3.10 or higher
- pip (Python package manager)

## Setup Instructions

### 1. Clone the repository

```bash
git clone <repository-url>
cd PREMs-Biblo
```

### 2. Create and activate a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate       # Linux / macOS
# venv\Scripts\activate        # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root (if it doesn't exist):

```
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

### 5. Run database migrations

```bash
python3 manage.py migrate
```

### 6. Seed initial data

```bash
python3 manage.py seed_data
```

This creates:
- Admin account, 17 SDG goals, 10 news categories
- 47 Don Bosco institution accounts with profiles

### 7. Start the development server

```bash
python3 manage.py runserver
```

The application will be available at **http://127.0.0.1:8000/**

## Login Credentials

| Role        | Username    | Password     |
|-------------|-------------|--------------|
| Admin       | admin       | Admin@1234   |
| Institution | inst01–inst47 | Inst@1234  |

## Project Structure

```
PREMs-Biblo/
├── prems_portal/      # Django project settings
├── accounts/          # User authentication app
├── institutions/      # Institution management app
├── news/              # News management app
├── templates/         # HTML templates
├── static/            # Static files (CSS, JS, images)
├── manage.py
└── requirements.txt
```

## API Endpoints

| Endpoint                      | Method | Description            |
|-------------------------------|--------|------------------------|
| `/news/api/news/`             | GET    | List all approved news |
| `/news/api/news/<slug>/`      | GET    | News article detail    |
