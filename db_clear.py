import psycopg2

def clear_database():
    connection = None
    try:
        connection = psycopg2.connect(
            database="photon",
            user="student",
            password="student",
            host="127.0.0.1",
            port="5432"
        )
        pointer = connection.cursor()
        
        pointer.execute("DELETE FROM players")
        
        connection.commit()
        
        pointer.execute("SELECT COUNT(*) FROM players")
        count = pointer.fetchone()[0]
        
        print(f"Database cleared successfully!")
        print(f"Current number of players in database: {count}")
        
    except Exception as e:
        print(f"Error while clearing database: {e}")
        if connection:
            connection.rollback()
    finally:
        if connection:
            pointer.close()
            connection.close()
            

if __name__ == "__main__":
    clear_database()
