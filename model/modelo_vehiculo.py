# modelos/modelo_vehiculo.py
from fpdf import FPDF
from utils.db_config import ConfiguracionBaseDeDatos

class ModeloVehiculo:
    def __init__(self):
        self.configuracion_bd = ConfiguracionBaseDeDatos()
    
    def obtener_todos_vehiculos(self):
        conexion = self.configuracion_bd.conectar()
        cursor = conexion.cursor(dictionary=True)
        query = "SELECT * FROM vehiculos ORDER BY numero_control ASC"
        cursor.execute(query)
        vehiculos = cursor.fetchall()
        cursor.close()
        conexion.close()
        return vehiculos

    def insertar_vehiculo(self, cedula, numero_control, marca, modelo, ano, placa):
        conexion = self.configuracion_bd.conectar()
        cursor = conexion.cursor()
        query = """
        INSERT INTO vehiculos (cedula, numero_control, marca, modelo, ano, placa)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (cedula, numero_control, marca, modelo, ano, placa))
        conexion.commit()
        cursor.close()
        conexion.close()

    def actualizar_vehiculo(self, id_vehiculo, cedula, numero_control, marca, modelo, ano, placa):
        conexion = self.configuracion_bd.conectar()
        cursor = conexion.cursor()
        query = """
        UPDATE vehiculos 
        SET cedula = %s, numero_control = %s, marca = %s, modelo = %s, ano = %s, placa = %s
        WHERE id_vehiculo = %s
        """
        cursor.execute(query, (cedula, numero_control, marca, modelo, ano, placa, id_vehiculo))
        conexion.commit()
        cursor.close()
        conexion.close()

    def eliminar_vehiculo(self, id_vehiculo):
        conexion = self.configuracion_bd.conectar()
        cursor = conexion.cursor()
        query = "DELETE FROM vehiculos WHERE id_vehiculo = %s"
        cursor.execute(query, (id_vehiculo,))
        conexion.commit()
        cursor.close()
        conexion.close()

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Tabla de Datos de Vehículos', 0, 1, 'C')

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