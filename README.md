# Treklog API 🌍

A personal travel tracker backend to log countries you've visited, want to visit, and build bucket lists of landmarks, food, and activities.

---

## Stack

| Layer | Technology |
|---|---|
| Backend | Django + Django REST Framework |
| Database | PostgreSQL |
| Cache | Redis |
| Storage | AWS S3 |
| Containerization | Docker + Docker Compose |

---

## Getting started

### Prerequisites

- Docker and Docker Compose installed

### 1. Clone the repository

```bash
git clone https://github.com/your-username/treklog.git
cd treklog
```

### 2. Configure environment variables

Create a `.env` file in the root folder:

```env
# Database
POSTGRES_DB=traveldb
POSTGRES_USER=your_db_user
POSTGRES_PASSWORD=your_db_password

# Django
SECRET_KEY=your_django_secret_key
DEBUG=True

# AWS S3
AWS_ACCESS_KEY_ID=your_access_key_id
AWS_SECRET_ACCESS_KEY=your_secret_access_key
AWS_STORAGE_BUCKET_NAME=your_bucket_name
AWS_S3_REGION_NAME=eu-north-1

# Exchange rates (optional)
EXCHANGERATE_API_KEY=your_api_key
```

### 3. Start the backend

```bash
docker-compose up --build
```

This starts:
- Django API on `http://localhost:8000`
- PostgreSQL on port `5434`
- Redis on port `6379`

### 4. Run database migrations

```bash
docker-compose exec web python manage.py migrate
```

### 5. Create an API key

```bash
docker-compose exec web python manage.py shell
```

```python
from django.contrib.auth.models import User
from users.models import APIKey

user = User.objects.create_user(username='admin', password='yourpassword')
key = APIKey.objects.create(user=user, name='my-key')
print(key.key)
```

Copy the printed key — you'll need it to authenticate API requests.

---

## Running tests

```bash
docker-compose exec web python manage.py test countries
```

---

## API endpoints

All endpoints require an `Authorization: Api-Key <your-key>` header.

### Countries

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/countries/` | List all countries |
| `GET` | `/api/countries/:iso_code/` | Get a single country |

### My countries

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/my-countries/` | List tracked countries |
| `POST` | `/api/my-countries/` | Add a country |
| `GET` | `/api/my-countries/stats/` | Get travel stats |
| `GET` | `/api/my-countries/:id/` | Get a single entry |
| `PATCH` | `/api/my-countries/:id/` | Update status or notes |
| `DELETE` | `/api/my-countries/:id/` | Remove a country |

### Regions

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/my-countries/:id/regions/` | List regions for a country |
| `POST` | `/api/my-countries/:id/regions/` | Add a region |
| `GET` | `/api/regions/:id/` | Get a single region |
| `PATCH` | `/api/regions/:id/` | Update a region |
| `DELETE` | `/api/regions/:id/` | Delete a region |
| `POST` | `/api/my-countries/:id/regions/:regionId/fetch-boundary/` | Fetch region boundary from Nominatim |

### Items

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/my-countries/:id/items/` | List items for a country |
| `POST` | `/api/my-countries/:id/items/` | Add an item |
| `GET` | `/api/items/` | List all items across countries |
| `GET` | `/api/items/:id/` | Get a single item |
| `PATCH` | `/api/items/:id/` | Update an item (e.g. mark as done) |
| `DELETE` | `/api/items/:id/` | Delete an item |

### Photos

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/photos/` | List all photos (filter by `?country_entry=id`) |
| `POST` | `/api/photos/` | Upload a photo (multipart/form-data) |
| `DELETE` | `/api/photos/:id/` | Delete a photo |

---

## Project structure

```
treklog/
  countries/             # Main app — models, views, serializers
    services/
      s3.py              # AWS S3 upload/delete/presigned URL
      currency.py        # Exchange rate fetching
    tests.py             # Django test suite
  users/                 # API key authentication
  treklog/               # Django project settings
  docker-compose.yml
  Dockerfile
  requirements.txt
```

---

## Reporting bugs

Found a bug? Please open an issue on GitHub with:

- A description of what happened
- Steps to reproduce
- What you expected to happen
- Screenshots if relevant
