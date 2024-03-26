import psycopg2

# Connect to the database
connection = psycopg2.connect(
    user="postgres",
    password="123456",
    host="localhost",
    port="5432",
    database="chatbot_business_manage"
)
cursor = connection.cursor()