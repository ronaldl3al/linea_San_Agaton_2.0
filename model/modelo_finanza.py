# modelos/modelo_finanza.py
from fpdf import FPDF
from utils.db_config import ConfiguracionBaseDeDatos

class ModeloFinanza:
    def __init__(self):
        self.configuracion_bd = ConfiguracionBaseDeDatos()
    
    def obtener_todas_finanzas(self):
        conexion = self.configuracion_bd.conectar()
        cursor = conexion.cursor(dictionary=True)
        query = "SELECT * FROM finanzas ORDER BY numero_contr ASC"
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



class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Tabla de Datos de Finanzas', 0, 1, 'C')

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