from pymongo import MongoClient
from bson import ObjectId
from pymongo.errors import PyMongoError
import re

# DATABASE CONNECTION
client = MongoClient("mongodb://localhost:27017/", serverSelectionTimeoutMS=5000)
db = client["ewaste_db"]
collection = db["ewaste_records"]

VALID_CATEGORIES = {"TV", "Mobile", "Laptop", "Appliance"}
VALID_CONDITIONS = {"Working", "Partially Working", "Broken"}
VALID_RECYCLING_METHODS = {"Manual", "Automated", "Both", "Pending"}


def display_record(record):
    print("-" * 45)
    print("MongoDB ID:", str(record.get("_id", "")))
    print("Source ID:", record.get("ID", "N/A"))
    print("Item:", record.get("Item_Name", "N/A"))
    print("Brand:", record.get("Brand", "N/A"))
    print("Model:", record.get("Model", "N/A"))
    print("Category:", record.get("Category", "N/A"))
    print("Condition:", record.get("Condition", "N/A"))
    print("Quantity:", record.get("Quantity", "N/A"))
    print("Weight (kg):", record.get("Weight_kg", "N/A"))
    print("Location:", record.get("Location", "N/A"))
    print("Recycling Method:", record.get("Recycle_Method", "N/A"))
    print("Facility:", record.get("Recycling_Facility", "N/A"))
    print("Status/End Use:", record.get("End_Use", "N/A"))
    print("Estimated Recycled Price (USD):", record.get("Recycled_Price_USD", "N/A"))
    print("-" * 45)


def read_text(prompt, allowed_values=None):
    """Read a non-empty string; optionally enforce an allowed set."""
    while True:
        value = input(prompt).strip()
        if not value:
            print("This field cannot be empty. Please try again.")
            continue
        if allowed_values is not None:
            matched = next(
                (option for option in allowed_values if option.casefold() == value.casefold()),
                None
            )
            if matched is None:
                print("Choose one of: " + ", ".join(sorted(allowed_values)))
                continue
            return matched
        return value


def read_number(prompt, minimum=None, allow_decimal=False):
    while True:
        raw = input(prompt).strip()
        try:
            number = float(raw) if allow_decimal else int(raw)
            if allow_decimal and not number == number:  # reject NaN
                print("Please enter a finite number.")
                continue
            if number in (float("inf"), float("-inf")):
                print("Please enter a finite number.")
                continue
            if minimum is not None and number < minimum:
                print(f"Enter a value greater than or equal to {minimum}.")
                continue
            return number
        except ValueError:
            print("Please enter a valid number.")


def find_by_mongo_id():
    mongo_id = input("Enter MongoDB ID: ").strip()
    if not ObjectId.is_valid(mongo_id):
        print("Invalid MongoDB ID format.")
        return None
    try:
        record = collection.find_one({"_id": ObjectId(mongo_id)})
        if record is None:
            print("Record not found.")
        return record
    except PyMongoError as error:
        print("Could not retrieve record:", error)
        return None


def add_record():
    print("\n--- ADD E-WASTE RECORD ---")
    item_name = read_text("Item name: ")
    category = read_text(
        "Category (TV/Mobile/Laptop/Appliance): ", VALID_CATEGORIES
    )
    brand = read_text("Brand: ")
    condition = read_text(
        "Condition (Working/Partially Working/Broken): ", VALID_CONDITIONS
    )
    location = read_text("Location: ")
    quantity = read_number("Quantity (whole number, minimum 1): ", minimum=1)
    weight = read_number("Weight in kg (minimum 0): ", minimum=0, allow_decimal=True)
    price = read_number(
        "Estimated recycled price in USD (enter 0 if unknown): ",
        minimum=0,
        allow_decimal=True
    )

    record = {
        "Item_Name": item_name,
        "Category": category,
        "Brand": brand,
        "Condition": condition,
        "Location": location,
        "Quantity": quantity,
        "Weight_kg": weight,
        "Recycled_Price_USD": price,
        "Recycle_Method": "Pending",
        "End_Use": "Pending processing"
    }

    try:
        result = collection.insert_one(record)
        print("Record added successfully!")
        print("MongoDB ID:", result.inserted_id)
    except PyMongoError as error:
        print("Could not add record:", error)


