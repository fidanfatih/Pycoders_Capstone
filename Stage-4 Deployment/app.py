# streamlit run app.py
# pip freeze > requirements.txt
# pip install -r requirements.txt

import streamlit as st
import pickle
import pandas as pd
import numpy as np
from PIL import Image
import base64
from io import BytesIO

# st.title('Car Price Prediction')
# st.markdown("<h1 style='text-align: center; color: black;'>Car Price Prediction</h1>", unsafe_allow_html=True)
st.write('Created on Wed April 13 10:21:04 2020')
st.write('@author:fidanfatih')
im = Image.open("cover.png")
st.image(im, width=700)

html_temp = """
<div style="width:700px;background-color:maroon;padding:10px">
<h1 style="color:white;text-align:center;">Car Price Prediction (Demo)</h1>
</div>"""
st.markdown(html_temp,unsafe_allow_html=True)

st.markdown("<h3></h3>", unsafe_allow_html=True)

def main():
    st.sidebar.header("How would you like to predict?")
    add_selectbox = st.sidebar.selectbox("", ("Unique Input", "Batch Input"))
    slider_cols = ['fuel_type','power', 'age', 'co2_emissions', 'mileage','fuel_consumption_mean', 'engine_size', 'empty_weight','warranty']
#     side_slider_cols= []
    mapping_cols= ['make_model',]
    selectbox_cols = ['inspection_new','gears','body_type','province','make_country',
                 'type','emission_class','colour','upholstery_colour', 'full_service_history',
                 'gearbox','seller','drivetrain','upholstery','paint','non_smoker_vehicle']
   
    # @st.cache
    # bir buyuk bir datatyi read_csv ile tekrar tekrar okutmamak icin hafuzada tutmasi icin st.cache kullanilir.
    lightGBM = pickle.load(open("LGBReg.pkl","rb"))
    
    with open('make_model.dict', 'rb') as handle:
        make_model_dict = pickle.load(handle)

    with open('limits.dict', 'rb') as handle:
        limits_dict = pickle.load(handle)
        
    with open('car_tools.dict', 'rb') as handle:
        car_tools_dict = pickle.load(handle)

    with open('cat_cols_uniques.dict', 'rb') as handle:
        cat_cols_uniques_dict = pickle.load(handle)
        
    with open('all_cols.dict', 'rb') as handle:
        all_cols_dict = pickle.load(handle)
       

    if add_selectbox == "Unique Input":
        st.markdown("""
 :dart: Top 10 Most Important Features:\n
""")
        st.sidebar.info(':dart: Low-Importance Features:')
        my_dict=dict()
        
        # Mapping Columns (Label Encoding)
        for col in mapping_cols:
            value= st.selectbox(f"{col} :", list(make_model_dict.keys()))
            my_dict[col] = make_model_dict[value]
            my_dict['make'+'_'+value.split()[0]] = 1

        # Top 10 Most Important Features
        for i,col in enumerate(slider_cols):
            if col=='mileage':
                bins = np.array([0,2500,7000,10000, 33000,68000, 100000, 135000, 170000,210000, 255000, 310000, 10000000])
                my_dict[col] =np.digitize(st.slider(f"{col} (x1000 km) :", 0, 1000,50, step=1), bins)
            elif col=='empty_weight':
                bins = np.array([900, 1050, 1150, 1260, 1360, 1480, 1700, 2030, 2400, 4500])
                my_dict[col] =np.digitize(st.slider(f"{col} (kg) :", 900, 4500,1600, step=1), bins)  
            elif col=='warranty':
                my_dict[col] =st.select_slider(f"{col} (months):", [3,6,12,24,84])    
            elif col=='engine_size':
                my_dict[col] =st.slider(f"{col} (cc):", limits_dict[col][0], limits_dict[col][1],limits_dict[col][2], step=1)
            elif col=='fuel_consumption_mean':
                my_dict[col] =st.slider(f"{col} (l/100 km (comb.)):", limits_dict[col][0], limits_dict[col][1],limits_dict[col][2], step=1)
            elif col=='co2_emissions':
                my_dict[col] =st.slider(f"{col} (g/km (comb.)):", limits_dict[col][0], limits_dict[col][1],limits_dict[col][2], step=1)
            elif col=='power':
                my_dict[col] =st.slider(f"{col} (hp):", limits_dict[col][0], limits_dict[col][1],limits_dict[col][2], step=1)
            elif col=='age':
                my_dict[col] =2022 - st.slider(f"first_registration (year):", 2000, 2022, 2020, step=1)
            elif col=='fuel_type':
                value=st.selectbox(f"fuel_type:", ['Gasoline','Diesel','Hybrit','Electric','LPG','Others'])
                my_dict[col+"_"+value] = 1 
            else:    
                my_dict[col] =st.slider(f"{col} :", limits_dict[col][0], limits_dict[col][1],limits_dict[col][2], step=1)
     
        # Sidebar Columns
        for i, col in enumerate(selectbox_cols):
            if col=='inspection_new':
                value= st.sidebar.radio('Is inspection new?',('Yes', 'No'))
                my_dict[col+"_"+value]=1
            elif col=='gears':
                my_dict[col] =st.sidebar.slider(f"{col} :", limits_dict[col][0], limits_dict[col][1],limits_dict[col][2], step=1)
            else:
                value = st.sidebar.selectbox(f"{col} :", cat_cols_uniques_dict[col])
                my_dict[col+"_"+value] = 1    
                
        # Car Tools 
        for col in car_tools_dict.keys():
            if col=='cc':
                st.sidebar.write(f"\nSelect Confort & Convenience Equipments:")
            elif col=='em':
                st.sidebar.write(f"\nSelect Entertainment Media Equipments:")
            elif col=='ss':
                st.sidebar.write(f"\nSelect Safety & Security Equipments:")    
            elif col=='ex':
                st.sidebar.write(f"\nSelect Extra Equipments:")
            for i in car_tools_dict[col]:
                my_dict[col+"_"+i] = st.sidebar.checkbox(i)

        df = pd.DataFrame([my_dict]) 
        df = df.reindex(columns=all_cols_dict, fill_value=0)

        # Table
        def single_customer(my_dict):
            df_table = pd.DataFrame.from_dict([my_dict])
        #     st.table(df_table) 
            st.write('')
            st.dataframe(data=df_table, width=700, height=400)
            st.write('')

        single_customer(my_dict)

        # Button
        if st.button("Submit Manuel Inputs"):
            import time
            with st.spinner("ML Model is loading..."):
                my_bar=st.progress(0)
                for p in range(0,101,10):
                    my_bar.progress(p)
                    time.sleep(0.1)

                prediction= lightGBM.predict(df)
                st.success(f"The Estimated Price of the Car is €{int(prediction[0])}")

                
    
    else:
        # Upload a csv
        output = pd.DataFrame()
        uploaded_file = st.file_uploader("Choose a file")
        if uploaded_file is not None:
            file = pd.read_csv(uploaded_file, index_col=[0])
            flag=file.copy()
            st.dataframe(data=file, width=700, height=1000)
            st.write('')
        #  st.table(file)
        
        # Load Button
        if st.button("Submit CSV File"):
            import time
            with st.spinner("ML Model is loading..."):
                my_bar=st.progress(0)
                for p in range(0,101,10):
                    my_bar.progress(p)
                    time.sleep(0.1)

            for i in file.index:
                col="make model"
                file.loc[i,'make'+'_'+file.loc[i,col].split()[0]]  = 1
                file.loc[i,'make_model']  = make_model_dict[file.loc[i,col]]
                    

