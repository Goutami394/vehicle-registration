import streamlit as st
import re
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Date, Numeric, Boolean, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

# Set page configuration
st.set_page_config(page_title="🚗 Vehicle Registration System")


# Database configuration
DATABASE_URI = 'mysql+pymysql://root:goutami123@localhost/vehicle_registration'
engine = create_engine(DATABASE_URI)
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()

# Models
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(150), unique=True, nullable=False)
    password = Column(String(150), nullable=False)
    is_admin = Column(Boolean, default=False)

class Owner(Base):
    __tablename__ = 'owners'
    owner_id = Column(Integer, primary_key=True)
    first_name = Column(String(50))
    last_name = Column(String(50))
    email = Column(String(100), unique=True)
    phone = Column(String(15), unique=True)
    addresses = relationship('Address', backref='owner', lazy=True)
    vehicles = relationship('Vehicle', backref='owner', lazy=True)
    UniqueConstraint('first_name', 'last_name', 'phone', name='uq_owner')

class Address(Base):
    __tablename__ = 'addresses'
    address_id = Column(Integer, primary_key=True)
    owner_id = Column(Integer, ForeignKey('owners.owner_id'), nullable=False)
    street = Column(String(100))
    city = Column(String(50))
    state = Column(String(50))
    zip = Column(String(10))

class Vehicle(Base):
    __tablename__ = 'vehicles'
    vehicle_id = Column(Integer, primary_key=True)
    owner_id = Column(Integer, ForeignKey('owners.owner_id'), nullable=False)
    make = Column(String(50))
    model = Column(String(50))
    year = Column(Integer)
    plate_number = Column(String(20))
    inspections = relationship('Inspection', backref='vehicle', lazy=True)
    fees = relationship('Fee', backref='vehicle', lazy=True)

class Inspection(Base):
    __tablename__ = 'inspections'
    inspection_id = Column(Integer, primary_key=True)
    vehicle_id = Column(Integer, ForeignKey('vehicles.vehicle_id'), nullable=False)
    inspection_date = Column(Date)
    result = Column(String(50))

class Fee(Base):
    __tablename__ = 'fees'
    fee_id = Column(Integer, primary_key=True)
    vehicle_id = Column(Integer, ForeignKey('vehicles.vehicle_id'), nullable=False)
    amount = Column(Numeric(10, 2))
    due_date = Column(Date)
    paid = Column(Boolean)

# User authentication
def check_user_credentials(username, password):
    user = session.query(User).filter_by(username=username, password=password).first()
    return user

# Validate email format
def validate_email(email):
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return False
    return True

# Validate phone number (digits only)
def validate_phone(phone):
    if not re.match(r"^\d+$", phone):
        return False
    return True

# Display login or signup form
def display_login_signup():
    st.title("Login / Sign Up")
    st.write("Please log in or sign up to access the system.")
    
    # Login form
    with st.form("login_form"):
        st.subheader("Login")
        username = st.text_input("Username", placeholder="Enter your username")
        password = st.text_input("Password", type="password", placeholder="Enter your password")
        submit_button = st.form_submit_button("Login")

        if submit_button:
            if not username or not password:
                st.error("Username and Password are required.")
            else:
                user = check_user_credentials(username, password)
                if user:
                    st.session_state['user'] = user
                    st.session_state['is_logged_in'] = True
                    st.session_state['show_login'] = False
                else:
                    st.error("Invalid username or password")
    
    # Signup form
    with st.form("signup_form"):
        st.subheader("Sign Up")
        new_username = st.text_input("New Username", placeholder="Choose a username")
        new_password = st.text_input("New Password", type="password", placeholder="Choose a password")
        submit_button = st.form_submit_button("Sign Up")

        if submit_button:
            if not new_username or not new_password:
                st.error("Username and Password are required.")
            else:
                existing_user = session.query(User).filter_by(username=new_username).first()
                if existing_user:
                    st.error("Username already exists!")
                else:
                    new_user = User(username=new_username, password=new_password)
                    session.add(new_user)
                    session.commit()
                    st.success("Sign up successful! You can now log in.")
                    st.session_state['show_login'] = True

# Streamlit App
if 'is_logged_in' not in st.session_state or not st.session_state['is_logged_in']:
    if st.session_state.get('show_login', True):
        display_login_signup()
    else:
        st.session_state['is_logged_in'] = False
