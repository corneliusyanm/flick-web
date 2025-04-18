# Flick - PlayStation Rental Web Application

Flick is a web-based management system for PlayStation rental services. It provides interfaces for both administrators and members to manage stations, transactions, and inventory.

## Features

- **Admin Dashboard**: Manage stations, transactions, and inventory
- **Active Station Display**: View all active stations in a card grid layout
- **Transaction Management**: Create, complete, and move transactions
- **Payment Processing**: Handle payments for regular and loss transactions
- **Member Registration**: Allow users to register as members

## Tech Stack

- **Backend**: Django 4.2
- **Database**: PostgreSQL
- **Frontend**: Bootstrap 5
- **Docker**: PostgreSQL containerization

## Installation

### Prerequisites

- Python 3.9+
- Docker (for PostgreSQL)
- Git

### Setup Instructions

1. **Clone the repository**

```bash
git clone https://github.com/yourusername/flick-web.git
cd flick-web
```

2. **Create and activate a virtual environment**

**For macOS/Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

**For Windows:**
```powershell
python -m venv .venv
.venv\Scripts\activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Start PostgreSQL with Docker**

**For macOS/Linux:**
```bash
docker run --name flick-postgres -e POSTGRES_PASSWORD=postgres -e POSTGRES_USER=postgres -e POSTGRES_DB=flick -p 5439:5432 -d postgres:latest
```

**For Windows:**
```powershell
docker run --name flick-postgres -e POSTGRES_PASSWORD=postgres -e POSTGRES_USER=postgres -e POSTGRES_DB=flick -p 5439:5432 -d postgres:latest
```

If you need to stop and restart the container later:
```bash
# Stop the container
docker stop flick-postgres

# Start the container
docker start flick-postgres
```

5. **Configure the database**

The settings are already configured to use PostgreSQL on port 5439. If you need to modify these settings, edit `flick_web/settings.py`.

6. **Apply migrations**

**For macOS/Linux:**
```bash
python manage.py migrate
```

**For Windows:**
```powershell
python manage.py migrate
```

7. **Create a superuser**

**For macOS/Linux:**
```bash
python manage.py createsuperuser
```

**For Windows:**
```powershell
python manage.py createsuperuser
```

8. **Load sample data (optional)**

**For macOS/Linux:**
```bash
python manage.py populate_sample_data
```

**For Windows:**
```powershell
python manage.py populate_sample_data
```

9. **Run the development server**

**For macOS/Linux:**
```bash
python manage.py runserver
```

**For Windows:**
```powershell
python manage.py runserver
```

10. **Access the application**

- Main site: http://127.0.0.1:8000/
- Admin interface: http://127.0.0.1:8000/admin/
- Active stations: http://127.0.0.1:8000/stations/active/

## Docker Management

### PostgreSQL Container

#### Running PostgreSQL (Port 5439)

To run PostgreSQL in a Docker container on port 5439:

```bash
# Initial setup and run
docker run --name flick-postgres -e POSTGRES_PASSWORD=postgres -e POSTGRES_USER=postgres -e POSTGRES_DB=flick -p 5439:5432 -d postgres:latest

# Check if container is running
docker ps -a | grep flick-postgres

# Start an existing container
docker start flick-postgres

# Stop the container
docker stop flick-postgres

# View container logs
docker logs flick-postgres

# Enter PostgreSQL command line (from host)
docker exec -it flick-postgres psql -U postgres -d flick
```

#### Common PostgreSQL Commands

Once inside the PostgreSQL shell:

```sql
-- List all tables
\dt

-- View database structure
\d+ tablename

-- Select all records from a table
SELECT * FROM core_transaction;

-- Exit PostgreSQL shell
\q
```

## Project Structure

- **core/**: Main application with models, views, and templates
- **flick_web/**: Project settings and main URL configuration
- **templates/**: HTML templates for the application
- **management/commands/**: Custom management commands including sample data population

## User Roles

1. **Admin**: Can manage stations, transactions, and view reports
2. **Member**: Can register and use the PlayStation rental service
3. **Super Admin (Owner)**: Has full access to all features including user management

## Development

### Creating a New App

**For macOS/Linux:**
```bash
python manage.py startapp app_name
```

**For Windows:**
```powershell
python manage.py startapp app_name
```

### Running Tests

**For macOS/Linux:**
```bash
python manage.py test
```

**For Windows:**
```powershell
python manage.py test
```

## Timezone

The application uses Asia/Jakarta (UTC+7) timezone by default.

## Contributors

- Your Name <your.email@example.com>

## License

[MIT License](LICENSE)
