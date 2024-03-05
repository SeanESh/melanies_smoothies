# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests

# Write directly to the app
st.title("Customine Your Smoothie :cup_with_straw:")

name_on_order = st.text_input('Name on Smoothie:', '')
st.write('The name on the smoothie will be:', name_on_order)


cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME')) 
#st.dataframe(data=my_dataframe, use_container_width=True)
ingredients_list = st.multiselect(
'Choose up to 5 ingredients',
my_dataframe,
max_selections=5)

ingredients_string=''

if ingredients_list:
    
    for fruit_chosen in ingredients_list:
        ingredients_string+=fruit_chosen + ' '
        st.subheader(fruit_chosen+' Nutrition Info')
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+fruit_chosen)
        fv_df=st.dataframe(data=fruityvice_response.json(),use_container_width=True)
        
time_to_insert = st.button('Submit Order')        

my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string +"""','"""+name_on_order+ """')"""

if time_to_insert:
    session.sql(my_insert_stmt).collect()
    st.success('Your Smoothie is ordered!', icon="✅")


