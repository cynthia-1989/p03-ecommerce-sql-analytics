# ================================================================
# src/data_extractor.py
# ================================================================
# CONTEXT:
#   SQLQueryRunner can run any query. DataExtractor runs ONE specific
#   query: the production extraction query in 05_extract_raw_data.sql.
#
#   DataExtractor is the DELIVERY of Module 03.
#   Its output — raw-data.csv — is the INPUT to Module 05 ETL.
#
# THE PIPELINE CONNECTION:
#   Module 03 DataExtractor → raw-data.csv → Module 05 ETLPipeline
# ================================================================


import sys
import pathlib

_root = pathlib.Path(__file__).resolve().parent
while not (_root / "config.py").exists() and _root != _root.parent:
    _root = _root.parent

if str(_root) not in sys.path:
    sys.path.insert(0, str(_root))

import pandas as pd
from config import INDUSTRY, RAW_DATA_PATH, DB_AVAILABLE, logger
from src.query_runner import SQLQueryRunner


class DataExtractor:
    """
    Runs the production extraction query and saves raw-data.csv.
    """

    def __init__(self):
        self.industry = INDUSTRY
        self.runner = SQLQueryRunner()
        self.raw_df = None
        self._status = "ready"

    def extract(self) -> "DataExtractor":
        """
        Run 05_extract_raw_data.sql and load results.
        """
        logger.info(f"[EXTRACT] Starting extraction — industry: {self.industry}")

        if DB_AVAILABLE:
            self.raw_df = self.runner.run_file("05_extract_raw_data.sql")
        else:
            logger.warning("[EXTRACT] DB unavailable — generating synthetic ecommerce data")
            self.raw_df = self._synthetic_raw_data()

        if self.raw_df is None or len(self.raw_df) == 0:
            logger.warning("[EXTRACT] Query returned 0 rows — using synthetic data")
            self.raw_df = self._synthetic_raw_data()

        self._status = "extracted"
        logger.info(
            f"[EXTRACT] {len(self.raw_df):,} rows × {self.raw_df.shape[1]} columns extracted"
        )
        return self

    def save(self) -> "DataExtractor":
        """
        Save to raw-data.csv
        """
        if self.raw_df is None or len(self.raw_df) == 0:
            logger.error("[EXTRACT] No data to save. Run extract() first.")
            return self

        self.raw_df.to_csv(RAW_DATA_PATH, index=False, encoding="utf-8")

        file_size_kb = RAW_DATA_PATH.stat().st_size / 1024

        logger.info(
            f"[EXTRACT] Saved {len(self.raw_df):,} rows to {RAW_DATA_PATH.name} ({file_size_kb:.1f} KB)"
        )

        self._status = "saved"
        return self

    def report(self) -> None:
        """
        Print summary
        """
        if self.raw_df is None:
            print("Run extract() first.")
            return

        print("\n" + "=" * 60)
        print(f"  MODULE 03 — EXTRACTION COMPLETE | {self.industry.upper()}")
        print("=" * 60)

        print(f"Rows: {len(self.raw_df):,}")
        print(f"Columns: {self.raw_df.shape[1]}")
        print(f"File: {RAW_DATA_PATH.name}")

        if RAW_DATA_PATH.exists():
            print(f"Size: {RAW_DATA_PATH.stat().st_size/1024:.1f} KB")

        print("\nDATA QUALITY ISSUES (expected for ETL stage):")

        nulls = self.raw_df.isna().sum()
        for col in nulls[nulls > 0].index:
            pct = round(nulls[col] / len(self.raw_df) * 100, 1)
            print(f"NULL {col}: {nulls[col]} ({pct}%)")

        # Ecommerce-specific checks
        if "total_amount" in self.raw_df.columns:
            negative = (self.raw_df["total_amount"] < 0).sum()
            if negative:
                print(f"Negative total_amount: {negative} rows")

        if "quantity" in self.raw_df.columns:
            zero_qty = (self.raw_df["quantity"] <= 0).sum()
            if zero_qty:
                print(f"Invalid quantity: {zero_qty} rows")

        print("\nNext step:")
        print("python module-05-data-engineering-and-etl/run.py")
        print("=" * 60)

    @staticmethod
    def _synthetic_raw_data(n: int = 300) -> pd.DataFrame:
        """
        Generate fake ecommerce data
        """
        import random
        import datetime
        import numpy as np

        random.seed(42)
        np.random.seed(42)

        customers = ["Alice", "Bob", "Charlie", "David", "Emma"]
        products = ["Laptop", "Phone", "Tablet", "Headphones"]
        sellers = ["StoreA", "StoreB", "StoreC"]

        rows = []

        for i in range(1, n + 1):
            rows.append({
                "order_id": i,
                "customer_name": random.choice(customers),
                "product_name": random.choice(products),
                "seller_name": random.choice(sellers),
                "quantity": random.randint(1, 5),
                "unit_price": round(random.uniform(10, 1000), 2),
                "total_amount": round(random.uniform(-50, 2000), 2),  # includes bad data
                "order_date": f"2024-{random.randint(1,12):02d}-{random.randint(1,28):02d}",
                "status": random.choice(["completed", "returned", "pending"]),
                "is_returned": random.choice([True, False]),
                "extracted_date": datetime.date.today().isoformat(),
            })

        return pd.DataFrame(rows)

    def __str__(self):
        return f"DataExtractor(industry={self.industry!r}, status={self._status!r})"

    def __repr__(self):
        return f"DataExtractor(industry={self.industry!r})"