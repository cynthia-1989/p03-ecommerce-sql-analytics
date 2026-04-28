# ================================================================
# src/query_runner.py
# ================================================================
# CONTEXT:
#   We wrote SQL in .sql files. Now we need to EXECUTE those queries
#   from Python and get back pandas DataFrames we can work with.
#
# THE ANALOGY:
#   Think of SQLQueryRunner as a translator.
#   You hand it a SQL query (a string).
#   It sends that query to PostgreSQL.
#   PostgreSQL sends back rows of data.
#   SQLQueryRunner catches those rows and packages them as a DataFrame.
#
# KEY pandas FUNCTION: pd.read_sql()
#   pd.read_sql(sql_string, engine) executes SQL and returns a DataFrame.
#   This is what powers every Python + database workflow.
#
# WHY A CLASS AND NOT JUST pd.read_sql() DIRECTLY?
#   The class adds:
#     - Error handling
#     - Logging
#     - Timing
#     - Query loading from .sql files
#   These extras make it production-grade rather than just a script.
# ================================================================

import sys
import pathlib
import time

_root = pathlib.Path(__file__).resolve().parent
while not (_root / "config.py").exists() and _root != _root.parent:
    _root = _root.parent

if str(_root) not in sys.path:
    sys.path.insert(0, str(_root))

import pandas as pd
from config import engine, DB_AVAILABLE, SQL_DIR, INDUSTRY, logger


