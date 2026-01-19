#!/bin/bash

set -e

# Define variables
APP_NAME="my_web_app"
DOCKER_IMAGE="my_web_app_image"
DOCKER_CONTAINER="my_web_app_container"
POSTGRES_DB="my_database"
POSTGRES_USER="my_user"
POSTGRES_PASSWORD="my_password"
NEXT_PUBLIC_API_URL="http://localhost:8000"
GITHUB_REPO="https://github.com/username/my_web_app.git"
BRANCH="main"

# Function to build and run Docker containers
function deploy_docker() {
    echo "Building Docker image..."
    docker build -t $DOCKER_IMAGE .

    echo "Stopping existing container if running..."
    docker stop $DOCKER_CONTAINER || true
    docker rm $DOCKER_CONTAINER || true

    echo "Running Docker container..."
    docker run -d --name $DOCKER_CONTAINER -p 8000:8000 -e DATABASE_URL="postgresql://$POSTGRES_USER:$POSTGRES_PASSWORD@db:5432/$POSTGRES_DB" $DOCKER_IMAGE
}

# Function to set up PostgreSQL database
function setup_database() {
    echo "Setting up PostgreSQL database..."
    docker run --name postgres -e POSTGRES_DB=$POSTGRES_DB -e POSTGRES_USER=$POSTGRES_USER -e POSTGRES_PASSWORD=$POSTGRES_PASSWORD -d -p 5432:5432 postgres:latest

    # Wait for PostgreSQL to start
    sleep 10

    echo "Running database migrations..."
    # Assuming migrations are handled by Alembic or similar
    docker exec -it $DOCKER_CONTAINER alembic upgrade head
}

# Function to set up CI/CD with GitHub Actions
function setup_cicd() {
    echo "Setting up CI/CD pipeline..."
    cat <<EOL > .github/workflows/deploy.yml
name: Deploy

on:
  push:
    branches:
      - $BRANCH

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v2

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v1

      - name: Login to Docker Hub
        uses: docker/login-action@v1
        with:
          username: \${{ secrets.DOCKER_USERNAME }}
          password: \${{ secrets.DOCKER_PASSWORD }}

      - name: Build and push Docker image
        uses: docker/build-push-action@v2
        with:
          context: .
          push: true
          tags: $DOCKER_IMAGE:latest

      - name: Deploy to server
        run: ssh user@your-server "docker pull $DOCKER_IMAGE:latest && docker-compose up -d"
EOL
}

# Main script execution
echo "Starting deployment setup..."

deploy_docker
setup_database
setup_cicd

echo "Deployment setup completed successfully."