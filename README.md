# E-Waste Management System

## 1. Project Overview
The E-Waste Management System is a Python-based application that uses MongoDB to store and manage electronic waste records. It allows users to add, view, search, update, delete, filter, and sort records. It also provides statistical analysis, data visualizations, and report exports.

## 2. Problem Statement
Electronic waste contains materials that can harm the environment if not handled properly. Managing e-waste records helps organize information about electronic items, their condition, quantity, weight, collection locations, and recycling methods.

## 3. Objectives
- Store and manage e-waste records using MongoDB.
- Perform CRUD operations on records.
- Search and filter records efficiently.
- Analyze e-waste by category, condition, and location.
- Generate charts and export reports for further analysis.

## 4. Technologies Used
- **Python** — application logic
- **MongoDB** — NoSQL database
- **PyMongo** — Python-MongoDB connection
- **Pandas** — data processing and report generation
- **Matplotlib** — data visualization
- **OpenPyXL** — Excel report export

## 5. Main Features
1. Add e-waste records
2. View records with pagination
3. Search records
4. Update existing records
5. Delete records with confirmation
6. Display dataset statistics using MongoDB aggregation
7. Filter records by category, condition, location, and recycling method
8. Sort records by weight, recycled price, and quantity
9. Generate charts
10. Export data to CSV and Excel reports

## 6. Database Details
- **Database:** `ewaste_db`
- **Collection:** `ewaste_records`

The collection stores fields such as item name, brand, model, category, condition, quantity, weight, location, recycling method, recycling facility, and estimated recycled price.

MongoDB's `_id` field is used to identify individual records.

## 7. Project Structure
```text
E-Waste-Management/
├── data/
│   └── e_waste_dataset.csv
├── charts/
├── reports/
├── main.py
├── import_dataset.py
├── charts.py
├── dashboard.py
├── export_reports.py
├── requirements.txt
└── README.md
```

## 8. Installation and Execution
1. Install Python and MongoDB.
2. Open the project folder in VS Code.
3. Activate the virtual environment.
4. Install the required packages:
   `pip install -r requirements.txt`
5. Ensure MongoDB is running.
6. Run the main application:
   `python main.py`
7. Run the dashboard:
   `python dashboard.py`
8. Generate charts:
   `python charts.py`
9. Export reports:
   `python export_reports.py`

## 9. Dataset and Limitations
The project uses an e-waste dataset containing 3,000 original records. Additional records may be created through the application's Add Record feature.

The dataset contains some missing values and inconsistent category labels. Therefore, the quality of the analysis depends on the quality of the available data. Input validation helps maintain consistency for newly added and updated records.

## 10. Conclusion
The E-Waste Management System demonstrates how Python and MongoDB can be used together to manage electronic waste data. CRUD operations, filtering, sorting, aggregation, visualizations, and report generation make the system useful for organizing and analyzing e-waste records.
