import streamlit 
import pandas
import requests
import snowflake.connector
from urllib.error import URLError
streamlit.title('My Parents New Healthy Diner')
streamlit.header('Breakfast Menu')
streamlit.text('🥣Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔Hard-Boiled Free-Range egg')
streamlit.text('🥑🍞 Avocade Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')
# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected=streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries','Apple'])
fruits_to_show = my_fruit_list.loc[fruits_selected]
#Display the table on the page 
streamlit.dataframe(fruits_to_show)

streamlit.header("Fruityvice Fruit Advice!")
fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
streamlit.write('The user entered ', fruit_choice)
streamlit.text (fruit_choice)
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+fruit_choice)
#streamlit.text(fruityvice_response.json()) #just writes the data to the screen 
# write your own comment -what does the next line do? 
fruityvice_normalized = pandas.json_normalize(fruityvice_response.json()) #put josn data to normaise using panda
# write your own comment - what does this do?
streamlit.dataframe(fruityvice_normalized) #display normalised json content 

my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("SELECT * from fruit_load_list")
my_data_row = my_cur.fetchall()
streamlit.header("The fruit load list contains:")
streamlit.dataframe(my_data_row)
def insert_row_snowflake(new_fruit):
  with my_cnx.cursor() as my_cur:
    my_cur.execute("inset into fruit_load_list values ('"+new_fruit+"')")
    return "Thanks for adding" + new_fruit
  add_my_fruit =streamlit.text_input('What fruit would you like to add?')
if streamlit.button ('Add a Fruit to the List'):
  my_cnx=snowflake.connector.connect(**streamlit.secrets["snowflake"])
  back_from_function =insert_row_snowflake(add_my_fruit)
streamlit.write('Thanks for adding ', add_my_fruit)

streamlit.text(back_from_function)

