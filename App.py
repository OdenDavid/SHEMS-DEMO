"""
In an environment with streamlit installed,
Run with `streamlit run App.py`
"""

# Streamlit and Data Visualization
import streamlit as st # For building the web application
import pandas as pd # Data manipulation and analysis
import plotly.express as px # Data visualization
import plotly.graph_objects as go # Data visualization

# Database Connectivity
import psycopg2
from urllib.parse import urlparse

# Email Sending
from email_validator import validate_email, EmailNotValidError # For validating email addresses
import smtplib # Simple Mail Transfer Protocol library for sending emails
from email.mime.text import MIMEText # For constructing email messages
from email.mime.image import MIMEImage # For constructing email messages
from email.mime.multipart import MIMEMultipart # For constructing email messages

# Miscellaneous
import random # For generating random numbers
from datetime import datetime # For working with dates and times
import math # For mathematical operations
import os # communicate with system

# =========== Establish Connection ==========
try:
    DATABASE_URL = os.getenv('DATABASE_URL')

    # Parse the URL
    result = urlparse(DATABASE_URL)

    # Extract the components
    username = result.username
    password = result.password
    database = result.path[1:]  # remove the leading '/'
    hostname = result.hostname
    port = result.port

    # Connect to the PostgreSQL database
    conn = psycopg2.connect(
        dbname=database,
        user=username,
        password=password,
        host=hostname,
        port=port
    )
    cursor = conn.cursor() # Cursor object
except psycopg2.OperationalError as e:
    st.error(body=f"Error: {e}", icon="🚨")

# ============= PAGE SETUP ============
# Set up the page configuration
st.set_page_config(
    page_title="SHEMS",  # Set the page title
    page_icon="",  # Set the page icon
    layout="wide"  # Set the page layout to wide
)

# ============== Session States/Pages ==================
# Initialize session states for page navigation and data storage
if "page" not in st.session_state:
    # Default page
    st.session_state.page = "home"
if "homeid" not in st.session_state:
    # Default home ID
    st.session_state.homeid = 0000
if "home_name" not in st.session_state:
    # Default home name
    st.session_state.home_name = "Default"
if "data_to_show" in st.session_state:
    # Initialize data to show
    st.session_state.data_to_show = {}
if "refresh_trigger" not in st.session_state:
    # Flag to trigger data refresh
    st.session_state.refresh_trigger = False

def goto_login():
    st.session_state.page = "login"  # Go to login page
    st.rerun()

def goto_dashboard(homeid, home_name):
    st.session_state.page = "dashboard"  # Go to dashboard
    st.session_state.homeid = homeid
    st.session_state.home_name = home_name
    st.rerun()

def restart():
    st.session_state.page = "home" # Go back to beginning
    st.rerun()

