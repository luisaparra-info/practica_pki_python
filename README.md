# Práctica PKI con Nginx y Python (plantilla inicial)

Este repositorio es la **plantilla base** de la práctica de
implementación de autenticación con certificados digitales usando:

- OpenSSL (para la CA y los certificados)
- Nginx (como servidor HTTPS y proxy inverso)
- Python + Flask (como aplicación web)

## Contenido del repositorio

- `app.py`  
  Aplicación Flask que:
  - recibe la información del certificado de cliente desde Nginx,
  - muestra nombre, email, IP y fecha/hora,
  - registra el acceso en `/var/log/user_access.log`.

- `requirements.txt`  
  Dependencias de Python (Flask).

- `nginx/practicapki.conf`  
  Plantilla de configuración para Nginx (sitio `practicapki`).

- `docs/INSTRUCCIONES.md`  
  Guía rápida.

## Qué NO va en este repositorio

- Claves privadas (`.key`)
- Certificados (`.crt`)
- CSRs (`.csr`)
- Certificados PKCS#12 (`.p12`)
- Ficheros de log reales

Todos esos ficheros se trabajan en `$HOME/pki` y en rutas del sistema
(` /etc/nginx/certs`, `/var/log/...`), **nunca** en el repositorio de Git.

## Pasos generales para el alumnado

1. Clonar el repositorio en `$HOME/` .
2. Crear y activar un entorno virtual de Python.
3. Instalar dependencias con `pip install -r requirements.txt`.
4. Generar la CA, el certificado de servidor y los certificados de cliente en `$HOME/pki`.
5. Copiar y adaptar la configuración de Nginx (`nginx/practicapki.conf` → `/etc/nginx/sites-available/practicapki`).
6. Copiar los certificados del servidor y la CA a `/etc/nginx/certs`.
7. Comprobar Nginx (`sudo nginx -t`) y recargar.
8. Ejecutar `python3 app.py`.
9. Acceder vía `https://...` con el certificado de cliente instalado en el navegador.
