"""
app.py
Aplicación web inicial de la práctica PKI con Nginx y Python.

Objetivo de esta versión:
- Atender peticiones HTTPS que llegan desde Nginx.
- Leer la información del certificado de cliente (enviado por Nginx en cabeceras).
- Mostrar al usuario autenticado sus datos básicos.
- Registrar cada acceso en un fichero de log.

IMPORTANTE:
- Nginx debe estar configurado para:
    - exigir certificado de cliente (ssl_verify_client on).
    - pasar el subject del certificado y el resultado de la verificación
      en cabeceras HTTP (por ejemplo SSL_CLIENT_SUBJECT y SSL_CLIENT_VERIFY).
"""

from flask import Flask, request
import datetime
import os

# Creamos la instancia de la aplicación Flask.
# __name__ indica a Flask dónde está la aplicación.
app = Flask(__name__)

# Ruta del fichero de log de accesos.
# Se usará para ir guardando cada acceso con fecha, nombre, email e IP.
LOG_FILE = "user_access.log"


def parse_dn(dn: str):
    """
    Función auxiliar para extraer el nombre (CN) y el email
    a partir del Subject del certificado.

    El parámetro 'dn' suele tener un formato similar a:
    /C=ES/ST=Andalucía/L=Almeria/O=MiEmpresa/OU=Usuarios/CN=Juan Perez/emailAddress=juan.perez@ejemplo.com

    De ahí queremos obtener:
        nombre = "Juan Perez"
        email  = "juan.perez@ejemplo.com"
    """

    nombre = "Desconocido"
    email = "No disponible"

    # Dividimos la cadena por "/" para separar los campos.
    partes = dn.split("/")
    for p in partes:
        p = p.strip()
        if p.startswith("CN="):
            nombre = p.replace("CN=", "", 1)
        elif p.startswith("emailAddress="):
            email = p.replace("emailAddress=", "", 1)

    return nombre, email


@app.route("/")
def index():
    """
    Ruta principal de la aplicación.
    Esta función se ejecuta cuando el usuario accede a "/".

    Su cometido:
    - Comprobar si Nginx ha verificado correctamente el certificado de cliente.
    - Extraer datos del certificado (nombre y email).
    - Registrar el acceso en un fichero de log.
    - Devolver una página HTML sencilla con la información del usuario.
    """

    # Nginx debe enviar estas cabeceras:
    # - SSL_CLIENT_SUBJECT: Subject completo del certificado del cliente.
    # - SSL_CLIENT_VERIFY:  "SUCCESS" si el certificado es válido.
    subject_dn = request.headers.get("SSL_CLIENT_SUBJECT", "")
    verify = request.headers.get("SSL_CLIENT_VERIFY", "NONE")
    tabla="<table>"
    for k, v in request.environ.items():
        tabla += f"<tr><td>{k}</td><td>{v}</td></tr>"
    tabla += "</table>"
    

    # Si la verificación no fue exitosa, no dejamos pasar al usuario.
    if verify != "SUCCESS":
        return f"""Certificado de cliente no válido o no presentado.{verify} {subject_dn}{tabla}""", 403

    # Obtenemos nombre y email a partir del subject.
    nombre, email = parse_dn(subject_dn)

    # Obtenemos la IP del cliente (la IP que ve Flask).
    ip = request.remote_addr

    # Fecha y hora actual.
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Línea de log.
    log_entry = f"{timestamp}, {nombre}, {email}, {ip}\n"

    # Creamos el fichero de log si no existe y escribimos la entrada.
    try:
        if not os.path.exists(LOG_FILE):
            with open(LOG_FILE, "w", encoding="utf-8") as f:
                f.write("timestamp, nombre, email, ip\n")

        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(log_entry)
    except PermissionError:
        return "Error de permisos al escribir el log. Revisa la configuración de /var/log.", 500

    # Página HTML sencilla.
    html = f"""
    <html>
        <head>
            <title>Práctica PKI con Python</title>
            <meta charset="utf-8" />
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    margin: 40px;
                    background-color: #f5f5f5;
                }}
                .container {{
                    background-color: #ffffff;
                    padding: 20px;
                    border-radius: 8px;
                    box-shadow: 0 0 10px rgba(0,0,0,0.1);
                    max-width: 600px;
                }}
                h1 {{
                    color: #2e6c80;
                }}
                p {{
                    margin: 5px 0;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Bienvenido/a, {nombre}</h1>
                <p><strong>Correo:</strong> {email}</p>
                <p><strong>IP:</strong> {ip}</p>
                <p><strong>Fecha y hora de acceso:</strong> {timestamp}</p>
                <p>Tu acceso ha sido verificado mediante un certificado de cliente emitido por la CA de la práctica.</p>
            </div>
        </body>
    </html>
    """

    return html


if __name__ == "__main__":
    # Servidor de desarrollo de Flask.
    app.run(host="127.0.0.1", port=5000, debug=True)