
import pandas as pd
from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["ewaste_db"]
collection = db["ewaste_records"]

# Load dataset
df = pd.read_csv("data/e_waste_dataset.csv")

print("Total records in CSV:", len(df))
print("Duplicate source IDs:", df["ID"].duplicated().sum())

# Convert missing values to None
df = df.astype(object).where(pd.notna(df), None)

# Convert data to dictionaries
data = df.to_dict(orient="records")

# Remove the old unique index on ID, if it exists
collection.drop_index("ID_1")

# Insert only records not already imported.
# MongoDB's generated _id distinguishes each document.
existing_count = collection.count_documents({})

if existing_count == 0:
    collection.insert_many(data)
    print("Dataset imported successfully!")
else:
    print("Some records already exist in MongoDB.")
    print("Existing records:", existing_count)
    print("Please clear the partial import before importing again.")

print("Total records in MongoDB:",
      collection.count_documents({}))

client.close()
