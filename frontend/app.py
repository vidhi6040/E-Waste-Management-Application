
from flask import (
    Flask, render_template, request,
    redirect, url_for, flash, Response
)
from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime
from pathlib import Path
import csv
import io
import math

app = Flask(__name__)
app.secret_key = "ewaste-local-development-key"

# Existing MongoDB database — do not recreate or re-import data
client = MongoClient("mongodb://localhost:27017/", serverSelectionTimeoutMS=3000)
db = client["ewaste_db"]
collection = db["ewaste_records"]

CATEGORIES = ["TV", "Mobile", "Laptop", "Appliance"]
CONDITIONS = ["Working", "Partially Working", "Broken"]
METHODS = ["Manual", "Automated", "Both", "Pending"]


def get_records(query=None):
    query = query or {}
    records = list(collection.find(query).sort("_id", -1))

    for record in records:
        record["_id"] = str(record["_id"])

    return records


def get_dashboard_stats(query=None):
    query = query or {}

    total_records = collection.count_documents(query)
    totals = list(collection.aggregate([
        {"$match": query},
        {"$group": {
            "_id": None,
            "quantity": {"$sum": {"$ifNull": ["$Quantity", 0]}},
            "weight": {"$sum": {"$ifNull": ["$Weight_kg", 0]}},
            "price": {"$sum": {"$ifNull": ["$Recycled_Price_USD", 0]}}
        }}
    ]))

    summary = totals[0] if totals else {}

    return {
        "total_records": total_records,
        "quantity": summary.get("quantity", 0),
        "weight": summary.get("weight", 0),
        "price": summary.get("price", 0)
    }


def make_filter():
    query = {}

    category = request.args.get("category", "").strip()
    condition = request.args.get("condition", "").strip()
    location = request.args.get("location", "").strip()
    search = request.args.get("search", "").strip()

    if category in CATEGORIES:
        query["Category"] = category

    if condition in CONDITIONS:
        query["Condition"] = condition

    if location:
        query["Location"] = {
            "$regex": __import__("re").escape(location),
            "$options": "i"
        }

    if search:
        safe_search = __import__("re").escape(search)
        query["$or"] = [
            {"Item_Name": {"$regex": safe_search, "$options": "i"}},
            {"Brand": {"$regex": safe_search, "$options": "i"}},
            {"Model": {"$regex": safe_search, "$options": "i"}},
            {"Location": {"$regex": safe_search, "$options": "i"}}
        ]

    return query


@app.route("/")
def dashboard():
    query = make_filter()
    stats = get_dashboard_stats(query)

    category_data = list(collection.aggregate([
        {"$match": query},
        {"$group": {
            "_id": {"$ifNull": ["$Category", "Unknown"]},
            "count": {"$sum": 1},
            "weight": {"$sum": {"$ifNull": ["$Weight_kg", 0]}}
        }},
        {"$sort": {"count": -1}}
    ]))

    condition_data = list(collection.aggregate([
        {"$match": query},
        {"$group": {
            "_id": {"$ifNull": ["$Condition", "Unknown"]},
            "count": {"$sum": 1}
        }},
        {"$sort": {"count": -1}}
    ]))

    location_data = list(collection.aggregate([
        {"$match": query},
        {"$group": {
            "_id": {"$ifNull": ["$Location", "Unknown"]},
            "count": {"$sum": 1}
        }},
        {"$sort": {"count": -1}},
        {"$limit": 8}
    ]))

    return render_template(
        "dashboard.html",
        stats=stats,
        category_data=category_data,
        condition_data=condition_data,
        location_data=location_data,
        categories=CATEGORIES,
        conditions=CONDITIONS,
        selected_category=request.args.get("category", ""),
        selected_condition=request.args.get("condition", ""),
        selected_location=request.args.get("location", ""),
        search=request.args.get("search", "")
    )


@app.route("/records")
def records_page():
    query = make_filter()
    records = get_records(query)

    return render_template(
        "records.html",
        records=records,
        categories=CATEGORIES,
        conditions=CONDITIONS,
        methods=METHODS,
        selected_category=request.args.get("category", ""),
        selected_condition=request.args.get("condition", ""),
        selected_location=request.args.get("location", ""),
        search=request.args.get("search", "")
    )


