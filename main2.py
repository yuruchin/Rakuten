import requests
import streamlit as st
import pandas as pd
import plotly.express as px

area_code_list = {
    "那覇市" : "nahashi",
    "恩納 名護 本部 今帰仁" : "hokubu",
    "宜野湾 北谷 読谷 沖縄市 うるま" : "chubu",
    "糸満 豊見城 南城" : "nanbu",
    "慶良間 渡嘉敷 座間味 阿嘉" : "kerama"
}

st.title('沖縄本島ホテル検索アプリ') 


area_code_index = st.selectbox("地域を選んでください。",area_code_list.keys())

areacode = area_code_list[area_code_index]
APP_ID ='1094102683800240340'

params = {
    "format" : "json",
    "largeClassCode" : "japan",
    "middleClassCode": "okinawa",
    "smallClassCode": areacode,
    "applicationId" : APP_ID
}

REQUEST_URL = 'https://app.rakuten.co.jp/services/api/Travel/SimpleHotelSearch/20170426?'

res = requests.get(REQUEST_URL, params)
result = res.json()

hotel_info = result["hotels"][0]["hotel"][0]['hotelBasicInfo']
df = pd.DataFrame(hotel_info, index = [0])

for i in range(0, len(result["hotels"])):
    hotel_info = result["hotels"][i]["hotel"][0]['hotelBasicInfo']
    temp_df = pd.DataFrame(hotel_info, index = [i])
    df = pd.concat([df, temp_df])

df = df[['hotelName', 'hotelMinCharge', 'reviewAverage']]

rank = df.sort_values(by = "reviewAverage", ascending=False).head(10)

fig = px.scatter(
    df,
    x="hotelMinCharge",
    y="reviewAverage",
    hover_name="hotelName",
    labels={"hotelMinCharge": "Hotel Min Charge", "reviewAverage": "Review Average"}
)

tab1, tab2 = st.tabs(["Streamlit theme (default)", "Review score top ten"])
with tab1:
    # Use the Streamlit theme.
    # This is the default. So you can also omit the theme argument.
    st.plotly_chart(fig, theme="streamlit", use_container_width=True)
with tab2:
    # Use the native Plotly theme.
    st.table(rank)