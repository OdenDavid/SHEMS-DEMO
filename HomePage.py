"""
In an environment with streamlit installed,
Run with `streamlit run HomePage.py`
"""

import streamlit as st

# ============= PAGE SETUP ============
st.set_page_config(page_title="SHEMS", page_icon="♻️", layout="wide")

#image = Image.open('images/logo.png')
#st.image(image)

# ============== Session States/Pages ==================
if "page" not in st.session_state:
    st.session_state.page = 0
if "userid" not in st.session_state:
    st.session_state.userid = ""

def nextpage(userid):
    st.session_state.page += 1 # Go to next page
    st.session_state.userid = userid
    st.rerun()

def restart():
    st.session_state.page = 0 # Go back to beginning
    st.rerun()

placeholder = st.empty() # Initialize a container widget to hold entire page contents

# ===== Open new window ========
def open_page():
    pass
    #webbrowser.o(where)

# ================= Page 1: Home Page ==================
if st.session_state.page == 0:
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
                st.button(label="Home",on_click=open_page())
            with cc2:
                st.button(label="Features",on_click=open_page())
            with cc3:
                st.button(label="About Us",on_click=open_page())
            with cc4:
                st.button(label="Get Started",on_click=open_page())
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