def sendmail(type, mail, homename="", homeid="", appliance_name="", appliance_type="", old_condition="", new_condition=""):
    """
    Sends an email based on the specified type.

    Args:
        type (str): Type of email to send (signup, add appliance, appliance condition)
        mail (str): Recipient's email address
        homename (str, optional): Home name. Defaults to "".
        homeid (str, optional): Home ID. Defaults to "".
        appliance_name (str, optional): Appliance name. Defaults to "".
        appliance_type (str, optional): Appliance type. Defaults to "".
        old_condition (str, optional): Old appliance condition. Defaults to "".
        new_condition (str, optional): New appliance condition. Defaults to "".
    """
    # Email configuratio
    from_email = "odendavid0@gmail.com"
    to_email = mail
    password = "hhpr lmml ulhk qytb"
    image_path = "images/mail.png"

    # Set email subject and body based on type
    if type == "signup":
        subject = "Welcome to SHEMS"
        body = f"""
                <html>
                <body>
                    <img src="cid:logo" alt="Logo">
                    <h3>Welcome to SHEMS!</h3>
                    <div>A warm welcome to SHEMS! We're thrilled to have you on board.</div>
                    <div>Your registration is now complete, and we're excited to help you manage your home's energy usage efficiently. To get started, please note down your login details:</div>
                    <ul>
                    <li>
                    <div>Home Name: <strong>{homename}</strong></div>
                    </li>
                    <li>
                    <div>Home ID: <strong>{homeid}</strong></div>
                    </li>
                    </ul>
                    <div>These will be your login credentials, so please remember them for future reference.</div>
                    <div>&nbsp;</div>
                    <div>With SHEMS, you'll be able to monitor and control your home's energy consumption, receive personalized recommendations, and enjoy a more sustainable living experience.</div>
                    <div>If you have any questions or need assistance, feel free to reply to this email or contact our support team.</div>
                    <div>&nbsp;</div>
                    <div>Thank you for choosing SHEMS!</div>
                    <div>&nbsp;</div>
                    <div>Best regards,<br />The SHEMS Team</div>
                </body>
                </html>"""
    elif type == "add appliance":
        subject = "SHEMS - Appliance Added"
        body = """
                <html>
                <body>
                    <img src="cid:logo" alt="Logo">
                    <h3>Appliance Added</h3>
                    <div>
                    <div>A new appliance has been added to your home!</div>
                    <div>Appliance Details:</div>
                    <ul>
                    <li>
                    <div>Appliance Name: <strong>{}</strong></div>
                    </li>
                    <li>
                    <div>Appliance Type: <strong>{}</strong></div>
                    </li>
                    <li>
                    <div>Home ID: <strong>{}</strong></div>
                    </li>
                    </ul>
                    </div>
                    <div>
                    <div>To view your appliance's energy usage and settings, simply log in to your SHEMS account and navigate to the "Appliance Control" section.</div>
                    <div>If you have any questions or need assistance, feel free to reply to this email or contact our support team.</div>
                    </div>
                    <div>&nbsp;</div>
                    <div>Best regards,<br />The SHEMS Team</div>
                </body>
                </html>""".format(appliance_name, appliance_type, homeid)
    elif type == "appliance delete":
        subject = "SHEMS - Appliance Deleted"
        body = """
                <html>
                <body>
                    <img src="cid:logo" alt="Logo">
                    <h3>Appliance Deleted</h3>
                    <div>
                    <div>We've removed an appliance from your home's inventory.</div>
                    <div>Appliance Details:</div>
                    <ul>
                    <li>
                    <div>Appliance Name: <strong>{}</strong></div>
                    </li>
                    <li>
                    <div>Appliance Type: <strong>{}</strong></div>
                    </li>
                    <li>
                    <div>Home ID: <strong>{}</strong></div>
                    </li>
                    </ul>
                    </div>
                    <div>
                    <div>This appliance is no longer monitored or controlled through your SHEMS account.</div>
                    <div><strong>Note:</strong> Historical energy usage data for this appliance will still be available in your SHEMS account for reference.</div>
                    </div>
                    <div>Best regards,<br />The SHEMS Team</div>
                </body>
                </html>""".format(appliance_name, appliance_type, homeid)
    elif type == "appliance condition":
        subject = "SHEMS - Appliance Condition Update: {}".format(appliance_name)
        body = """
                <html>
                <body>
                    <img src="cid:logo" alt="Logo">
                    <div>
                        This is an automated notification from your energy management system. The
                        condition of your {} has been updated due to the threshold you
                        set.
                    </div>
                    <div>
                        Previous Condition: {} <br/>
                        New Condition: {}
                    </div>
                    <div>
                        This change was triggered because the appliance's energy consumption
                        exceeded your set threshold. The SHEMS system is designed to
                        help you stay on top of your energy usage and make informed decisions.
                    </div>
                    <div>
                        Please log in to your account to view the updated appliance information.
                    </div>
                    <div>
                        Best regards, <br/>
                        SHEMS Team
                    </div>
                </body>
                </html>""".format(appliance_name, old_condition, new_condition)

    # Create a multipart message
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = from_email
    msg['To'] = to_email

    # Attach the HTML message
    html = MIMEText(body, 'html')
    msg.attach(html)

    # Attach the image
    image = MIMEImage(open(image_path, 'rb').read())
    image.add_header('Content-ID', '<logo>')
    image.add_header('Content-Disposition', 'inline')
    msg.attach(image)

    # Send the email using SMTP
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(from_email, password)
    server.sendmail(from_email, to_email, msg.as_string())
    server.quit()

def register_home(home_id, home_name, email, address="", other=""):
    """
    Registers a new home in the database.

    Args:
        home_id (int): Unique home ID
        home_name (str): Name of the home
        email (str): Email address associated with the home
        address (str, optional): Physical address of the home. Defaults to "".
        other (str, optional): Additional information about the home. Defaults to "".
    """
    # Insert new home data into the Homes table
    cursor.execute(f'''INSERT INTO Homes (HomeID, HomeName, Address, Others, email) VALUES ({home_id}, '{home_name}', '{address}', '{other}', '{email}');''')
    conn.commit() # Commit the changes to the database

