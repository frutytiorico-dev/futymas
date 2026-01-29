# Imagen ligera y estable
FROM nginx:alpine

# Eliminar configuración por defecto
RUN rm -rf /etc/nginx/conf.d/*

# Copiar configuración personalizada
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Limpiar html por defecto de nginx
RUN rm -rf /usr/share/nginx/html/*

# Copiar el proyecto web limpio
COPY . /usr/share/nginx/html

# Exponer puerto
EXPOSE 80

# Ejecutar Nginx en primer plano
CMD ["nginx", "-g", "daemon off;"]
