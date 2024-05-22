
import streamlit as st
from deta import Deta
import pandas as pd 
import plotly.express as px

# Data to be written to Deta Base
st.title('⚕️医研趣与美的小调查📋')
st.write('进行小调查的目的，一方面是想了解大家的一些信息，更加熟悉一些；另一方面是展示新学习的这个调查问卷APP！这种APP组合了一个网络数据库detabase，填写的数据可以储存在网络数据库中，并可以进行调用，比如进行可视化。\
         可以用于患者随访，问卷调查、信息收集等场合。具有轻量便携的特点。')
with st.form("问卷"):
    id = st.text_input("Q1: ID(任意字符)")
    age = st.slider("Q2: 年龄",min_value=10, max_value=60, step=1, value=20)
    language= st.selectbox("Q3: 最常使用的编程语言?", ["Python", "R", "其它"])
    major=st.selectbox("Q4: 专业?", ["软件工程", "医学", "生物学", "其它"])
    app_type=st.selectbox("Q5: 希望使用web做什么?", ["预测模型", "深度学习模型", "统计工具","生信工具"])
    submitted = st.form_submit_button("Submit")


# Connect to Deta Base with your Data Key
deta = Deta(st.secrets["data_key"])# data_key was stored in secret.toml file 

# Create a new database "example-db"
# If you need a new database, just use another name.
db = deta.Base("survey")#my database

# If the user clicked the submit button,
# write the data from the form to the database.
# You can store any data you want here. Just modify that dictionary below (the entries between the {}).
if submitted:
    db.put({"name": id, "age": age, "language": language, "major": major, "app_type": app_type})

"***"
with st.container():
    "Here's everything stored in the database:"
    # This reads all items from the database and displays them to your app.
    # db_content is a list of dictionaries. You can do everything you want with it.
    db_content = db.fetch().items
    df_plot=st.dataframe(db_content)
#bubble chart
#creat dataframe for json data
df_plot=pd.DataFrame(db_content, columns=["name","age","language","major","app_type"])
interested_var = st.selectbox("choose variable", ["age", "language", "major", "app_type"]) 
var_count_plot = df_plot[interested_var].value_counts().rename_axis(interested_var).reset_index(name='count')
'***'
with st.container():
    st.write("Showing data with interested variable:", interested_var)
    col1, col2 = st.columns(2)
    with col2:
        st.write(var_count_plot,height=300) 
    
    with col1:
        fig = px.pie(var_count_plot, values='count', names=interested_var, title='interested variable')
        st.plotly_chart(fig)
  
    
