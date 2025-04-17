# MultiTenant Application

## Table of Contents
- [Project Description](#description)
- [Features](#features)
- [Technologies](#technologies)
- [Installation](#installation)
- [API Usage](#api-usage)
- [Testing](#testing)
- [License](#license)

## Project Description

This project is a multi-tenant web application. It allows each tenant to independently manage their data and configurations. The application is built using FastAPI, PostgreSQL, and Tortoise ORM.

## Features
Tenant Isolation:

Tenant-Specific User Management: 

Multi-Tenant Authentication: 

Dynamic Tenant Configuration: 

- **Tenant Isolation**:  Each tenant has isolated data and configurations, ensuring data privacy and independence..
- **Tenant-Specific User Management**: Each tenant can manage their users separately.
- **Multi-Tenant Authentication**: Support for tenant-specific authentication mechanisms.
- **Unit Testing**: Includes tests for the API.

## Technologies

- Python
- FastAPI
- PostgreSQL
- Docker
- Docker Compose
- Tortoise ORM
- Aerich Migration
- JWT token

## Installation

### Prerequisites

- Docker
- Docker Compose
- Git
- Python 3.9+

## Setup

### 1. Clone the Repository

```bash
git clone https://github.com/narminnsn/probit_app.git
cd your_repo_name
```

### 2. Environment Variables
Create a .env file in the root directory with the following content:

- POSTGRES_DB=<db_name>
- POSTGRES_USER=<dbuser>
- POSTGRES_PASSWORD=<db_password>
- JWT_SECRET_KEY=<supersecretkey>
- JWT_ALGORITHM=HS256
- JWT_ACCESS_TOKEN_EXPIRE_MINUTES= 30

These environment variables are used by Docker Compose to configure the PostgreSQL.


### 3. Starting Docker

Make sure Docker is running on your machine. To start the application along with PostgreSQL and Redis using Docker Compose, run:

```bash
docker-compose up
```
This command will start the PostgreSQL. Ensure that the services are running properly, and you should see logs indicating that the database is ready to accept connections.

### 4. Virtual Environment

```bash
python3 -m venv .venv

source .venv/bin/activate

pip install -r requirements.txt
```



### 5. Running Migrations

After the services are up, run the database migrations:

```bash
aerich init -t app.db.TORTOISE_ORM
aerich init-db
aerich migrate
aerich upgrade
```

This will create the database tables for you.

### 6. Running Application

```bash
uvicorn app.main:app --reload

```


# API Documentation

For detailed API documentation, visit:

- Swagger: http://localhost:8000/docs
- Redoc: http://localhost:8000/redoc

# Testing

You can run tests:

```bash
pytest tests/
```

