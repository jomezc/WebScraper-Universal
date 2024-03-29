"""
Created on Fri Apr 26 20:33:45 2022
@author: Jesús Gómez Cánovas
Grado en Ingeniería Informática - Web Scraping universal con entrada - UNIR
"""
# LIBRERIAS
from lib.libExternas import *
from lib.WebScraper import WebScraper


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


class WebScraperSelenium(WebScraper):
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
                  'DRIVER.EXECUTE_SCRIPT': 'self.driver.execute_script(contenido)',
                  'VARS.HANDLE': 'self.variables[contenido] = self.driver.window_handles',
                  'TITLE.CONTAINS': 'WebDriverWait(self.driver, espera).until(EC.title_contains(contenido))',
                  'DRIVER.CHANGE_WINDOW': 'self.cambio_ventana(ventana, espera, self.fichero)',
                  'NAME.SEND_KEYS': 'WebDriverWait(self.driver, espera).until(EC.element_to_be_clickable((By.NAME, contenido))).send_keys(adicional)',
                  'NAME.CLICK': 'WebDriverWait(self.driver, espera).until(EC.element_to_be_clickable((By.NAME, contenido))).click()',
                  'NAME.CLEAR': 'WebDriverWait(self.driver, espera).until(EC.element_to_be_clickable((By.NAME, contenido))).clear()',
                  'NAME.SELECT_VALUE': 'Select(self.driver.find_element(By.NAME, contenido)).select_by_value(adicional)',
                  'NAME.SELECT_INDEX': 'Select(self.driver.find_element(By.NAME, contenido)).select_by_index(adicional)',
                  'NAME.SELECT_TEXT': 'Select(self.driver.find_element(By.NAME, contenido)).select_by_visible_text(adicional)',
                  'NAME.GET_HREF': 'self.a_texto(self.driver.find_element(By.NAME, contenido).get_attribute("href"),self.fichero)',
                  'NAME.GET_IMG': 'self.a_texto(self.driver.find_element(By.NAME, contenido).get_attribute("src"),self.fichero)',
                  'NAME.GET_PROPERTY': 'self.a_texto(self.driver.find_element(By.NAME, contenido).get_property(adicional),self.fichero)',
                  'NAME.GET_CSS': 'self.a_texto(self.driver.find_element(By.NAME, contenido).value_of_css_property(adicional),self.fichero)',
                  'NAME.GET_TXT': 'self.a_texto(self.driver.find_element(By.NAME, contenido).text,self.fichero)',

                  'XPATH.CLICK': 'WebDriverWait(self.driver, espera).until(EC.element_to_be_clickable((By.XPATH, contenido))).click()',
                  'XPATH.DOUBLE_CLICK': 'ActionChains(self.driver).double_click(on_element = WebDriverWait(self.driver, espera).until(EC.element_to_be_clickable((By.XPATH, contenido)))).perform()',
                  'XPATH.SEND_KEYS': 'WebDriverWait(self.driver, espera).until(EC.element_to_be_clickable((By.XPATH, contenido))).send_keys(adicional)',
                  'XPATH.CLEAR': 'WebDriverWait(self.driver, espera).until(EC.element_to_be_clickable((By.XPATH, contenido))).clear()',
                  'XPATH.SELECT_VALUE': 'Select(self.driver.find_element(By.XPATH, contenido)).select_by_value(adicional)',
                  'XPATH.SELECT_INDEX': 'Select(self.driver.find_element(By.XPATH, contenido)).select_by_index(adicional)',
                  'XPATH.SELECT_TEXT': 'Select(self.driver.find_element(By.XPATH, contenido)).select_by_visible_text(adicional)',
                  'XPATH.GET_HREF': 'self.a_texto(self.driver.find_element(By.XPATH, contenido).get_attribute("href"),self.fichero)',
                  'XPATH.GET_IMG': 'self.a_texto(self.driver.find_element(By.XPATH, contenido).get_attribute("src"),self.fichero)',
                  'XPATH.GET_PROPERTY': 'self.a_texto(self.driver.find_element(By.XPATH, contenido).get_property(adicional),self.fichero)',
                  'XPATH.GET_CSS': 'self.a_texto(self.driver.find_element(By.XPATH, contenido).value_of_css_property(adicional),self.fichero)',
                  'XPATH.GET_TXT': 'self.a_texto(self.driver.find_element(By.XPATH, contenido).text,self.fichero)',

                  'ID.SEND_KEYS': 'WebDriverWait(self.driver, espera).until(EC.element_to_be_clickable((By.ID, contenido))).send_keys(adicional)',
                  'ID.CLICK': 'WebDriverWait(self.driver, espera).until(EC.element_to_be_clickable((By.ID, contenido))).click()',
                  'ID.CLEAR': 'WebDriverWait(self.driver, espera).until(EC.element_to_be_clickable((By.ID, contenido))).clear()',
                  'ID.SELECT_VALUE': 'Select(self.driver.find_element(By.ID, contenido)).select_by_value(adicional)',
                  'ID.SELECT_INDEX': 'Select(self.driver.find_element(By.ID, contenido)).select_by_index(adicional)',
                  'ID.SELECT_TEXT': 'Select(self.driver.find_element(By.ID, contenido)).select_by_visible_text(adicional)',
                  'ID.GET_HREF': 'self.a_texto(self.driver.find_element(By.ID, contenido).get_attribute("href"),self.fichero)',
                  'ID.GET_IMG': 'self.a_texto(self.driver.find_element(By.ID, contenido).get_attribute("src"),self.fichero)',
                  'ID.GET_PROPERTY': 'self.a_texto(self.driver.find_element(By.ID, contenido).get_property(adicional),self.fichero)',
                  'ID.GET_CSS': 'self.a_texto(self.driver.find_element(By.ID, contenido).value_of_css_property(adicional),self.fichero)',
                  'ID.GET_TXT': 'self.a_texto(self.driver.find_element(By.ID, contenido).text,self.fichero)',

                  'PARTIAL_LINK_TEXT.CLICK': 'WebDriverWait(self.driver, espera).until(EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, contenido))).click()',
                  'LINK_TEXT.CLICK': 'WebDriverWait(self.driver, espera).until(EC.element_to_be_clickable((By.LINK_TEXT, contenido))).click()',
                  'CSS.CLICK': 'WebDriverWait(self.driver, espera).until(EC.element_to_be_clickable((By.CSS_SELECTOR, contenido))).send_keys(adicional)',
                  'CSS.SEND_KEYS': 'WebDriverWait(self.driver, espera).until(EC.element_to_be_clickable((By.CSS_SELECTOR, contenido))).click()',
                  'CSS.CLEAR': 'WebDriverWait(self.driver, espera).until(EC.element_to_be_clickable((By.CSS_SELECTOR, contenido))).clear()',
                  'CSS.GET_HREF': 'self.a_texto(self.driver.find_element(By.CSS, contenido).get_attribute("href"),self.fichero)',
                  'CSS.GET_IMG': 'self.a_texto(self.driver.find_element(By.CSS, contenido).get_attribute("src"),self.fichero)',
                  'CSS.GET_PROPERTY': 'self.a_texto(self.driver.find_element(By.CSS, contenido).get_property(adicional),self.fichero)',
                  'CSS.GET_CSS': 'self.a_texto(self.driver.find_element(By.CSS, contenido).value_of_css_property(adicional),self.fichero)',
                  'CSS.GET_TXT': 'self.a_texto(self.driver.find_element(By.CSS, contenido).text,self.fichero)',

                  'TAG_NAME.CLICK': 'WebDriverWait(self.driver, espera).until(EC.element_to_be_clickable((By.TAG_NAME, contenido))).click()',
                  'TAG_NAME.SEND_KEYS': 'WebDriverWait(self.driver, espera).until(EC.element_to_be_clickable((By.TAG_NAME, contenido))).send_keys(adicional)',
                  'TAG_NAME.CLEAR': 'WebDriverWait(self.driver, espera).until(EC.element_to_be_clickable((By.TAG_NAME, contenido))).clear()',
                  'TAG_NAME.GET_HREF': 'self.a_texto(self.driver.find_element(By.TAG_NAME, contenido).get_attribute("href"),self.fichero)',
                  'TAG_NAME.GET_IMG': 'self.a_texto(self.driver.find_element(By.TAG_NAME, contenido).get_attribute("src"),self.fichero)',
                  'TAG_NAME.GET_PROPERTY': 'self.a_texto(self.driver.find_element(By.TAG_NAME, contenido).get_property(adicional),self.fichero)',
                  'TAG_NAME.GET_CSS': 'self.a_texto(self.driver.find_element(By.TAG_NAME, contenido).value_of_css_property(adicional),self.fichero)',
                  'TAG_NAME.GET_TXT': 'self.a_texto(self.driver.find_element(By.TAG_NAME, contenido).text,self.fichero)',

                  'CLASS_NAME.CLICK': 'WebDriverWait(self.driver, espera).until(EC.element_to_be_clickable((By.CLASS_NAME, contenido))).click()',
                  'CLASS_NAME.SEND_KEYS': 'WebDriverWait(self.driver, espera).until(EC.element_to_be_clickable((By.CLASS_NAME, contenido))).send_keys(adicional)',
                  'CLASS_NAME.CLEAR': 'WebDriverWait(self.driver, espera).until(EC.element_to_be_clickable((By.CLASS_NAME, contenido))).clear()',
                  'CLASS_NAME.GET_HREF': 'self.a_texto(self.driver.find_element(By.CLASS_NAME, contenido).get_attribute("href"),self.fichero)',
                  'CLASS_NAME.GET_IMG': 'self.a_texto(self.driver.find_element(By.CLASS_NAME, contenido).get_attribute("src"),self.fichero)',
                  'CLASS_NAME.GET_PROPERTY': 'self.a_texto(self.driver.find_element(By.CLASS_NAME, contenido).get_property(adicional), self.fichero)',
                  'CLASS_NAME.GET_CSS': 'self.a_texto(self.driver.find_element(By.CLASS_NAME, contenido).value_of_css_property(adicional), self.fichero)',
                  'CLASS_NAME.GET_TXT': 'self.a_texto(self.driver.find_element(By.CLASS_NAME, contenido).text, self.fichero)',
                  }

    def __init__(self, datos, acciones, fichero):
        self.__tipo = 'Extracción con un motor visual'
        self.__datos = datos  # Contiene el diccionario con la configuración
        self.__acciones = acciones # Contiene el dataframe con las acciones
        self.__variables = {}
        self.__fichero = fichero
        self.__driver = self.modo_driver()
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

    @property
    def fichero(self):
        return self.__fichero

    @variables.setter
    def variables(self, variables):
        self.__variables = variables

    @driver.setter
    def driver(self, driver):
        self.__driver = driver

    def modo_driver(self):
        # Declaramos la variable de opciones de Chrome
        opciones_chrome = Options()
        opciones_chrome.add_argument("--disable-extensions")
        opciones_chrome.add_argument("--start-maximized")
        opciones_chrome.add_argument("--disable-dev-shm-usage")
        profile = {"plugins.plugins_list": [{"enabled": False, "name": "Chrome PDF Viewer"}],
                   "download.default_directory": self.datos['RUTA_DESCARGA_CONSOLA'],
                   "download.extensions_to_open": "application/pdf",
                   "useAutomationExtension": False,
                   "excludeSwitches": ["enable-automation"],
                   "download.prompt_for_download": False,
                   "download.directory_upgrade": True,
                   "plugins.always_open_pdf_externally": True
                   }
        opciones_chrome.add_experimental_option("prefs", profile)

        # Selección de MODO
        if self.datos['MODO'] == 'VISUAL':
            texto = f'{datetime.datetime.now()}: ***** INICIANDO EXTRACTOR EN MODO VISUAL ***** '
        else:
            texto = f'{datetime.datetime.now()}: ***** INICIANDO EXTRACTOR EN MODO CONSOLA ***** '
            opciones_chrome.add_argument("--headless")

        self.a_texto(texto, self.fichero)
        return webdriver.Chrome(self.datos['DRIVER'], options=opciones_chrome)  # Llama al chromedriver

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
        try:
            exec(self.__comandos['WINDOW.SIZE'])

            for fila in self.acciones.index:
                # Variables temporales de bucle
                contenido = str(self.acciones["CONTENIDO"][fila])
                adicional = str(self.acciones["ADICIONAL"][fila])
                espera = int(self.acciones["ESPERA"][fila])
                salida = str(self.acciones["SALIDA"][fila])
                dias = str(self.acciones["DIAS"][fila])
                comando = str(self.acciones["IDENTIFICADOR"][fila]) + '.' + str(self.acciones["TIPO"][fila])
                info = f'{datetime.datetime.now()}: ***** Acción {fila} {comando}: {contenido} ******'
                lista = dias.split(',')  # introducimos en una lista los dias de filtro
                ventana = self.driver.current_window_handle
                # Vamos imprimiendo por consola y en el fichero las acciones
                self.a_texto(info, self.fichero)
                try:
                    lista = list(map(int, lista))

                except:
                    lista = ()
                if date.today().day in lista or len(
                        lista) == 0:  # Si no hay filtro de dias o hoy es el un dia entre los días introducidos
                    try:
                        exec(self.__comandos[comando])
                        self.especificacion(self.driver.current_url)
                        if comando == 'VARS.HANDLE':
                            try:
                                ventana = self.driver.current_window_handle
                            except Exception as e:
                                error = f'{datetime.datetime.now()}: Error en el WebScraperSelenium al intentar guardar el manejador de la ventana:{e} '
                                self.a_texto(error, self.fichero)
                    except Exception as e:

                        error = f'{datetime.datetime.now()}: Error en el WebScraperSelenium al intentar ejecutar una acción:{e} ' \
                                f'\n Vamos a intentar volver a hacer lo mismo esperando el tiempo definido'
                        self.a_texto(error, self.fichero)
                        self.esperamos_pantalla(espera)
                        exec(self.__comandos[comando])
                        self.especificacion(self.driver.current_url)

                    if salida == 'X':  # Si es salida significa que queremos esperar a que una salida o fichero se descargue
                        info = f'{datetime.datetime.now()}: Esperamos la respuesta de la pagina ó la descarga de un contenido'
                        self.a_texto(info, self.fichero)
                        self.esperamos(espera)
            try:
                visitadas = f"""{datetime.datetime.now()}: ***** FIN EXTRACCION ***** 
                \n\nLas páginas visitadas han sido: {self.especificacion()}"""
                self.a_texto(visitadas, self.fichero)
            except Exception as e:
                error = f'{datetime.datetime.now()}: Error en el WebScraperSelenium al intentar grabar las páginas visitadas:{e}'
                self.a_texto(error, self.fichero)


        except Exception as e:  # declaramos una excepción para poder tratar los posibles errores de lectura
            error = f'{datetime.datetime.now()}: Error en el WebScraperSelenium al intentar ejecutar una acción:{e}'
            self.a_texto(error, self.fichero)

        finally:
            self.apagar()
