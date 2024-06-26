# modelos/modelo_avance.py
from fpdf import FPDF
from utils.db_config import ConfiguracionBaseDeDatos

class ModeloAvance:
    def __init__(self):
        self.configuracion_bd = ConfiguracionBaseDeDatos()
    
    def obtener_todos_avances(self):
        conexion = self.configuracion_bd.conectar()
        cursor = conexion.cursor(dictionary=True)
        query = "SELECT * FROM avances ORDER BY numero_control ASC"
        cursor.execute(query)
        avances = cursor.fetchall()
        cursor.close()
        conexion.close()
        return avances

    def insertar_avance(self, numero_control, nombre, apellido, fecha_nacimiento, rif, cedula_avance, numero_telf):
        conexion = self.configuracion_bd.conectar()
        cursor = conexion.cursor()
        query = """
        INSERT INTO avances (numero_control, nombre, apellido, fecha_nacimiento, rif, cedula_avance, numero_telf)
        VALUES (%s, %s, %s, %s, %s, %s, %s)"""
        cursor.execute(query, (numero_control, nombre, apellido, fecha_nacimiento, rif, cedula_avance, numero_telf))
        conexion.commit()
        cursor.close()
        conexion.close()

    def actualizar_avance(self, ID_avance, numero_control, nombre, apellido, fecha_nacimiento, rif, cedula_avance, numero_telf):
        conexion = self.configuracion_bd.conectar()
        cursor = conexion.cursor()
        query = """
        UPDATE avances 
        SET numero_control = %s, nombre = %s, apellido = %s, fecha_nacimiento = %s, rif = %s, cedula_avance = %s, numero_telf = %s
        WHERE ID_avance = %s
        """
        cursor.execute(query, (numero_control, nombre, apellido, fecha_nacimiento, rif, cedula_avance, numero_telf, ID_avance))
        conexion.commit()
        cursor.close()
        conexion.close()

    def eliminar_avance(self, ID_avance):
        conexion = self.configuracion_bd.conectar()
        cursor = conexion.cursor()
        query = "DELETE FROM avances WHERE ID_avance = %s"
        cursor.execute(query, (ID_avance,))
        conexion.commit()
        cursor.close()
        conexion.close()

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Tabla de Datos de Avances', 0, 1, 'C')

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