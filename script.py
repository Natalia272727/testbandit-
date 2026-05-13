archivo = input("Ingrese nombre del archivo: ")
file = open(archivo, "r")
lineas = file.readlines()
total = 0
for linea in lineas[1:]:
 datos = linea.split(",")
 monto = float(datos[2])
 total += monto
print("Balance total:", total)

import pandas as pd
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Umbral configurable para detectar transacciones sospechosas
UMBRAL_SOSPECHA = float(os.getenv("UMBRAL_SOSPECHA", "1000000"))


def cargar_archivo(ruta: str) -> pd.DataFrame:
    if not ruta or not isinstance(ruta, str):
        raise ValueError("Ruta inválida")

    if not os.path.exists(ruta):
        raise FileNotFoundError("El archivo no existe")

    if not ruta.endswith(".csv"):
        raise ValueError("El archivo debe ser CSV")

    try:
        df = pd.read_csv(ruta)
    except pd.errors.EmptyDataError:
        raise ValueError("El archivo está vacío")
    except pd.errors.ParserError:
        raise ValueError("Error en el formato del CSV")
    except Exception as e:
        raise RuntimeError(f"Error inesperado al leer el archivo: {e}")

    return df


def validar_datos(df: pd.DataFrame) -> None:
    columnas_esperadas = {"fecha", "descripcion", "monto"}

    if not columnas_esperadas.issubset(df.columns):
        raise ValueError("El archivo no tiene las columnas requeridas")

    # Validar tipos
    try:
        df["monto"] = pd.to_numeric(df["monto"], errors="raise")
    except Exception:
        raise ValueError("La columna 'monto' contiene valores inválidos")

    # Validar nulos
    if df.isnull().any().any():
        raise ValueError("El archivo contiene valores nulos")

    # Validar fechas
    try:
        df["fecha"] = pd.to_datetime(df["fecha"], errors="raise")
    except Exception:
        raise ValueError("Formato de fecha inválido")


def calcular_balance(df: pd.DataFrame) -> float:
    return df["monto"].sum()


def detectar_sospechosas(df: pd.DataFrame) -> pd.DataFrame:
    return df[df["monto"].abs() > UMBRAL_SOSPECHA]


def exportar_reporte(df: pd.DataFrame, nombre_archivo: str) -> None:
    try:
        df.to_csv(nombre_archivo, index=False)
    except Exception as e:
        raise RuntimeError(f"No se pudo exportar el reporte: {e}")


def main():
    archivo = input("Ingrese nombre del archivo: ").strip()

    try:
        df = cargar_archivo(archivo)
        validar_datos(df)

        total = calcular_balance(df)
        print(f"Balance total: {total}")

        sospechosas = detectar_sospechosas(df)

        if not sospechosas.empty:
            print("\n⚠ Transacciones sospechosas detectadas:")
            print(sospechosas)

            exportar_reporte(sospechosas, "reporte_sospechosas.csv")
            print("\nReporte exportado: reporte_sospechosas.csv")
        else:
            print("\nNo se detectaron transacciones sospechosas")

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()

    