class SQLQueryRunner:
    """
    Executes SQL queries against the Supabase PostgreSQL database.
    Returns results as pandas DataFrames.
    """

    def __init__(self):
        self.industry = INDUSTRY
        self.history = []
        logger.info(f"SQLQueryRunner ready — db_available: {DB_AVAILABLE}")

    def run(self, sql: str, params: dict = None) -> pd.DataFrame:
        """
        Execute a SQL query and return results as a DataFrame.
        """
        if not DB_AVAILABLE or engine is None:
            logger.warning("[SQL] Database not available. Returning empty DataFrame.")
            return pd.DataFrame()

        sql = sql.replace("{industry}", self.industry)

        start_time = time.time()

        try:
            df = pd.read_sql(sql, engine, params=params)
            duration_ms = round((time.time() - start_time) * 1000, 1)

            self.history.append({
                "sql_preview": sql[:80].strip(),
                "rows": len(df),
                "cols": len(df.columns),
                "duration_ms": duration_ms,
                "status": "success",
            })

            logger.info(
                f"[SQL] Query complete — "
                f"{len(df):,} rows × {len(df.columns)} cols | "
                f"{duration_ms}ms"
            )

            return df

        except Exception as e:
            self.history.append({
                "sql_preview": sql[:80].strip(),
                "rows": 0,
                "cols": 0,
                "duration_ms": round((time.time() - start_time) * 1000, 1),
                "status": f"error: {str(e)[:100]}",
            })

            logger.error(f"[SQL] Query failed: {e}")
            return pd.DataFrame()

    def run_file(self, filename: str) -> pd.DataFrame:
        """
        Load a .sql file and execute it.
        """
        sql_path = SQL_DIR / filename

        if not sql_path.exists():
            logger.error(f"[SQL] File not found: {sql_path}")
            return pd.DataFrame()

        logger.info(f"[SQL] Loading: {filename}")

        sql_text = sql_path.read_text(encoding="utf-8")
        return self.run(sql_text)

    def demo_basics(self) -> None:
        """
        Run selected ecommerce queries for demonstration.
        """
        demos = [
            (
                "Distinct customer countries",
                f"""
                SELECT DISTINCT country
                FROM {self.industry}.customers
                ORDER BY country
                """
            ),
            (
                "Recent orders",
                f"""
                SELECT
                    order_id,
                    customer_id,
                    product_id,
                    seller_id,
                    total_amount,
                    status
                FROM {self.industry}.orders
                ORDER BY order_date DESC
                LIMIT 10
                """
            ),
            (
                "Active products",
                f"""
                SELECT
                    product_id,
                    product_name,
                    category,
                    price,
                    stock_qty
                FROM {self.industry}.products
                WHERE is_active = TRUE
                ORDER BY product_id
                LIMIT 10
                """
            ),
        ]

        for title, sql in demos:
            print(f"\n── {title}:")
            df = self.run(sql)
            if not df.empty:
                print(df.to_string(index=False))

    def demo_aggregation(self) -> None:
        """
        Demo ecommerce aggregation queries.
        """
        sql = f"""
            SELECT
                s.seller_id,
                s.store_name,
                SUM(o.total_amount) AS total_revenue
            FROM {self.industry}.orders o
            JOIN {self.industry}.sellers s
                ON o.seller_id = s.seller_id
            GROUP BY s.seller_id, s.store_name
            ORDER BY total_revenue DESC
            LIMIT 10
        """

        print("\n── Revenue by Seller:")
        df = self.run(sql)
        if not df.empty:
            print(df.to_string(index=False))

    def demo_joins(self) -> None:
        """
        Demo five-table ecommerce join.
        """
        sql = f"""
            SELECT
                o.order_id,
                o.order_date,
                o.total_amount,
                o.status,

                c.customer_id,
                c.first_name,
                c.last_name,
                c.country AS customer_country,
                c.city,
                c.segment,

                p.product_id,
                p.product_name,
                p.category AS product_category,

                s.seller_id,
                s.store_name,
                s.category AS seller_category,

                r.review_id,
                r.rating AS review_rating,
                r.review_title
            FROM {self.industry}.orders o
            LEFT JOIN {self.industry}.customers c
                ON o.customer_id = c.customer_id
            LEFT JOIN {self.industry}.products p
                ON o.product_id = p.product_id
            LEFT JOIN {self.industry}.sellers s
                ON o.seller_id = s.seller_id
            LEFT JOIN {self.industry}.reviews r
                ON o.order_id = r.order_id
            ORDER BY o.order_date DESC
            LIMIT 10
        """

        print("\n── Sample Ecommerce Five-Table Join:")
        df = self.run(sql)
        if not df.empty:
            print(df.to_string(index=False))

    def demo_cte(self) -> None:
        """
        Demo CTE query showing customer spending.
        """
        sql = f"""
            WITH customer_spending AS (
                SELECT
                    c.customer_id,
                    c.first_name,
                    c.last_name,
                    SUM(o.total_amount) AS total_spent
                FROM {self.industry}.orders o
                JOIN {self.industry}.customers c
                    ON o.customer_id = c.customer_id
                GROUP BY c.customer_id, c.first_name, c.last_name
            )
            SELECT *
            FROM customer_spending
            ORDER BY total_spent DESC
            LIMIT 10
        """

        print("\n── Customer Spending CTE:")
        df = self.run(sql)
        if not df.empty:
            print(df.to_string(index=False))

    def demo_window_function(self) -> None:
        """
        Demo window function ranking customers by total spend.
        """
        sql = f"""
            SELECT
                c.customer_id,
                c.first_name,
                c.last_name,
                SUM(o.total_amount) AS total_spent,
                RANK() OVER (
                    ORDER BY SUM(o.total_amount) DESC
                ) AS spend_rank
            FROM {self.industry}.orders o
            JOIN {self.industry}.customers c
                ON o.customer_id = c.customer_id
            GROUP BY c.customer_id, c.first_name, c.last_name
            ORDER BY spend_rank
            LIMIT 10
        """

        print("\n── Customer Spend Ranking:")
        df = self.run(sql)
        if not df.empty:
            print(df.to_string(index=False))

    def __str__(self) -> str:
        return (
            f"SQLQueryRunner(industry={self.industry!r}, "
            f"queries_run={len(self.history)})"
        )

    def __repr__(self) -> str:
        return f"SQLQueryRunner(industry={self.industry!r})"