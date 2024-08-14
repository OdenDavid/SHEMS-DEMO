"""
In an environment with streamlit installed,
Run with `streamlit run App.py`
"""

import streamlit as st
import random
from datetime import datetime
import math

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

import sqlite3

# =========== Initialize SQL ==========
conn = sqlite3.connect("Data.db") # db - database
cursor = conn.cursor() # Cursor object

# ============= PAGE SETUP ============
st.set_page_config(page_title="SHEMS", page_icon="♻️", layout="wide")

# ============== Session States/Pages ==================
if "page" not in st.session_state:
    st.session_state.page = "home"
if "homeid" not in st.session_state:
    st.session_state.homeid = 0000
if "home_name" not in st.session_state:
    st.session_state.home_name = "Default"
if "data_to_show" in st.session_state:
    st.session_state.data_to_show = {}

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

def register_home(home_id, home_name, address, other):
    """Register a new home:
        Collect Home name, address, homeid. Insert Into Database."""
    
    cursor.execute('''INSERT INTO Homes (HomeID, HomeName, Address, Others) VALUES (?, ?, ?, ?)''', (home_id, home_name, address, other))
    conn.commit()

# ========= Get all Home Names and IDs ==========
def check_login(home_name, home_id):
    """Login an existing home:
        Collect Home name, homeid. Check if both are in database"""
    
    cursor.execute('''
        SELECT * FROM Homes
        WHERE HomeID = ? AND HomeName = ?
    ''', (home_id, home_name))
    result = cursor.fetchone()
    if result:
        return True
    else:
        return False


placeholder = st.empty() # Initialize a container widget to hold entire page contents

# ===== Open new window ========
def open_page():
    pass
    #webbrowser.open(where)

# ================= Page 1: Home Page ==================
if st.session_state.page == "home":
    placeholder.empty()
    with placeholder.container():
        c1, c2, c3, c4 = st.columns([0.6,1,6,4], vertical_alignment="top")
        with c1:
            st.image('images/logo.png', use_column_width=True)
        with c2:    
            st.subheader('SHEMS')
        with c4:
            cc1, cc2, cc3, cc4 = st.columns([0.5,0.5,0.5,0.5])
            with cc1:
                st.button(label="Home")
            with cc2:
                st.button(label="Features")
            with cc3:
                st.button(label="About Us")
            with cc4:
                if st.button(label="Get Started"):
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
        
        st.write("")
        st.write("")
        st.write("")

        c1, c2 = st.columns([1.7,4], vertical_alignment="center")
        with c1:
            st.markdown("<h1>Greener future with <span style='color: #487955'>energy storage</span> solutions</h1>", unsafe_allow_html=True)
        with c2:
            st.image('images/home.png', use_column_width=True)

        st.write("")
        st.write("")
        #======= FEATURES ========
        c0, c1, c2, c3, c4 = st.columns([2,3,3,3,2], vertical_alignment="center")
        with c1:
            cc1, cc2 = st.columns([1.0,7.5], vertical_alignment="center")
            with cc1:
                st.image('images/energy.png', use_column_width=True)
            st.markdown("<h4 style='font-size: 18px'>Energy Monitoring</h4>", unsafe_allow_html=True)
            st.markdown("<p style='font-size: 14px'>Track and analyze your energy usage in real-time, optimizing your consumption for a sustainable future.</p>", unsafe_allow_html=True)
        with c2:
            cc1, cc2 = st.columns([1.0,7.5], vertical_alignment="center")
            with cc1:
                st.image('images/controls.png', use_column_width=True)
            st.markdown("<h4 style='font-size: 18px'>Automated Controls</h4>", unsafe_allow_html=True)
            st.markdown("<p style='font-size: 14px'>Experience seamless automation, effortlessly regulating your appliances to optimize energy efficiency and convenience.</p>", unsafe_allow_html=True)
        with c3:
            cc1, cc2 = st.columns([1.0,7.5], vertical_alignment="center")
            with cc1:
                st.image('images/reports.png', use_column_width=True)
            st.markdown("<h4 style='font-size: 18px'>Detailed Reports</h4>", unsafe_allow_html=True)
            st.markdown("<p style='font-size: 14px'>Gain valuable insights with comprehensive reports, visualizing your energy usage and suggesting opportunities for improvement.</p>", unsafe_allow_html=True)
        
        st.write("")
        st.write("")
        st.write("")
        #======== Footer ========
        c1, c2, c3 = st.columns([4,2,4], vertical_alignment="center")
        with c2:
            st.markdown("<p style='font-size: 14px'>© 2024 SHEMS. All rights reserved.</p>", unsafe_allow_html=True)

