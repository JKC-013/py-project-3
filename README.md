# E-Commerce Data Simulation Project

> **Note:** Files that end with `_3` belong to **Project 3** (initial setup and Faker generation), and files that end with `_4` belong to **Project 4** (mass synthetic data, optimizations, and reporting).

---

## Project 3

This phase simulates an e-commerce database with 8 interconnected tables, including Brands, Categories, Sellers, Products, Orders, and Promotions. It uses Faker to generate 2,000 realistic products and transactional data.

### 1. Installation

This project uses Poetry for dependency management. Ensure you have Poetry installed on your system.

1. Clone the repository and navigate to the root folder `py-project-3`.

2. Install libraries defined in `pyproject.toml`:
```bash
poetry install
```

3. Activate the virtual environment:
```bash
poetry shell
```

### 2. Database Setup

Before running the scripts, you must configure your PostgreSQL connection.

1. **Configure Credentials:** Open `src/py_project_3/database.ini` and update the settings to match your local PostgreSQL instance (host, database, user, password, and port).

2. **Create Tables:** Run the schema creation script to build the 8 tables and their relationships:
```bash
python src/py_project_3/create_tables_3.py
```

### 3. Data Generation

The data generation is split into two phases to maintain referential integrity.
 
**Phase 1: Core Catalog**
Generates Brands (20), Categories (10), Sellers (25), and Products (2,000):
```bash
python src/py_project_3/gen_data_p1_3.py
```

**Phase 2: Transactions & Marketing**
Generates Orders (100), Order Items, Promotions (10), and mapping:
```bash
python src/py_project_3/gen_data_p2_3.py
```

### 4. Verification & Testing

**View Data Summary**
To see the total row counts for every table and a sample of the first 5 rows:
```bash
python src/py_project_3/top5_tables_3.py
```

**Test Relationships**
To verify that Foreign Keys are working correctly (e.g., Products link to Categories):
```bash
python tests/test_relationships_3.py
```

---

## Project 4

This phase scales up the database by generating massive synthetic transactional data (2.5M - 3M records), optimizing the PostgreSQL instance with partitions and indexes, and setting up dynamic reporting functions.

### 1. Database Configuration
Ensure your database connection details are properly configured in the central config file (`database.ini`) and accessed via your connection scripts (`config.py`, `connect.py`) before running the generation.

### 2. Schema Setup
Create the structure for the `order` and `order_item` tables according to the new schema requirements:
```bash
python src/py_project_3/create_tables_4.py
```

### 3. Mass Data Generation
Generate millions of realistic order and item records. This script outputs to CSV files to bypass the bottlenecks of standard Python insertion:
```bash
python src/py_project_3/gen_data_4.py
```

### 4. Bulk Data Import
Utilize PostgreSQL's `COPY` command to ingest the generated CSV files efficiently into the database:
```bash
python src/py_project_3/import_data_4.py
```

### 5. Optimization & Partitioning
Optimize query performance by partitioning the transactional data by month (August, September, October 2025) and creating indexes (e.g., on `product_id`):
```bash
python src/py_project_3/optimization_4.py
```

### 6. Query Execution Plans
Run business requirement queries using `EXPLAIN ANALYZE` to review execution plans and run times before and after optimizations:
```bash
python src/py_project_3/queries_explain_4.py
```

### 7. Dynamic Reports
Generate database stored procedures and functions required for dynamic business reporting (Monthly Revenue, Seller Performance, etc.):
```bash
python src/py_project_3/report_procedures_4.py
```

---

## Project Structure

Based on the current repository, the project is organized as follows:

```text
py-project-3/
├── src/
│   └── py_project_3/
│       ├── config.py                 # Configuration loader
│       ├── connect.py                # Database connection logic
│       ├── create_tables_3.py        # Project 3: Core schema creation
│       ├── create_tables_4.py        # Project 4: Order schema creation
│       ├── database.ini              # Database credentials
│       ├── gen_data_4.py             # Project 4: Mass CSV data generation
│       ├── gen_data_p1_3.py          # Project 3: Catalog data generation
│       ├── gen_data_p2_3.py          # Project 3: Transaction data generation
│       ├── import_data_4.py          # Project 4: Bulk CSV import
│       ├── optimization_4.py         # Project 4: Partitions and indexes
│       ├── queries_explain_4.py      # Project 4: Performance testing
│       └── report_procedures_4.py    # Project 4: Stored procedures
├── tests/                            # Validation and testing scripts
├── .gitignore                        
├── poetry.lock                       # Dependency lock file
├── pyproject.toml                    # Poetry configuration
└── README.md                         # Project documentation
```
