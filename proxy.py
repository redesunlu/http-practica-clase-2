#!/usr/bin/env python3
import requests
import urllib3
from http.server import BaseHTTPRequestHandler, HTTPServer
from socketserver import ThreadingMixIn

""" HTTP Proxy de ejemplo para la cursada de Teleinformática y Redes """

urllib3.disable_warnings()

hostname = 'www.unlu.edu.ar'
port = 8080

def get_headers() -> dict:
    """ Devolver el diccionario de headers que quiero enviar forzadamente al servidor real """
    headers = {
        'Host': hostname
    }

    return headers


class ProxyHTTPRequestHandler(BaseHTTPRequestHandler):
    protocol_version = 'HTTP/1.0'

    def do_HEAD(self):
        self.do_GET(body=False)  # la respuesta a un HEAD es un GET pero sin body
        return

    def do_GET(self, body=True):
        sent = False
        try:
            url = f'https://{hostname}{self.path}'  # armo el string con la URL real a la cual invocar
            req_header = dict(self.headers)  # En principio, seteamos los mismos headers del cliente
            req_header.update(get_headers())  # Actualiza los elementos del diccionario "pisando" los actuales

            print(url)  # Imprimo la petición que voy a hacer al servidor
            resp = requests.get(url, headers=req_header, verify=False)
            sent = True

            self.send_response(resp.status_code)  # Enviar el status code de la petición a nuestro cliente
            self.send_resp_headers(resp)  # Enviar los headers de la petición a nuestro cliente
            if body:  # Si devolvemos un body, escribo hacia el cliente el contenido en bytes del body obtenido
                self.wfile.write(resp.content)  # (requests se ocupa del Content-Encoding+Content-Type automáticamente)
            return
        finally:
            if not sent:
                self.send_error(404, 'error haciendo proxy de la peticion')

    def send_resp_headers(self, resp):
        respheaders = resp.headers
        for key in respheaders:
            # Limpio estos headers de la petición al servidor
            if key not in ['Content-Encoding', 'Transfer-Encoding', 'content-encoding', 'transfer-encoding',
                           'content-length', 'Content-Length', 'Date', 'date', 'Server', 'server']:
                self.send_header(key, respheaders[key])  # Envío el header del servidor al cliente
        self.send_header('Content-Length', len(resp.content))  # Envío el tamaño de la respuesta al cliente
        self.end_headers()  # Fin de headers


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """ Permite manejar las peticiones del navegador en hilos de ejecución separados """
    pass


def main():
    global hostname, port
    print(f'El servidor HTTP se está iniciando en {hostname} port {port}...')
    server_address = ('127.0.0.1', port)
    httpd = ThreadedHTTPServer(server_address, ProxyHTTPRequestHandler)
    print('El Servidor HTTP se está ejecutando como HTTP Proxy Reverso')
    httpd.serve_forever()


if __name__ == '__main__':
    main()
