# wallet web-app

## Overview

This web application is a personal project created to demonstrate my technical skills and expertise. It is a personal finance tracker with Telegram ID registration using JWT authentication.

## Features

- **Recording transactions by expense/income categories and custom financial accounts**:Users can create expense/income categories and cash accounts, then use them to record transactions(FastAPI, Postgres).
- **Multiple currencies**:Users can track transactions and balances in multiple currencies that update automatically(Celery, Redis).
- **Registration**: Users can register and authenticate using their Telegram ID. They receive a JWT token, which allows them to perform further operations on the web app.

## Technologies Usedmonetaryand track them afterward

- **Backend**: FastAPI
- **Database**: Postgres, Redis (for task management and storage for сurrency exchange rate storage)
- **Task Queue**: Celery
- **Containerization**: Docker Compose

## Installation

Follow these steps to install and run the web application on your local machine.

### Prerequisites

Make sure you have the following tools installed:

- Python 3.12.3
- Docker
- Docker Compose
  
### Installation Steps

1. **Clone the repository:**

   ```bash
   git clone https://github.com/samypushisty/finance_app_api
   cd Finance_app_back
2. **Installing dependencies**

   ```bash
    pip install -r requirements.txt
3. **Work repository**
   
   ```bash
   cd Finance-application
4. **Create redis container**

   ```bash
    docker-compose up -d
5. **Start celery app**

    To update currency exchange rates, run Celery worker and Celery Beat for 6 minutes, then shut them down.

   ```bash
     celery -A celery_app.app worker --loglevel=INFO -P solo
     celery -A celery_app.app beat --loglevel=INFO
   
  For shutdown ctrl c
6. **Start main app**

   start main.py
