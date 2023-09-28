import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.title('My Mom\'s New Healthy Diner')

streamlit.header('Breakfast Favourites')
streamlit.text('🥣Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞Avocado Toast')

streamlit.header('🍌🥭Build Your Own Fruit Smoothie🥝🍇')
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

#Pick list to allow users to select fruits to go into their smoothie
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

#Displays table with fruits on the page
streamlit.dataframe(fruits_to_show)

def get_fruityvice_data(this_fruit_choice):
  #Displays fruityvice api response
  fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + this_fruit_choice)
  #normalizes the json version of the response received
  fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
  return fruityvice_normalized
  

#Header for fruityvice api response
streamlit.header("Fruityvice Fruit Advice!")

try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
    streamlit.error('Please select a fruit to get information.')
  else:
    back_from_function = get_fruityvice_data(fruit_choice)
    #displays the normalize response in a table
    streamlit.dataframe(fruityvice_normalized)

except URLError as e:
  streamlit.error()

my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("select * from fruit_load_list")
my_data_rows = my_cur.fetchall()
streamlit.header("The fruit load list contains:")
streamlit.dataframe(my_data_rows)

#Allow the user to add a fruit to the list
add_my_fruit = streamlit.text_input('What fruit would you like to add?')

streamlit.text("Thanks for adding " + add_my_fruit)

my_cur.execute("insert into fruit_load_list values ('from streamlit')")
