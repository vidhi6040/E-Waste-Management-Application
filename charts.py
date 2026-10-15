from pathlib import Path

from pymongo import MongoClient
import pandas as pd
import matplotlib.pyplot as plt

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
collection = client["ewaste_db"]["ewaste_records"]

# Create charts folder automatically
CHARTS_DIR = Path("charts")
CHARTS_DIR.mkdir(exist_ok=True)

try:
    data = list(collection.find({}, {"_id": 0}))
    df = pd.DataFrame(data)

    if df.empty:
        print("No e-waste data found.")

    else:
        # 1. Category-wise E-Waste Chart
        df["Category"].fillna("Unknown").value_counts().plot(
            kind="bar",
            title="E-Waste by Category"
        )
        plt.xlabel("Category")
        plt.ylabel("Number of Records")
        plt.tight_layout()
        plt.savefig(CHARTS_DIR / "category_chart.png")
        plt.show()
        plt.close()

        # 2. Condition-wise E-Waste Chart
        df["Condition"].fillna("Unknown").value_counts().plot(
            kind="pie",
            autopct="%1.1f%%",
            title="E-Waste Condition"
        )
        plt.ylabel("")
        plt.tight_layout()
        plt.savefig(CHARTS_DIR / "condition_chart.png")
        plt.show()
        plt.close()

        # 3. Top 5 Locations Chart
        df["Location"].fillna("Unknown").value_counts().head(5).plot(
            kind="bar",
            title="Top 5 E-Waste Locations"
        )
        plt.xlabel("Location")
        plt.ylabel("Number of Records")
        plt.tight_layout()
        plt.savefig(CHARTS_DIR / "location_chart.png")
        plt.show()
        plt.close()

        # 4. Total E-Waste Weight by Category
        df["Weight_kg"] = pd.to_numeric(
            df["Weight_kg"], errors="coerce"
        )

        df.groupby("Category")["Weight_kg"].sum().sort_values(
            ascending=False
        ).plot(
            kind="bar",
            title="Total E-Waste Weight by Category"
        )

        plt.xlabel("Category")
        plt.ylabel("Total Weight (kg)")
        plt.tight_layout()
        plt.savefig(CHARTS_DIR / "weight_chart.png")
        plt.show()
        plt.close()

        print("\nAll charts created successfully!")
        print(f"Charts saved in: {CHARTS_DIR.resolve()}")

finally:
    client.close()