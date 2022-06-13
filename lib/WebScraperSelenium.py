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
import os, sys


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
                  'XPATH.CLICK': 'WebDriverWait(self.driver, espera).until(EC.element_to_be_clickable((By.XPATH, contenido))).click()',
                  'XPATH.DOUBLE_CLICK': 'ActionChains(self.driver).double_click(on_element = WebDriverWait(self.driver, espera).until(EC.element_to_be_clickable((By.XPATH, contenido)))).perform()',
                  'XPATH.GET_HREF': 'self.driver.find_element(By.XPATH, contenido).get_attribute("href")',
                  'XPATH.GET_IMG': 'self.driver.find_element(By.XPATH, contenido).get_attribute("src")',
                  'XPATH.GET_PROPERTY': 'self.driver.find_element(By.XPATH, contenido).get_property(adicional)',
                  'XPATH.GET_CSS': 'self.driver.find_element(By.XPATH, contenido).value_of_css_property(adicional)',
                  'XPATH.GET_TXT': 'self.driver.find_element(By.XPATH, contenido).text'
                  }

    def __init__(self):
        self.__tipo = 'Extracción con un motor visual'
        self.__datos = cargarFicheroDiccionario(ruta_relativa('archivos/configuracion.txt'), ' ')  # Contiene el diccionario con la configuración
        self.__acciones = cargaExcelVariable(ruta_relativa('archivos/Plantilla.xlsx'), 'str')  # Contiene el dataframe con las acciones
        self.__driver = webdriver.Chrome(self.datos['DRIVER'])  # Llama al chromedriver
        self.__variables = {}

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

    def extrae(self):
        ancho = self.datos['ANCHO_PANTALLA']
        alto = self.datos['ALTO_PANTALLA']
        try:
            exec(self.__comandos['WINDOW.SIZE'])

            for fila in self.acciones.index:
                contenido = str(self.acciones["CONTENIDO"][fila])
                adicional = str(self.acciones["ADICIONAL"][fila])
                espera = int(self.acciones["ESPERA"][fila])
                salida = str(self.acciones["SALIDA"][fila])
                dias = str(self.acciones["DIAS"][fila])
                print(fila)
                print(str(self.acciones["IDENTIFICADOR"][fila]) + '.' + str(self.acciones["TIPO"][fila]))
                print(
                    self.__comandos[str(self.acciones["IDENTIFICADOR"][fila]) + '.' + str(self.acciones["TIPO"][fila])])
                lista = dias.split(',')  # introducimos en una lista lis dias de filtro

                try:
                    lista = list(map(int, lista))
                except:
                    lista = ()
                if date.today().day in lista or len(
                        lista) == 0:  # Si no hay filtro de dias o hoy es el un dia entre los días introducidos
                    try:
                        exec(self.__comandos[
                                 str(self.acciones["IDENTIFICADOR"][fila]) + '.' + str(self.acciones["TIPO"][fila])])
                        self.especificacion(self.driver.current_url)

                    except Exception as e:
                        print(f'Error en el WebScraperVisual al intentar ejecutar una acción:{e}')
                        print(f'Vamos a intentar volver a hacer lo mismo esperando el tiempo definido')
                        self.esperamos_pantalla(espera)

                        exec(self.__comandos[
                                 str(self.acciones["IDENTIFICADOR"][fila]) + '.' + str(self.acciones["TIPO"][fila])])
                        self.especificacion(self.driver.current_url)

                    if salida == 'X':  # Si es salida significa que queremos esperar a que una salida o fichero se descargue
                        self.esperamos(espera)

        except Exception as e:  # declaramos una excepción para poder tratar los posibles errores de lectura
            print(f'Error en el WebScraperVisual al intentar ejecutar una acción:{e}')
        finally:
            self.apagar()
