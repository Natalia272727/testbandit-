archivo = input("Ingrese nombre del archivo: ")
file = open(archivo, "r")
lineas = file.readlines()
total = 0
for linea in lineas[1:]:
 datos = linea.split(",")
 monto = float(datos[2])
 total += monto
print("Balance total:", total)

