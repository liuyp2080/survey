
import streamlit as st
from deta import Deta
import pandas as pd     
import plotly.express as px
import streamlit_survey as ss
import json
from streamlit_option_menu import option_menu
# sidebar for navigation
with st.sidebar:
    selected = option_menu('××队列研究',

                           ['研究设计',
                            '调查问卷'
                            ],
                           menu_icon='hospital-fill',
                           icons=['activity', 'heart'],
                           default_index=0)



if selected=='知情同意':
    st.title('⚕️知情同意')
if selected=='调查问卷':
# Data to be written to Deta Base
    st.title('⚕️调查问卷（胸部手术后慢性疼痛队列）demo📋')
    st.write('''
            建立一个临床研究队列是临床上流行的研究形式，这种研究形式是通过收集临床诊疗过程中形成的数据来阐明疾病相关的因素。在收集医学数据的过程中，调查问卷、患者随访是医学研究中获取数据的重要形式之一，使用纸质的的量表或者excel表格都有不便之处，而web APP轻量便携，扩展性强，
            是作为调查问卷新的形式,在收集变量结束后还可以作为队列数据库展示的页面，与大型调查网站的相比，可以登陆数据库后台对数据操作，自主性更高。
            下面是一个调查问卷类的APP Demo，使用streamlit框架搭配其扩展包streamlit_survey构建而成。
            ''')


    '***'  
    #首先建立一个问卷调查的界面
    survey = ss.StreamlitSurvey("Survey Example - Advanced Usage")
    #构建页面
    pages = survey.pages(4, on_submit=lambda: st.success("感谢参与调查，谢谢!祝早日康复!"))
    with pages:
        if pages.current == 0:#第一页，患者基本信息
            
            st.subheader("数据输入：1.患者的基本信息")#问题1
            
            survey.number_input("识别号（ID）", min_value=0, max_value=1000,value=0,id="id")
            
            survey.slider("Q1：患者的年龄?",min_value=0, max_value=100,step=1,  id="age")
            
            survey.radio("Q2：患者的性别",options=["男", "女"],id="gender",horizontal=True)
            
            survey.slider('Q3：患者的身高(cm)',min_value=0, max_value=200,step=1, id="height")
            
            survey.slider('q4：患者的体重(kg)',min_value=0, max_value=200,step=1, id="weight")
            
        
        elif pages.current == 1:#第二页，患者疾病信息
            st.subheader("数据输入：2.患者的术前术中信息")
            survey.radio('Q5:手术类型？',options=["Axillary thoracotomy","Posterolateral thoracotomy"],id="operation",horizontal=True)
            
            survey.radio('Q6:是患有癌症？',options=["Yes","No"],id="cancer",horizontal=True)
            
            survey.radio('Q7：术前是否有疼痛？',options=["Yes","No"],id="preoperation_pain",horizontal=True)
            
            survey.slider('Q8：术中麻醉时长？',min_value=0, max_value=100,step=1, id="anaesthesia_duration")
            
            survey.slider('Q9：手术时长？',min_value=0, max_value=100,step=1,  id="operation_duration")
            
            survey.radio('Q10：肺叶切除？',options=["Lobectomy","No"],id="Lobectomy",horizontal=True)
            
            survey.radio('Q11:肺楔型切除？',options=["Wedge","No"],id="wedge",horizontal=True)
            
            survey.radio('Q12:肺切除？',options=["Pneumonectomy","No"],id="pneumonectomy",horizontal=True)
            
            survey.radio('Q13:左侧还是右侧？',options=["Left","Right"],id="left_right",horizontal=True)
            
            survey.radio('Q14：术中使用牵拉器？',options=["Yes","No"],id="surgical_retractor",horizontal=True)
            
            survey.radio('Q15：是否有肋骨骨折？',options=["Yes","No"],id="rib_fracture",horizontal=True)
            
            survey.radio("Q16：是否经肋缝合？",options=["Yes","No"],id="transcostal_suture",horizontal=True)
            
            survey.slider('Q17:切口长度（cm）？',min_value=0, max_value=100,step=1, id="scar_length")
        if pages.current == 2:#第三页，患者术后信息
            
            st.subheader('数据输入：3.患者术后信息')
            
            survey.radio('Q18:术后镇痛方式？',options=[1,2,3,4],id="postoperation_anathesia",horizontal=True)
            
            survey.slider('Q19:引流管留置时长？',min_value=0, max_value=10,step=1, id="chest_tube")
            
            survey.slider('Q20:静息时疼痛评分？',min_value=0, max_value=10,step=1, id="rest_pain_score")
            
            survey.slider('Q21:咳嗽时疼痛评分？',min_value=0, max_value=10,step=1, id="cough_pain_score") 
            
            survey.slider('Q22:活动同侧肩时疼痛评分？',min_value=0, max_value=10,step=1, id="moving_shoulder_pain_score")
            
            survey.slider('Q23:住院时长？',min_value=0, max_value=100,step=1, id="long_of_stay")
            
        if pages.current == 3:#第四页，患者随访信息
            
            st.subheader('数据输入：4.患者随访信息')
            
            survey.slider('Q24:术后四个月慢性痛评分？',min_value=0, max_value=10,step=1, id="chronic_pain_score_4months")
            
            survey.radio('Q25:术后四个月神经病理性痛？',options=["Yes","No"],id="chronic_neuropathic_pain",horizontal=True)
            
    '***'       
    st.subheader("数据预览:")        
    data=survey.to_json()# string形式
    #string to json
    data=json.loads(data)
    st.table(data)

    submit=st.button("提交",type="primary",use_container_width=True)
    '*请确认数据正确无误！'

    #josn to dataframe

    data_df=pd.DataFrame(data)
    data_df_value=data_df[data_df.index=='value']
    data_dict=data_df_value.to_dict(orient='index')
    submit_value=data_dict['value']
    # st.write(submit_value)

    # Connect to Deta Base with your Data Key
    deta = Deta(st.secrets["data_key"])# data_key was stored in secret.toml file 

    # Create a new database "example-db"
    # If you need a new database, just use another name.
    db = deta.Base("survey")#my database
    if submit:
        st.balloons()   
        db.put(submit_value)

    "***"
    with st.container():
        st.subheader("数据展示:")
        # This reads all items from the database and displays them to your app.
        # db_content is a list of dictionaries. You can do everything you want with it.
        db_content = db.fetch().items
        df_plot=st.dataframe(db_content)
    #bubble chart
    #creat dataframe for json data
    df_plot=pd.DataFrame(db_content)
    interested_var = st.selectbox("choose variable", df_plot.columns)

    var_count_plot = df_plot[interested_var].value_counts().rename_axis(interested_var).reset_index(name='count')

    '***'   
    with st.container():
        st.write("Showing data with interested variable:", interested_var)
        col1, col2 = st.columns(2)
        with col2:
            st.write(var_count_plot) 
        
        with col1:
            fig = px.pie(var_count_plot, values='count', names=f'{interested_var}', title=f'{interested_var} Count')
            st.plotly_chart(fig)
        
        fig_density = px.density_contour(df_plot, x=f'{interested_var}',title=f'{interested_var} Density')
        st.plotly_chart(fig_density)
