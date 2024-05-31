# utils/db_config.py

import mysql.connector

class ConfiguracionBaseDatos:
    def __init__(self):
        self.host = "127.0.0.1"
        self.port = 3306
        self.user = "root"
        self.password = "admin"
        self.database = "linea_taxi"

    def conectar(self):
        conexion = mysql.connector.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
            database=self.database
        )
        return conexion
