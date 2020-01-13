import mysql.connector
from mysql.connector import errorcode
from core.model.customer import Customer

config = {
  'user': 'root',
  'password': 'shihang123',
  'host': '127.0.0.1',
  'database': 'bike_fit',
  'raise_on_warnings': True
}


add_customer = ("INSERT INTO customers "
               "VALUES (0, %(first_name)s, %(last_name)s, %(age)s, %(sex)s, %(mobile)s, %(email)s, %(bike_make)s, %(bike_size)s, %(bike_year)s, %(bike_type)s)")

data_customer = {
  "first_name": 'stephen',
  "last_name": 'Yu',
  "age": 28,
  "sex": 'male',
  "mobile": '00971544523599',
  "email": 'shihang.yu@gmail.com',
  "bike_make": 'boardman',
  "bike_size": 'm54',
  "bike_year": 2007,
  "bike_type": 'triathlon'
}
#
customer = Customer("stephen", "yu", 28, "male", "0325235", "sdad@gmail.com", "daf", "fdsf", 2018, "fsdf")

try:
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    # Insert new employee
    cursor.execute(add_customer, customer)
    # Make sure data is committed to the database
    cnx.commit()

except mysql.connector.Error as err:
  if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
    print("Something is wrong with your user name or password")
  elif err.errno == errorcode.ER_BAD_DB_ERROR:
    print("Database does not exist")
  else:
    print(err)
else:
  cursor.close()
  cnx.close()