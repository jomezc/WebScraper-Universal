"""
Created on Fri Apr 26 19:00:24 2022
@author: Jesús Gómez Cánovas
Grado en Ingeniería Informática - Web Scraping universal con entrada - UNIR
"""

# LIB
import unittest, os, sys
from lib.WebScraperSelenium import WebScraperSelenium

def ruta_relativa(ruta_relativa):
    """
    Versión modificada basada en:  Rahimi, M. (21 de 07 de 2021). Relative path setting fail via pyinstaller.
    Obtenido de stackoverflow: https://stackoverflow.com/a/57134187
    :param ruta_relativa: ruta parcial en este caso desde .. (directorio anterior)
    :return: la ruta relativa
    """

    if hasattr(sys, "_MEIPASS"):
        path_base = sys._MEIPASS
    else:
        path_base = os.path.abspath("..")
    return os.path.join(path_base, ruta_relativa)

# CLASES


class TestWebScraperSelenium(unittest.TestCase):
    """
    ARRANGE Clase de test de cálculo que irá conteniendo las funciones de prueba de las Tareas
    """

    def setUp(self):
        """
        ARRANGE, Inicialización del objeto WebScraperSelenium y establece los valores para las pruebas que vamos a hacer
        """
        self.datos_navegacion = {'https://boe.es/', 'https://boe.es/organismo/',
                                 'https://boe.es/organismo/#presentacion_organismo', 'https://boe.es/contactar/'}
        self.fichero = 'datos.txt'
        self.datos_fichero = {
            'URL.FIRST: https://boe.es',
            'XPATH.CLICK: //*[@id="contenido"]/div[3]/div/ul[1]/li[1]/a',
            'XPATH.CLICK: //*[@id="contenido"]/div/div/ul/li[1]/a',
            'XPATH.CLICK: //*[@id="menuPie"]/div/div[1]/div[1]/a',
            'El Servicio de atención al ciudadano de la Agencia Estatal Boletín Oficial del Estado cuenta con personal especializado para resolver sus dudas y proporcionarle los documentos que necesite relacionados con la actividad, los servicios y los productos que gestiona la Agencia.'}

    def abrirFichero(self):
        try:
            with open(ruta_relativa('archivos/datos.txt'), 'r', encoding='utf8') as archivo:
                contenido_fichero = archivo.readlines()
        except Exception as e:
            print(e)
            contenido_fichero = None
        return contenido_fichero

    def testNavegacion(self):
        """
        Método de test de la tarea 1.1: Navegación por la pagina desde plantilla
        datos_navegacion: set con las páginas que debe haber visitado tras la ejecución
        """
        # ARRANGE, Inicialización del objeto WebScraperSelenium
        self.WebScraperSelenium = WebScraperSelenium()
        # ACT, invocamos al método de extracción
        self.WebScraperSelenium.extrae()
        self.resultado = WebScraperSelenium.especificacion()  # Recogemos las URL visitadas
        # ASSER, validamos los resultados
        error = f'se deberían haber visitado {self.datos_navegacion} páginas'
        self.assertEqual(len(self.resultado), len(self.datos_navegacion), error)
        for dato in self.datos_navegacion:
            error = f'La página {dato} debía haber sido visitada y no está registrada'
            self.assertEqual(dato in self.resultado, True, error)  # Compara el resultado con lo esperado (sea igual)

    def testFichero(self):
        """
        Método de test de la tarea 1.2: log de los pasos y contenido
        datos_fichero: set con los comandos que debe hacer ejecutado y el contenido
        """
        # ACT, invocamos al método de extracción
        contenido_fichero = self.abrirFichero()

        # ASSER, validamos los resultados
        error = f'fichero {self.fichero} no encontrado'
        resultado = self.fichero in os.listdir(ruta_relativa('archivos/'))
        self.assertEqual(resultado, True, error)
        # compresión de lista para comprobar si el esperado (datos_fichero)
        # está en el fichero cargado (contenido_fichero) (Delfstack, 2021)
        resultado = {dato for dato in self.datos_fichero if any(dato in linea for linea in contenido_fichero)}
        error = f"""
        No se han encontrado todos los pasos en el fichero, el contenido es
        {contenido_fichero}
        
        Se ha encontrado: {resultado}
        Esperaba: {self.datos_fichero}
        * Son conjuntos, por lo que no existe el orden ni repeticiones, lo importante es que estén todos
        """
        self.assertEqual(resultado, self.datos_fichero, error)


#   MAIN
if __name__ == '__main__':
    unittest.main()
