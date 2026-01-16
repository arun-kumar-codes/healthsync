# HealthSync ![Build Status](https://img.shields.io/badge/build-passing-brightgreen) ![Version](https://img.shields.io/badge/version-1.0.0-blue)

## Project Description
HealthSync is a web application that aggregates health data from multiple wearable devices, providing users with personalized insights and recommendations based on their health metrics. The platform allows users to securely share their data with healthcare providers, facilitating better-informed medical decisions.

## Features
- 📊 Real-time health data integration from various wearable devices
- 🤖 Personalized health insights and recommendations using AI
- 🔒 Secure sharing of health data with healthcare providers

## Tech Stack
### Frontend
- **Next.js** 🌐

### Backend
- **FastAPI** 🚀
- **LangChain** 📚
- **OpenAI** 🤖

### Database
- **PostgreSQL** 🗄️

## Installation
To set up the project locally, follow these steps:

- Clone the repository
bash
git clone https://github.com/arun-kumar-codes/healthsync
- Navigate to the project directory
bash
cd healthsync
- Install the required dependencies
bash
pip install -r requirements.txt
- Set up the PostgreSQL database
bash
# Create a new database
createdb healthsync

# Run migrations
alembic upgrade head
- Start the FastAPI server
bash
uvicorn app.main:app --reload
- Start the Next.js development server
bash
npm install
npm run dev
## Usage
Once the application is running, navigate to `http://localhost:3000` in your web browser to access the HealthSync interface. Connect your wearable devices to start aggregating health data and receive personalized insights.

## API Documentation
For detailed API documentation, please refer to the [API Docs](https://github.com/arun-kumar-codes/healthsync/wiki/API-Documentation).

## Testing
To run the tests for the application, use the following command:
bash
pytest
## Deployment
For deploying the application, follow these steps:

- Build the Next.js application
bash
npm run build
- Deploy the FastAPI application using a WSGI server like Gunicorn
bash
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker
## Contributing
We welcome contributions! Please follow these guidelines:

- Fork the repository
- Create a new branch for your feature or bug fix
- Make your changes and commit them
- Push your branch and create a pull request

For more details, please refer to our [CONTRIBUTING.md](https://github.com/arun-kumar-codes/healthsync/blob/main/CONTRIBUTING.md).