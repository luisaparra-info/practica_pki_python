docs/INSTRUCCIONES.md
# Instrucciones básicas para la práctica PKI con Nginx y Python

## 1. Clonar el repositorio

En tu `$HOME`:

cd $HOME
git clone <URL_DEL_REPOSITORIO_CLASSROOM> practica-pki-python
cd practica-pki-python

2. Crear y activar entorno virtual
python3 -m venv venv
source venv/bin/activate

3. Instalar dependencias
pip install -r requirements.txt

4. Generar la PKI en $HOME/pki

Sigue el enunciado de la práctica para:

Crear la CA en $HOME/pki/ca

Crear el certificado de servidor en $HOME/pki/servidor

Crear certificados de cliente en $HOME/pki/clientes

5. Configurar Nginx

Copiar la plantilla:

sudo mkdir -p /etc/nginx/certs
sudo cp nginx/practicapki.conf /etc/nginx/sites-available/practicapki


Copiar certificados:

sudo cp $HOME/pki/servidor/servidor.crt /etc/nginx/certs/
sudo cp $HOME/pki/servidor/servidor.key /etc/nginx/certs/
sudo cp $HOME/pki/ca/ca.crt          /etc/nginx/certs/


Activar el sitio:

sudo ln -s /etc/nginx/sites-available/practicapki /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx

6. Ejecutar la aplicación Flask

Desde la carpeta del repo, con el entorno virtual activo:

python3 app.py

7. Acceso a la web

Importa tu certificado de cliente (.p12) en el navegador.

Accede a:

https://practicapki.com/


(o la IP del servidor)

Si todo está bien, el navegador te pedirá elegir un certificado y verás la página con tu nombre, correo e IP.
