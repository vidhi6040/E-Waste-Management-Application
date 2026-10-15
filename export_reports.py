from pathlib import Path

import pandas as pd
from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
collection = client["ewaste_db"]["ewaste_records"]

# Create reports folder
REPORTS_DIR = Path("reports")
REPORTS_DIR.mkdir(exist_ok=True)

try:
    # Fetch records from MongoDB
    records = list(collection.find({}, {"_id": 0}))

    if not records:
        print("No records found to export.")

    else:
        df = pd.DataFrame(records)

        # Export all records to CSV
        csv_path = REPORTS_DIR / "ewaste_records.csv"
        df.to_csv(csv_path, index=False)

        # Export all records to Excel
        excel_path = REPORTS_DIR / "ewaste_records.xlsx"
        df.to_excel(excel_path, index=False)

        # Create category summary
        summary = df.groupby("Category", dropna=False).agg(
            Total_Records=("Category", "size"),
            Total_Quantity=("Quantity", "sum"),
            Total_Weight_kg=("Weight_kg", "sum")
        ).reset_index()

        # Export detailed records and summary to separate Excel sheets
        with pd.ExcelWriter(excel_path) as writer:
            df.to_excel(
                writer,
                sheet_name="All Records",
                index=False
            )
            summary.to_excel(
                writer,
                sheet_name="Category Summary",
                index=False
            )

        print("\nReports exported successfully!")
        print(f"CSV report: {csv_path.resolve()}")
        print(f"Excel report: {excel_path.resolve()}")

finally:
    client.close()