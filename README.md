# Job Recruitment API

A  Job Recruitment REST API built using Django,
Django REST Framework and PostgreSQL.

## Features

- JWT authentication
- Employer and Candidate roles
- Employer job CRUD
- Candidate job search and filtering
- Job applications
- Duplicate application prevention
- Employer applicant management
- Application status management
- Role-based permissions
- PostgreSQL database
- API tests

## Tech Stack

- Python
- Django
- Django REST Framework
- PostgreSQL
- Simple JWT
- django-filter

## Project Structure

job_recruitment/
│
├── accounts/
├── jobs/
├── applications/
├── config/
├── manage.py
├── requirements.txt
└── README.md

## Setup

### Clone the repository

git clone YOUR_GITHUB_REPOSITORY_URL

cd Job_Recruitment_Apis

### Create virtual environment

python -m venv venv

### Activate virtual environment

Windows:

venv\Scripts\activate

### Install dependencies

pip install -r requirements.txt

### Environment Variables

Create a `.env` file:

DB_NAME=job_recruitment_db
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432

### Run migrations

python manage.py migrate

### Create superuser

python manage.py createsuperuser

### Run server

python manage.py runserver

## Authentication

### Register

POST /api/auth/register/

Example:

{
    "username": "candidate1",
    "email": "candidate@yopmail.com",
    "password": "password123",
    "password_confirm": "password123",
    "role": "CANDIDATE"
}

### Login

POST /api/auth/login/

Returns JWT access and refresh tokens.

### Refresh Token

POST /api/auth/refresh/

## Jobs

### List Jobs

GET /api/jobs/

### Create Job

POST /api/jobs/

Employer only.

### Get Job

GET /api/jobs/{id}/

### Update Job

PUT /api/jobs/{id}/

Job owner only.

### Delete Job

DELETE /api/jobs/{id}/

Job owner only.

## Search and Filtering

GET /api/jobs/?search=django

GET /api/jobs/?title=django

GET /api/jobs/?location=Delhi

GET /api/jobs/?skills=Python

GET /api/jobs/?employment_type=FULL_TIME

## Applications

### Apply for Job

POST /api/applications/

Candidate only.

### View Applications

GET /api/applications/

Candidates see their own applications.

Employers see applications for their own jobs.

### View Application

GET /api/applications/{id}/

### Update Application Status

PATCH /api/applications/{id}/

Example:

{
    "status": "SHORTLISTED"
}

Available statuses:

- APPLIED
- SHORTLISTED
- REJECTED
- HIRED

## Permissions

### Employer

- Create jobs
- Update own jobs
- Delete own jobs
- View applicants for own jobs
- Update application status

### Candidate

- View jobs
- Search/filter jobs
- Apply for jobs
- View own applications

A candidate cannot apply for the same job twice.

## Testing

Run:

python manage.py test
