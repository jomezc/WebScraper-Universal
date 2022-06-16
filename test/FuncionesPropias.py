import os, sys, time, imaplib, email


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


def abrirFichero():
    try:
        with open(ruta_relativa('archivos/datos.txt'), 'r', encoding='utf8') as archivo:
            contenido_fichero = archivo.readlines()
    except Exception as e:
        print(e)
        contenido_fichero = None
    return contenido_fichero