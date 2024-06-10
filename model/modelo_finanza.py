# modelos/modelo_finanza.py

from utils.db_config import ConfiguracionBaseDeDatos

class ModeloFinanza:
    def __init__(self):
        self.configuracion_bd = ConfiguracionBaseDeDatos()
    
    def obtener_todas_finanzas(self):
        conexion = self.configuracion_bd.conectar()
        cursor = conexion.cursor(dictionary=True)
        query = "SELECT * FROM finanzas ORDER BY ID_finanzas ASC"
        cursor.execute(query)
        finanzas = cursor.fetchall()
        cursor.close()
        conexion.close()
        return finanzas

    def insertar_finanza(self, cedula, pagos_mensuales, impuestos_anuales, fecha_pago, numero_contr):
        conexion = self.configuracion_bd.conectar()
        cursor = conexion.cursor()
        query = """
        INSERT INTO finanzas (cedula, pagos_mensuales, impuestos_anuales, fecha_pago, numero_contr)
        VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(query, (cedula, pagos_mensuales, impuestos_anuales, fecha_pago, numero_contr))
        conexion.commit()
        cursor.close()
        conexion.close()

    def actualizar_finanza(self, ID_finanzas, cedula, pagos_mensuales, impuestos_anuales, fecha_pago, numero_contr):
        conexion = self.configuracion_bd.conectar()
        cursor = conexion.cursor()
        query = """
        UPDATE finanzas 
        SET cedula = %s, pagos_mensuales = %s, impuestos_anuales = %s, fecha_pago = %s, numero_contr = %s
        WHERE ID_finanzas = %s
        """
        cursor.execute(query, (cedula, pagos_mensuales, impuestos_anuales, fecha_pago, numero_contr, ID_finanzas))
        conexion.commit()
        cursor.close()
        conexion.close()

    def eliminar_finanza(self, ID_finanzas):
        conexion = self.configuracion_bd.conectar()
        cursor = conexion.cursor()
        query = "DELETE FROM finanzas WHERE ID_finanzas = %s"
        cursor.execute(query, (ID_finanzas,))
        conexion.commit()
        cursor.close()
        conexion.close()
