import streamlit as st


st.set_page_config(page_title="Anavadyaa", page_icon="🍃")
st.title("Place order for Anavadyaa Complete Care Hair Oil")

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


# streamlit_app.py

import streamlit as st
from google.oauth2 import service_account
from gsheetsdb import connect

# Create a connection object.
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=[
        "https://www.googleapis.com/auth/spreadsheets",
    ],
)
conn = connect(credentials=credentials)

# Perform SQL query on the Google Sheet.
# Uses st.cache_data to only rerun when the query changes or after 10 min.
@st.cache_data(ttl=600)
def run_query(query):
    rows = conn.execute(query, headers=1)
    rows = rows.fetchall()
    return rows

sheet_url = st.secrets["private_gsheets_url"]
rows = run_query(f'SELECT * FROM "{sheet_url}"')

# Print results.
for row in rows:
    st.write(row)
    #st.write(f"{row.name} has a :{row.pet}:")



	

	

