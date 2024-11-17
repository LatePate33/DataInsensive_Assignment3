import psycopg2

def main():
    userInput = -1
    database = None
    while(userInput != "0"):
        print("1 Choose database")
        print("2 Print tables")
        print("0 Terminate")
        userInput = input("What do you want to do? ")
        if userInput == "1":
            database = choose_database()
        if userInput == "2":
            if database:
                print_tables(database)
            else:
                print("Choose db first")
        if userInput == "0":
            print("Ending software...")
        else:
            pass
    return 

def choose_database():
    print("Available databases:")
    print("1. Sales")
    print("2. Inventory")
    print("3. Support")
    database_choice = input("Choose a database (1/2/3): ")

    if database_choice == "1":
        return connect_to_database("DataIntensiv_DB1") #Sales
    elif database_choice == "2":
        return connect_to_database("DataIntensiv_DB2") #Inventory
    elif database_choice == "3":
        return connect_to_database("DataIntensiv_DB3") #Support
    else:
        print("Invalid choice. Returning to main menu.")
        return None

def connect_to_database(db_name):
    try:
        connection = psycopg2.connect(
            database=db_name,
            user="postgres",
            password="",
            host="localhost",
            port="5432"
        )
        print(f"Connected")
        return connection
    except Exception as e:
        print(f"Error connecting to database {db_name}: {e}")
        return None
    
def print_tables(database):
    try:
        cursor = database.cursor()

        # Fetch all table names
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public';
        """)
        tables = cursor.fetchall()

        if not tables:
            print("\nNo tables found")
            return

        print("\nTables and their entities in the database:")
        for table in tables:
            table_name = table[0]
            print(f"\nTable: {table_name}")

            cursor.execute(f"SELECT * FROM {table_name}")
            rows = cursor.fetchall()

            # Fetch column names
            cursor.execute(f"""
                SELECT column_name
                FROM information_schema.columns
                WHERE table_name = '{table_name}';
            """)
            columns = [col[0] for col in cursor.fetchall()]

            print(f"Columns: {', '.join(columns)}")

            if rows:
                for row in rows:
                    print(row)
            else:
                print("No entities found in this table")
    except Exception as e:
        print(f"Error fetching tables: {e}")
    finally:
        database.close()
        print("Connection closed")

main()