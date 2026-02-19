# Pin-voyage

## Overview

Pin-voyage is a backend-first web application for collecting and exploring **Points of Interest (POIs)** using spatial data.

The project deliberately prioritizes **backend architecture, data modeling, and spatial logic** over frontend complexity. All rendering is server-side; there is no JavaScript or client-side framework involved.

The application is built with:

* **FastAPI** for routing and application logic
* **PostgreSQL + PostGIS** for persistent spatial data
* **Folium** for server-side map generation
* **Jinja2** for HTML templating
* **Docker Compose** as the default runtime

---

## What exists today

* FastAPI application with a modular router structure
* CRUD operations for Points of Interest
* PostgreSQL database with required PostGIS support
* Alembic-based database migrations
* Fully containerized development setup

This repository represents an **early but well-defined backend foundation**, designed to be extended incrementally.

---

## Design approach

Pin-voyage treats maps as backend artifacts.

The core flow is intentionally simple and predictable:

1. A base map is generated using **Folium**.
2. The map is embedded into a **Jinja2 template**.
3. POIs are loaded from the database and rendered as markers and lists.
4. User interactions are handled via standard HTTP requests and HTML forms.

This approach keeps complexity on the backend, where spatial logic and data integrity can be enforced reliably.

---

## Project structure

```
pin_voyage/
├── main.py                     # Application entry point
├── points_crud/
│   └── router.py               # POI CRUD router
├── database/
│   └── ...
alembic/                        # Database migrations
docker-compose.yml              # Default runtime setup
pyproject.toml                  # Poetry configuration
poetry.lock                     # Locked dependencies
requirements.txt                # Auxiliary dependency list
.env                             # Environment variables (not committed)
.env.example                     # Example environment file
```

---

## Dependency management

**Poetry** is the primary dependency manager.

* Dependencies are defined in `pyproject.toml`
* Versions are locked in `poetry.lock`

A `requirements.txt` file exists for auxiliary or compatibility purposes, but Poetry is the source of truth.

---

## Requirements

* Docker
* Docker Compose
* Poetry
* PostgreSQL with **PostGIS enabled**

---

## Installation

Clone the repository:

```sh
git clone https://github.com/Codeminister2137/Pin-voyage.git
cd Pin-voyage
```

Install dependencies:

```sh
poetry install
```

---

## Environment configuration

Create a local environment file:

```sh
cp .env.example .env
```

Fill in database connection details and required settings. PostGIS support is mandatory.

---

## Running the application

The supported way to run the application is via Docker Compose:

```sh
docker-compose up --build
```

This starts the FastAPI application and the PostgreSQL + PostGIS database.

---

## Database migrations

Database schema changes are managed using **Alembic**.

Apply migrations inside the Docker environment:

```sh
docker-compose exec app alembic upgrade head
```

(Service name may vary depending on the Compose configuration.)

---

## API

* Entry point: `pin_voyage/main.py`
* POI routes: `pin_voyage/points_crud/router.py`

Interactive documentation is available at:

* `/docs`
* `/redoc`

---

## Project status

Pin-voyage is under active development.

The backend foundation and spatial data handling are in place. Feature exploration and longer-term ideas are documented separately in `docs/ideas.md`.
