import os
import psycopg
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def connect_and_select_users():
    try:
        # Connect to the PostgreSQL database using context manager
        with psycopg.connect(
            host=os.getenv("DB_HOST"),
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD")
        ) as connection:
            # Create a cursor object using context manager
            with connection.cursor() as cursor:
                # Execute the SELECT query
                cursor.execute("SELECT * FROM users;")

                # Fetch all rows
                rows = cursor.fetchall()

                # Print the results
                print("All users:")
                for row in rows:
                    print(row)

    except psycopg.Error as error:
        print(f"Error while connecting to PostgreSQL or executing query: {error}")

if __name__ == "__main__":
    connect_and_select_users()