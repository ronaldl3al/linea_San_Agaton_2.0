# modelos/modelo_socio.py
from fpdf import FPDF
from utils.db_config import ConfiguracionBaseDeDatos

#region ModeloSocio Class
# Modelo de datos para los socios
class ModeloSocio:
    def __init__(self):
        # Inicializa la configuración de la base de datos
        self.configuracion_bd = ConfiguracionBaseDeDatos()
    
    # Metodo para obtener todos los socios
    def obtener_todos_socios(self):
        conexion = self.configuracion_bd.conectar()  # Conectar a la base de datos
        cursor = conexion.cursor(dictionary=True)
        query = "SELECT * FROM socio ORDER BY numero_control ASC"
        cursor.execute(query)
        socios = cursor.fetchall()  # Obtener todos los registros
        cursor.close()
        conexion.close()
        return socios

    # Metodo para insertar un nuevo socio
    def insertar_socio(self, cedula, nombres, apellidos, direccion, numero_telefono, numero_control, rif, fecha_nacimiento):
        conexion = self.configuracion_bd.conectar()  # Conectar a la base de datos
        cursor = conexion.cursor()
        query = """
        INSERT INTO socio (cedula, nombres, apellidos, direccion, numero_telefono, numero_control, rif, fecha_nacimiento)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
        cursor.execute(query, (cedula, nombres, apellidos, direccion, numero_telefono, numero_control, rif, fecha_nacimiento))
        conexion.commit()  # Confirmar la transacción
        cursor.close()
        conexion.close()

    # Metodo para actualizar un socio existente
    def actualizar_socio(self, cedula, nombres, apellidos, direccion, numero_telefono, numero_control, rif, fecha_nacimiento):
        conexion = self.configuracion_bd.conectar()  # Conectar a la base de datos
        cursor = conexion.cursor()
        query = """
        UPDATE socio 
        SET nombres = %s, apellidos = %s, direccion = %s, 
            numero_telefono = %s, numero_control = %s, rif = %s, fecha_nacimiento = %s
        WHERE cedula = %s
        """
        cursor.execute(query, (nombres, apellidos, direccion, numero_telefono, numero_control, rif, fecha_nacimiento, cedula))
        conexion.commit()  # Confirmar la transacción
        cursor.close()
        conexion.close()

    # Metodo para eliminar un socio
    def eliminar_socio(self, cedula):
        conexion = self.configuracion_bd.conectar()  # Conectar a la base de datos
        cursor = conexion.cursor()
        query = "DELETE FROM socio WHERE cedula = %s"
        cursor.execute(query, (cedula,))
        conexion.commit()  # Confirmar la transacción
        cursor.close()
        conexion.close()


#region PDF 

# generación de PDF
class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Tabla de Datos de Socios', 0, 1, 'C')

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
