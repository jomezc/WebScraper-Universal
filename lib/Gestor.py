from lib.libExternas import ABC, abstractmethod, read_excel, datetime, os, MIMEBase, \
                                  MIMEText, MIMEMultipart, smtplib, encoders, sys


class Gestor(ABC):
    """
    Declara el método abstracto de tipo asignarMotor, sería el creador (FactoryMethod)
    """

    @abstractmethod
    def iniciarScraper(self, tipo):
        pass


    def ruta_relativa(self, ruta_relativa):
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

    def cargaExcelVariable(self, nombre, tipocol):
        """
        utiliza la función de leer excel de pandas
        :param nombre: nombre de la excel
        :param tipocol: tipo de columnas de la excel, está pensado para todas por igual
        :return: devolvemos la estructura tipo 'tabla' con pandas de la hoja de excel
        """
        try:
            return read_excel(nombre, dtype=tipocol)
        except Exception as e:  # declaramos una excepción para poder tratar los posibles errores de lectura
            print(f'{datetime.datetime.now()}:Error en el gestor al intentar cargar la excel {nombre}:{e}')

    def cargarFicheroDiccionario(self, nomFichero, separador):
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
            print(f'{datetime.datetime.now()}: Error en el gestor al intentar cargar la el fichero {nomFichero}:{e}')
        finally:
            return datos

    def fichero_init(self):
        fichero = self.datos['ENTRADA']
        if fichero != '':
            try:
                fichero_r = self.ruta_relativa('archivos/' + fichero)
                os.remove(fichero_r)
            except Exception as e:
                print(f'{datetime.datetime.now()}: Error al borrar el fichero:{e}')
        return fichero

    def renombra_Mueve_Descargas(self, datos):
        """
        Renombra los ficheros "base de cada dia a generico"
        """
        for identificador in datos['RENOMBRA'].split(','):
            try:
                for filename in os.listdir(datos['RUTA_DESCARGA']):
                    if filename.startswith(identificador):
                        try:
                            os.remove(datos['RUTA_DESTINO'] +identificador + datos['TIPO_FICHEROS'])
                        except Exception as e:
                            print(f"{datetime.datetime.now()}: no había fichero {identificador} \n Error: {e}")
                        finally:
                            os.rename(datos['RUTA_DESCARGA'] + filename,
                                      datos['RUTA_DESTINO'] + identificador + datos['TIPO_FICHEROS'])


            except Exception as e:
                print(f'Error en el Gestor al intentar listar el directorio:{e}')


    def prepara_manda_mail(self, datos):

        # CONECTAMOS VIA SMTP A GMAIL
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(datos['DIRECCION_ORIGEN'], datos['CONTRASEÑA_MAIL'])

        destinatarios = datos['DIRECCIONES_DESTINO'].strip().split(',')

        msg = MIMEMultipart()
        msg['Subject'] = datos['ASUNTO']
        msg['From'] = datos['DIRECCION_ORIGEN']

        html = """\
            <html>
            <head></head>
            <body>
            <p>Buenas, adjuntamos los archivos \n</p>
            </body>
            </html>
            """
        cuerpo = MIMEText(html, 'html')
        msg.attach(cuerpo)

        for fichero in os.listdir(self.ruta_relativa(datos['RUTA_DESTINO_PARCIAL'])):
            for identificador in datos['FICHEROS_MAIL'].split(','):
                if fichero.startswith(identificador):
                    try:
                        fichero_path = self.ruta_relativa(datos['RUTA_DESTINO_PARCIAL'] + fichero)
                        print(f'cargando fichero: {fichero}')
                        part = MIMEBase('application', "octet-stream")
                        with open(fichero_path, 'rb') as file:
                            part.set_payload(file.read())
                            encoders.encode_base64(part)
                            part.add_header('Content-Disposition', 'attachment', filename=fichero)
                            msg.attach(part)
                    except Exception as e:
                        print(f"Error aql adjuntar el archi val mail {fichero} \n Error: {e}")

        server.sendmail(msg['From'], destinatarios, msg.as_string())
