__author__ = 'blues'
import web

TOKEN = 'zq_door'
SERVICE_HOST = "192.168.34.200"
SERVICE_PORT = "10086"
SERVICE_NAME = "DoorLib"
RESULT = 'SUCCESS'

DB = web.database(
    dbn='mysql',
    db='bluesDoorDB',
    user='root',
    pw='ziqiang%net',
    host='192.168.32.31',
    port=3306
)