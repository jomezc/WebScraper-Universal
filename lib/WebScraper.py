#   LIBRERIAS
from lib.libExternas import ABC, abstractmethod


class WebScraper(ABC):
    """
    Define la interfaz de objetos creada, sería el producto.
    """

    @abstractmethod  # Método abstracto, sin implementación
    def especificacion(self):
        pass

    @abstractmethod  # Método abstracto, sin implementación
    def extrae(self):
        pass

