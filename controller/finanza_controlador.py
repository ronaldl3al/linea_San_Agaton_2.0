from model.modelo_finanza import ModeloFinanza

class FinanzaControlador:
    def __init__(self):
        self.modelo_finanza = ModeloFinanza()

    def obtener_todas_finanzas(self):
        return self.modelo_finanza.obtener_todas_finanzas()

    def insertar_finanza(self, cedula, pagos_mensuales, impuestos_anuales, fecha_pago):
        self.modelo_finanza.insertar_finanza(cedula, pagos_mensuales, impuestos_anuales, fecha_pago)

    def actualizar_finanza(self, ID_finanza, cedula, pagos_mensuales, impuestos_anuales, fecha_pago):
        self.modelo_finanza.actualizar_finanza(ID_finanza, cedula, pagos_mensuales, impuestos_anuales, fecha_pago)

    def eliminar_finanza(self, ID_finanza):
        self.modelo_finanza.eliminar_finanza(ID_finanza)
