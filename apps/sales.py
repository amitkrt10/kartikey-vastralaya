import streamlit as st
import appModules as am
import pandas as pd
import numpy as np
import pygsheets
gc = pygsheets.authorize(service_file='creds.json')

def app():
    purchaseDf = am.purchaseDf
    productTypeList = list(purchaseDf['productType'].unique())
    productTypeList.sort()
    productList = list(purchaseDf['productName'].unique())
    productList.sort()
    salesDf = am.salesDf

    st.markdown("<h3 style='text-align: center;'>Billing Form</h3>", unsafe_allow_html=True)
    billingDate = st.date_input("Billing Date")
    customerName = st.text_input("Customer Name")
    mobile = st.text_input("Customer Mobile")
    productType = st.radio("Product Type",productTypeList)
    with st.form("Product Form",clear_on_submit=True):
        rowList = []
        productList = list(purchaseDf[purchaseDf["productType"]==productType]['productName'].unique())
        productList.sort()
        productName = st.selectbox("Product",productList)
        quantity = st.text_input("Quantity")
        scp = st.text_input("Unit Selling Price")
        submitted = st.form_submit_button("Submit")
        if submitted:
            rowList.append(billingDate)
            rowList.append(customerName)
            rowList.append(mobile)
            rowList.append(productType)
            rowList.append(productName)
            rowList.append(quantity)
            rowList.append(scp)
            salesDf.loc[len(salesDf.index)] = rowList
            #Update Gsheet
            sh = gc.open(st.secrets["sheetName"])
            wks = sh[am.salesDfIndex]
            wks.set_dataframe(salesDf,(1,1))
            st.success(f"{productName} added successfully.")