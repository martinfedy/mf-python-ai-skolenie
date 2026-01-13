import yaml
import psycopg

def load_config():
    with open('config.yaml', 'r') as file:
        return yaml.safe_load(file)

def connect_and_select_users():
    config = load_config()
    db_config = config['database']

    try:
        # Connect to the PostgreSQL database using context manager
        with psycopg.connect(
            host=db_config['host'],
            dbname=db_config['name'],
            user=db_config['user'],
            password=db_config['password']
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