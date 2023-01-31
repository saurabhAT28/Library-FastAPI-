import requests
import streamlit as st
from streamlit_lottie import st_lottie
from streamlit_option_menu import option_menu
# import streamlit_authenticator as stauth
import yaml
from yaml import SafeLoader
# from config import config
# from PIL import Image
st.set_page_config(layout="wide")


def app():
    def load_lottieurl(url):
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()

    # lottie_anim1 = load_lottieurl("https://assets6.lottiefiles.com/packages/lf20_qq7lkxtl.json")
    # lottie_anim1 = load_lottieurl("https://assets6.lottiefiles.com/private_files/lf30_ipvphpwo.json")
    lottie_anim1 = load_lottieurl("https://assets6.lottiefiles.com/packages/lf20_1a8dx7zj.json")

    st.markdown("<h1 style='text-align: center; color: red; margin-top: none;'>City Library</h1>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)

    with c1:
        st.header("Library Management")
        st.write('''
                Founded in 2023
                Managed by City Council
            ''')
    
    with c2:
        st_lottie(lottie_anim1, height=200, key="books1 anim")
    

def user():
    # placeholder = st.empty()

    # actual_email = "email"
    # actual_password = "password"

    # # Insert a form in the container
    # with placeholder.form("login"):
    #     st.markdown("#### Enter your credentials")
    #     email = st.text_input("Email")
    #     password = st.text_input("Password", type="password")
    #     submit = st.form_submit_button("Login")

    # if submit and email == actual_email and password == actual_password:
    #     # If the form is submitted and the email and password are correct,
    #     # clear the form/container and display a success message
    #     placeholder.empty()
    #     st.success("Login successful")
    # elif submit and email != actual_email and password != actual_password:
    #     st.error("Login failed")
    # else:
    #     pass

    option = st.selectbox('Select option', ('Display all users', 'Display user by id', 'Display all books'))

    if option=='Display all users':
        # res = requests.get(url="http://127.0.0.1:8000/users/users/")
        res = requests.get(url="http://127.0.0.1:8000/user/")
        # http://localhost:8000/user
        st.dataframe(res.json())

    # if option=='Display user by id':
    #     id = st.number_input('ID', 1)
    #     res = requests.get(url="http://127.0.0.1:8000/users/users/1")
    #     # st.write(res.json)
    #     st.dataframe(res.json())

    # if option=='Issue book':
    #     user_id = st.number_input('user id', 1)
    #     book_id = st.number_input('book id', 1)

    if option=='Display all books':
        res = requests.get(url="http://127.0.0.1:8000/book/")
        st.dataframe(res.json())


def admin():
    option = st.selectbox('Select option', ('Display all issues',))

    if option=='Display all issues':
        res = requests.get(url="http://127.0.0.1:8000/issue/")
        st.dataframe(res.json())


selected = option_menu(
    menu_title="",
    options=['Home', 'User', 'Admin'],
    orientation="horizontal"
)

if selected=='User':
    user()
elif selected=='Admin':
    admin()
else:
    app()