# =========================== Page 2: Login/Register ==================================
elif st.session_state.page == "login":
    placeholder.empty()
    with placeholder.container():
        c1, c2, c3 = st.columns([2,6,2], vertical_alignment="top")
        with c2:
            t1, t2 = st.tabs(["Login","Register"])
            with t2:
                st.subheader("Register a home")
                home_name = st.text_input("Name", placeholder="Home Name")
                address = st.text_input("Address", placeholder="No 123, Ozumba Mbadiwe")
                txt = st.text_area("Extra",placeholder="Something extra we don't need")
                if st.button("Register",type="primary",use_container_width=True):
                    home_id=str(random.randint(1000, 9999)) # Generate home ID
                    try:
                        register_home(home_id, home_name, address, txt)
                        conn.close()
                        st.success("{} registered successfully".format(home_name), icon="✅")
                        goto_dashboard(home_id, home_name)
                    except Exception as e:
                        st.error("An Error occured while registering", icon="❌")
    
            with t1:
                st.subheader("Login your home")
                home_name = st.text_input("Name", key=2, placeholder="Home Name")
                home_id = st.text_input("Home ID",placeholder="****")
                if st.button("Login",type="primary",use_container_width=True):
                    if check_login(home_name, home_id):
                        st.success("login successfull".format(home_name), icon="✅")
                        goto_dashboard(home_id, home_name)
                    else:
                        st.error("Wrong HomeID or HomeName", icon="❌")

                c1, c2, c3 = st.columns([2,2,2])
                with c2:
                    st.markdown("<p style='font-size: 14px'>Forgot your Home ID? Contact Support</p>", unsafe_allow_html=True)

