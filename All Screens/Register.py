import streamlit as st

def login_page(placeholder):
    # ================= Page 2: Register ==================
    if st.session_state.page == 0:
        placeholder.empty()
        with placeholder.container():
            c1, c2, c3 = st.columns([2,6,2], vertical_alignment="top")
            with c2:
                t1, t2 = st.tabs(["Register","Login"])
                with t1:
                    st.subheader("Register a home")
                    name = st.text_input("Name", placeholder="Home Name")
                    address = st.text_input("Address", placeholder="No 123, Ozumba Mbadiwe")
                    txt = st.text_area("Extra",placeholder="Something extra we don't need")
                    st.button("Register",type="primary",use_container_width=True)
                with t2:
                    st.subheader("Login into your home")
                    name = st.text_input("Name", key=2, placeholder="Home Name")
                    unique = st.text_input("Unique ID",placeholder="****")
                    st.button("Login",type="primary",use_container_width=True)
                    c1, c2, c3 = st.columns([2,2,2])
                    with c2:
                        st.markdown("<p style='font-size: 14px'>Forgot your unique ID? Contact Support</p>", unsafe_allow_html=True)