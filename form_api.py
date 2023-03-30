import streamlit as st
import json 
import requests

from datetime import date

today = date.today()


st.set_page_config(page_title="Anavadyaa", page_icon="🍃")
col1,col2,col3 = st.columns(3)
with col2:
	st.image("logo.png",width=200)
st.title("Place order for Anavadyaa Complete Care Hair Oil")





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

	submitted = st.form_submit_button("Submit")

	if submitted:
		st.write("Thank you for response")

		url = "https://apiv2.shiprocket.in/v1/external/orders/create/adhoc"

		payload = json.dumps({
  		"order_id": "224-448",
  		"order_date": str(today),
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

		st.write(response.text)