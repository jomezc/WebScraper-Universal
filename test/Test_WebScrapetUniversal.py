"""
Created on Fri Apr 26 19:00:24 2022
@author: Jesús Gómez Cánovas
Grado en Ingeniería Informática - Web Scraping universal con entrada - UNIR
"""

# LIB
import unittest, os, sys,time
from lib.WebScraperSelenium import WebScraperSelenium
import pytest
import imaplib
import base64
import email
def descargaMail(usuario, contraseña, host, puerto, ruta):
    """
    Versión modificada basada en:  (Doshi, 2018). To read emails and download attachments in Python
    Obtenido de stackoverflow: https://medium.com/@sdoshi579/to-read-emails-and-download-attachments-in-python-6d7d6b60269
    Función que se descarga los adjuntos del correo nuevo y devuelve los datos del email
    """
    correo_descargado = [] # lista para introducir los archivos descargados

    #  Accede vía IMAP4 al host y puerto especificado mediante los datos de acceso
    mail = imaplib.IMAP4_SSL(host, puerto)
    mail.login(usuario, contraseña)

    # seleccionas la carpeta o buzón donde quieres descargar el correo
    mail.select()

    # .search busca desde el correo
    # podríamos seleccionar filtros como desde, hacia o el asunto del correo
    # None es un conjunto de caracteres y ALL devuelve todos los mensajes sin ningún filtro.
    tipo, datos = mail.search(None, 'ALL')
    mail_ids = datos[0]
    # Esta función devuelve el tipo que es si la solicitud estaba bien o no.
    # Los datos son identificadores de todos los correos electrónicos.
    id_list = mail_ids.split()

    for num in datos[0].split():
        # fetch obtiene el correo para un identificador determinado
        # 'RFC822' es un protocolo de acceso a mensajes de Internet.
        typ, datos = mail.fetch(num, '(RFC822)')
        raw_email = datos[0][1]

        # Los datos de fetch están codificados en binario,
        # por lo que necesitamos decodificar en el conjunto de caracteres UTF-8.
        raw_email_string = raw_email.decode('utf-8')
        # Ahora, pasamos esa cadena decodificada a email.message_from_string
        # que acepta una cadena y la convierte en formato de diccionario
        email_message = email.message_from_string(raw_email_string)

        # Descarga de adjuntos
        for parte in email_message.walk():

            if parte.get_content_maintype() == 'multipart':
                continue
            if parte.get('Content-Disposition') is None:
                continue
            fileName = parte.get_filename()
            if bool(fileName):
                filePath = os.path.join(ruta, fileName)
                if not os.path.isfile(filePath):
                    fp = open(filePath, 'wb')
                    fp.write(parte.get_payload(decode=True))
                    fp.close()
                subject = str(email_message).split("Subject: ", 1)[1].split("\nTo:", 1)[0]
                # correo_descargado.append(f'Hemos descargado "{fileName}" del mail con asunto "{subject}".')

    for parte_Respuesta in datos:
        if isinstance(parte_Respuesta, tuple):
            msg = email.message_from_string(parte_Respuesta[1].decode('utf-8'))
            email_subject = msg['subject']
            email_from = msg['from']
            correo_descargado.append('From : ' + email_from + '\n')
            correo_descargado.append('Subject : ' + email_subject + '\n')
            correo_descargado.append(msg.get_payload(decode=True)) # cuerpo
    mail.close()
    del mail
    return correo_descargado


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

        # ACT, invocamos al método de extracción
        self.WebScraperSelenium = WebScraperSelenium()
        self.resultado = WebScraperSelenium.especificacion()  # Recogemos las URL visitadas
        # ASSER, validamos los resultados
        error = f'se deberían haber visitado {self.datos_navegacion} páginas'
        self.assertEqual(len(self.resultado), len(self.datos_navegacion), error)
        for dato in self.datos_navegacion:
            error = f'La página {dato} debía haber sido visitada y no está registrada'
            self.assertEqual(dato in self.resultado, True, error)  # Compara el resultado con lo esperado (sea igual)
        del self.WebScraperSelenium

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
        print(self.datos_mail)
        print(correo_descargado)
        resultado = {dato for dato in self.datos_mail if dato in correo_descargado}
        error = f"""
                                        No se han encontrado todos los pasos en el fichero, el contenido es
                                        {correo_descargado}
                                        Se ha encontrado: {resultado}
                                        Esperaba: {self.datos_fichero}
                                        * Son conjuntos, por lo que no existe el orden ni repeticiones, lo importante es que estén todos
                                """
        self.assertEqual(resultado, self.datos_mail, error)

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

    def testDescarga(self):
        # ACT, preparamos la variable
        for fichero in self.datos_descarga:
        # ASSER, validamos los resultados
            error = f'fichero {fichero} no encontrado'
            resultado = fichero in os.listdir(ruta_relativa('archivos/'))
            self.assertEqual(resultado, True, error)


    def testEmail(self):
        pass


#   MAIN
if __name__ == '__main__':
    unittest.main()
