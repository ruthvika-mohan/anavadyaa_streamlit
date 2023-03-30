import streamlit as st
import streamlit as st
from google.oauth2 import service_account
from gsheetsdb import connect
import  gspread
import json
import requests

from datetime import date

today = str(date.today())


st.set_page_config(page_title="Anavadyaa", page_icon="🍃")
col1,col2,col3 = st.columns(3)
with col2:
	st.image("logo.png",width=200)
st.title("Place order for Anavadyaa Complete Care Hair Oil")
st.write("Thank you for choosing Anavadyaa for your hair care needs. Please fill this form so we can deliver a freshly brewed bottle of the Complete Care Hair Oil to your doorstep. We can't wait for your hair to fall in love with Anavadyaa's magic!")

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

if 'stage' not in st.session_state:
    st.session_state.stage = 0

def set_stage(stage):
    st.session_state.stage = stage

def clear_cache():
    st.legacy_caching.caching.clear_cache()


print("STAGE",st.session_state.stage)

flag = 0
with st.form("my_form"):
	quant = st.slider("How many bottles would you like to order?",0,10,1,1)
	fname = st.text_input("First Name")
	lname = st.text_input("Last Name")
	email = st.text_input("Email")
	addr = st.text_input("Address")
	city = st.text_input("City")
	pincode = st.number_input("Pincode",format="%d",min_value=100000,max_value=800000)
	state = st.selectbox("State",('Karnataka','Punjab','Other'))
	phone = st.number_input("Phone Number",6000000000,9999999999,format="%d")
	submit_placeholder = st.empty()
	submitted = st.form_submit_button("Submit",on_click=set_stage,args=(1,))

	
	if submitted:
		#submit_placeholder.form_submit_button("Submit",on_click=set_stage,args=(1,),disabled=True,key='2')
		st.write("Thank you for your response")
		st.write("Please make payment through this QR code")
		st.image("qr.jpg")

		url = "https://apiv2.shiprocket.in/v1/external/orders/create/adhoc"

		sheet_url = st.secrets["private_gsheets_url"]
		rows = run_query(f'SELECT * FROM "{sheet_url}"')
		id = 6000+len(rows)

		payload = json.dumps({
  		"order_id": id,
  		"order_date": today,
  		"pickup_location": "Primary",
  		"channel_id": "",
  		"comment": "Reseller: M/s Goku",
  		"billing_customer_name": fname,
  		"billing_last_name": lname,
  		"billing_address": addr,
  		"billing_address_2": "",
  		"billing_city": city,
  		"billing_pincode": int(pincode),
  		"billing_state": state,
  		"billing_country": "India",
  		"billing_email": email,
  		"billing_phone": int(phone),
  		"shipping_is_billing": True,
  		"shipping_customer_name": "",
  		"shipping_last_name": "",
  		"shipping_address": "",
  		"shipping_address_2": "",
  		"shipping_city": "",
  		"shipping_pincode": "",
  		"shipping_country": "",
  		"shipping_state": "",
  		"shipping_email": "",
  		"shipping_phone": "",
  		"order_items": [
    		{
      		"name": "Anavadyaa Complete Care Hair Oil",
      		"sku": "200ml",
      		"units": quant,
      		"selling_price": quant*350,
      		"discount": "",
      		"tax": "",
      		"hsn": 441122
    		}
  		],
  		"payment_method": "Prepaid",
  		"shipping_charges": 70,
  		"giftwrap_charges": 0,
  		"transaction_charges": 0,
  		"total_discount": 0,
  		"sub_total": 350*quant,
  		"length": 10,
  		"breadth": 15,
  		"height": 20,
  		"weight": 2.5
		})
		headers = {
  		'Content-Type': 'application/json',
  		'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOjM0MjEwNjcsImlzcyI6Imh0dHBzOi8vYXBpdjIuc2hpcHJvY2tldC5pbi92MS9leHRlcm5hbC9hdXRoL2xvZ2luIiwiaWF0IjoxNjc5OTI1ODkzLCJleHAiOjE2ODA3ODk4OTMsIm5iZiI6MTY3OTkyNTg5MywianRpIjoiSkZ6d2RQaUlqWjJYYUF3diJ9.uBmuFmUx8f3JyeLroUvrsGMhyXjfRv57o19oDRbmyaA'}

		response = requests.request("POST", url, headers=headers, data=payload)

		print(response.text)
		client = gspread.authorize(credentials)
 
		sh = client.open('Anavadyaa Orders DB').worksheet('Sheet1')  
		row = [today,fname,email,addr,city,pincode,phone,lname,state,quant,]
		sh.append_row(row)
		flag = 1

if st.session_state.stage > 0:
	placeholder = st.empty()
	btn = placeholder.button('Click if payment completed', disabled=False, key='1')
	if btn:
		placeholder.button('Click if payment completed', disabled=True, key='2')
		st.write("Your order will be delivered soon once payment is received! Watch out for an email confirmation from Anavadyaa and WhatsApp message from our shipping partner for real time updates on your order")
		if st.button('Create new order'):
			clear_cache()
			st.experimental_rerun()
			set_stage(0)
			print("STAGE",st.session_state.stage)
			
	
		
		
		