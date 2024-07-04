import pyodbc

server = 'nttltdddpedw1.azuresynapse.net'
database = 'BDM'
username = ''
password = ''
driver = '{ODBC Driver 17 for SQL Server}'


connection_string = f'SERVER={server};DATABASE={database};UID={username};PWD={password};DRIVER={driver}'

try:

    conn = pyodbc.connect(connection_string)
    cursor = conn.cursor()


    cursor.execute("SELECT 'Conexión exitosa' AS Resultado")
    row = cursor.fetchone()


    print(row.Resultado)


    conn.close()

except pyodbc.Error as e:
    print(f"Error de conexión: {str(e)}")

