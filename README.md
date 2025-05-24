# Chaluu Plate - Vehicle Details App

## Overview
Chaluu Plate is a Streamlit-based app that detects vehicle details (color, type, and number plate) from uploaded images and retrieves owner information from a MySQL database. It also supports sending SMS notifications to the vehicle owner via Twilio.

---

## Setup and Installation

### 1. Clone the repository
git clone <your-repo-url>
cd <your-repo-folder>
### 2. Create and activate a Python virtual environment (optional but recommended)

python -m venv venv
source venv/bin/activate    # Linux/macOS
venv\Scripts\activate       # Windows
### 3. Install dependencies
pip install -r requirements.txt
requirements.txt content:
tensorflow
keras
numpy
opencv-python
ultralytics
pytesseract
matplotlib
streamlit
mysql-connector-python
python-Levenshtein
twilio
### Database Setup (MySQL)
You need to create a MySQL database and a table named vehicles with the following structure for the app to work:

sql
CREATE DATABASE vehicle_db;

USE vehicle_db;

CREATE TABLE vehicles (
    number_plate VARCHAR(20) PRIMARY KEY,
    owner_name VARCHAR(100),
    owner_phone VARCHAR(15),
    car_color VARCHAR(50),
    vehicle_type VARCHAR(50)
);

Note: Populate this table with vehicle records for lookup functionality.

Ensure MySQL server is running and accessible.

Configuration
MySQL Connection
Edit your database credentials in the relevant Python file (e.g., db.py or wherever the MySQL connection is established):

db_config = {
    "host": "localhost",
    "user": "<your_mysql_username>",
    "password": "<your_mysql_password>",
    "database": "vehicle_db"
}
Twilio API Setup
Create a Twilio account: https://www.twilio.com/try-twilio

Get your Account SID, Auth Token, and buy a Twilio phone number.

Store your Twilio credentials in the sms.py file:

account_sid = "<your_twilio_account_sid>"
auth_token = "<your_twilio_auth_token>"
from_phone_number = "<your_twilio_phone_number>"


Running the App

1. Upload images via the app
When running, the app will save uploaded images to the uploaded folder automatically.

2. Run the Streamlit app
Run the main application file (assumed to be main.py):
streamlit run main.py

3. upload image from pictures
in the streamlit app click on brownse file and choose the image in the pictures folder and test it with the image inside the test folder within pictures


