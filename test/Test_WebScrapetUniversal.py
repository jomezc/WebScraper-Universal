"""
Created on Fri Apr 26 19:00:24 2022
@author: Jesús Gómez Cánovas
Grado en Ingeniería Informática - Web Scraping universal con entrada - UNIR
"""

# LIB
import unittest, os, sys, time, imaplib, email
from lib.GestorScraper import GestorScraper
from FuncionesPropias import *


class TestWebScraperSelenium(unittest.TestCase):
    """
    ARRANGE Clase de test de cálculo que irá conteniendo las funciones de prueba de las Tareas
    """

    def setUp(self):
        """
        ARRANGE, Inicialización del objeto scraper y establece los valores para las pruebas que vamos a hacer
        """
        self.gestor = GestorScraper()
        self.datos_navegacion = {'https://boe.es/', 'https://boe.es/organismo/',
                                 'https://boe.es/organismo/#presentacion_organismo', 'https://boe.es/contactar/','https://boe.es/buscar/','https://boe.es/buscar/doc.php?id=BOE-A-1978-31229','https://boe.es/buscar/legislacion.php?campo%5B2%5D=tit&dato%5B2%5D=Constituci%C3%B3n%20Espa%C3%B1ola&accion=Buscar&checkbox_solo_tit=S&sort_field%5B0%5D=PESO&sort_order%5B0%5D=desc'}
        self.fichero = 'datos.txt'
        self.datos_fichero = {
            'URL.FIRST: https://boe.es',
            'XPATH.CLICK: //*[@id="contenido"]/div[3]/div/ul[1]/li[1]/a',
            'XPATH.CLICK: //*[@id="contenido"]/div/div/ul/li[1]/a',
            'XPATH.CLICK: //*[@id="menuPie"]/div/div[1]/div[1]/a',
            'El Servicio de atención al ciudadano de la Agencia Estatal Boletín Oficial del Estado cuenta con personal especializado para resolver sus dudas y proporcionarle los documentos que necesite relacionados con la actividad, los servicios y los productos que gestiona la Agencia.',
            'GET_TXT: atencion-ciudadano',
            'Atención al ciudadano\n',
            'XPATH.DOUBLE_CLICK: /html/body/div[4]/div/div[1]/div/ul/li[2]/a'}
        self.datos_descarga = ['A29313-29424.pdf']
        self.adjuntos_mail = ['A29313-29424.pdf']
        self.datos_mail = {
            'Subject : WebScraping\n',
            'From : fulgenciovalleverde@gmail.com\n'}
        self.usuario = 'fulgenciovalleverde@gmail.com'
        self.contraseña = 'gfmxjfwesjygolge'
        self.host = 'imap.gmail.com'
        self.puerto = 993
        self.ruta = '/Users/jesusgomezcanovas/Dropbox/guapo/programar/python/WSU/test/DescargaEmail/'



    def testScraper(self):
        """
        Método de test de la tarea 1.1: Navegación por la pagina desde plantilla
        datos_navegacion: set con las páginas que debe haber visitado tras la ejecución
        """
        ### Navegacion ###
        # ACT, invocamos al método de extracción
        scraper = self.gestor.iniciarScraper()
        self.resultado = scraper.especificacion()  # Recogemos las URL visitadas
        # ASSER, validamos los resultados
        error = f'se deberían haber visitado {self.datos_navegacion} páginas'
        self.assertEqual(len(self.resultado), len(self.datos_navegacion), error)
        for dato in self.datos_navegacion:
            error = f'La página {dato} debía haber sido visitada y no está registrada'
            self.assertEqual(dato in self.resultado, True, error)  # Compara el resultado con lo esperado (sea igual)


        ##### FICHERO #####
            # ACT, invocamos al método de extracción
            contenido_fichero = abrirFichero()

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


        #### DESCARGA ####
            # ACT, preparamos la variable
            for fichero in self.datos_descarga:
                # ASSER, validamos los resultados
                error = f'fichero {fichero} no encontrado'
                resultado = fichero in os.listdir(ruta_relativa('archivos/'))
                self.assertEqual(resultado, True, error)

        #### EMAIL #####

        time.sleep(15)
        # ACT, invocamos al método de descarga de mail
        correo_descargado = descargaMail(self.usuario, self.contraseña,
                                         self.host, self.puerto, self.ruta)
        correo_descargado = set(correo_descargado)
        # ASSER, validamos los resultados

        # Ficheros en directorio
        for fichero in self.adjuntos_mail:
            error = f'fichero {fichero} no encontrado'
            resultado = fichero in os.listdir(ruta_relativa('test/DescargaEmail/'))
            self.assertEqual(resultado, True, error)

        # compresión de lista para comprobar si el esperado (datos_fichero)
        # está en el fichero cargado (contenido_fichero) (Delfstack, 2021)

        resultado = {dato for dato in self.datos_mail if dato in correo_descargado}
        error = f"""
                                        No se han encontrado todos los pasos en el fichero, el contenido es
                                        {correo_descargado}
                                        Se ha encontrado: {resultado}
                                        Esperaba: {self.datos_fichero}
                                        * Son conjuntos, por lo que no existe el orden ni repeticiones, lo importante es que estén todos
                                """
        self.assertEqual(resultado, self.datos_mail, error)


#   MAIN
if __name__ == '__main__':
    unittest.main()
