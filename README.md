# P03 ⭐⭐⭐ — Ecommerce SQL 🛒

## Overview

This project builds an ecommerce SQL extraction pipeline for analysing customer orders, seller performance, product activity, ecommerce reviews, and revenue behaviour.

The pipeline connects to a PostgreSQL ecommerce database, performs SQL extraction queries, joins multiple ecommerce tables, and generates a flat raw dataset for downstream ETL, forecasting, customer segmentation, and analytics workflows.

---

## Table of Contents

1. [Project Brief](#project-brief)
2. [SQL Workflow](#sql-workflow)
3. [Input and Output](#input-and-output)
4. [Project Structure](#project-structure)
5. [Order Analysis](#order-analysis)
6. [Customer Analysis](#customer-analysis)
7. [Seller Analysis](#seller-analysis)
8. [Review Analysis](#review-analysis)
9. [Aggregation Queries](#aggregation-queries)
10. [Join Operations](#join-operations)
11. [CTE and Window Functions](#cte-and-window-functions)
12. [Visualisations](#visualisations)
13. [How to Run](#how-to-run)
14. [Tests](#tests)
15. [Git Workflow](#git-workflow)

---

## Project Brief

**Company:** Shop Stream Global  
**Role:** Data Analyst

The ecommerce dataset includes records such as:

- Customer orders
- Customer profiles
- Product information
- Seller activity
- Ecommerce reviews

The analysis focuses on extracting ecommerce operational data from PostgreSQL and preparing a flat analytical dataset for downstream ETL processing, revenue forecasting, and customer segmentation.

---

## SQL Workflow

### 1. Database Connection

Connect to the PostgreSQL ecommerce database using:

- Supabase
- SQLAlchemy
- PostgreSQL driver

Database schema used:

```text
ecommerce
```

---

### 2. SQL Extraction

Run SQL extraction queries against the ecommerce schema.

Key ecommerce tables include:

```text
orders
customers
products
sellers
reviews
```

---

### 3. SQL Basics

The project includes basic SQL operations such as:

- SELECT
- WHERE
- ORDER BY
- LIMIT
- DISTINCT

---

### 4. Aggregation Queries

The project performs ecommerce aggregations including:

- Revenue by seller
- Return rate analysis
- Average review score analysis
- Customer spending summaries
- Product category performance

SQL functions used include:

```sql
COUNT()
SUM()
AVG()
MIN()
MAX()
GROUP BY
```

---

### 5. Join Operations

The project joins ecommerce tables to create a flat analytical dataset.

Joins include:

- Orders + customers
- Orders + products
- Products + sellers
- Orders + reviews

The final dataset combines ecommerce operational records into one extract.

---

### 6. CTE and Window Functions

The project includes advanced SQL using:

- Common Table Expressions (CTEs)
- Window functions

Examples include:

```sql
ROW_NUMBER()
RANK()
DENSE_RANK()
OVER(PARTITION BY ...)
```

CTEs and window functions are used to rank customers by total spend and analyse ecommerce purchasing behaviour.

---

## Input and Output

### Input

```text
PostgreSQL ecommerce database
```

### Outputs

```text
data/raw-data.csv
sql/
reports/
```

---

## Project Structure

```text
P03-ecommerce-sql/
│
├── data/
│   └── raw-data.csv
│
├── reports/
│
├── sql/
│   ├── 01_sql_basics.sql
│   ├── 02_aggregations.sql
│   ├── 03_joins.sql
│   ├── 04_cte_window.sql
│   └── 05_extract_raw_data.sql
│
├── src/
│   ├── query_runner.py
│   └── data_extractor.py
│
├── tests/
│
├── run.py
├── config.py
├── requirements.txt
└── README.md
```

---

## Order Analysis

The project analyses ecommerce transaction activity including:

- Order volume
- Revenue generation
- Product sales
- Order trends
- Customer purchase behaviour

Metrics generated include:

- Total revenue
- Average order value
- Order counts
- Revenue by category
- Customer spending statistics

---

## Customer Analysis

The project analyses ecommerce customer behaviour including:

- Customer spending activity
- Purchase frequency
- Customer segmentation
- Customer lifetime value
- Customer ranking

Metrics generated include:

- Total customer spend
- Average customer order value
- Purchase counts
- Customer ranking by spend

---

## Seller Analysis

The project analyses seller operational performance including:

- Seller revenue
- Seller product activity
- Seller review scores
- Seller transaction counts

Metrics generated include:

- Revenue by seller
- Average review score per seller
- Seller order volume
- Seller ranking statistics

---

## Review Analysis

The project analyses ecommerce review records including:

- Product review scores
- Seller review performance
- Customer review activity
- Review distribution analysis

Metrics generated include:

- Average review ratings
- Review counts
- Seller review rankings
- Product review summaries

---

## Aggregation Queries

The project performs ecommerce aggregation analysis using:

```sql
COUNT()
SUM()
AVG()
MIN()
MAX()
GROUP BY
```

Aggregations help summarise ecommerce operational performance.

Examples include:

- Revenue by seller
- Return rates by product category
- Average review score per seller

---

## Join Operations

The project joins multiple ecommerce tables into one analytical dataset.

Joined tables include:

```text
orders
customers
products
sellers
reviews
```

The joined dataset is exported as:

```text
data/raw-data.csv
```

The final extract produces one row per order with customer, product, seller, and review data.

---

## CTE and Window Functions

Advanced SQL functionality includes:

- CTE-based queries
- Ranking functions
- Partitioned analysis
- Customer spend rankings

Examples include:

- Ranking customers by total spend
- Ranking sellers by revenue
- Product category performance comparisons

---

## Visualisations

The project notebook can generate ecommerce visualisations including:

- Revenue trend charts
- Customer spending charts
- Seller performance comparisons
- Review distribution charts
- Product category charts

Saved charts are stored in:

```text
reports/
```

---

## How to Run

Run the complete ecommerce SQL extraction pipeline:

```bash
python run.py
```

The pipeline performs:

1. Database connection
2. SQL query execution
3. Join extraction
4. Raw dataset creation
5. CSV export

---

## Tests

Run unit tests using:

```bash
pytest tests/
```

Tests cover:

- Database connectivity
- SQL query execution
- Aggregation queries
- Join operations
- CTE functionality
- Window function analysis
- Data extraction
- CSV generation

---

## Git Workflow

```bash
git status
git add .
git commit -m "feat: complete ecommerce SQL extraction project"
git push
```

---

## Success Criteria Achieved

- All five tables queried successfully
- Aggregation queries completed
- Revenue analysis completed
- Review analysis completed
- Join operations completed
- CTE and window functions implemented
- raw-data.csv generated
- Five-table extract completed
- Project pushed to GitHub

---