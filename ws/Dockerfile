# Verwende das offizielle NGINX-Image als Basis
FROM nginx:latest

# Kopiere die benutzerdefinierte NGINX-Konfiguration in das Image
COPY ./nginx.conf /etc/nginx/nginx.conf

# Kopiere den Webinhalt in das NGINX-Standardverzeichnis
COPY ./html /usr/share/nginx/html

# Exponiere den Port 80 für eingehende Verbindungen
EXPOSE 80

# Starte den NGINX-Webserver
CMD ["nginx", "-g", "daemon off;"]