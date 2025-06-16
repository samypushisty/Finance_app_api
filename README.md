# wallet web-app

## Overview

This web application is a personal project created to demonstrate my technical skills and expertise. It is a personal finance tracker with Telegram ID registration using JWT authentication.

## Features

- **Recording transactions by expense/income categories and custom financial accounts**:Users can create expense/income categories and cash accounts, then use them to record transactions(FastAPI, Postgres).
- **Multiple currencies**:Users can track transactions and balances in multiple currencies that update automatically(Celery, Redis).
- **Registration**: Users can register and authenticate using their Telegram ID. They receive a JWT token, which allows them to perform further operations on the web app.

## Technologies Used

- **Backend**: FastAPI
- **Database**: Postgres, Redis (for task management and storage for сurrency exchange rate storage)
- **Task Queue**: Celery
- **Containerization**: Docker Compose, Docker File
- **Database queries**: SQL Alchemy
- **Database migrations**: Alembic
- **Data validation**: Pydantic
- **Tests**: Pytest
- **Test database**: Postgres (spescial DB for tests in Docker)
  
## Installation

Follow these steps to install and run the web application on your local machine.

### Prerequisites

Make sure you have the following tools installed:

- Python 3.12.3
- Docker
- Docker Compose
- Ubuntu
  
### Installation Steps

1. **Clone the repository:**

   ```bash
   git clone https://github.com/samypushisty/finance_app_api
   cd Finance_app_api

3. **Fill out .env, .test_env and redis.conf**

4. **Creating and activating a virtual environment**

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate

5. **Installing dependencies**

   ```bash
    pip install -r requirements.txt
   
6. **Docker compose up web app**

   ```bash
     sudo docker compose up --build
   
7. **Start celery app**

   To update currency exchange rates, run Celery worker and Celery Beat for 6 minutes, then shut them down.

   Open new terminal
   ```bash
     cd Finance_app_api
     python3 -m venv .venv
     cd Finance_application
     celery -A celery_app.app worker --loglevel=INFO -P solo &
     celery -A celery_app.app beat --loglevel=INFO
   ```
   
    Close terminal
   
9. **Create test db**

   Open new terminal
   ```bash
     source .venv/bin/activate
     cd Finance_application
     cd tests
     sudo docker compose up --build
   ```

10. **Start tests**

    Open new terminal
    ```bash
    cd Finance_application
    pytest
    ```
   
12. **Conect and use**

    connect to http://0.0.0.0:8000/docs
    
## Warning!
1. Do not allow spaces in file paths
2. All commands are for Ubuntu
3. If you are using windows replace the UVLoop library with the Asyncio(3.4.3) library
