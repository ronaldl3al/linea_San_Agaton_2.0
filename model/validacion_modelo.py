import re

class Validations:

    @staticmethod
    def validar_fecha(date_str):
        date_pattern = re.compile(r'\d{4}/\d{2}/\d{2}')
        if not date_pattern.match(date_str):
            return "AAAA/MM/DD"
        return None
    

    @staticmethod
    def validar_cedula(cedula):
        cedula_pattern = re.compile(r'^[VE]-\d{7,9}$')
        if not cedula_pattern.match(cedula):
            return "La cédula debe tener el formato V-12345678/E-12345678"
        return None
    

    @staticmethod
    def validar_rif(rif):
        rif_pattern = re.compile(r'^[VEJGPCA][A-Za-z0-9]{7,12}$')
        if not rif_pattern.match(rif):
            return "Rif incorrecto"
        return None
    
    @staticmethod
    def validar_nombre_apellido(nombre_apellido):
        nombre_apellido_pattern = re.compile(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ ]+$')
        if not nombre_apellido_pattern.match(nombre_apellido):
            return "El nombre o apellido solo puede contener letras y espacios"
        return None