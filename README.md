# Ejemplos para las clase prácticas sobre HTTP - TyR - UNLu
  - `http_server.py`: Este es un servidor HTTP escrito en Python, al cual hay que ejecutar y luego en un browser se accede a él mediante `http://localhost:8000`. 
  La idea es pararse sobre las clases HTTPServer y BaseHTTPRequestHandler de Python para abstraerse del manejo de sockets y concentrarse un poco más cómo se ve un servidor
  web al atender peticiones de los navegadores, cómo se gestionan los encabezados, los status codes y dar una idea de cómo funcionan las páginas dinámicas.
  - `proxy.py`: Este es el script del repo original que adapté y comenté todo para que sea simple explicarlo en clase. Se trata de un proxy que al ejecutarlo sólo "proxea"
  la página de la UNLu, por ende, se lo ejecuta en una terminal y en un navegador se accede a la url `http://localhost:8080` para verlo en acción.
  La idea es complementar esto con el flujo de petición browser <-> proxy <-> servidor de la UNLu, entender y describir cómo es el manejo de headers tanto a la idea como a la vuelta (sólo entiende peticiones GET).
