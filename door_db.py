__author__ = 'blues'
from settings import DB

'''
flag:
0:normal
1:resetting
2:registering
3:turning into manage status
4:manager
'''

'''
admin:
0:user
1:admin
2:super_admin
'''


class DataOperation:

    def __init__(self):
        pass

    @staticmethod
    def get_name(openid):
        result = DB.query("SELECT name FROM user WHERE openid='" + str(openid) + "'")
        result = list(result)
        if len(result) == 0:
            return None
        else:
            return result[0].name

    @staticmethod
    def get_keyword(openid):
        result = DB.query("SELECT keyword FROM user WHERE openid='" + str(openid) + "'")
        result = list(result)
        if len(result) == 0:
            return None
        else:
            return result[0].keyword

    @staticmethod
    def check_flag(openid):
        try:
            result = DB.query("SELECT flag FROM user WHERE openid='" + str(openid) + "'")
            result = list(result)
            if len(result) == 0:
                return None
            else:
                return result[0].flag
        except Exception as ex:
            print "change_flag:Exception:", ex
            return False

    @staticmethod
    def change_flag(openid, flag):
        try:
            DB.query("UPDATE user SET flag='" + str(flag) + "' WHERE openid='" + str(openid) + "'")
            return True
        except Exception as ex:
            print "change_flag:Exception:", ex
            return False

    @staticmethod
    def change_keyword(openid, keyword):
        try:
            DB.query("UPDATE user SET keyword='" + str(keyword) + "' WHERE openid='" + str(openid) + "'")
            return True
        except Exception as ex:
            print "change_keyword:Exception:",ex
            return False

    @staticmethod
    def change_name(openid, name):
        try:
            DB.query("UPDATE user SET name='" + str(name) + "' WHERE openid='" + str(openid) + "'")
            return True
        except Exception as ex:
            print "change_name:Exception:", ex
            return False

    @staticmethod
    def register_user_temp(openid, name, flag, keyword, admin):
        try:
            DB.insert('user', openid=openid, name=name, flag=flag, keyword=keyword, admin=admin)
            return True
        except Exception as ex:
            print "add_user_temp:Exception:", ex
        return False

    @staticmethod
    def delete_user_temp(content, method):
        try:
            if method == 0:
                DB.query("DELETE FROM user WHERE openid='" + str(content) + "'")
            elif method == 1:
                DB.query("DELETE FROM user WHERE name='" + str(content) + "'")
            else:
                return False
            return True
        except Exception as ex:
            print "delete_user_temp:Exception:", ex
        return False

    @staticmethod
    def register_user(openid, name):
        try:
            DB.query("UPDATE user SET openid='" + str(openid) + "' WHERE name='" + str(name) + "'")
            return True
        except Exception as ex:
            print "add_user:Exception:", ex
        return False

    @staticmethod
    def add_user(name, keyword):
        try:
            DB.insert('user', openid='#', name=name, flag=0, keyword=keyword, admin=0)
            return True
        except Exception as ex:
            print "add_user:Exception:", ex
        return False

    @staticmethod
    def check_permission(name):
        try:
            result = DB.query("SELECT openid FROM user WHERE name='" + str(name) + "'")
            result = list(result)
            if len(result) == 0:
                return False
            else:
                return True
        except Exception as ex:
            print "Exception:", ex
            return False

    @staticmethod
    def check_admin(content, method):
        try:
            if method == 0:
                result = DB.query("SELECT admin FROM user WHERE openid='" + str(content) + "'")
                result = list(result)
            elif method == 1:
                result = DB.query("SELECT admin FROM user WHERE name='" + str(content) + "'")
                result = list(result)
            else:
                return False

            if len(result) == 0:
                return None
            elif result[0].admin == 1 or result[0].admin == 2:
                return True
            else:
                return False
        except Exception as ex:
            print "Exception:", ex
            return False

    @staticmethod
    def check_super_admin(openid):
        try:
            result = DB.query("SELECT admin FROM user WHERE openid='" + str(openid) + "'")
            result = list(result)
            if len(result) == 0:
                return None
            elif result[0].admin == 2:
                return True
            else:
                return False
        except Exception as ex:
            print "Exception:", ex
            return False

    @staticmethod
    def change_admin(name, direction):
        try:
            if direction == 0:
                DB.query("UPDATE user SET admin=1 WHERE name='" + str(name) + "'")
                return True
            elif direction == 1:
                DB.query("UPDATE user SET admin=0 WHERE name='" + str(name) + "'")
                return True
            else:
                return False
        except Exception as ex:
            print "change_flag:Exception:", ex
            return False
