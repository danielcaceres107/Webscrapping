## Daniel, Daira y Cristian

from conexion import laConexion

def ver_tablas():
    conexion = laConexion()

    if conexion is None:
        print("No se pudo conectar a MySQL")
        return

    cursor = conexion.cursor()

    # query para extraer 1
    cursor.execute("""


select * from pisos;"""
                   )
    tablas = cursor.fetchall()

    for t in tablas:
        print(t)
    ## fin --

        # query para extraer 2
    # cursor.execute("""
    #     select a.nombre_autor, l.titulo, c.calificacion, c.total_libros_vendidos FROM autor a
    #                INNER JOIN libros l ON a.id = l.autor_id
    #                INNER JOIN calificacion c ON l.id = c.libro_id 
    #                ;"""
    #                )
    # tablas = cursor.fetchall()

    # for t in tablas:
    #     print(t)
    ## fin --

    ## query para hacer
    # cursor.execute("""
    #     DROP TABLE autor
    #         ;"""
    # )
    
    # conexion.commit()
    ## fin --

    cursor.close()
    conexion.close()


if __name__ == "__main__":
    ver_tablas()
