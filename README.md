
🚗 Vehicle Registration System

📌 Project Overview
This is a mini-project for a Vehicle Registration System using MySQL WorkBench, streamlit. It allows users to register vehicles, manage ownership, perform inspections, maintain address, handle registration fees.

✨ Features
User & Admin Authentication
Vehicle Registration & Management
Owner Details & Address Storage
Vehicle Inspection & Fee Tracking
Responsive Web Interface
Database Integration with MySQL WorkBench

🏗 Tech Stack
Backend: Python
Database: MySQL
Frameworks/Libraries: SQLAlchemy, Streamlit

📂 Project Structure

/vehicle-registration-system
│── vehicle_res.py # main code
│── README.md     # Project documentation

🚀 Installation & Setup
1.Clone the repository
   git clone https://github.com/your-username/vehicle-registration.git
   cd vehicle-registration
2.Create a virtual environment and install dependencies
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   pip install -r requirements.txt
3.Create a New Database
   *Open MySQL Workbench and connect to your MySQL server.
   *Click on the SQL Editor (Query tab).
   *Run the following SQL command to create the database:

      CREATE DATABASE vehicle_registration;
   *Select the newly created database:

      USE vehicle_registration;

4.Run the application

   streamlit run vehicle_res.py
   
   Open http://127.0.0.1:5000/ in your browser.

🛠 Future Enhancements
Add an API for vehicle lookup
Implement an admin dashboard with analytics
Integrate payment gateway for fee processing

🤝 Contribution
Feel free to fork this repository and contribute to the project.
