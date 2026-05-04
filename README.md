# E-Commerce Data Simulation Project

This project simulates a e-commerce database with 8 interconnected tables, including Brands, Categories, Sellers, Products, Orders, and Promotions. It uses Faker to generate 2,000 realistic products and transactional data.

## 1. Installation

This project uses Poetry for dependency management. Ensure you have Poetry installed on your system.

1. Clone the repository and navigate to the root folder `py-project-3`.

2. Install libraries defined in `pyproject.toml`:
```
poetry install
```

3. Activate the virtual environment:
```
poetry shell
```
---

## 2. Database Setup

Before running the scripts, you must configure your PostgreSQL connection.

1. Configure Credentials: Open `src/py_project_3/database.ini` and update the settings to match your local PostgreSQL instance (host, database, user, password, and port).

2. Create Tables: Run the schema creation script to build the 8 tables and their relationships:
```
python src/py_project_3/create_tables.py
```
---

## 3. Data Generation

The data generation is split into two phases to maintain referential integrity.
 
- Phase 1: Core Catalog

Generates Brands (20), Categories (10), Sellers (25), and Products (2,000):
```
python src/py_project_3/gen_data_p1.py
```

- Phase 2: Transactions & Marketing

Generates Orders (100), Order Items, Promotions (10), and mapping:
```
python src/py_project_3/gen_data_p2.py
```
---

## 4. Verification & Testing

- View Data Summary

To see the total row counts for every table and a sample of the first 5 rows:
```
python src/py_project_3/top5_tables.py
```

- Test Relationships

To verify that Foreign Keys are working correctly (e.g., Products link to Categories):

```
python tests/test_relationships.py
```
---

## 5. Project Structure

- `src/py_project_3/`: Contains the core application logic and configuration.

- `tests/`: Contains data validation and relationship test scripts.

- `pyproject.toml`: Defines project dependencies for Poetry.