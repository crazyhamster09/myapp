import pandas as pd
import streamlit as st
from PIL import Image
import plotly.express as px

image = Image.open('data/Store.jpg')

st.set_page_config(
        layout="wide",
        initial_sidebar_state="auto",
        page_title="Store",
        page_icon=image,

    )

st.write(
        """
        # Продажи магазинов Favorita 
        """
    )

st.image(image)
df = st.cache_data(pd.read_csv)("data/train2014.csv")

st.sidebar.header('Выберите параметры')


st.write(
        """
        Датасет включает объем продаж, дату, идентификационный номер магазина, тип товаров, количество рекламируемых товаров в магазине 
        """
    )
st.dataframe(df)

sn = st.sidebar.multiselect(
    'Номера магазинов',
    df['store_nbr'].unique()
)

fam = st.sidebar.multiselect(
    'Типы товаров',
    df['family'].unique()
)

on = st.sidebar.multiselect(
    'Рекламируются',
    df['onpromotion'].unique()
)

f = df[(df['store_nbr'].isin(sn)) & (df['family'].isin(fam)) & (df['onpromotion'].isin(on))]
g = f[["sales", "store_nbr"]].groupby("store_nbr")

fig = px.pie(df, values='sales', names='family')
st.plotly_chart(fig, use_container_width=True)

fig = px.scatter(f, x='store_nbr', y='sales', color='family')
st.plotly_chart(fig)

fig1 = px.scatter(f, x='date', y='sales', color='family')
st.plotly_chart(fig1)

fig2 = px.scatter(f, x='onpromotion', y='sales', color='family')
st.plotly_chart(fig2)

if st.button("Cколько продали?"):
    st.text(f"Магазин {sn} продал {f['sales'].sum()} товаров типа {fam}")
