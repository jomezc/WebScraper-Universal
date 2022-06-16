# LIBRERIAS
from lib.Gestor import Gestor
from lib.WebScraperSelenium import WebScraperSelenium


class GestorScraper(Gestor):
    """
    Hereda de Gestor, sobrescribe el método abstracto, asignarMotor en él crea un objeto
    de tipo WebScraper y dependiendo de la entrada con un if crea una nueva instancia del
    objeto de una de las dos clases de WebScraper (visual y motora)
    """
    __tipologiaAcciones = {'IDENTIFICADOR': 'str',
                           'TIPO': 'str',
                           'ADICIONAL': 'str',
                           'SALIDA': 'str'}

    def __init__(self):
        configuracion = super().ruta_relativa('archivos/configuracion.txt')
        plantilla = super().ruta_relativa('archivos/Plantilla.xlsx')
        self.__datos = super().cargarFicheroDiccionario(configuracion, ';')
        self.__acciones = super().cargaExcelVariable(plantilla, 'str')
        self.__fichero = self.fichero_init()


    @property
    def datos(self):
        return self.__datos

    @property
    def acciones(self):
        return self.__acciones

    @property
    def fichero(self):
        return self.__fichero

    def iniciarScraper(self):
        if self.datos['TIPO'] == 'SELENIUM':
            scraper = WebScraperSelenium(self.datos, self.acciones, self.fichero)
        else:
            scraper = None
        if self.datos['TIPO'] != '':
            super().renombra_Mueve_Descargas(self.datos)
        if self.datos['MANDA_MAIL'] == 'SI':
            super().prepara_manda_mail(self.datos)
        return scraper