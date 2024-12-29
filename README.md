# Essence Bot

This repository contains the code for the Essence Bot, a service designed to manage user subscriptions, channels, and provide digests of aggregated posts. The bot is built using the Aiogram framework and other modern Python libraries to ensure a robust and scalable architecture.

## Features

- **User Management**: Create, update, and retrieve user information.
- **Subscription Management**: Activate and deactivate user subscriptions, and retrieve information about current and expiring subscriptions.
- **Channel Management**: Add and remove channels for users, and retrieve all channels associated with a user.
- **Digest Generation**: Generate and retrieve digests of aggregated posts for users.
- **Logging**: Integrated with Logstash for centralized logging.
- **Docker**: Containerized deployment using Docker and Docker Compose.

## Project Structure

The project is organized into several directories and modules:

- `essence_bot/`: Contains the main bot application code.
  - `core/`: Core configuration and logger setup.
    - `config/`: Configuration loading and models.
    - `logger/`: Logger setup and custom handlers.
  - `handlers/`: Handlers for different bot commands and interactions.
  - `keyboards/`: Telegram keyboards for user interactions.
  - `messages/`: Predefined messages used in the bot.
  - `middlewear/`: Custom middlewares for the bot.
  - `schemas/`: Pydantic models for request and response validation.
  - `services/`: External service integrations.
  - `states/`: FSM states for handling user interactions.
- `docker/`: Docker configuration files for containerizing the application.
  - `elastic_search/`: Configuration for Elasticsearch, Logstash, and Kibana.
- `requirements/`: Python dependencies for different environments (development, production, codestyle).
- `tests/`: (Not included in the provided code, but typically where unit and integration tests would reside).

## Getting Started

### Prerequisites

- [Conda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html) for managing Python environments.
- [Docker](https://docs.docker.com/get-docker/) for containerization.
- [Docker Compose](https://docs.docker.com/compose/install/) for orchestrating multi-container Docker applications.

### Development Setup

1. **Create and activate a Conda environment**:

   ```sh
   conda create -n essence_bot python=3.11
   conda activate essence_bot
   ```

2. **Install dependencies**:

   ```sh
   pip install -r requirements/dev.txt
   ```

3. **Install pre-commit hooks**:

   ```sh
   pre-commit install
   ```

4. **Run pre-commit checks**:

   ```sh
   pre-commit run --all-files
   ```

5. **Start the development environment**:

   ```sh
   source docker/deploy.sh up --bot
   ```

6. **Stop the development environment**:
   ```sh
   source docker/deploy.sh stop --bot
   ```

### Production Setup

1. **Build and run the Docker container**:

   ```sh
   docker-compose --env-file .env -f docker/docker-compose.bot.yml up --build -d
   ```

2. **Stop the Docker container**:
   ```sh
   docker-compose --env-file .env -f docker/docker-compose.bot.yml down
   ```

### Logging

The application is configured to use Logstash for centralized logging. Ensure that the Logstash configuration is correctly set up in the `.env` file.

### API Integration

The bot interacts with a backend API for user and subscription management. Ensure that the backend API configuration is correctly set up in the `.env` file.

---

For any questions or issues, please open an issue on GitHub.
