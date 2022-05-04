import streamlit as st
import appModules as am
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import pygsheets
gc = pygsheets.authorize(service_file='creds.json')

def app():
    purchaseDf = am.analyticssDf
    purchaseDf.dropna(inplace=True)
    purchaseDf['availableStock'] = purchaseDf['availableStock'].astype(int)
    productTypeList = list(purchaseDf['productType'].unique())
    productTypeList.sort()

    st.markdown("<h3 style='text-align: center;'>Rate List</h3>", unsafe_allow_html=True)
    productType = st.selectbox("Select Category",productTypeList)
    filterDf = purchaseDf[(purchaseDf['productType']==productType) & (purchaseDf['availableStock']>0)]
    productList = list(filterDf['productName'].unique())
    productList.sort()
    productName = st.selectbox("Select Product",productList)
    unitPrice = filterDf[filterDf['productName']==productName]['rate80'].values[0]
    st.info(f'### Unit Price: {unitPrice}')
    fid = filterDf[filterDf['productName']==productName]['rate40'].values[0]
    oid = filterDf[filterDf['productName']==productName]['originalCostPrice'].values[0]
    st.write(f'fid: KV01SSD{fid:05}')
    st.write(f'oid: KV01DPK{oid:05}')

    lendf = len(filterDf)
    filterDf.sort_values(by=['productName'],inplace=True)
    dfValues = [list(filterDf['productName']),list(filterDf['rate80'])]

    fig = go.Figure(data=[go.Table(
    columnorder = [1,2],
    columnwidth = [110,70],
    header = dict(
        values = [[f'<b>Date</b>'],
                    ['<b>Unit Price</b>']],
        line_color='darkslategray',
        fill_color='royalblue',
        align='center',
        font=dict(color='white', size=16),
        height=40
    ),
    cells=dict(
        values=dfValues,
        line_color='darkslategray',
        fill=dict(color=['paleturquoise', 'white']),
        align=['left', 'right'],
        font=dict(color='black', size=14),
        height=30)
        )
    ])
    fig.update_layout(width=370, height=(100+((lendf+1)*30)), margin=dict(l=0, r=0, t=50, b=0))
    st.write(fig)
