import requests
from .db_config import cursor, connection

def get_categories(categories):
    formatted_categories = ', '.join(f"'{category}'" for category in categories)
    if formatted_categories == "":
        return []
    query = f"SELECT * FROM category WHERE category_name IN ({formatted_categories})"
    cursor.execute(query)
    result = cursor.fetchall()
    return result


def insert_data(data, table_name):
    # Create a cursor object
    cur = connection.cursor()

    # Construct the INSERT query with placeholders for values
    columns = ", ".join(data.keys())
    values = ", ".join(["%s"] * len(data))
    query = f"INSERT INTO {table_name} ({columns}) VALUES ({values})"

    # Execute the query with the data values
    cur.execute(query, tuple(data.values()))

    # Commit the changes to the database
    connection.commit()

    # Close the cursor
    cur.close()


# Get api
def get_api(url_link):
    response = requests.get(url=url_link)
    return response.json()