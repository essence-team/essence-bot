#!/bin/bash

ACTION=$1
OPTION=$2
RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m'

# Function to remove old containers and images that are not used
cleanup() {
  echo "Removing old containers and images..."
  docker system prune -f
  if [ $? -ne 0 ]; then
    echo "${RED}ERROR:${NC} Failed to clean up Docker resources. Exiting..."
  else
    echo "${GREEN}SUCCESS:${NC} Cleanup completed."
  fi
}

start_bot() {
  echo "Starting docker with telegram bot..."
  docker-compose --env-file .env -f docker/docker-compose.bot.yml up --build -d
  if [ $? -ne 0 ]; then
    echo "${RED}ERROR:${NC} Failed to start the telegram bot. Exiting..."
  else
    echo "${GREEN}SUCCESS:${NC} Telegram bot has been started."
  fi
}

stop_bot() {
  echo "Stopping telegram bot..."
  docker-compose --env-file .env -f docker/docker-compose.bot.yml down
  if [ $? -ne 0 ]; then
    echo "${RED}ERROR:${NC} Failed to stop telegram bot..."
  else
    echo "${GREEN}SUCCESS:${NC} Telegram bot has been stopped."
  fi
}

case $ACTION in
  up)
    case $OPTION in
      --bot)
        start_bot
        ;;
      *)
        echo "${RED}INVALID OPTION.${NC} Usage: $0 up {--bot}"
        ;;
    esac
    ;;
  stop)
    case $OPTION in
      --bot)
        stop_bot
        ;;
      *)
        echo "${RED}INVALID OPTION.${NC} Usage: $0 stop {--bot}"
        ;;
    esac
    ;;
  clean)
    cleanup
    ;;
  *)
    echo "${RED}INVALID COMMAND.${NC} Usage: $0 {up|stop|clean} [--bot]"
    ;;
esac
