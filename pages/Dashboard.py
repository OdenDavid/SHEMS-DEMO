import streamlit as st
import pandas as pd
import random
import plotly.express as px
import plotly.graph_objects as go

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
    appliance_usage_df = pd.read_csv("data/usage.csv")
    appliance_df = pd.read_csv("data/appliances.csv")
    
    home_appliances = appliance_usage_df[appliance_usage_df['Home ID'] == home_id]
    appliances_info = []
    
    for index, row in home_appliances.iterrows():
        appliance_id = row['Appliance ID']
        appliance_info = appliance_df[appliance_df['Appliance ID'] == appliance_id].iloc[0]
        appliance_dict = {
            'Appliance Name': appliance_info['Appliance Name'],
            'Appliance Description': appliance_info['Description'],
            'Current Energy Consumption (kWh)': row['Current Energy Consumption (kWh)'],
            'Current Output (°C)': row['Current Output (°C)']
        }
        appliances_info.append(appliance_dict)
    
    return appliances_info

@st.experimental_dialog("Add Appliance")
def add_appliances():
    appliance_df = pd.read_csv("data/appliances.csv")
    appliance_list = (appliance_df['Appliance Name'] + ' - ' + appliance_df['Description']).to_list()
    option = st.selectbox(
        "Add an appliance to your home",
        appliance_list,
        index=None,
        placeholder="Select an appliance",
    )
    stop_appliance, start_appliance = st.select_slider(
    "Select a range of automatic start and stop indicators for this appliance",
    options=[x for x in range(-30, 31)],
    value=(-15, 15))

    if st.button("Add",type="primary",use_container_width=True):
        st.success("Successfully Added {}".format(option))

# =========== Header ==============    
c1, c2, c3 = st.columns([1,0.4,8], vertical_alignment="center")
with c1:
    st.markdown("<h1 style='font-size: 24px'>{}</h1>".format("MyHome1  |"), unsafe_allow_html=True)
with c2:
    st.markdown("<p style='font-size: 13px'>{}</>".format("ID234"), unsafe_allow_html=True)
with c3:
    c1, c2 = st.columns([8,0.9], vertical_alignment="center")
    with c2:
        if st.button(":leftwards_arrow_with_hook: Refresh"):
            pass
# =========== Filter Row ==============   
c1, c2, c3 = st.columns([6,2.15,6], vertical_alignment="center")
with c2:
    t1, t2, t3 = st.tabs(["Today", "This Month", "All Time"])
# =============== Key Statistics =================
st.markdown("<h3 style='font-size: 20px'>{}</h3>".format("Key Statistics"), unsafe_allow_html=True)
c1, c2, c3 = st.columns([3.3,3.3,3.3])
with c1:
    plot_metric(
        "Total Energy Produced",
        1.4,
        prefix="",
        suffix=" kWh",
        show_graph=True,
        color_graph="rgba(0, 104, 201, 0.2)",
    )
    plot_gauge(0.7, "#0068C9", " kWh", "Current Rate", 2)
with c2:
    plot_metric(
        "Number of Appliances",
        2,
        prefix="",
        suffix="",
        show_graph=False,
        color_graph="rgba(255, 242, 175, 20)",
    )
with c3:
    plot_metric(
        "Total Energy Consumed",
        0.8,
        prefix="",
        suffix=" kWh",
        show_graph=True,
        color_graph="rgba(255, 242, 175, 20)",
    )
    plot_gauge(0.34, "#C7B452", " kWh", "Current Rate", 2)

st.write("")
st.write("")
# =========== Line Chart ==================
st.markdown("<h3 style='font-size: 20px'>{}</h3>".format("Appliance Consumption"), unsafe_allow_html=True)

df = pd.read_csv("data/dummy.csv")
df['Date'] = pd.to_datetime(df.Date, format='%Y-%m-%d %H:%M:%S')

# Melt the DataFrame to pivot the consumption data
df_melt = pd.melt(df.reset_index(), id_vars='Date', value_vars=['Air-Conditioner (kWh)', 'Fridge (kWh)'])

# Extract the hour from the Date column
df_melt['Hour'] = df_melt['Date'].dt.hour

# Rename column
df_melt.rename(columns={'value': 'Energy (kWh)', 'variable': 'Appliance'}, inplace=True)

# Plot the line chart
fig = px.line(df_melt, x='Hour', y='Energy (kWh)', color='Appliance')

st.plotly_chart(fig,use_container_width=True)

st.write("")
st.write("")
# =========== Appliance Control ==================
c1, c2 = st.columns([8,1.2])
with c1:
    st.markdown("<h3 style='font-size: 20px'>{}</h3>".format("Appliance Control"), unsafe_allow_html=True)
with c2:
    if st.button(":heavy_plus_sign: Add Appliance"):
        add_appliances()

home_id = 1
appliances = get_appliances(home_id)
N_cards_per_row = 3

for n_row, appliance in enumerate(appliances):
    i = n_row % N_cards_per_row
    if i == 0:
        st.write("---")
        cols = st.columns(N_cards_per_row, gap="large")
    
    with cols[n_row % N_cards_per_row]:
        # ==== Card ======
        st.markdown(f"**{appliance['Appliance Name']}: {appliance['Appliance Description']}**", unsafe_allow_html=True)
        st.write(f"**Current Energy Consumption:** {appliance['Current Energy Consumption (kWh)']} kWh")
        st.write(f"**Current Output:** {appliance['Current Output (°C)']} °C")
        on = st.toggle("Off/On",value=True,key=n_row)