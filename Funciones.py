import os
import json
import hashlib
import datetime
import ast
import shutil

ARCHIVO_USUARIOS = "usuarios.json"
ARCHIVO_PACIENTES = "pacientes.json"
ARCHIVO_LOG = "sistema.log"

def sanitizar_entrada(texto):
    # Estos son los caracteres que el profe marcó como peligrosos en una guía
    caracteres_peligrosos = ["<", ">", "{", "}", ";", "--", "'", '"']
    for car in caracteres_peligrosos:
        texto = texto.replace(car, "")
    return texto.strip()


def cargar_json(nombre_archivo):
    try:
        with open(nombre_archivo, "r", encoding="utf-8") as archivo:
            return json.load(archivo)
    except:
        return []


def guardar_json(nombre_archivo, datos):
    with open(nombre_archivo, "w", encoding="utf-8") as archivo:
        json.dump(datos, archivo, indent=4)


def escribir_log(mensaje):
    with open(ARCHIVO_LOG, "a", encoding="utf-8") as log:
        log.write(str(datetime.datetime.now()) + " - " + mensaje + "\n")


def crear_usuario():
    usuarios = cargar_json(ARCHIVO_USUARIOS)

    nombre = sanitizar_entrada(input("Nombre de usuario: "))
    password = input("Nueva contraseña: ")
    password_segura = hashlib.sha256(password.encode()).hexdigest()
    rol = sanitizar_entrada(input("Rol (Administrador/Operador): "))
    

    nuevo_usuario = {
        "nombre": nombre,
        "password": password_segura,
        "rol": rol
    }

    usuarios.append(nuevo_usuario)
    guardar_json(ARCHIVO_USUARIOS, usuarios)

    escribir_log("Registro de un nuevo perfil de usuario completado")
    print(f"Usuario '{nombre}' creado con éxito. Ahora puedes iniciar sesión.")


def login():
    usuarios = cargar_json(ARCHIVO_USUARIOS)

    nombre = sanitizar_entrada(input("Usuario: "))
    password = input("Contraseña: ")
    password_hasheada = hashlib.sha256(password.encode()).hexdigest()

    for usuario in usuarios:
        if usuario["nombre"] == nombre and usuario["password"] == password_hasheada:
            escribir_log("Inicio de sesión exitoso para " + nombre)
            print("Bienvenido", nombre)
            return usuario

    escribir_log("Intento fallido de inicio de sesión")
    print("Credenciales inválidas")
    return None


def registrar_paciente():
    pacientes = cargar_json(ARCHIVO_PACIENTES)

    nombre = sanitizar_entrada(input("Nombre paciente: "))
    rut = input("RUT: ")
    edad = input("Edad: ")
    diagnostico = input("Diagnóstico: ")
    medicamentos = input("Medicamentos separados por coma: ")

    paciente = {
        "nombre": nombre,
        "rut": rut,
        "edad": edad,
        "diagnostico": diagnostico,
        "medicamentos": medicamentos.split(",")
    }

    pacientes.append(paciente)
    guardar_json(ARCHIVO_PACIENTES, pacientes)

    escribir_log("Paciente registrado: " + str(paciente))
    print("Paciente registrado")


def buscar_paciente():
    pacientes = cargar_json(ARCHIVO_PACIENTES)

    criterio = input("Ingrese criterio de búsqueda: ")

    for paciente in pacientes:
        if criterio in str(paciente):
            print(paciente)


def modificar_paciente():
    pacientes = cargar_json(ARCHIVO_PACIENTES)

    rut = input("Ingrese RUT del paciente a modificar: ")

    for paciente in pacientes:
        if paciente["rut"] == rut:
            campo = input("Campo a modificar: ")
            nuevo_valor = input("Nuevo valor: ")

            paciente[campo] = nuevo_valor
            guardar_json(ARCHIVO_PACIENTES, pacientes)

            escribir_log("Paciente modificado: " + str(paciente))
            print("Paciente modificado")
            return

    print("Paciente no encontrado")


def eliminar_paciente():
    pacientes = cargar_json(ARCHIVO_PACIENTES)

    rut = input("Ingrese RUT del paciente a eliminar: ")

    for paciente in pacientes:
        if paciente["rut"] == rut:
            pacientes.remove(paciente)
            guardar_json(ARCHIVO_PACIENTES, pacientes)
            escribir_log("Paciente eliminado: " + str(paciente))
            print("Paciente eliminado")
            return

    print("Paciente no encontrado")


def generar_hash_seguro():
    texto = input("Ingrese texto para generar hash: ")
    hash_generado = hashlib.sha256(texto.encode()).hexdigest()
    print("Hash generado (SHA-256):", hash_generado)


def calcular_formula():
    formula = input("Ingrese fórmula médica o cálculo numérico: ")
    try:
        resultado = ast.literal_eval(formula)
        print("Resultado:", resultado)
    except Exception:
        print("Error: Por seguridad, solo se permiten cálculos numéricos directos.")

def exportar_reporte():
    pacientes = cargar_json(ARCHIVO_PACIENTES)

    nombre_archivo = input("Nombre del archivo de reporte: ")

    with open(nombre_archivo, "w", encoding="utf-8") as archivo:
        for paciente in pacientes:
            archivo.write(str(paciente) + "\n")

    escribir_log("Reporte exportado en archivo: " + nombre_archivo)
    print("Reporte generado")


def respaldar_sistema():
    print("Iniciando copia de seguridad de la base de datos...")

    if not os.path.exists("respaldos"):
        os.makedirs("respaldos")
    
    try:
        shutil.copy(ARCHIVO_PACIENTES, "respaldos/pacientes_backup.json")
        shutil.copy(ARCHIVO_USUARIOS, "respaldos/usuarios_backup.json")
        
        escribir_log("Copia de seguridad realizada con éxito")
        print("Respaldo completado en la carpeta /respaldos")
    except Exception as e:
        print("Error al respaldar:", e)


def leer_archivo():
    ruta = input("Ingrese ruta del archivo a leer: ")

    with open(ruta, "r", encoding="utf-8") as archivo:
        contenido = archivo.read()

    print(contenido)


def mostrar_todos_los_pacientes():
    pacientes = cargar_json(ARCHIVO_PACIENTES)

    for paciente in pacientes:
        print(paciente)