def view_records():
    print("\n--- VIEW E-WASTE RECORDS ---")
    try:
        total_records = collection.count_documents({})
        print("Total records:", total_records)
        if total_records == 0:
            print("No records available.")
            return

        page_size = 10
        max_page = (total_records + page_size - 1) // page_size
        page = read_number(f"Page number (1 to {max_page}): ", minimum=1)
        if page > max_page:
            print("That page does not exist.")
            return

        records = collection.find().sort("_id", 1).skip((page - 1) * page_size).limit(page_size)
        for record in records:
            display_record(record)
    except PyMongoError as error:
        print("Could not view records:", error)


def safe_regex(value):
    """Treat user input as literal text, not as a raw regular expression."""
    return re.escape(value)


def search_record():
    print("\n--- SEARCH E-WASTE RECORDS ---")
    print("1. Search item name")
    print("2. Search category")
    print("3. Search location")
    print("4. Search by MongoDB ID")
    choice = input("Choose search option: ").strip()

    if choice == "4":
        record = find_by_mongo_id()
        if record:
            display_record(record)
        return

    fields = {
        "1": ("Item_Name", "Enter item name: "),
        "2": ("Category", "Enter category: "),
        "3": ("Location", "Enter location: ")
    }
    if choice not in fields:
        print("Invalid choice.")
        return

    field, prompt = fields[choice]
    value = input(prompt).strip()
    if not value:
        print("Search value cannot be empty.")
        return

    try:
        records = list(collection.find({
            field: {"$regex": safe_regex(value), "$options": "i"}
        }).limit(20))
        if not records:
            print("No matching records found.")
            return
        print(f"\nShowing {len(records)} matching record(s), maximum 20:")
        for record in records:
            display_record(record)
    except PyMongoError as error:
        print("Search failed:", error)


def update_record():
    print("\n--- UPDATE E-WASTE RECORD ---")
    record = find_by_mongo_id()
    if not record:
        return

    print("Current record:")
    display_record(record)

    fields = {
        "1": ("Item_Name", "Item name", None),
        "2": ("Category", "Category", VALID_CATEGORIES),
        "3": ("Condition", "Condition", VALID_CONDITIONS),
        "4": ("Location", "Location", None),
        "5": ("Recycle_Method", "Recycling method", VALID_RECYCLING_METHODS),
        "6": ("End_Use", "Status / end use", None),
        "7": ("Brand", "Brand", None)
    }

    print("What do you want to update?")
    for key, (_, label, _) in fields.items():
        print(f"{key}. {label}")
    choice = input("Choose field: ").strip()

    if choice not in fields:
        print("Invalid choice.")
        return

    field, label, allowed_values = fields[choice]
    new_value = read_text(f"Enter new {label.lower()}: ", allowed_values)

    try:
        result = collection.update_one(
            {"_id": record["_id"]},
            {"$set": {field: new_value}}
        )
        if result.modified_count:
            print("Record updated successfully!")
        else:
            print("No changes were made.")
    except PyMongoError as error:
        print("Update failed:", error)


def delete_record():
    print("\n--- DELETE E-WASTE RECORD ---")
    record = find_by_mongo_id()
    if not record:
        return

    display_record(record)
    confirm = input("Delete this record permanently? (yes/no): ").strip().lower()
    if confirm != "yes":
        print("Deletion cancelled.")
        return

    try:
        result = collection.delete_one({"_id": record["_id"]})
        if result.deleted_count == 1:
            print("Record deleted successfully.")
        else:
            print("Record was not deleted.")
    except PyMongoError as error:
        print("Delete failed:", error)


