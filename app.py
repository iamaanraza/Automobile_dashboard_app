import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
# page configure 
st.set_page_config(page_icon="🚗", layout='wide',
                   page_title="Automobile Analysis")

@st.cache_data
def load_data():
    path = 'data/Automobile_data.csv'
    df = pd.read_csv(path)
    # preprocess data
    df = df.replace('?',np.nan)
    #? mark ko data se replace karke none aayega
    # fix the data types
    cols = ['bore','stroke','horsepower','peak-rpm','price']
    df[cols] = df[cols].astype('float')
    # drop the useless columns 
    cols_to_drop = ['symboling','normalized-losses']
    df = df.drop(columns=cols_to_drop) 
    return df 

df = load_data() # call the function to load data



# title and subtitle for the ui
st.title("Automobile Analysis")
st.markdown('''
this app is for analyzing the automobile data.
''')
with st.expander('Show raw data'):
    st.dataframe(df)

# create a column in streamlit
col1 , col2 , col3= st.columns(3)
col1.header("column wise data types")
col1.dataframe(df.dtypes, use_container_width=True )
col2.header("Column wise summary")
options = col2.radio("select column type",
                    ['Numerical','Textual'], horizontal=True )    
if options == 'Numerical':
    col2.dataframe(df.describe(include='number'),
                   use_container_width=True)
    
elif options == 'Textual' :
    col2.dataframe(df.describe(include='object'),
                   use_container_width=True)   
    
col3.header("Column data")
selected_col = col3.selectbox("select column ", df.columns, key='c1')
col3.dataframe(df[selected_col], use_container_width=True) 

# trend analysis (visualization)
col1, col2 = st.columns(2)
num_df = df.select_dtypes(include="number")
selected_col = col1.selectbox("select column",num_df.columns , key='c2' )
fig1 = px.line(df, y=selected_col)
col1.plotly_chart(fig1, use_container_width=True)

