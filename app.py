import streamlit as st
from multiapp import MultiApp
from apps import purchase, sales, ratelist, analytics

# Configure app display
st.set_page_config(
    page_title="कार्तिकेय वस्त्रालय",
    layout="wide",
    initial_sidebar_state='collapsed'
)

st.markdown("<h1 style='text-align: center; color: paleturquoise;'>कार्तिकेय वस्त्रालय</h1>", unsafe_allow_html=True)

app = MultiApp()

# Add all your application here
app.add_app("Rate List", ratelist.app)
app.add_app("Sales", sales.app)
app.add_app("Purchase", purchase.app)
app.add_app("Analytics", analytics.app)
#app.add_app("Payment Received", payment.app)
#app.add_app("Remove Tenant", exitTenant.app)

# The main app
app.run()