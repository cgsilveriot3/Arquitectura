#!/bin/bash

# Verifica si hay suficientes argumentos
if [ $# -lt 1 ]; then
    echo "Uso: $0 {start|stop|restart|up|down|rm} [nombre_del_servicio|all]"
    exit 1
fi

# Acción a realizar: start, stop, restart, up, down, rm
ACTION=$1
SERVICE=$2

# Ejecuta el comando correspondiente
case "$ACTION" in
    start)
        if [ "$SERVICE" == "all" ]; then
            docker-compose start
        else
            docker-compose start $SERVICE
        fi
        ;;
    stop)
        if [ "$SERVICE" == "all" ]; then
            docker-compose stop
        else
            docker-compose stop $SERVICE
        fi
        ;;
    restart)
        if [ "$SERVICE" == "all" ]; then
            docker-compose restart
        else
            docker-compose restart $SERVICE
        fi
        ;;
    up)
        if [ "$SERVICE" == "all" ]; then
            docker-compose up -d
        else
            docker-compose up -d $SERVICE
        fi
        ;;
    down)
        if [ "$SERVICE" == "all" ]; then
            docker-compose down
        else
            echo "La opción down no es aplicable a servicios individuales. Use 'all' para bajar todos los servicios."
            exit 1
        fi
        ;;
    rm)
        if [ "$SERVICE" == "all" ]; then
            docker-compose rm -f
        else
            docker-compose rm -f $SERVICE
        fi
        ;;
    *)
        echo "Acción desconocida: $ACTION"
        echo "Uso: $0 {start|stop|restart|up|down|rm} [nombre_del_servicio|all]"
        exit 1
        ;;
esac