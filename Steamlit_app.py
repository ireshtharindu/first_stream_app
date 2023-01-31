import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError


streamlit.title('My Pairents New Healthy Diner') 

streamlit.header('Breakfast Menu') 
streamlit.text('🥣 Omega 3 & blueberry Oatmeal') 
streamlit.text('🥗 Kale, spanish & Rocket Smoothie') 
streamlit.text('🐔 Hard-Boiled Free-Range Egg') 
streamlit.text('🥑🍞 Avocado Toast') 

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

#import pandas

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")

my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
#Let'sput a pick list here so they can pick the fruit they want to include 
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]



# Display the table on the page.
streamlit.dataframe(fruits_to_show)

#create new repeatable code block(called afunction)
def get_fruityvice_data(this_fruit_choice):
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+ this_fruit_choice)
        fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
        return fruityvice_normalized
  
  

#new selectionto response fruityvice api response
streamlit.header('Fruityvice Fruit Advice!')
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
    streamlit.error("Please select a fruit to get information")
  else:
       back_from_function = get_fruityvice_data(fruit_choice)
       streamlit.dataframe(back_from_function)
        
except URLError as e:
  streamlit.error()

#Do not run anything past hearwhile we troubleshoot
streamlit.stop()

#my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("SELECT * FROM fruit_load_list")
my_data_rows = my_cur.fetchall()
streamlit.header("The fruit load list contains:")
streamlit.dataframe(my_data_rows)


#new selectionto response fruityvice api response
#streamlit.header("Fruityvice Fruit Advice!")
#allow end user to add a fruit tothe list
def insert_row_snowflake(new_fruit):
        with my_cnx.cusor() as my_cur:
                my_cur.execute("insert into fruit_load_list values ('from streamlit')")
                return "Thanks for adding " + new_fruit
        
add_my_fruit = streamlit.text_input('What fruit would you like to add?')
if streamlit.button('Add  a Fruit to the list'):
        my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
        back_from_function = insert_row_snowflake(add_my_fruit)
        streamlit.text(back_from_function)

#lesson12