else:
    st.title("🚗 Vehicle Registration System")
    
    # Menu navigation
    menu = ["🏠 Home", "👥 View Owners", "➕ Add Owner", "🚗 View Vehicles", "➕ Add Vehicle", "🏠 View Addresses", "➕ Add Address", "💵 View Fees", "➕ Add Fee", "🔍 View Inspections", "➕ Add Inspection"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "🏠 Home":
        st.subheader("🏠 Welcome to the Vehicle Registration System")
        st.write("Welcome to the **Vehicle Registration System**! This application allows you to manage vehicle registrations, inspections, fees, and owner information efficiently.")
        
        # Overview
        st.write("### Overview")
        st.write("""
        - **👥 Owners**: Manage owner information.
        - **🚗 Vehicles**: Register and manage vehicles.
        - **🏠 Addresses**: Maintain owner addresses.
        - **💵 Fees**: Track fees related to vehicle registrations.
        - **🔍 Inspections**: Record and view vehicle inspections.
        """)

        # Statistics
        st.write("### 📊 System Statistics")
        num_owners = session.query(Owner).count()
        num_vehicles = session.query(Vehicle).count()
        num_inspections = session.query(Inspection).count()
        num_fees = session.query(Fee).count()

        st.metric(label="Total Owners", value=num_owners)
        st.metric(label="Total Vehicles", value=num_vehicles)
        st.metric(label="Total Inspections", value=num_inspections)
        st.metric(label="Total Fees", value=num_fees)

        # Navigation Tips
        st.write("### 🧭 Navigation Tips")
        st.write("""
        Use the menu on the left to navigate through the system. Here are some quick tips:
        - **Add Owner**: Register a new vehicle owner.
        - **Add Vehicle**: Register a new vehicle to an owner.
        - **View Owners**: See the list of all registered owners.
        - **View Vehicles**: See the list of all registered vehicles.
        - **Add Address**: Add or update an owner's address.
        - **Add Fee**: Record a new fee for a vehicle.
        - **Add Inspection**: Record a new inspection for a vehicle.
        """)

        # Contact Information
        st.write("### 📞 Contact Us")
        st.write("For any support or inquiries, please contact us at: **support@vehicle-registration.com**")

    elif choice == "👥 View Owners":
        st.subheader("👥 Owners List")
        owners = session.query(Owner).all()
        for owner in owners:
            st.write(f"{owner.first_name} {owner.last_name} - {owner.email} - {owner.phone}")

    elif choice == "➕ Add Owner":
        st.subheader("➕ Add New Owner")
        with st.form("owner_form"):
            first_name = st.text_input("First Name", placeholder="Enter first name")
            last_name = st.text_input("Last Name", placeholder="Enter last name")
            email = st.text_input("Email", placeholder="example@example.com")
            phone = st.text_input("Phone", placeholder="0000 000 000")
            submit_button = st.form_submit_button("Add Owner")

            if submit_button:
                if not first_name or not last_name or not email or not phone:
                    st.error("All fields are required.")
                elif not validate_email(email):
                    st.error("Invalid email format. Please use a valid email address (e.g., example@example.com).")
                elif not validate_phone(phone):
                    st.error("Phone number must contain only digits.")
                else:
                    existing_owner = session.query(Owner).filter_by(email=email).first()
                    existing_phone = session.query(Owner).filter_by(phone=phone).first()
                    existing_name = session.query(Owner).filter_by(first_name=first_name, last_name=last_name).first()
                    if existing_owner:
                        st.error("An owner with this email already exists.")
                    elif existing_phone:
                        st.error("An owner with this phone number already exists.")
                    elif existing_name:
                        st.error("An owner with this name already exists.")
                    else:
                        new_owner = Owner(first_name=first_name, last_name=last_name, email=email, phone=phone)
                        session.add(new_owner)
                        session.commit()
                        st.success("Owner added successfully!")

    elif choice == "🚗 View Vehicles":
        st.subheader("🚗 Vehicles List")
        vehicles = session.query(Vehicle).all()
        for vehicle in vehicles:
            st.write(f"{vehicle.make} {vehicle.model} ({vehicle.year}) - Owner ID: {vehicle.owner_id}")

    elif choice == "➕ Add Vehicle":
        st.subheader("➕ Add New Vehicle")
        owners = session.query(Owner).all()
        owner_options = {owner.owner_id: f"{owner.first_name} {owner.last_name}" for owner in owners}

        with st.form("vehicle_form"):
            owner_id = st.selectbox("Owner", options=list(owner_options.keys()), format_func=lambda x: owner_options[x])
            make = st.text_input("Make", placeholder="Enter vehicle make")
            model = st.text_input("Model", placeholder="Enter vehicle model")
            year = st.number_input("Year", min_value=1886, max_value=2100, step=1, placeholder="Enter vehicle year")
            plate_number = st.text_input("Plate Number", placeholder="Enter plate number")
            submit_button = st.form_submit_button("Add Vehicle")

            if submit_button:
                if not make or not model or not year or not plate_number:
                    st.error("All fields are required.")
                else:
                    new_vehicle = Vehicle(owner_id=owner_id, make=make, model=model, year=year, plate_number=plate_number)
                    session.add(new_vehicle)
                    session.commit()
                    st.success("Vehicle added successfully!")

    elif choice == "🏠 View Addresses":
        st.subheader("🏠 Addresses List")
        addresses = session.query(Address).all()
        for address in addresses:
            st.write(f"{address.street}, {address.city}, {address.state}, {address.zip} - Owner ID: {address.owner_id}")

    elif choice == "➕ Add Address":
        st.subheader("➕ Add New Address")
        owners = session.query(Owner).all()
        owner_options = {owner.owner_id: f"{owner.first_name} {owner.last_name}" for owner in owners}

        with st.form("address_form"):
            owner_id = st.selectbox("Owner", options=list(owner_options.keys()), format_func=lambda x: owner_options[x])
            street = st.text_input("Street", placeholder="Enter street")
            city = st.text_input("City", placeholder="Enter city")
            state = st.text_input("State", placeholder="Enter state")
            zip = st.text_input("Zip", placeholder="Enter zip code")
            submit_button = st.form_submit_button("Add Address")

            if submit_button:
                if not street or not city or not state or not zip:
                    st.error("All fields are required.")
                else:
                    new_address = Address(owner_id=owner_id, street=street, city=city, state=state, zip=zip)
                    session.add(new_address)
                    session.commit()
                    st.success("Address added successfully!")

    elif choice == "💵 View Fees":
        st.subheader("💵 Fees List")
        fees = session.query(Fee).all()
        for fee in fees:
            st.write(f"Amount: {fee.amount}, Due Date: {fee.due_date}, Paid: {fee.paid} - Vehicle ID: {fee.vehicle_id}")

    elif choice == "➕ Add Fee":
        st.subheader("➕ Add New Fee")
        vehicles = session.query(Vehicle).all()
        vehicle_options = {vehicle.vehicle_id: f"{vehicle.make} {vehicle.model} ({vehicle.year})" for vehicle in vehicles}

        with st.form("fee_form"):
            vehicle_id = st.selectbox("Vehicle", options=list(vehicle_options.keys()), format_func=lambda x: vehicle_options[x])
            amount = st.number_input("Amount", min_value=0.0, step=0.01, placeholder="Enter fee amount")
            due_date = st.date_input("Due Date")
            paid = st.checkbox("Paid")
            submit_button = st.form_submit_button("Add Fee")

            if submit_button:
                if not amount or not due_date:
                    st.error("Amount and Due Date are required.")
                else:
                    new_fee = Fee(vehicle_id=vehicle_id, amount=amount, due_date=due_date, paid=paid)
                    session.add(new_fee)
                    session.commit()
                    st.success("Fee added successfully!")

    elif choice == "🔍 View Inspections":
        st.subheader("🔍 Inspections List")
        inspections = session.query(Inspection).all()
        for inspection in inspections:
            st.write(f"Date: {inspection.inspection_date}, Result: {inspection.result} - Vehicle ID: {inspection.vehicle_id}")

    elif choice == "➕ Add Inspection":
        st.subheader("➕ Add New Inspection")
        vehicles = session.query(Vehicle).all()
        vehicle_options = {vehicle.vehicle_id: f"{vehicle.make} {vehicle.model} ({vehicle.year})" for vehicle in vehicles}

        with st.form("inspection_form"):
            vehicle_id = st.selectbox("Vehicle", options=list(vehicle_options.keys()), format_func=lambda x: vehicle_options[x])
            inspection_date = st.date_input("Inspection Date")
            result = st.text_input("Result", placeholder="Enter inspection result")
            submit_button = st.form_submit_button("Add Inspection")

            if submit_button:
                if not inspection_date or not result:
                    st.error("Inspection Date and Result are required.")
                else:
                    new_inspection = Inspection(vehicle_id=vehicle_id, inspection_date=inspection_date, result=result)
                    session.add(new_inspection)
                    session.commit()
                    st.success("Inspection added successfully!")

if __name__ == '__main__':
    with engine.begin() as connection:
        Base.metadata.create_all(connection)
    st.write("🗄️ Database connected successfully!")
