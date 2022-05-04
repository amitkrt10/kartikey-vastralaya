import streamlit as st
import appModules as am
import pygsheets
gc = pygsheets.authorize(service_file='creds.json')

def app():
    purchaseDf = am.purchaseDf
    productTypeList = list(purchaseDf['productType'].unique())
    productTypeList.sort()
    productTypeList.append('Other')

    st.markdown("<h3 style='text-align: center;'>Purchase Form</h3>", unsafe_allow_html=True)
    with st.form("Procurement Form",clear_on_submit=True):
        purchaseDate = st.date_input("Purchase Date")
        productType = st.selectbox("Product Type",productTypeList)
        if productType=='Other':
            productType = st.text_input("Enter New Product Type")
        productName = st.text_input("Product Name")
        quantity = st.text_input("Quantity")
        ucp = st.text_input("Unit Cost Price without GST")
        submitted = st.form_submit_button("Submit")
        if submitted:
            rowList = []
            rowList.append(purchaseDate)
            rowList.append(productType)
            rowList.append(productName)
            rowList.append(quantity)
            rowList.append(ucp)
            purchaseDf.loc[len(purchaseDf.index)] = rowList
            #Update Gsheet
            sh = gc.open(st.secrets["sheetName"])
            wks = sh[am.purchaseDfIndex]
            wks.set_dataframe(purchaseDf,(1,1))
            st.success(f"{productName} added successfully.")