def show_statistics():
    print("\n--- DATASET STATISTICS ---")
    try:
        total_records = collection.count_documents({})
        print("Total records:", total_records)
        if total_records == 0:
            print("No data available for statistics.")
            return

        print("\nCategory-wise statistics:")
        pipeline = [
            {"$group": {
                "_id": "$Category",
                "records": {"$sum": 1},
                "total_quantity": {"$sum": {"$convert": {
                    "input": "$Quantity", "to": "double",
                    "onError": 0, "onNull": 0
                }}},
                "total_weight": {"$sum": {"$convert": {
                    "input": "$Weight_kg", "to": "double",
                    "onError": 0, "onNull": 0
                }}}
            }},
            {"$sort": {"records": -1}}
        ]
        for item in collection.aggregate(pipeline):
            print(
                f"Category: {item['_id'] or 'Unknown'} | "
                f"Records: {item['records']} | "
                f"Quantity: {item['total_quantity']:g} | "
                f"Weight: {item['total_weight']:.2f} kg"
            )

        print("\nTop 5 locations by record count:")
        location_pipeline = [
            {"$group": {"_id": "$Location", "records": {"$sum": 1}}},
            {"$sort": {"records": -1}},
            {"$limit": 5}
        ]
        for item in collection.aggregate(location_pipeline):
            print(f"{item['_id'] or 'Unknown'}: {item['records']} records")

        print("\nCondition-wise statistics:")
        condition_pipeline = [
            {"$group": {"_id": "$Condition", "records": {"$sum": 1}}},
            {"$sort": {"records": -1}}
        ]
        for item in collection.aggregate(condition_pipeline):
            print(f"{item['_id'] or 'Unknown'}: {item['records']} records")
    except PyMongoError as error:
        print("Could not calculate statistics:", error)


def filter_records():
    print("\n--- FILTER E-WASTE RECORDS ---")
    print("1. Filter by category")
    print("2. Filter by condition")
    print("3. Filter by location")
    print("4. Filter by recycling method")
    choice = input("Choose filter: ").strip()

    fields = {
        "1": ("Category", "Enter category: "),
        "2": ("Condition", "Enter condition: "),
        "3": ("Location", "Enter location: "),
        "4": ("Recycle_Method", "Enter recycling method: ")
    }
    if choice not in fields:
        print("Invalid choice.")
        return

    field, prompt = fields[choice]
    value = input(prompt).strip()
    if not value:
        print("Value cannot be empty.")
        return

    try:
        records = list(collection.find({
            field: {"$regex": safe_regex(value), "$options": "i"}
        }).sort("_id", 1).limit(20))
        if not records:
            print("No matching records found.")
            return
        print("\nMatching records (showing up to 20):")
        for record in records:
            display_record(record)
    except PyMongoError as error:
        print("Filtering failed:", error)


def sort_records():
    print("\n--- SORT E-WASTE RECORDS ---")
    print("1. Heaviest items first")
    print("2. Lightest items first")
    print("3. Highest recycled price first")
    print("4. Largest quantity first")
    choice = input("Choose sorting option: ").strip()

    sort_options = {
        "1": ("Weight_kg", -1),
        "2": ("Weight_kg", 1),
        "3": ("Recycled_Price_USD", -1),
        "4": ("Quantity", -1)
    }
    if choice not in sort_options:
        print("Invalid choice.")
        return

    field, direction = sort_options[choice]
    try:
        records = list(collection.find().sort(field, direction).limit(10))
        if not records:
            print("No records available.")
            return
        print("\nTop 10 records:")
        for record in records:
            display_record(record)
    except PyMongoError as error:
        print("Sorting failed:", error)


def main():
    try:
        client.admin.command("ping")
        print("Connected to MongoDB successfully.")
        print("Database: ewaste_db | Collection: ewaste_records")
    except PyMongoError as error:
        print("Could not connect to MongoDB. Make sure MongoDB is running.")
        print("Details:", error)
        return

    while True:
        print("\n===================================")
        print("      E-WASTE MANAGEMENT SYSTEM")
        print("===================================")
        print("1. Add record")
        print("2. View records")
        print("3. Search records")
        print("4. Update record")
        print("5. Delete record")
        print("6. Dataset statistics")
        print("7. Filter records")
        print("8. Sort records")
        print("0. Exit")

        choice = input("Enter your choice: ").strip()
        if choice == "1":
            add_record()
        elif choice == "2":
            view_records()
        elif choice == "3":
            search_record()
        elif choice == "4":
            update_record()
        elif choice == "5":
            delete_record()
        elif choice == "6":
            show_statistics()
        elif choice == "7":
            filter_records()
        elif choice == "8":
            sort_records()
        elif choice == "0":
            print("Thank you for using the E-Waste Management System!")
            break
        else:
            print("Invalid choice. Please enter a number from 0 to 8.")


if __name__ == "__main__":
    try:
        main()
    finally:
        client.close()
