# modelos/modelo_sancion.py
from fpdf import FPDF
from utils.db_config import ConfiguracionBaseDeDatos

class ModeloSancion:
    def __init__(self):
        self.configuracion_bd = ConfiguracionBaseDeDatos()
    
    def obtener_todas_sanciones(self):
        conexion = self.configuracion_bd.conectar()
        cursor = conexion.cursor(dictionary=True)
        query = "SELECT * FROM sanciones ORDER BY final_sancion ASC"
        cursor.execute(query)
        sanciones = cursor.fetchall()
        cursor.close()
        conexion.close()
        return sanciones

    def insertar_sancion(self, cedula, motivo_sancion, monto, inicio_sancion, final_sancion, nombre, apellido):
        conexion = self.configuracion_bd.conectar()
        cursor = conexion.cursor()
        query = """
        INSERT INTO sanciones (cedula, motivo_sancion, monto, inicio_sancion, final_sancion, nombre, apellido)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (cedula, motivo_sancion, monto, inicio_sancion, final_sancion, nombre, apellido))
        conexion.commit()
        cursor.close()
        conexion.close()

    def actualizar_sancion(self, ID_sancion, cedula, motivo_sancion, monto, inicio_sancion, final_sancion, nombre, apellido):
        conexion = self.configuracion_bd.conectar()
        cursor = conexion.cursor()
        query = """
        UPDATE sanciones 
        SET cedula = %s, motivo_sancion = %s, monto = %s, inicio_sancion = %s, final_sancion = %s, nombre = %s, apellido = %s
        WHERE ID_sancion = %s
        """
        cursor.execute(query, (cedula, motivo_sancion, monto, inicio_sancion, final_sancion, nombre, apellido, ID_sancion))
        conexion.commit()
        cursor.close()
        conexion.close()

    def eliminar_sancion(self, ID_sancion):
        conexion = self.configuracion_bd.conectar()
        cursor = conexion.cursor()
        query = "DELETE FROM sanciones WHERE ID_sancion = %s"
        cursor.execute(query, (ID_sancion,))
        conexion.commit()
        cursor.close()
        conexion.close()

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Tabla de Datos de Sanciones', 0, 1, 'C')

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Página {self.page_no()}', 0, 0, 'C')

    def celda_multiple(self, w, h, text, border=0, ln=0, align='', fill=False):
        lines = self.multi_cell(w, h, text, border=0, ln=0, align='', fill=False, split_only=True)
        for line in lines:
            self.cell(w, h, line, border=border, ln=2, align=align, fill=fill)
            border = 0
        if ln > 0:
            self.ln(h)