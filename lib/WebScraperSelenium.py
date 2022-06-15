"""
Created on Fri Apr 26 20:33:45 2022
@author: Jesús Gómez Cánovas
Grado en Ingeniería Informática - Web Scraping universal con entrada - UNIR
"""
# LIBRERIAS

from pandas import read_excel  # Solo nos traemos lo estrictamente necesario
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
import time
from datetime import date
import os, sys, datetime


# FUNCIONES

# FUNCIONES GENERALES
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


def cargaExcelVariable(nombre, tipocol):
    """
    utiliza la función de leer excel de pandas
    :param nombre: nombre de la excel
    :param tipocol: tipo de columnas de la excel, está pensado para todas por igual
    :return: devolvemos la estructura tipo 'tabla' con pandas de la hoja de excel
    """
    try:
        return read_excel(nombre, dtype=tipocol)
    except Exception as e:  # declaramos una excepción para poder tratar los posibles errores de lectura
        print(f'Error en el gestor al intentar cargar la excel {nombre}:{e}')


def cargarFicheroDiccionario(nomFichero, separador):
    """
    :param nomFichero: nombre del fichero
    :param separador: indica el separador del fichero
    :return:  devuelve un diccionario con el contenido del fichero
    """
    try:
        datos = {}  # diccionario vacío
        with open(nomFichero, 'r', encoding='utf8') as fichero:  # Apertura de fichero
            #   nos aseguramos de que se cierre el fichero con el with
            for linea in fichero:  # para cada línea del fichero
                linea = linea.strip('\n\t')  # limpiamos la línea de fin de línea y salto de línea
                clave, valor = linea.split(separador, 1)  # un split por ser a medida de un diccionario
                datos[clave] = valor
    except Exception as e:  # declaramos una excepción para poder tratar los posibles errores de lectura
        print(f'Error en el gestor al intentar cargar la el fichero {nomFichero}:{e}')
    finally:
        return datos


