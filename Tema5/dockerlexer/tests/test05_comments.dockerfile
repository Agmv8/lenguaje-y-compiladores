# syntax=docker/dockerfile:1
# Este es un Dockerfile de ejemplo con comentarios
FROM node:18-alpine

# Establecer directorio de trabajo
WORKDIR /usr/src/app

# Copiar archivos de dependencias primero (cache layer)
COPY package*.json ./

# Instalar dependencias
RUN npm install

# Copiar el resto del codigo fuente
COPY . .

# Variables de entorno
ENV NODE_ENV=production
ENV PORT=3000

# Puerto expuesto
EXPOSE 3000

# Comando de arranque
CMD ["node", "server.js"]
