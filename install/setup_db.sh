#!/bin/bash

DB_NAME="email_moonitor"
DB_USER="vicente"
DB_PASSWORD="vblp2267"
DB_HOST="81.19.160.18"


# Comprobamos si la base de datos ya existe
mysql -h "$DB_HOST" -u "$DB_USER" -p"$DB_PASSWORD" -e "USE $DB_NAME" 2>/dev/null
if [ $? -eq 0 ]; then
    echo "La base de datos $DB_NAME ya existe. No es necesario crearla."
else
    # Creamos la base de datos
    mysql -h "$DB_HOST" -u "$DB_USER" -p"$DB_PASSWORD" -e "CREATE DATABASE $DB_NAME"
    if [ $? -eq 0 ]; then
        echo "La base de datos $DB_NAME se ha creado correctamente."
    else
        echo "Error al crear la base de datos $DB_NAME."
        exit 1
    fi
fi

# Ejecutamos el script SQL para crear las tablas
mysql -h "$DB_HOST" -u "$DB_USER" -p"$DB_PASSWORD" "$DB_NAME" < create_tables.sql

if [ $? -eq 0 ]; then
    echo "Tablas creadas correctamente."
else
    echo "Error al crear las tablas."
    exit 1
fi
