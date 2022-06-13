"""
Created on Fri Apr 26 19:00:24 2022
@author: Jesús Gómez Cánovas
Grado en Ingeniería Informática - Web Scraping universal con entrada - UNIR
"""

# LIB
import unittest
from lib.WebScraperSelenium import WebScraperSelenium

# CLASES


class TestWebScraperSelenium(unittest.TestCase):
    """
    Clase de test de cálculo que irá conteniendo las funciones de prueba de las Tareas
    """

    def setUp(self):
        """
        ARRANGE, Inicialización del objeto WebScraperSelenium y establece los valores para las pruebas que vamos a hacer
        """
        self.WebScraperSelenium = WebScraperSelenium()
        self.datos_navegacion = {'https://boe.es', 'https://boe.es/organismo/',
                                 'https://boe.es/organismo/#presentacion_organismo', 'https://boe.es/contactar/'}

    def testNavegacion(self):
        """
        Método de test de la tarea 1.1 : Navegación por la pagina desde plantilla
        datos_navegacion: set con las páginas que debe haber visitado tras la ejecución
        """
        # ACT, invocamos al método de extracción
        self.WebScraperSelenium.extrae()
        resultado = WebScraperSelenium.especificacion()  # Recogemos las URL visitadas
        # ASSER, validamos los resultados
        error = f'se deberían haber visitado {self.datos_navegacion} páginas'
        self.assertEqual(len(resultado), len(self.datos_navegacion), error)
        for dato in self.datos_navegacion:
            error = f'La página {dato} debía haber sido visitada y no está registrada'
            self.assertEqual(dato in resultado, True, error)  # Compara el resultado con lo esperado (sea igual)


#   MAIN
if __name__ == '__main__':
    unittest.main()