# =========================== Page 3: Dashboard ==================================
elif st.session_state.page == "dashboard":
    placeholder.empty()
    # ========= Charts and Functions ==========
    def plot_metric(label, value, prefix="", suffix="", show_graph=False, color_graph=""):
        fig = go.Figure()

        fig.add_trace(
            go.Indicator(
                value=value,
                gauge={"axis": {"visible": False}},
                number={
                    "prefix": prefix,
                    "suffix": suffix,
                    "font.size": 24,
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
        """"""
        # Get the latest energy usage data for each appliance
        cursor.execute('''
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
                EU.HomeID = ? 
            ORDER BY 
                EU.DateTime DESC
        ''', (home_id,))

        appliances = cursor.fetchall()
        if len(appliances) != 0:
            # Group the results by appliance and get the latest values
            appliance_data = {}
            for appliance in appliances:
                name, description, condition, energy_consumed, current_output = appliance
                if name not in appliance_data:
                    appliance_data[name] = {
                        'Appliance Name': name,
                        'Appliance Description': description,
                        'Appliance Condition': condition,
                        'Current Energy Consumption (kWh)': energy_consumed,
                        'Current Output (°C)': current_output
                    }
            return list(appliance_data.values())
        else:
            return None

    @st.experimental_dialog("Add Appliance")
    def add_appliances(home_id=0):

        # Get all unique appliances
        cursor.execute('''
            SELECT DISTINCT
                ApplianceID, 
                ApplianceName, 
                ApplianceType
            FROM 
                Appliances
        ''')

        allappliances = cursor.fetchall()

        # Convert the results to a list of dictionaries
        appliance_list = [
            name + ' - ' + description
            for name, description in allappliances
        ]

        # Create a dictionary to map appliance names to IDs
        appliance_ids = {appliance[1]: appliance[0] for appliance in allappliances}

        option = st.selectbox(
            "Add an appliance to your home",
            appliance_list,
            index=None,
            placeholder="Select an appliance",
        )
        start_value = st.number_input("Start this appliance at (°C)", min_value=-30, max_value=30, value=15, help="This appliance will turn on automatically at this value", label_visibility="visible")
        stop_value = st.number_input("Stop this appliance at (°C)", min_value=-30, max_value=30, value=-15, help="This appliance will turn off automatically at this value", label_visibility="visible")

        if st.button("Add",type="primary",use_container_width=True):
            allhomeappliances = []
            for appliance in home_appliances:
                allhomeappliances.append(appliance['Appliance Name'])

            if option.split(' - ')[0] in allhomeappliances:
                st.error('{} already added to {}'.format(option, st.session_state.home_name), icon="🚨")
            else:
                # Get the ApplianceID from the dictionary
                appliance_id = appliance_ids[option.split(' - ')[0]]
                
                # Add appliance to table
                cursor.execute('''
                    INSERT INTO Appliances (ApplianceID, HomeID, ApplianceName, ApplianceType, StartValue, StopValue, ApplianceCondition)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (appliance_id, home_id, option.split(' - ')[0], option.split(' - ')[1], start_value, stop_value, 'True'))
                conn.commit()
                conn.close()

                st.success("Successfully Added {}".format(option))

    def update_appliance_condition(home_id, appliance_name, condition):
        cursor.execute('''
            UPDATE Appliances
            SET ApplianceCondition = ?
            WHERE HomeID = ? AND ApplianceName = ?
        ''', (condition, home_id, appliance_name))
        conn.commit()

    def get_appliance_condition(home_id, appliance_name):
        cursor.execute('''
            SELECT ApplianceCondition
            FROM Appliances
            WHERE HomeID = ? AND ApplianceName = ?
        ''', (home_id, appliance_name))
        condition = cursor.fetchone()[0]
        return condition

    def get_energy_data(home_id, filter_by):
        """
            This function takes three arguments:
                home_id: the ID of the home to retrieve data for
                filter_by: the filter to apply to the data (today, this month, or all time)
            
            The function returns a dictionary containing the following data:
                total_energy_produced: the total energy produced for the selected filter
                current_energy_produced: the current energy produced (last recorded observation)
                total_energy_consumed: the total energy consumed for the selected filter
                current_energy_consumed: the current energy consumed (last recorded observation)
                num_appliances: the number of appliances for the selected filter
                df_plot: a pandas DataFrame for plotting appliance consumption
        """
        
        # Filter by date
        if filter_by == 'today':
            start_date = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)
            cursor.execute('''
                SELECT * FROM EnergyUsage
                WHERE HomeID = ? AND DateTime >= ?
            ''', (home_id, start_date))
        elif filter_by == 'this_month':
            start_date = datetime.today().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            cursor.execute('''
                SELECT * FROM EnergyUsage
                WHERE HomeID = ? AND DateTime >= ?
            ''', (home_id, start_date))
        elif filter_by == 'all_time':
            cursor.execute('''
                SELECT * FROM EnergyUsage
                WHERE HomeID = ?
            ''', (home_id,))

        energy_data = cursor.fetchall()

        # Calculate totals and currents
        total_energy_produced = sum(row[4] for row in energy_data)
        current_energy_produced = energy_data[-1][4] if energy_data else 0
        total_energy_consumed = sum(row[5] for row in energy_data)
        current_energy_consumed = energy_data[-1][5] if energy_data else 0
        num_appliances = len(set(row[2] for row in energy_data))

        # Create dataframe for plotting
        df = pd.DataFrame(energy_data, columns=['EnergyUsageID', 'HomeID', 'ApplianceID', 'DateTime', 'EnergyConsumed', 'EnergyProduced', 'CurrentOutput'])
        df['DateTime'] = pd.to_datetime(df['DateTime'])
        
        # Map ApplianceID to Appliance names
        appliance_map = {1: 'Hisense Deep Freezer', 2: 'Scanfrost Refrigerator', 3: 'LG Air Conditioner'}
        df['Appliance'] = df['ApplianceID'].map(appliance_map)

        # Rename columns for consistency
        df.rename(columns={'EnergyConsumed': 'Energy (kWh)'}, inplace=True)

        if filter_by == 'today':
            df['Hour'] = df['DateTime'].dt.hour
            df_plot = df[['Hour', 'Energy (kWh)', 'Appliance']]
            x_axis = 'Hour'
        elif filter_by in ['this_month', 'all_time']:
            df['Day'] = df['DateTime'].dt.day
            df_plot = df[['Day', 'Energy (kWh)', 'Appliance']]
            x_axis = 'Day'

        return {
            'total_energy_produced': float(total_energy_produced),
            'current_energy_produced': float(current_energy_produced),
            'total_energy_consumed': float(total_energy_consumed),
            'current_energy_consumed': float(current_energy_consumed),
            'num_appliances': int(num_appliances),
            'df_plot': df_plot,
            'x_axis': x_axis
        }

    def show_dashboard(data): 
        # =============== Key Statistics =================
        st.markdown("<h3 style='font-size: 20px'>{}</h3>".format("Key Statistics"), unsafe_allow_html=True)
        c1, c2, c3 = st.columns([3.3,3.3,3.3])
        with c1:
            plot_metric(
                "Total Energy Produced",
                data['total_energy_produced'],
                prefix="",
                suffix=" kWh",
                show_graph=True,
                color_graph="rgba(0, 104, 201, 0.2)",
            )
            plot_gauge(data['current_energy_produced'], "#0068C9", " kWh", "Current Rate", 8)
        with c2:
            plot_metric(
                "Number of Appliances",
                data['num_appliances'],
                prefix="",
                suffix="",
                show_graph=False,
                color_graph="rgba(255, 242, 175, 20)",
            )
        with c3:
            plot_metric(
                "Total Energy Consumed",
                data['total_energy_consumed'],
                prefix="",
                suffix=" kWh",
                show_graph=True,
                color_graph="rgba(255, 242, 175, 20)",
            )
            plot_gauge(data['current_energy_consumed'], "#C7B452", " kWh", "Current Rate", 8)

        st.write("")
        st.write("")
        # =========== Line Chart ==================
        st.markdown("<h3 style='font-size: 20px'>{}</h3>".format("Appliance Consumption"), unsafe_allow_html=True)

        # Plot the line chart
        fig = px.line(data['df_plot'], x=data['x_axis'], y='Energy (kWh)', color='Appliance')

        st.plotly_chart(fig, use_container_width=True)

        st.write("")
        st.write("")
    
    # =========== Header ==============    
    c1, c2 = st.columns([4,7], vertical_alignment="center")
    with c1:
        st.markdown("<div><h1 style='font-size: 24px'>{} |</h1><p style='font-size: 13px'>{}</p></div>".format(st.session_state.home_name, st.session_state.homeid), unsafe_allow_html=True)
    with c2:
        c1, c2 = st.columns([7,1.5], vertical_alignment="center")
        with c2:
            if st.button(":leftwards_arrow_with_hook: Refresh"):
                pass
    # ========== Dashboard Data ==========
    dashboard_data_today = get_energy_data(home_id=st.session_state.homeid,filter_by='today')
    dashboard_data_this_month = get_energy_data(home_id=st.session_state.homeid,filter_by='this_month')
    dashboard_data_all_time = get_energy_data(home_id=st.session_state.homeid,filter_by='all_time')
    # =========== Filter Row ==============   
    t1, t2, t3 = st.tabs(["Today", "This Month", "All Time"])
    with t1:
        show_dashboard(data=dashboard_data_today)
    with t2:
        show_dashboard(data=dashboard_data_this_month)
    with t3:
        show_dashboard(data=dashboard_data_all_time)
    
    # =========== Appliance Control ==================
    c1, c2 = st.columns([8,1.2])
    with c1:
        st.markdown("<h3 style='font-size: 20px'>{}</h3>".format("Appliance Control"), unsafe_allow_html=True)
    with c2:
        if st.button(":heavy_plus_sign: Add Appliance",key='a'):
            add_appliances()

    home_appliances = get_appliances(st.session_state.homeid)
    if home_appliances == None:
        pass
    else:
        N_cards_per_row = 3

        for n_row, appliance in enumerate(home_appliances):
            i = n_row % N_cards_per_row
            if i == 0:
                st.write("---")
                cols = st.columns(N_cards_per_row, gap="large")
            
            with cols[n_row % N_cards_per_row]:
                # ==== Card ======
                st.markdown(f"**{appliance['Appliance Name']}: {appliance['Appliance Description']}**", unsafe_allow_html=True)
                st.write(f"**Current Energy Consumption:** {str(round(appliance['Current Energy Consumption (kWh)'], 1))} kWh")
                st.write(f"**Current Output:** {str(math.floor(appliance['Current Output (°C)']))} °C")
                
                initial_condition = get_appliance_condition(st.session_state.homeid, appliance['Appliance Name'])
                print(initial_condition, appliance['Appliance Name'], st.session_state.homeid)
                if st.toggle("Off/On", value=bool(), key=n_row):
                    update_appliance_condition(st.session_state.homeid, appliance['Appliance Name'], 'True')
                else:
                    update_appliance_condition(st.session_state.homeid, appliance['Appliance Name'], 'False')

