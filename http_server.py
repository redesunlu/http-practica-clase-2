#!/usr/bin/env python3
# coding: utf-8
from http.server import BaseHTTPRequestHandler, HTTPServer
from datetime import datetime

HOST_NAME = 'localhost'
PORT = 8000


def detectar_so(user_agent):
    # Ver listados en http://www.useragentstring.com/pages/useragentstring.php
    if 'Linux' in user_agent:
        return b'Veo que Ud. esta usando Linux como S.O.'
    elif 'Windows' in user_agent:
        return b'Veo que Ud. esta usando Windows como S.O.'
    else:
        return b'No conozco su S.O.'


def get_hora_actual():
    dt_string = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    return bytes(dt_string, 'utf-8')


def get_pagina_ok():
    """ Función que dvuelve la página de exito de ejemplo """
    # Como alternativa podría abrirse un archivo del disco, leerlo y devolverlo
    # como cadena de texto.
    return (b'<html><head><title>Pagina HTML de ejemplo</title>'
            b'</head><body><p>Esta es una prueba, con texto en <b>negrita</b>,'
            b'<i>cursiva</i> e incluso una imagen externa:</p>'
            b'<img src="http://www.labredes.unlu.edu.ar/themes/glossyblue/images'
            b'/header-bg.jpg" />')


class Handler(BaseHTTPRequestHandler):
    def do_GET(server):
        """Respondo a una petición de tipo GET"""
        # Imprimo los encabezados por consola
        print('-' * 80)
        print(server.command, server.path, server.request_version)
        print(server.headers)

        # TODO: Parsear parámetros del GET (el querystring)

        # Devuelvo la respuesta
        if server.path.startswith('/ir_a/'):
            ir_a = server.path.split('/')[-1]
            server.send_response(302)
            server.send_header('Location', 'http://' + ir_a)
            server.end_headers()
        elif server.path.startswith('/no_existe'):
            server.send_response(404)
            server.send_header('Content-Type', 'text/plain')
            server.end_headers()
            server.wfile.write(b'Pagina no encontrada')
        else:
            server.send_response(200)
            server.send_header('Content-Type', 'text/html')
            server.end_headers()
            server.wfile.write(get_pagina_ok())
            server.wfile.write(b'<p>' + detectar_so(server.headers['User-Agent']))
            server.wfile.write(b' y la fecha y hora actual es ' + get_hora_actual() + b'<br />')
            archivo_texto = open('/proc/cpuinfo', 'r').read(100)
            server.wfile.write(bytes(archivo_texto, 'utf-8'))
            server.wfile.write(b'</p></body></html>')

    def log_message(*args):
        """ Deshabilito la salida por defecto del servidor """
        pass


if __name__ == '__main__':
    http_server = HTTPServer((HOST_NAME, PORT), Handler)
    print('Ejecutando Server HTTP - %s:%s' % (HOST_NAME, PORT))
    print('Presione Ctrl+C para detener...')
    try:
        http_server.serve_forever()
    except KeyboardInterrupt:
        pass
    http_server.server_close()
    print('Deteniendo Server HTTP - %s:%s' % (HOST_NAME, PORT))