# ========= Get all Home Names and IDs ==========
def check_login(home_name, home_id):
    """
    Checks if a home exists in the database.

    Args:
        home_name (str): Name of the home
        home_id (int): Unique home ID

    Returns:
        bool: True if the home exists, False otherwise
    """
    # Query the Homes table for the specified home name and ID
    cursor.execute(f'''
        SELECT * FROM Homes
        WHERE HomeID = {home_id} AND HomeName = '{home_name}';''')
    result = cursor.fetchone() # Fetch the result of the query
    return result is not None # Return True if the home exists, False otherwise

placeholder = st.empty() # Initialize a container widget to hold entire page contents

# ================= Page 1: Home Page ==================
if st.session_state.page == "home":
    placeholder.empty() # Clear the container
    with placeholder.container(): # Create a container for the home page content
        c1, c2, c3, c4 = st.columns([0.6,1,6,4], vertical_alignment="top") # Divide the page into columns for logo, title, and navigation
        with c1: # Logo column
            st.image('images/logo.png', use_column_width=True)
        with c2: # Title column
            st.subheader('SHEMS')
        with c4: # Navigation column
            cc1, cc2, cc3, cc4 = st.columns([0.5,0.5,0.5,0.5]) # Create sub-columns for navigation buttons
            with cc1:
                st.button(label="Home")
            with cc2:
                st.button(label="Features")
            with cc3:
                st.button(label="About Us")
            with cc4:
                if st.button(label="Get Started"): # Get Started button redirects to login page
                    goto_login()
            st.markdown(
                    """
                    <style>
                    button {
                        background: none!important;
                        border: none;
                        padding: 0!important;
                        color: black !important;
                        text-decoration: none;
                        cursor: pointer;
                        border: none !important;
                    }
                    button:hover {
                        text-decoration: none;
                        color: black !important;
                    }
                    button:focus {
                        outline: none !important;
                        box-shadow: none !important;
                        color: black !important;
                    }
                    </style>
                    """,
                    unsafe_allow_html=True,
            )
        # Add vertical spacing
        st.write("")
        st.write("")
        st.write("")
        # Hero section
        c1, c2 = st.columns([1.7,4], vertical_alignment="center")
        with c1: # Hero text
            st.markdown("<h1>Greener future with <span style='color: #487955'>energy storage</span> solutions</h1>", unsafe_allow_html=True)
        with c2: # Hero image
            st.image('images/home.png', use_column_width=True)
        # Add vertical spacing
        st.write("")
        st.write("")
        # Features section
        c0, c1, c2, c3, c4 = st.columns([2,3,3,3,2], vertical_alignment="center")
        with c1: # Feature 1: Energy Monitoring
            cc1, cc2 = st.columns([1.0,7.5], vertical_alignment="center")
            with cc1:
                st.image('images/energy.png', use_column_width=True)
            st.markdown("<h4 style='font-size: 18px'>Energy Monitoring</h4>", unsafe_allow_html=True)
            st.markdown("<p style='font-size: 14px'>Track and analyze your energy usage in real-time, optimizing your consumption for a sustainable future.</p>", unsafe_allow_html=True)
        with c2: # Feature 2: Automated Controls
            cc1, cc2 = st.columns([1.0,7.5], vertical_alignment="center")
            with cc1:
                st.image('images/controls.png', use_column_width=True)
            st.markdown("<h4 style='font-size: 18px'>Automated Controls</h4>", unsafe_allow_html=True)
            st.markdown("<p style='font-size: 14px'>Experience seamless automation, effortlessly regulating your appliances to optimize energy efficiency and convenience.</p>", unsafe_allow_html=True)
        with c3: # Feature 3: Detailed Reports
            cc1, cc2 = st.columns([1.0,7.5], vertical_alignment="center")
            with cc1:
                st.image('images/reports.png', use_column_width=True)
            st.markdown("<h4 style='font-size: 18px'>Detailed Reports</h4>", unsafe_allow_html=True)
            st.markdown("<p style='font-size: 14px'>Gain valuable insights with comprehensive reports, visualizing your energy usage and suggesting opportunities for improvement.</p>", unsafe_allow_html=True)
        # Add vertical spacing
        st.write("")
        st.write("")
        st.write("")
        # Footer section
        c1, c2, c3 = st.columns([4,2,4], vertical_alignment="center")
        with c2:
            st.markdown("<p style='font-size: 14px'>© 2024 SHEMS. All rights reserved.</p>", unsafe_allow_html=True)

