import xmlrpclib

from conf.settings import SERVICE_PORT, SERVICE_NAME, SERVICE_HOST


url = "http://%s:%s/%s" % (SERVICE_HOST, SERVICE_PORT, SERVICE_NAME)
server = xmlrpclib.ServerProxy(url)


def open_door():
    try:
        server.OpenDoor(1)
        print "SUCCESS"
        return True
    except Exception as ex:
        print "exception", ex
        return False

