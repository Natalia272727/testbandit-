
from Funciones import *

usuario_actual = None

while True:
    print("\n--- Sistema de Gestión de Fichas Médicas ---")
    print("1. Crear usuario")
    print("2. Login")
    print("3. Registrar paciente")
    print("4. Buscar paciente")
    print("5. Modificar paciente")
    print("6. Eliminar paciente")
    print("7. Mostrar todos los pacientes")
    print("8. Generar hash")
    print("9. Calcular fórmula")
    print("10. Exportar reporte")
    print("11. Respaldar sistema")
    print("12. Leer archivo")
    print("13. Salir")

    opcion = input("Seleccione una opción: ")

    if opcion == "1":
        crear_usuario()
    elif opcion == "2":
        usuario_actual = login()
    elif opcion == "3":
        registrar_paciente()
    elif opcion == "4":
        buscar_paciente()
    elif opcion == "5":
        modificar_paciente()
    elif opcion == "6":
        eliminar_paciente()
    elif opcion == "7":
        mostrar_todos_los_pacientes()
    elif opcion == "8":
        generar_hash_seguro()
    elif opcion == "9":
        calcular_formula()
    elif opcion == "10":
        exportar_reporte()
    elif opcion == "11":
        respaldar_sistema()
    elif opcion == "12":
        leer_archivo()
    elif opcion == "13":
        break
    else:
        print("Opción inválida")