#             file = file.drop(["make model"], axis=1)
            file = file.reindex(columns=all_cols_dict, fill_value=0)
            pred_file = pd.DataFrame(lightGBM.predict(file)).rename({0:'Price (€)'}, axis=1)
            output = pd.concat([pred_file,flag], axis=1).reset_index().drop('index', axis=1)
            st.write('')
            st.dataframe(data=output, width=700, height=400)
            st.write('')

        def download_link(object_to_download, download_filename, download_link_text):
            if isinstance(object_to_download,pd.DataFrame):
                object_to_download = object_to_download.to_csv(index=False)

            # some strings <-> bytes conversions necessary here
            b64 = base64.b64encode(object_to_download.encode()).decode()

            return f'<a href="data:file/txt;base64,{b64}" download="{download_filename}">{download_link_text}</a>'

        # if st.button('Download Output as CSV'):
        tmp_download_link = download_link(output, 'output.csv', 'Click here to download output as csv!')
        st.markdown(tmp_download_link, unsafe_allow_html=True)

        comment = st.text_input('Write your comments below.')
        # st.write(comment)

        # if st.button('Download input as a text file'):
        tmp_download_link = download_link(comment, 'commend.txt', 'Click here to download comment text!')
        st.markdown(tmp_download_link, unsafe_allow_html=True)

if __name__ == '__main__':
    main()