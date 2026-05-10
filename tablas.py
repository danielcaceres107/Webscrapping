"""
Tablas.py

Crea la tabla `pisos` en MySQL y carga la información generada
por el script principal desde `pisos.json`.
"""

import json

from conexion import laConexion


# ---------------------------------------------------------------------------
# Crear tabla
# ---------------------------------------------------------------------------

def crear_tabla(cursor):
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pisos (
            id INT AUTO_INCREMENT PRIMARY KEY,
            precio VARCHAR(50) NOT NULL,
            precio_usd DECIMAL(12, 2) NULL,
            descripcion VARCHAR(500) NOT NULL,
            pagina INT NOT NULL,
            fecha DATETIME DEFAULT CURRENT_TIMESTAMP
        ) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
    """)


def asegurar_columna_precio_usd(cursor):
    cursor.execute("SHOW COLUMNS FROM pisos LIKE 'precio_usd'")

    if cursor.fetchone() is None:
        cursor.execute("""
            ALTER TABLE pisos
            ADD COLUMN precio_usd DECIMAL(12, 2) NULL AFTER precio
        """)


# ---------------------------------------------------------------------------
# Insertar datos
# ---------------------------------------------------------------------------

def insertar_datos(cursor, datos):

    sql = """
        INSERT INTO pisos (precio, precio_usd, descripcion, pagina)
        VALUES (%s, %s, %s, %s)
    """

    for piso in datos:

        cursor.execute(
            sql,
            (
                piso["precio"],
                piso.get("precio_usd"),
                piso["descripcion"],
                piso["pagina"]
            )
        )


# ---------------------------------------------------------------------------
# Programa principal
# ---------------------------------------------------------------------------

def main():

    # Conexión
    conexion = laConexion()

    if conexion is None:
        print("❌ No se pudo conectar a MySQL")
        return

    cursor = conexion.cursor()

    # Crear tabla
    crear_tabla(cursor)
    asegurar_columna_precio_usd(cursor)

    # Leer JSON generado por el scraping
    with open("pisos.json", "r", encoding="utf-8") as f:
        datos = json.load(f)

    # Insertar datos
    insertar_datos(cursor, datos)

    # Guardar cambios
    conexion.commit()

    print(f"✅ {len(datos)} registros insertados correctamente")

    # Cerrar conexión
    cursor.close()
    conexion.close()


if __name__ == "__main__":
    main()
