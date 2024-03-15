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
# numerical analysis
st.header("Numerical Analysis")
num_df = df.select_dtypes(include='number')
selected_col = st.selectbox("select column", num_df.columns, key='c2')

fig1 = px.line(num_df, y=selected_col)
fig2 = px.histogram(num_df, x=selected_col, nbins=50)

col1, col2 = st.columns(2)
col1.plotly_chart(fig1, use_container_width=True)
col2.plotly_chart(fig2, use_container_width=True)

# textual analysis
st.header("Textual Analysis")
text_df = df.select_dtypes(include='object')
selected_col = st.selectbox("select column", text_df.columns, key='c3')
count = text_df[selected_col].value_counts()

fig3 = px.pie(count, values=count.values, names=count.index, hole=.6)
fig4 = px.bar(count, x=count.index, y=count.values, text=count.values)

col1, col2 = st.columns(2)
col1.plotly_chart(fig3, use_container_width=True)
col2.plotly_chart(fig4, use_container_width=True)

# correlation analysis
st.header("Correlation Analysis")
c1, c2 = st.columns(2)
c1.subheader("Numerical Correlation")
sel_num_col = c1.selectbox("select column", num_df.columns, key='c4')
sel_num_col2 = c1.selectbox("select column", num_df.columns, key='c5')

fig5 = px.scatter(num_df, 
                x=sel_num_col, 
                y=sel_num_col2,
                trendline='ols')
c1.plotly_chart(fig5, use_container_width=True)

c2.subheader("Categorical Correlation")
sel_cat_col = c2.selectbox("select column", text_df.columns, key='c6')
sel_num_col = c2.selectbox("select column", num_df.columns, key='c7')

fig6 = px.box(df, x=sel_cat_col, y=sel_num_col)
c2.plotly_chart(fig6, use_container_width=True)

# other graph

st.header('1D Distribution') # sunburst
cat_cols = st.multiselect("select columns", text_df.columns, key='c8')
num_col = st.selectbox("select columns", num_df.columns, key='c9')

temp_df = df[cat_cols + [num_col]].copy()
temp_df = temp_df.dropna()

fig7 = px.sunburst(temp_df, path=cat_cols, values=num_col, height=600)
st.plotly_chart(fig7, use_container_width=True)

# run this code in terminal
# streamlit run app.py
