.PHONY: up down build clean logs

# Start the application
up:
	docker-compose up --build

# Stop the application
down:
	docker-compose down

# Build containers
build:
	docker-compose build

# Clean up containers and volumes
clean:
	docker-compose down -v
	docker system prune -f

# View logs
logs:
	docker-compose logs -f

