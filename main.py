import utils.transport
import utils.session
from database.connection import get_connection


conn = get_connection()

if conn.is_connected():
    print("Connected successfully to DATA_ENG_PROJ")

conn.close()