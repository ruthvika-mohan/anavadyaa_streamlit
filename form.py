import streamlit as st
import streamlit as st
from google.oauth2 import service_account
from gsheetsdb import connect
import  gspread


st.set_page_config(page_title="Anavadyaa", page_icon="🍃")
st.title("Place order for Anavadyaa Complete Care Hair Oil")


# Create a connection object.
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=[
        "https://www.googleapis.com/auth/spreadsheets",'https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive'
    ],
)
conn = connect(credentials=credentials)

# Perform SQL query on the Google Sheet.
# Uses st.cache_data to only rerun when the query changes or after 10 min.
#@st.cache_data(ttl=600)
def run_query(query):
    rows = conn.execute(query, headers=1)
    rows = rows.fetchall()
    return rows


sheet_url = st.secrets["private_gsheets_url"]
rows = run_query(f'SELECT * FROM "{sheet_url}"')


with st.form("my_form"):
	quant = st.slider("How many bottles would you like to order?",0,10,1,1)
	fname = st.text_input("First Name")
	lname = st.text_input("Last Name")
	email = st.text_input("Email")
	addr = st.text_input("Address")
	city = st.text_input("City")
	pincode = st.number_input("Pincode")
	state = st.selectbox("State",('Karnataka','Punjab','Other'))
	phone = st.number_input("Phone Number",6000000000,9999999999)

	submitted = st.form_submit_button("Submit")

	if submitted:
		st.write("Thank you for response")
		client = gspread.authorize(credentials)
 
		sh = client.open('Anavadyaa Orders DB').worksheet('Sheet1')  
		row = [fname,lname]
		sh.append_row(row)
		st.write("Your order will be delivered soon! Watch out for a mail from our shipping partner for real time updates on your order")


# streamlit_app.py
















	

	

