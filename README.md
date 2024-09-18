# BreezeBound API

## Table of Contents
1. [Introduction](#introduction)
2. [Setup](#setup)
3. [API Endpoints](#api-endpoints)
4. [API Usage Examples](#api-usage-examples)
5. [Running Tests](#running-tests)
6. [Contributing](#contributing)

## Introduction

BreezeBound API is a Django-based RESTful service that allows users to create and manage travel schedules, including destinations, date ranges, and weather forecasts. It integrates with external services for geocoding and weather data.

## Setup

### Prerequisites
- Python 3.8+
- Docker and Docker Compose
- PostgreSQL

### Installation

1. Clone the repository:
   ```
   git clone https://github.com/iamramtin/breezebound.git
   cd breezebound
   ```

2. Build and start the Docker containers:
   ```
   docker-compose up --build
   ```

3. Apply migrations:
   ```
   docker-compose exec web python manage.py migrate
   ```

## API Endpoints

- Destinations: `/api/destinations/`
- Schedules: `/api/schedules/`
- Schedule Destinations: `/api/schedule-destinations/`

## API Usage Examples

### Destinations

1. Create a destination:
   ```
   curl -X POST http://localhost:8000/api/destinations/ \
   -H "Content-Type: application/json" \
   -d '{"city": "Paris", "country": "France"}'
   ```

2. List all destinations:
   ```
   curl http://localhost:8000/api/destinations/
   ```

3. Retrieve a specific destination:
   ```
   curl http://localhost:8000/api/destinations/1/
   ```

4. Update a destination:
   ```
   curl -X PUT http://localhost:8000/api/destinations/1/ \
   -H "Content-Type: application/json" \
   -d '{"city": "Paris", "country": "France", "latitude": 48.8566, "longitude": 2.3522}'
   ```

5. Delete a destination:
   ```
   curl -X DELETE http://localhost:8000/api/destinations/1/
   ```

### Schedules

1. Create a schedule:
   ```
   curl -X POST http://localhost:8000/api/schedules/ \
   -H "Content-Type: application/json" \
   -d '{"name": "Summer Vacation 2024", "start_date": "2024-07-01", "end_date": "2024-07-14"}'
   ```

2. List all schedules:
   ```
   curl http://localhost:8000/api/schedules/
   ```

3. Retrieve a specific schedule:
   ```
   curl http://localhost:8000/api/schedules/1/
   ```

4. Update a schedule:
   ```
   curl -X PUT http://localhost:8000/api/schedules/1/ \
   -H "Content-Type: application/json" \
   -d '{"name": "Updated Summer Vacation 2024", "start_date": "2024-07-02", "end_date": "2024-07-15"}'
   ```

5. Delete a schedule:
   ```
   curl -X DELETE http://localhost:8000/api/schedules/1/
   ```

6. Get schedule summary:
   ```
   curl http://localhost:8000/api/schedules/1/summary/
   ```

7. Get weather forecast for a schedule:
   ```
   curl http://localhost:8000/api/schedules/1/weather/
   ```

### Schedule Destinations

1. Add a destination to a schedule:
   ```
   curl -X POST http://localhost:8000/api/schedule-destinations/ \
   -H "Content-Type: application/json" \
   -d '{"schedule": 1, "destination": 1, "arrival_date": "2024-07-02", "departure_date": "2024-07-05"}'
   ```

2. List all schedule destinations:
   ```
   curl http://localhost:8000/api/schedule-destinations/
   ```

3. Retrieve a specific schedule destination:
   ```
   curl http://localhost:8000/api/schedule-destinations/1/
   ```

4. Update a schedule destination:
   ```
   curl -X PUT http://localhost:8000/api/schedule-destinations/1/ \
   -H "Content-Type: application/json" \
   -d '{"schedule": 1, "destination": 1, "arrival_date": "2024-07-03", "departure_date": "2024-07-06"}'
   ```

5. Delete a schedule destination:
   ```
   curl -X DELETE http://localhost:8000/api/schedule-destinations/1/
   ```

6. Get stay info for a schedule destination:
   ```
   curl http://localhost:8000/api/schedule-destinations/1/stay_info/
   ```

## Running Tests

To run the automated test suite:

```
docker-compose exec web python manage.py test api
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE.txt) file for details.