class WebScraperSelenium():
    """
    WebScraper
    """
    # Variable estática
    __urls = set()
    __comandos = {'URL.FIRST': 'self.driver.get(contenido)',
                  'WINDOW.SIZE': 'self.driver.set_window_size(ancho, alto)',
                  'DRIVER.BACK': 'self.driver.back()',
                  'DRIVER.FORWARD': 'self.driver.forward()',
                  'DRIVER.REFRESH': 'self.driver.refresh()',
                  'DRIVER.WAIT': 'self.esperamos(espera)',
                  'DRIVER.EXECUTE_SCRIPT':'self.driver.execute_script(contenido)',
                  'VARS.HANDLE': 'self.variables[contenido] = self.driver.window_handles',
                  'TITLE.CONTAINS': 'WebDriverWait(self.driver, espera).until(EC.title_contains(contenido))',
                  'DRIVER.CHANGE_WINDOW': 'self.cambio_ventana(ventana, espera, fichero)',
                  'NAME.CLICK': 'WebDriverWait(self.driver, espera).until(EC.element_to_be_clickable((By.NAME, contenido))).click()',
                  'NAME.CLEAR': 'WebDriverWait(self.driver, espera).until(EC.element_to_be_clickable((By.NAME, contenido))).clear()',
                  'NAME.GET_HREF': 'self.a_texto(self.driver.find_element(By.NAME, contenido).get_attribute("href"),fichero)',
                  'NAME.GET_IMG': 'self.a_texto(self.driver.find_element(By.NAME, contenido).get_attribute("src"),fichero)',
                  'NAME.GET_PROPERTY': 'self.a_texto(self.driver.find_element(By.NAME, contenido).get_property(adicional),fichero)',
                  'NAME.GET_CSS': 'self.a_texto(self.driver.find_element(By.NAME, contenido).value_of_css_property(adicional),fichero)',
                  'NAME.GET_TXT': 'self.a_texto(self.driver.find_element(By.NAME, contenido).text,fichero)',

                  'XPATH.CLICK': 'WebDriverWait(self.driver, espera).until(EC.element_to_be_clickable((By.XPATH, contenido))).click()',
                  'XPATH.DOUBLE_CLICK':'ActionChains(self.driver).double_click(on_element = WebDriverWait(self.driver, espera).until(EC.element_to_be_clickable((By.XPATH, contenido)))).perform()',
                  'XPATH.CLEAR': 'WebDriverWait(self.driver, espera).until(EC.element_to_be_clickable((By.XPATH, contenido))).clear()',
                  'XPATH.GET_HREF': 'self.a_texto(self.driver.find_element(By.XPATH, contenido).get_attribute("href"),fichero)',
                  'XPATH.GET_IMG': 'self.a_texto(self.driver.find_element(By.XPATH, contenido).get_attribute("src"),fichero)',
                  'XPATH.GET_PROPERTY': 'self.a_texto(self.driver.find_element(By.XPATH, contenido).get_property(adicional),fichero)',
                  'XPATH.GET_CSS': 'self.a_texto(self.driver.find_element(By.XPATH, contenido).value_of_css_property(adicional),fichero)',
                  'XPATH.GET_TXT': 'self.a_texto(self.driver.find_element(By.XPATH, contenido).text,fichero)',

                  'ID.CLICK': 'WebDriverWait(self.driver, espera).until(EC.element_to_be_clickable((By.ID, contenido))).click()',
                  'ID.CLEAR': 'WebDriverWait(self.driver, espera).until(EC.element_to_be_clickable((By.ID, contenido))).clear()',
                  'ID.GET_HREF': 'self.a_texto(self.driver.find_element(By.ID, contenido).get_attribute("href"),fichero)',
                  'ID.GET_IMG': 'self.a_texto(self.driver.find_element(By.ID, contenido).get_attribute("src"),fichero)',
                  'ID.GET_PROPERTY': 'self.a_texto(self.driver.find_element(By.ID, contenido).get_property(adicional),fichero)',
                  'ID.GET_CSS': 'self.a_texto(self.driver.find_element(By.ID, contenido).value_of_css_property(adicional),fichero)',
                  'ID.GET_TXT': 'self.a_texto(self.driver.find_element(By.ID, contenido).text,fichero)',
                  'PARTIAL_LINK_TEXT.CLICK': 'WebDriverWait(self.driver, espera).until(EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, contenido))).click()',
                  'LINK_TEXT.CLICK': 'WebDriverWait(self.driver, espera).until(EC.element_to_be_clickable((By.LINK_TEXT, contenido))).click()',
                  'CSS.CLICK': 'WebDriverWait(self.driver, espera).until(EC.element_to_be_clickable((By.CSS_SELECTOR, contenido))).send_keys(adicional)',
                  'CSS.CLEAR': 'WebDriverWait(self.driver, espera).until(EC.element_to_be_clickable((By.CSS_SELECTOR, contenido))).clear()',
                  'CSS.GET_HREF': 'self.a_texto(self.driver.find_element(By.CSS, contenido).get_attribute("href"),fichero)',
                  'CSS.GET_IMG': 'self.a_texto(self.driver.find_element(By.CSS, contenido).get_attribute("src"),fichero)',
                  'CSS.GET_PROPERTY': 'self.a_texto(self.driver.find_element(By.CSS, contenido).get_property(adicional),fichero)',
                  'CSS.GET_CSS': 'self.a_texto(self.driver.find_element(By.CSS, contenido).value_of_css_property(adicional),fichero)',
                  'CSS.GET_TXT': 'self.a_texto(self.driver.find_element(By.CSS, contenido).text,fichero)',

                  'TAG_NAME.CLICK': 'WebDriverWait(self.driver, espera).until(EC.element_to_be_clickable((By.TAG_NAME, contenido))).click()',
                  'TAG_NAME.CLEAR': 'WebDriverWait(self.driver, espera).until(EC.element_to_be_clickable((By.TAG_NAME, contenido))).clear()',
                  'TAG_NAME.GET_HREF': 'self.a_texto(self.driver.find_element(By.TAG_NAME, contenido).get_attribute("href"),fichero)',
                  'TAG_NAME.GET_IMG': 'self.a_texto(self.driver.find_element(By.TAG_NAME, contenido).get_attribute("src"),fichero)',
                  'TAG_NAME.GET_PROPERTY': 'self.a_texto(self.driver.find_element(By.TAG_NAME, contenido).get_property(adicional),fichero)',
                  'TAG_NAME.GET_CSS': 'self.a_texto(self.driver.find_element(By.TAG_NAME, contenido).value_of_css_property(adicional),fichero)',
                  'TAG_NAME.GET_TXT': 'self.a_texto(self.driver.find_element(By.TAG_NAME, contenido).text,fichero)',

                  'CLASS_NAME.CLICK': 'WebDriverWait(self.driver, espera).until(EC.element_to_be_clickable((By.CLASS_NAME, contenido))).click()',
                  'CLASS_NAME.CLEAR': 'WebDriverWait(self.driver, espera).until(EC.element_to_be_clickable((By.CLASS_NAME, contenido))).clear()',
                  'CLASS_NAME.GET_HREF': 'self.a_texto(self.driver.find_element(By.CLASS_NAME, contenido).get_attribute("href"),fichero)',
                  'CLASS_NAME.GET_IMG': 'self.a_texto(self.driver.find_element(By.CLASS_NAME, contenido).get_attribute("src"),fichero)',
                  'CLASS_NAME.GET_PROPERTY': 'self.a_texto(elf.driver.find_element(By.CLASS_NAME, contenido).get_property(adicional),fichero)',
                  'CLASS_NAME.GET_CSS': 'self.a_texto(self.driver.find_element(By.CLASS_NAME, contenido).value_of_css_property(adicional),fichero)',
                  'CLASS_NAME.GET_TXT': 'self.a_texto(self.driver.find_element(By.CLASS_NAME, contenido).text,fichero)'

                  }

    def __init__(self):
        self.__tipo = 'Extracción con un motor visual'
        self.__datos = cargarFicheroDiccionario(ruta_relativa('archivos/configuracion.txt'), ' ')  # Contiene el diccionario con la configuración
        self.__acciones = cargaExcelVariable(ruta_relativa('archivos/Plantilla.xlsx'), 'str')  # Contiene el dataframe con las acciones
        self.__driver = webdriver.Chrome(self.datos['DRIVER'])  # Llama al chromedriver
        self.__variables = {}
        self.extrae()

    @property
    def tipo(self):
        return self.__tipo

    @property
    def datos(self):
        return self.__datos

    @property
    def acciones(self):
        return self.__acciones

    @property
    def driver(self):
        return self.__driver

    @property
    def variables(self):
        return self.__variables

    @variables.setter
    def variables(self, variables):
        self.__variables = variables

    @driver.setter
    def driver(self, driver):
        self.__driver = driver


    @classmethod
    def especificacion(cls, url=False):
        if url:
            if url not in cls.__urls:
                cls.__urls.add(url)
        else:
            return cls.__urls

    def apagar(self):
        """
        Cerramos el driver
        """
        self.driver.quit()

    def esperamos(self, timeout=2):
        time.sleep(timeout)

    def esperamos_pantalla(self, timeout=10):
        """
        https://stackoverflow.com/questions/26641779/python-selenium-how-to-wait-for-new-window-opens
        :param timeout: tiempo maximo de espera si no indica nada 10 segundos
        :return:
        """
        manejadores_antes = self.window_handles
        yield
        WebDriverWait(self, timeout).until(
            lambda driver: len(manejadores_antes) != len(driver.window_handles))

    def a_texto(self, texto, fichero):
        try:
            fichero_r = ruta_relativa('archivos/' + fichero)
            # OPEN **** puede abrir un archivo nuevo (si no existe) o existente y puede escribir en el o leer
            archivo = open(fichero_r, 'a', encoding='utf8')  # encoding ='utf8' hace que permita acentos
            archivo.write(texto + '\n\n')
            print(texto + '\n\n')
        except Exception as e:
            print(e)
        finally:
            archivo.close()  # siempre debe cerrarse, despues de cerrar falla al escribir claro

    def extrae(self):
        ancho = self.datos['ANCHO_PANTALLA']
        alto = self.datos['ALTO_PANTALLA']
        fichero = self.datos['ENTRADA']

        try:
            exec(self.__comandos['WINDOW.SIZE'])

            if fichero != '':
                try:
                    fichero_r = ruta_relativa('archivos/' + fichero)
                    os.remove(fichero_r)
                except Exception as e:
                    print(f'{datetime.datetime.now()}: Error al borrar el fichero:{e}')

            for fila in self.acciones.index:
                contenido = str(self.acciones["CONTENIDO"][fila])
                adicional = str(self.acciones["ADICIONAL"][fila])
                espera = int(self.acciones["ESPERA"][fila])
                salida = str(self.acciones["SALIDA"][fila])
                comando = str(self.acciones["IDENTIFICADOR"][fila]) + '.' + str(self.acciones["TIPO"][fila])
                info = f'{datetime.datetime.now()}: ***** Acción {fila} {comando}: {contenido} ******'
                ventana = self.driver.current_window_handle
                # Vamos imprimiendo por consola y en el fichero las acciones
                self.a_texto(info, fichero)
                try:
                    exec(self.__comandos[comando])
                    self.especificacion(self.driver.current_url)
                    if comando == 'VARS.HANDLE':
                        try:
                            ventana = self.driver.current_window_handle
                        except Exception as e:
                            error = f'{datetime.datetime.now()}: Error en el WebScraperSelenium al intentar guardar el manejador de la ventana:{e} '
                            self.a_texto(error, fichero)

                except Exception as e:
                    error = f'{datetime.datetime.now()}: Error en el WebScraperSelenium al intentar Ejecutar una acción:{e} '
                    self.a_texto(error, fichero)

                except Exception as e:
                    error = f'{datetime.datetime.now()}: Error en el WebScraperSelenium al intentar ejecutar una acción:{e} ' \
                            f'\n Vamos a intentar volver a hacer lo mismo esperando el tiempo definido'
                    self.a_texto(error, fichero)
                    self.esperamos_pantalla(espera)

                    exec(self.__comandos[comando])
                    self.especificacion(self.driver.current_url)

                    if salida == 'X':  # Si es salida significa que queremos esperar a que una salida o fichero se descargue
                        info = f'{datetime.datetime.now()}: Esperamos la respuesta de la pagina ó la descarga de un contenido'
                        self.a_texto(info, fichero)
                        self.esperamos(espera)
            try:
                visitadas = f"""***** FIN EXTRACCION ***** \n\nLas páginas visitadas han sido: {self.especificacion()}
                """
                self.a_texto(visitadas, fichero)
            except Exception as e:
                error = f'{datetime.datetime.now()}: Error en el WebScraperSelenium al intentar grabar las páginas visitadas:{e}'
                self.a_texto(error, fichero)
        except Exception as e:  # declaramos una excepción para poder tratar los posibles errores de lectura
            print(f'Error en el WebScraperVisual al intentar ejecutar una acción:{e}')
        finally:
            self.apagar()