# =========================== Page 2: Login/Register ==================================
elif st.session_state.page == "login":
    placeholder.empty() # Clear the container
    
    def check_input(input_string): # Function to check input string validity
        """
        Checks if the input string is valid.

        Args:
            input_string (str): Input string to check

        Returns:
            bool: True if the input string is not empty, has a length of 2 or less, and contains only alphanumeric characters, False otherwise
        """
        return input_string and len(input_string) <= 2 and input_string.isalnum()
    
    def check_email(email): # Function to check email validity
        """
        Checks if the email is valid.

        Args:
            email (str): Email to check

        Returns:
            str: Normalized email if valid, raises Exception otherwise
        """
        try:
            emailinfo = validate_email(email, check_deliverability=False)
            email = emailinfo.normalized
            return email
        except EmailNotValidError as e:
            raise Exception(str(e))
            
    with placeholder.container(): # Create a container for the login page content
        c1, c2, c3 = st.columns([2,6,2], vertical_alignment="top") # Divide the page into columns
        with c2: # Login and Register tabs
            t1, t2 = st.tabs(["Login","Register"])
            
            with t2: # Register tab
                st.subheader("Register a home")
                # Input fields for registration
                home_name = st.text_input("Name", placeholder="Home Name")
                email = st.text_input("Email Address", placeholder="name@email.com")
                address = st.text_input("Address", placeholder="No 123, Ozumba Mbadiwe")
                txt = st.text_area("Extra",placeholder="Something extra we don't need")
                
                # Register button
                if st.button("Register",type="primary",use_container_width=True):
                    if check_input(home_name): # Check input validity
                        st.error("Kindly check your home name and try again!", icon="❌")
                    else:
                        try:
                            email = check_email(email) # Check email validity
                            try:
                                home_id=str(random.randint(1000, 9999)) # Generate home ID and register home
                                register_home(home_id, home_name, email, address, txt) # Register home
                                
                                # Send Success mail
                                sendmail(type="signup",mail=email,homename=home_name,homeid=str(home_id))
                                st.success("{} registered successfully".format(home_name), icon="✅")
                                
                                # Redirect to dashboard
                                goto_dashboard(home_id, home_name)

                            except Exception as e:
                                st.error("An Error occured while registering", icon="❌")
                        except Exception as e:
                            st.error(e, icon="❌")
    
            with t1: # Login tab
                st.subheader("Login your home")
                # Input fields for login
                home_name = st.text_input("Name", key=2, placeholder="Home Name")
                home_id = st.text_input("Home ID",placeholder="****")
                if st.button("Login",type="primary",use_container_width=True): # Login button
                    if check_login(home_name, home_id): # Check login credentials
                        st.success("login successfull".format(home_name), icon="✅")
                        goto_dashboard(home_id, home_name) # Redirect to dashboard
                    else:
                        st.error("Wrong HomeID or HomeName", icon="❌")
                # Forgot Home ID message
                c1, c2, c3 = st.columns([2,2,2])
                with c2:
                    st.markdown("<p style='font-size: 14px'>Forgot your Home ID? Contact Support</p>", unsafe_allow_html=True)

