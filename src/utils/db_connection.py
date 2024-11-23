import psycopg2
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

# Database configuration
DB_CONFIG = {
    "host": "orbitaldev.ch00sm2gcxj9.eu-west-2.rds.amazonaws.com",
    "dbname": "postgres",
    "user": "admin_dev",  # Replace with your actual username
    "password": "o4rb4[tial23",  # Replace with your actual password
    "port": "5432",
}


def connect_to_postgres():
    """
    Establish connection to desired database
    """
    try:
        connection = psycopg2.connect(**DB_CONFIG)
        logging.info("Connected to the database successfully.")
        return connection
    except psycopg2.OperationalError as e:
        logging.error(f"Operational error connecting to the database: {e}")
    except psycopg2.Error as e:
        logging.error(f"Database error: {e}")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
    return None


def execute_query(connection, query, fetch_results=False):
    """
    Execute a query and optionally fetch results
    """
    if connection is None:
        logging.warning("No valid database connection.")
        return None

    try:
        with connection.cursor() as cursor:
            cursor.execute(query)

            results = None
            if fetch_results:
                results = cursor.fetchall()

            connection.commit()
            logging.info("Query executed successfully.")
            return results
    except psycopg2.ProgrammingError as e:
        logging.error(f"Programming error: {e}")
    except psycopg2.Error as e:
        logging.error(f"Database error: {e}")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
    return None


def close_connection(connection):
    """
    Close the database connection
    """
    if connection is not None:
        try:
            connection.close()
            logging.info("Connection closed.")
        except psycopg2.Error as e:
            logging.error(f"Error closing connection: {e}")
        except Exception as e:
            logging.error(f"Unexpected error: {e}")
    else:
        logging.warning("Connection is already closed or was never established.")
