from pymongo import MongoClient
import pandas as pd

client = MongoClient("mongodb://localhost:27017/")
collection = client["ewaste_db"]["ewaste_records"]

try:
    records = list(collection.find({}, {"_id": 0}))
    df = pd.DataFrame(records)

    if df.empty:
        print("No e-waste records found.")

    else:
        print("\n" + "=" * 50)
        print("       E-WASTE MANAGEMENT DASHBOARD")
        print("=" * 50)

        # Overall statistics
        total_records = len(df)

        total_quantity = pd.to_numeric(
            df["Quantity"], errors="coerce"
        ).sum()

        total_weight = pd.to_numeric(
            df["Weight_kg"], errors="coerce"
        ).sum()

        print(f"\nTotal Records       : {total_records}")
        print(f"Total Quantity      : {total_quantity:,.0f}")
        print(f"Total Weight        : {total_weight:,.2f} kg")

        # Category-wise statistics
        print("\n--- CATEGORY-WISE RECORDS ---")
        print(df["Category"].fillna("Unknown").value_counts().to_string())

        # Condition-wise statistics
        print("\n--- CONDITION-WISE RECORDS ---")
        print(df["Condition"].fillna("Unknown").value_counts().to_string())

        # Top 5 locations
        print("\n--- TOP 5 COLLECTION LOCATIONS ---")
        print(
            df["Location"]
            .fillna("Unknown")
            .value_counts()
            .head(5)
            .to_string()
        )

        # Recycling methods
        print("\n--- RECYCLING METHODS ---")
        print(
            df["Recycle_Method"]
            .fillna("Unknown")
            .value_counts()
            .to_string()
        )

        print("\n" + "=" * 50)
        print("          DASHBOARD COMPLETED")
        print("=" * 50)

        print("\nYour charts are available in the 'charts' folder.")
        print("Your exported reports are available in the 'reports' folder.")

finally:
    client.close()