# ♻️ E-Waste Management System

A web-based E-Waste Management Application built using **Python, Flask, MongoDB, HTML, CSS, and JavaScript**. The application provides an interactive interface for managing electronic waste records, monitoring e-waste data, performing database operations, and generating meaningful insights through data visualization and reports.

## 📌 Project Overview

Electronic waste (e-waste) is one of the fastest-growing environmental challenges. Managing discarded electronic devices requires an organized system to maintain records, track quantities, monitor recycling activities, and analyze collected data.

The E-Waste Management System provides a centralized platform to manage electronic waste efficiently. It features a Flask-powered web interface connected to a MongoDB database, allowing users to interact with records through a browser instead of manually executing database queries.

The application combines web development, database management, and data analytics to simplify e-waste record management.

## ✨ Key Features

### 1. Interactive Web Interface

The application provides a web-based interface developed using Flask, HTML, CSS, and JavaScript.

- Dynamic pages rendered using Flask and Jinja2 templates.
- Dashboard for accessing important application information.
- Dedicated interface for viewing and managing e-waste records.
- Forms for adding and updating records.
- Reusable base template for consistent navigation and layout.
- Organized CSS and static assets.

### 2. Dashboard

- Centralized dashboard for accessing application functionality.
- Overview of e-waste records and relevant statistics.
- Easy navigation between different application sections.
- Visual representation of important information.

### 3. E-Waste Record Management

- Add new electronic waste records.
- View existing records.
- Update record information.
- Delete unwanted records.
- Manage electronic waste information through the web interface.

### 4. Search, Filtering and Sorting

- Search for specific e-waste records.
- Filter records using relevant attributes.
- Sort records based on selected fields.
- Retrieve relevant information efficiently.

### 5. MongoDB Database Integration

- Store e-waste records in MongoDB.
- Perform database operations using Python and PyMongo.
- Support CRUD operations.
- Use MongoDB aggregation pipelines for data analysis.

### 6. Data Analytics and Visualization

- Analyze e-waste records and distributions.
- Generate statistical summaries.
- Visualize relevant data through charts.
- Identify useful patterns in the collected dataset.

### 7. Report Generation

- Export records into CSV format.
- Generate Excel reports.
- Organize processed data for further analysis.

## 🖥️ Frontend Architecture

The frontend is developed using **Flask, HTML, CSS, and JavaScript**. Flask handles routing and renders HTML templates to provide a dynamic web application.

### Frontend Structure

```text
frontend/
│
├── app.py
├── requirements.txt
│
├── static/
│   ├── css/
│   │   └── style.css
│   │
│   └── js/
│
└── templates/
    ├── base.html
    ├── dashboard.html
    ├── records.html
    └── record_form.html
```

### Frontend Components

| File | Responsibility |
|---|---|
| `app.py` | Flask application, routing, and frontend integration |
| `base.html` | Common layout and reusable page structure |
| `dashboard.html` | Main dashboard interface |
| `records.html` | Displays e-waste records |
| `record_form.html` | Form for adding and updating records |
| `style.css` | Application styling and layout |
| `static/js/` | JavaScript functionality |

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python | Application logic and backend processing |
| Flask | Web application framework |
| HTML5 | Webpage structure |
| CSS3 | Styling and responsive layouts |
| JavaScript | Client-side interactions |
| MongoDB | NoSQL database |
| PyMongo | Python-MongoDB integration |
| Pandas | Data processing and analysis |
| Matplotlib | Data visualization |
| OpenPyXL | Excel report generation |

## 🗄️ Database Design

**Database:** `ewaste_db`

**Collection:** `ewaste_records`

The MongoDB database stores electronic waste information, including fields such as:

- Item name
- Brand and model
- E-waste category
- Device condition
- Quantity
- Weight
- Collection location
- Recycling method
- Recycling facility
- Estimated recycled price

MongoDB provides flexible document-based storage for managing e-waste records.

## 📂 Project Structure

```text
E-Waste-Management-Application/
│
├── frontend/
│   ├── app.py
│   ├── requirements.txt
│   ├── static/
│   │   ├── css/
│   │   └── js/
│   └── templates/
│       ├── base.html
│       ├── dashboard.html
│       ├── records.html
│       └── record_form.html
│
├── data/
│   └── e_waste_dataset.csv
│
├── charts/
├── reports/
│
├── main.py
├── import_dataset.py
├── charts.py
├── dashboard.py
├── export_reports.py
├── requirements.txt
└── README.md
```

## 🚀 Installation and Setup

Follow these steps to run the application locally.

### Prerequisites

Make sure the following are installed:

- Python 3.9 or above
- MongoDB Community Server
- Git
- A web browser

### Step 1: Clone the Repository

```bash
git clone https://github.com/vidhi6040/E-Waste-Management-Application.git
```

Navigate to the project directory:

```bash
cd E-Waste-Management-Application
```

### Step 2: Create a Virtual Environment

```bash
python -m venv venv
```

Activate the environment.

**Windows PowerShell:**

```powershell
.\venv\Scripts\Activate.ps1
```

**Linux / macOS:**

```bash
source venv/bin/activate
```

### Step 3: Install Backend Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Configure MongoDB

Make sure MongoDB is installed and running on your system.

The application uses MongoDB for storing and retrieving e-waste records.

If your application uses a custom MongoDB connection string, configure it according to the database settings in the source code.

### Step 5: Run the Frontend Application

Navigate to the frontend directory:

```bash
cd frontend
```

Install frontend application dependencies:

```bash
pip install -r requirements.txt
```

Start the Flask application:

```bash
python app.py
```

Once the Flask server starts successfully, open the local URL displayed in the terminal in your web browser.

The default Flask development address is generally:

```text
http://127.0.0.1:5000/
```

### Step 6: Access the Application

Open your browser and visit the local application URL.

You can now interact with the web interface, navigate through the dashboard, view e-waste records, and use the available record management functionality.

**Note:** Run the frontend Flask application from the `frontend` directory. Keep MongoDB running while using database-dependent functionality.

## 📊 Dataset

The project includes an e-waste dataset containing approximately 3,000 records.

Dataset location:

```text
data/e_waste_dataset.csv
```

The dataset is used for storing, processing, and analyzing electronic waste information.

## 🔍 Key Learning Outcomes

This project demonstrates practical implementation of:

- Full-stack application development.
- Flask routing and template rendering.
- Frontend development using HTML, CSS, and JavaScript.
- MongoDB database integration.
- CRUD operations using PyMongo.
- MongoDB aggregation pipelines.
- Data processing with Pandas.
- Data visualization with Matplotlib.
- CSV and Excel report generation.

## 🔮 Future Enhancements

- User authentication and role-based access control.
- Advanced dashboard analytics.
- Real-time e-waste collection tracking.
- Predictive analytics for e-waste generation.
- Integration with recycling facilities.
- Enhanced reporting and data visualization.

## 👩‍💻 Author

**Diya**

GitHub: [@vidhi6040](https://github.com/vidhi6040)

**Project Repository:** [E-Waste Management Application](https://github.com/vidhi6040/E-Waste-Management-Application)

---

⭐ If you find this project useful, consider giving the repository a star!
