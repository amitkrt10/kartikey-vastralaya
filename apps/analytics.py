import streamlit as st
import appModules as am
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import pygsheets
gc = pygsheets.authorize(service_file='creds.json')

def app():
    st.markdown("<h3 style='text-align: center;'>Analytics</h3>", unsafe_allow_html=True)
    analyticssDf = am.analyticssDf
    analyticssDf.dropna(inplace=True)
    groupDf = analyticssDf.groupby('productType').agg(np.sum)
    groupDf = groupDf.astype(int)
    totalsp = groupDf['sellingPrice'].sum()
    totalscp = groupDf['soldCostPrice'].sum()
    totalcp = groupDf['totalCostPrice'].sum()
    profit = totalsp - totalscp
    try:
        profitP = profit/totalscp*100
    except:
        profitP = 0
    netProfit = totalsp - totalcp
    try:
        netProfitP = netProfit/totalcp*100
    except:
        netProfitP = 0
    if profit > 0:
        st.info(f'Sales Profit = ₹ {profit} ({int(profitP)}%)')
    else:
        st.error(f'Sales Profit = ₹ {-(profit)} ({int(-(profitP))}%)')
    if netProfit > 0:
        st.info(f'Net Profit = ₹ {netProfit} ({int(netProfitP)}%)')
    else:
        st.error(f'Net Loss = ₹ {-(netProfit)} ({int(-(netProfitP))}%)')
    
    #Profit
    profitDf = groupDf[['sellingPrice','soldCostPrice','totalCostPrice']]
    profitDf['profit'] = profitDf['sellingPrice'] - profitDf['soldCostPrice']
    profitDf['profitP'] = profitDf['profit']/profitDf['soldCostPrice']*100
    profitDf['netProfit'] = profitDf['sellingPrice'] - profitDf['totalCostPrice']
    profitDf['netProfitP'] = profitDf['netProfit']/profitDf['totalCostPrice']*100
    profitDf.fillna(0,inplace=True)
    profitDf.sort_values(by=['profit'],ascending=False,inplace=True)
    profitDf['profitP'] = profitDf['profitP'].apply(lambda x: str(int(x))+'%')
    profitDf['netProfitP'] = profitDf['netProfitP'].apply(lambda x: str(int(x))+'%')
    lendf = len(profitDf)+1
    cols = list(profitDf.columns)
    dfValues = [list(profitDf.index) + ['<b>Total</b>'],
                    list(profitDf[cols[3]]) + [f'<b>{profit}</b>'],
                    list(profitDf[cols[4]]) + [f'<b>{int(profitP)}%</b>'],
                    list(profitDf[cols[5]]) + [f'<b>{netProfit}</b>'],
                    list(profitDf[cols[6]]) + [f'<b>{int(netProfitP)}%</b>']]
    fig = go.Figure(data=[go.Table(
    columnorder = [1,2,3,4,5],
    columnwidth = [50,35,30,35,30],
    header = dict(
        values = [['<b>Category</b>'],
                    ['<b>Profit</b>'],
                    ['<b>%</b>'],
                    ['<b>Net Profit</b>'],
                    ['<b>Net %</b>']],
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
    ],
    layout=go.Layout(title=go.layout.Title(text="<b>Profits</b>"))
    )
    fig.update_layout(width=370, height=(100+((lendf+1)*30)), margin=dict(l=0, r=0, t=50, b=0))
    st.write(fig)

    #Stocks
    stockDf = groupDf[['stock','soldStock','availableStock']]
    stockDf.sort_values(by=['availableStock'],ascending=False,inplace=True)
    lendf = len(stockDf)+1
    cols = list(stockDf.columns)
    dfValues = [list(stockDf.index) + ['<b>Total</b>'],
                    list(stockDf[cols[0]]) + [f'<b>{stockDf[cols[0]].sum()}</b>'],
                    list(stockDf[cols[1]]) + [f'<b>{stockDf[cols[1]].sum()}</b>'],
                    list(stockDf[cols[2]]) + [f'<b>{stockDf[cols[2]].sum()}</b>']]
    fig = go.Figure(data=[go.Table(
    columnorder = [1,2,3,4],
    columnwidth = [60,40,40,40],
    header = dict(
        values = [['<b>Category</b>'],
                    ['<b>Purchase Stocks</b>'],
                    ['<b>Sold Stocks</b>'],
                    ['<b>Availabe Stocks</b>']],
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
    ],
    layout=go.Layout(title=go.layout.Title(text="<b>Stocks</b>"))
    )
    fig.update_layout(width=370, height=(100+((lendf+1)*30)), margin=dict(l=0, r=0, t=50, b=0))
    st.write(fig)