def read_form_data():
    name = request.form.get("Item_Name", "").strip()
    brand = request.form.get("Brand", "").strip()
    model = request.form.get("Model", "").strip()
    category = request.form.get("Category", "").strip()
    condition = request.form.get("Condition", "").strip()
    method = request.form.get("Recycle_Method", "").strip()
    location = request.form.get("Location", "").strip()

    if not all([name, brand, model, category, condition, method, location]):
        raise ValueError("Please fill in all required fields.")

    if category not in CATEGORIES:
        raise ValueError("Please select a valid category.")

    if condition not in CONDITIONS:
        raise ValueError("Please select a valid condition.")

    if method not in METHODS:
        raise ValueError("Please select a valid recycling method.")

    def number(field, minimum=0, integer=False):
        value = float(request.form.get(field, ""))
        if not math.isfinite(value) or value < minimum:
            raise ValueError(f"Invalid value for {field}.")
        if integer:
            if not value.is_integer():
                raise ValueError(f"{field} must be a whole number.")
            return int(value)
        return value

    return {
        "Item_Name": name,
        "Brand": brand,
        "Model": model,
        "Category": category,
        "Year_of_Purchase": number("Year_of_Purchase", 1900, True),
        "Condition": condition,
        "Quantity": number("Quantity", 1, True),
        "Weight_kg": number("Weight_kg"),
        "Recycle_Method": method,
        "Location": location,
        "Recycling_Facility": request.form.get("Recycling_Facility", "").strip(),
        "Collection_Date": request.form.get("Collection_Date", "").strip(),
        "End_Use": request.form.get("End_Use", "").strip(),
        "Recycled_Price_USD": number("Recycled_Price_USD"),
        "Toxic_Components": request.form.get("Toxic_Components", "").strip(),
        "E-Waste_Collector": request.form.get("E-Waste_Collector", "").strip(),
        "Carbon_Footprint": request.form.get("Carbon_Footprint", "").strip(),
        "Exported_To": request.form.get("Exported_To", "").strip()
    }


@app.route("/add", methods=["GET", "POST"])
def add_record():
    if request.method == "POST":
        try:
            record = read_form_data()
            collection.insert_one(record)
            flash("E-waste record added successfully.", "success")
            return redirect(url_for("records_page"))
        except (ValueError, TypeError, OverflowError) as error:
            flash(str(error), "error")

    return render_template(
        "record_form.html",
        record={},
        categories=CATEGORIES,
        conditions=CONDITIONS,
        methods=METHODS,
        page_title="Add E-Waste Record"
    )


@app.route("/edit/<record_id>", methods=["GET", "POST"])
def edit_record(record_id):
    if not ObjectId.is_valid(record_id):
        flash("Invalid record ID.", "error")
        return redirect(url_for("records_page"))

    record = collection.find_one({"_id": ObjectId(record_id)})

    if not record:
        flash("Record not found.", "error")
        return redirect(url_for("records_page"))

    if request.method == "POST":
        try:
            updated_record = read_form_data()
            collection.update_one(
                {"_id": ObjectId(record_id)},
                {"$set": updated_record}
            )
            flash("Record updated successfully.", "success")
            return redirect(url_for("records_page"))
        except (ValueError, TypeError, OverflowError) as error:
            flash(str(error), "error")

    record["_id"] = str(record["_id"])

    return render_template(
        "record_form.html",
        record=record,
        categories=CATEGORIES,
        conditions=CONDITIONS,
        methods=METHODS,
        page_title="Edit E-Waste Record"
    )


@app.route("/delete/<record_id>", methods=["POST"])
def delete_record(record_id):
    if not ObjectId.is_valid(record_id):
        flash("Invalid record ID.", "error")
        return redirect(url_for("records_page"))

    result = collection.delete_one({"_id": ObjectId(record_id)})

    if result.deleted_count:
        flash("Record deleted successfully.", "success")
    else:
        flash("Record not found.", "error")

    return redirect(url_for("records_page"))


@app.route("/export")
def export_csv():
    query = make_filter()
    records = list(collection.find(query, {"_id": 0}))

    if not records:
        flash("No records available to export.", "error")
        return redirect(url_for("records_page"))

    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=list(records[0].keys()))
    writer.writeheader()
    writer.writerows(records)

    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment; filename=ewaste_records.csv"}
    )


@app.route("/health")
def health():
    try:
        client.admin.command("ping")
        return {"status": "connected", "database": db.name,
                "collection": collection.name}
    except Exception:
        return {"status": "database unavailable"}, 503


if __name__ == "__main__":
    try:
        client.admin.command("ping")
        print("Connected to existing MongoDB database:", db.name)
        print("Records currently in collection:", collection.count_documents({}))
    except Exception as error:
        print("MongoDB connection failed:", error)
        raise SystemExit(1)

    app.run(debug=True)