# =========================== Page 3: Dashboard ==================================
elif st.session_state.page == "dashboard":
    placeholder.empty()
    # ========= Charts and Functions ==========
    def plot_metric(label, value, prefix="", suffix="", show_graph=False, color_graph=""):
        
        color = None
        if label == "Energy Saved" and float(value) < 0: # If Energy saved is Lower than zero
            color = "#FF0209"
        elif label == "Energy Saved" and float(value) > 0:
            color = "#078D4A"
        
        fig = go.Figure()

        fig.add_trace(
            go.Indicator(
                value=value,
                gauge={"axis": {"visible": False}},
                number={
                    "prefix": prefix,
                    "suffix": suffix,
                    "font.size": 24,
                    "font.color": color
                },
                title={
                    "text": label,
                    "font": {"size": 20},
                },
            )
        )

        if show_graph:
            fig.add_trace(
                go.Scatter(
                    y=random.sample(range(0, 101), 30),
                    hoverinfo="skip",
                    fill="tozeroy",
                    fillcolor=color_graph,
                    line={
                        "color": color_graph,
                    },
                )
            )

        fig.update_xaxes(visible=False, fixedrange=True)
        fig.update_yaxes(visible=False, fixedrange=True)
        fig.update_layout(
            # paper_bgcolor="lightgrey",
            margin=dict(t=30, b=0),
            showlegend=False,
            plot_bgcolor="white",
            height=100,
        )

        st.plotly_chart(fig, use_container_width=True)

    def plot_gauge(indicator_number, indicator_color, indicator_suffix, indicator_title, max_bound):
        fig = go.Figure(
            go.Indicator(
                value=indicator_number,
                mode="gauge+number",
                domain={"x": [0, 1], "y": [0, 1]},
                number={
                    "suffix": indicator_suffix,
                    "font.size": 22,
                },
                gauge={
                    "axis": {"range": [0, max_bound], "tickwidth": 1},
                    "bar": {"color": indicator_color},
                },
                title={
                    "text": indicator_title,
                    "font": {"size": 24},
                },
            )
        )
        fig.update_layout(
            # paper_bgcolor="lightgrey",
            height=200,
            margin=dict(l=10, r=10, t=50, b=10, pad=8),
        )
        st.plotly_chart(fig, use_container_width=True)

    def get_appliances(home_id):
        """
        Retrieves the latest energy usage data for each appliance in the specified home.

        Args:
            home_id (int): ID of the home

        Returns:
            list or None: List of dictionaries containing appliance data, or None if no appliances found
        """
        
        # Query the database to get the latest energy usage data for each appliance
        cursor.execute(f'''
            SELECT 
                A.ApplianceName, 
                A.ApplianceType,
                A.ApplianceCondition,
                EU.EnergyConsumed, 
                EU.CurrentOutput
            FROM 
                Appliances A 
            JOIN 
                EnergyUsage EU ON A.ApplianceID = EU.ApplianceID
            WHERE 
                A.HomeID = {home_id}
                AND EU.HomeID = A.HomeID
            ORDER BY 
                EU.DateTime DESC;
        ''')
        appliances = cursor.fetchall() # Fetch the query results
        
        if len(appliances) != 0: # Check if any appliances were found
            # Group the results by appliance and get the latest values
            appliance_data = {}
            for appliance in appliances:
                name, description, condition, energy_consumed, current_output = appliance

                # Create a dictionary for each appliance
                if name not in appliance_data: 
                    appliance_data[name] = {
                        'Appliance Name': name,
                        'Appliance Description': description,
                        'Appliance Condition': condition,
                        'Current Energy Consumption (kWh)': energy_consumed,
                        'Current Output (°C)': current_output
                    }
            return list(appliance_data.values()) # Return the list of appliance dictionaries
        else:
            return None # Return None if no appliances were found

    @st.experimental_dialog("Add Appliance")
    def add_appliances(home_id=0):
        """
            Dialog to add a new appliance to a home.

            Args:
                home_id (int, optional): ID of the home. Defaults to 0.
        """
        # Get unique appliances from database
        cursor.execute('''
            SELECT DISTINCT 
                ApplianceName, 
                ApplianceType,
                ApplianceID
            FROM 
                Appliances;
        ''')
        allappliances = cursor.fetchall()

        # Retrieve user email from database
        cursor.execute(f'''
            SELECT email
            FROM Homes
            WHERE HomeID={home_id};
        ''')
        email = cursor.fetchone()[0]

        # Convert the results to a list of dictionaries
        appliance_list = [
            name + ' - ' + description
            for name, description, id_ in allappliances
        ]

        # Create a dictionary to map appliance names to IDs
        appliance_ids = {appliance[0]: appliance[2] for appliance in allappliances}
        # Selectbox for appliance selection
        option = st.selectbox(
            "Add an appliance to your home",
            appliance_list,
            index=None,
            placeholder="Select an appliance",
        )
        # Input fields for start and stop values
        start_value = st.number_input("Start this appliance at (°C)", min_value=-30, max_value=30, value=15, help="This appliance will turn on automatically at this value", label_visibility="visible")
        stop_value = st.number_input("Stop this appliance at (°C)", min_value=-30, max_value=30, value=-15, help="This appliance will turn off automatically at this value", label_visibility="visible")

        if st.button("Add",type="primary",use_container_width=True): # Add appliance button
            # Get current home appliances
            home_appliances = get_appliances(st.session_state.homeid)
            all_home_appliances = []

            if home_appliances == None: # A new home
                pass
            else:
                for appliance in home_appliances:
                    all_home_appliances.append(appliance['Appliance Name'])
            # Check if appliance already exists in home
            if option.split(' - ')[0] in all_home_appliances:
                st.error('{} already added to {}'.format(option, st.session_state.home_name), icon="🚨")
            else:
                # Get the ApplianceID from the dictionary
                appliance_id = appliance_ids[option.split(' - ')[0]]
                
                # Add appliance to Appliances table
                cursor.execute(f'''
                    INSERT INTO Appliances (ApplianceID, HomeID, ApplianceName, ApplianceType, StartValue, StopValue, ApplianceCondition)
                    VALUES ({appliance_id}, {home_id}, '{option.split(' - ')[0]}', '{option.split(' - ')[1]}', {start_value}, {stop_value}, '{'True'}');
                ''')   

                # Add initial energy usage to EnergyUsage table
                now = datetime.now()
                now = now.strftime("%Y-%m-%d %H:%M:%S")
                cursor.execute(f'''
                    INSERT INTO EnergyUsage (HomeID, ApplianceID, DateTime, EnergyConsumed, EnergyProduced, CurrentOutput)
                    VALUES ({home_id}, {appliance_id}, '{now}', {0.0}, {0.0}, {0.0});
                ''')
                conn.commit() # Commit changes
                conn.close() # Close connection

                # Send success mail
                sendmail(type="add appliance", mail=email, appliance_name=option.split(' - ')[0], appliance_type=option.split(' - ')[1], homeid=home_id)
                st.success("Successfully Added {}".format(option)) # Display success message

    def update_appliance_condition(home_id, appliance_name, condition):
        """
        Updates the condition of an appliance in the Appliances table.

        Args:
            home_id (int): ID of the home
            appliance_name (str): Name of the appliance
            condition (str): New condition of the appliance
        """
        # Update the ApplianceCondition column in the Appliances table
        cursor.execute(f'''
            UPDATE Appliances
            SET ApplianceCondition = '{condition}'
            WHERE HomeID = {home_id} AND ApplianceName = '{appliance_name}';
        ''')
        conn.commit() # Commit the changes

    def get_appliance_condition(home_id, appliance_name):
        """
        Retrieves the condition of an appliance from the Appliances table.

        Args:
            home_id (int): ID of the home
            appliance_name (str): Name of the appliance

        Returns:
            str: Condition of the appliance
        """
        # Select the ApplianceCondition column from the Appliances table
        cursor.execute(f'''
            SELECT ApplianceCondition
            FROM Appliances
            WHERE HomeID = {home_id} AND ApplianceName = '{appliance_name}';
        ''')
        condition = cursor.fetchone()[0] # Fetch the result
        return condition

    def get_energy_data(home_id, filter_by):
        """
        Retrieves energy data for a home based on the specified filter.

        Args:
            home_id (int): ID of the home
            filter_by (str): Filter to apply ('today', 'this_month', 'all_time')

        Returns:
            dict: Energy data, including total energy consumed, current energy consumed, number of appliances, plotting data, and energy saved
        """
        
        # Filter by date
        if filter_by == 'today':
            start_date = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0).strftime('%Y-%m-%d %H:%M:%S')
            cursor.execute(f'''
                SELECT * FROM EnergyUsage
                WHERE HomeID = {home_id} AND DateTime >= '{start_date}';
            ''')
        elif filter_by == 'this_month':
            start_date = datetime.today().replace(day=1, hour=0, minute=0, second=0, microsecond=0).strftime('%Y-%m-%d %H:%M:%S')
            cursor.execute(f'''
                SELECT * FROM EnergyUsage
                WHERE HomeID = {home_id} AND DateTime >= '{start_date}';
            ''')
        elif filter_by == 'all_time':
            cursor.execute(f'''
                SELECT * FROM EnergyUsage
                WHERE HomeID = {home_id};
            ''')
        energy_data = cursor.fetchall()

        total_energy_consumed = sum(row[4] for row in energy_data) # Calculate total energy consumed

        # Get the number of appliances for the home
        cursor.execute(f'''
            SELECT COUNT(*) 
            FROM Appliances 
            WHERE HomeID = {home_id};
        ''')
        num_appliances = cursor.fetchone()[0]

        # Get the sum of EnergyConsumed for the last hour
        cursor.execute(f'''
            SELECT SUM(EnergyConsumed) 
            FROM (
                SELECT EnergyConsumed 
                FROM EnergyUsage 
                WHERE HomeID = {home_id} 
                ORDER BY DateTime DESC 
                LIMIT {num_appliances}
            ) AS LastHourEnergy;
        ''')
        current_energy_consumed = cursor.fetchone()[0] if cursor.fetchone() else 0
        # Count unique appliances
        num_appliances = len(set(row[2] for row in energy_data))

        # Create dataframe for plotting
        df = pd.DataFrame(energy_data, columns=['EnergyUsageID', 'HomeID', 'ApplianceID', 'DateTime', 'EnergyConsumed', 'EnergyProduced', 'CurrentOutput'])
        df['DateTime'] = pd.to_datetime(df['DateTime'])
        
        # Map ApplianceID to Appliance names
        appliance_map = {1: 'Hisense Deep Freezer', 2: 'Scanfrost Refrigerator', 3: 'LG Air Conditioner'}
        df['Appliance'] = df['ApplianceID'].map(appliance_map)

        # Rename column
        df.rename(columns={'EnergyConsumed': 'Energy (kWh)'}, inplace=True)

        # Filter data for plotting
        if filter_by == 'today':
            df['Hour'] = df['DateTime'].dt.hour
            df_plot = df[['Hour', 'Energy (kWh)', 'Appliance']]
            x_axis = 'Hour'
        elif filter_by in ['this_month', 'all_time']:
            df['Day'] = df['DateTime'].dt.day
            df_plot = df[['Day', 'Energy (kWh)', 'Appliance']]
            x_axis = 'Day'

        # Calculate Energy Saved
        appliance_energy_consumption = {
            'Scanfrost Refrigerator': 0.04,
            'Hisense Deep Freezer': 0.8,
            'LG Air Conditioner': 0.001
        }

        # Calculate total energy consumption based on appliance usage
        total_energy_consumption_from_appliances = sum(
            appliance_energy_consumption[list(appliance_energy_consumption.keys())[row[2] - 1]] * 1  # assuming 1 hour interval
            for row in energy_data
        )

        # Calculate energy saved
        energy_saved = total_energy_consumption_from_appliances - total_energy_consumed

        # Calculate energy saved percentage
        energy_saved_percentage = (energy_saved / total_energy_consumption_from_appliances) * 100 if total_energy_consumption_from_appliances != 0 else 0

        return {
            'total_energy_consumed': round(float(total_energy_consumed), 1),
            'current_energy_consumed': round(float(current_energy_consumed), 4),
            'num_appliances': int(num_appliances),
            'df_plot': df_plot,
            'x_axis': x_axis,
            'energy_saved': round(float(energy_saved_percentage), 1)
        }

    def show_dashboard(data): 
        """
        Displays the dashboard with key statistics and appliance consumption chart.

        Args:
            data (dict): Dictionary containing dashboard data
        """
         # Key Statistics Section
        st.markdown("<h3 style='font-size: 20px'>{}</h3>".format("Key Statistics"), unsafe_allow_html=True)
        # Create two columns for key statistics
        cc1, cc2 = st.columns([5,5])
        with cc1: # Left column
            # Number of Appliances metric
            plot_metric(
                "Number of Appliances",
                data['num_appliances'],
                prefix="",
                suffix="",
                show_graph=False,
                color_graph="rgba(255, 242, 175, 20)",
            )
            # Energy Saved metric
            plot_metric(
                "Energy Saved",
                data['energy_saved'],
                prefix="",
                suffix="%",
                show_graph=False,
                color_graph="rgba(18, 169, 94, 100)",
            )

        with cc2: # Right column
            # Total Energy Consumed metric
            plot_metric(
                "Total Energy Consumed",
                data['total_energy_consumed'],
                prefix="",
                suffix=" kWh",
                show_graph=True,
                color_graph="rgba(255, 242, 175, 20)",
            )
            # Current Energy Consumption gauge
            plot_gauge(data['current_energy_consumed'], "#C7B452", " kWh", "Current Rate", 2)
        
        # Add whitespace
        st.write("")
        st.write("")
        
        # Appliance Consumption Line Chart Section
        st.markdown("<h3 style='font-size: 20px'>{}</h3>".format("Appliance Consumption"), unsafe_allow_html=True)

        # Plot line chart using Plotly Express
        fig = px.line(data['df_plot'], x=data['x_axis'], y='Energy (kWh)', color='Appliance')
        # Display chart
        st.plotly_chart(fig, use_container_width=True)
        # Add whitespace
        st.write("")
        st.write("")

    def show_appliances():
        """
        Displays the appliance control interface.

        Allows users to add, toggle, and delete appliances.
        """

        # Get user email from database
        cursor.execute(f'''
            SELECT email FROM Homes
            WHERE HomeID = {st.session_state.homeid};
        ''')
        email = cursor.fetchone()[0]

        # Appliance Control Section
        c1, c2 = st.columns([8,1.2])
        with c1:
            st.markdown("<h3 style='font-size: 20px'>{}</h3>".format("Appliance Control"), unsafe_allow_html=True)
        with c2:
            if st.button(":heavy_plus_sign: Add Appliance",key='a'): # Add Appliance button
                add_appliances(home_id=st.session_state.homeid)

        home_appliances = get_appliances(st.session_state.homeid) # Retrieve home appliances from database
        if home_appliances == None: # Check if home appliances exist
            pass
        else:
            N_cards_per_row = 3 # Number of appliances per row

            for n_row, appliance in enumerate(home_appliances): # Iterate over appliances
                i = n_row % N_cards_per_row
                if i == 0:
                    st.write("---") # Horizontal line separator
                    cols = st.columns(N_cards_per_row, gap="large") # Create columns for appliance cards
                
                with cols[n_row % N_cards_per_row]:
                    # Appliance Card
                    st.markdown(f"**{appliance['Appliance Name']}: {appliance['Appliance Description']}**", unsafe_allow_html=True)
                    st.write(f"**Current Energy Consumption:** {str(round(appliance['Current Energy Consumption (kWh)'], 4))} kWh")
                    st.write(f"**Current Output:** {str(math.floor(appliance['Current Output (°C)']))} °C")
                    
                    # Toggle and delete buttons
                    c1, c2 = st.columns([6,4])
                    with c1:
                        # Get current appliance condition
                        current_condition = get_appliance_condition(st.session_state.homeid, appliance['Appliance Name'])
                        if current_condition == 'True':
                            value = True
                        else:
                            value = False
                        # Toggle button
                        on = st.toggle("Off/On", value=value, key=n_row)
                        if on: # Update appliance condition to 'True'
                            update_appliance_condition(st.session_state.homeid, appliance['Appliance Name'], 'True')
                        else:# Update appliance condition to 'False'
                            update_appliance_condition(st.session_state.homeid, appliance['Appliance Name'], 'False')
                    with c2:
                        # Delete button
                        if st.button("🗑️Delete",key=n_row+3):
                            # Delete the appliance from the Appliances table
                            try:
                                cursor.execute(f'''
                                    DELETE FROM Appliances
                                    WHERE HomeID = {st.session_state.homeid} AND ApplianceName = '{appliance['Appliance Name']}';
                                ''')
                                conn.commit()
                                st.toast(appliance['Appliance Name']+ ' Deleted!', icon="✅") # Display success toast
                                # Refresh page
                                st.session_state.refresh_trigger = True                               
                                # Send success mail
                                sendmail(type="appliance delete", mail=email, appliance_name=appliance['Appliance Name'], appliance_type=appliance['Appliance Description'], homeid=st.session_state.homeid)
                            except:
                                st.toast('An Error occured: Appliance not found!', icon="❌") # Display error toast
                            
    # =========== Header ==============
    # Create two columns for the header  
    c1, c2 = st.columns([4,7], vertical_alignment="center")
    
    with c1: # Left column: Display home name and ID
        st.markdown("<div><h1 style='font-size: 24px'>{} |</h1><p style='font-size: 13px'>{}</p></div>".format(st.session_state.home_name, st.session_state.homeid), unsafe_allow_html=True)
    with c2: # Right column: Refresh and logout buttons
        c1, c2, c3 = st.columns([6,2,2], vertical_alignment="center") # Create three columns for buttons
        with c2: # Refresh button
            if st.button("🔄 Refresh"):
                st.session_state.refresh_trigger = True # Trigger refresh
        with c3: # Logout button
            if st.button(":leftwards_arrow_with_hook: Logout"):
                goto_login() # Go to login page

    # ========== Dashboard Data ==========
    # Check if data needs to be refreshed or if it's the first load
    if st.session_state.refresh_trigger or "dashboard_data_today" not in st.session_state:
        # Retrieve energy data for different time periods
        st.session_state.dashboard_data_today = get_energy_data(home_id=st.session_state.homeid, filter_by='today')
        st.session_state.dashboard_data_this_month = get_energy_data(home_id=st.session_state.homeid, filter_by='this_month')
        st.session_state.dashboard_data_all_time = get_energy_data(home_id=st.session_state.homeid, filter_by='all_time')
        
        # Reset refresh trigger
        st.session_state.refresh_trigger = False
    
    # =========== Filter Row ==============   
    # Create tabs for different time periods 
    t1, t2, t3 = st.tabs(["Today", "This Month", "All Time"])
    
    # Today tab
    with t1:
        # Display dashboard for today's data
        show_dashboard(data=st.session_state.dashboard_data_today)
    
    # This Month tab
    with t2:
        # Display dashboard for this month's data
        show_dashboard(data=st.session_state.dashboard_data_this_month)
    
    # All Time tab
    with t3:
        # Display dashboard for all-time data
        show_dashboard(data=st.session_state.dashboard_data_all_time)
    
    # Display appliance control interface
    show_appliances()