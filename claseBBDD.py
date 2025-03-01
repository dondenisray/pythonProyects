import mysql.connector  # Importamos el conector de MySQL

class BBDD:
    def __init__(self, user, password, host, database):
        # Inicializamos los parámetros de conexión a la base de datos
        self.user = user
        self.password = password
        self.host = host
        self.database = database

    def conectar(self):
        # Establece y devuelve una conexión a la base de datos
        # Si hay un error, devuelve None
        try:
            conn = mysql.connector.connect(
                user=self.user,
                password=self.password,
                host=self.host,
                database=self.database
            )
            return conn  # Devolvemos la conexión para usarla en otras funciones
        except mysql.connector.Error as e:
            print(f" Error al conectar a la base de datos: {e}")
            return None  # Si hay error, devolvemos None

    def createDB(self):
        # Crea la base de datos si no existe
        conn = None
        cursor = None
        try:
            # Conexión sin base de datos para poder crearla
            conn = mysql.connector.connect(
                user=self.user,
                password=self.password,
                host=self.host
            )
            cursor = conn.cursor()
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.database}")
            print(f" Base de datos '{self.database}' creada o ya existente")
        except mysql.connector.Error as e:
            print(f" Error al crear la base de datos: {e}")
        finally:
            if cursor:
                cursor.close()  # Cerramos el cursor si fue creado
            if conn:
                conn.close()  # Cerramos la conexión

    def createTable(self):
        # Crea la tabla 'temperaturas' si no existe
        conn = None
        cursor = None
        try:
            # Usamos el nuevo método conectar()
            conn = self.conectar()
            if conn is None:
                print(" Error: No se pudo establecer conexión con la base de datos.")
                return

            cursor = conn.cursor()
            query = """
            CREATE TABLE IF NOT EXISTS temperaturas (
                id INT AUTO_INCREMENT PRIMARY KEY,
                comunidad VARCHAR(100),
                max_temp INT,
                min_temp INT
            )
            """
            cursor.execute(query)
            print(" Tabla 'temperaturas' creada o ya existente")
        except mysql.connector.Error as e:
            print(f" Ha ocurrido un error al crear la tabla: {e}")
        finally:
            if cursor:
                cursor.close()  # Cerramos el cursor si fue creado
            if conn:
                conn.close()  # Cerramos la conexión

    def executeQuery(self, query: str):
        # Ejecuta una consulta SQL que no devuelve resultados (INSERT, UPDATE, DELETE)
        conn = None
        cursor = None
        try:
            conn = self.conectar()  # Ahora usamos conectar() aquí también
            if conn is None:
                print(" Error: No se pudo establecer conexión con la base de datos.")
                return

            cursor = conn.cursor()
            cursor.execute(query)
            conn.commit()  # Guardamos los cambios en la base de datos
            print(" Consulta ejecutada correctamente")
        except mysql.connector.Error as e:
            print(f" Ha ocurrido un error en la consulta: {e}")
        finally:
            if cursor:
                cursor.close()  # Cerramos el cursor si fue creado
            if conn:
                conn.close()  # Cerramos la conexión
