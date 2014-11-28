# -*- coding: utf-8 -*-
import web
from wechat_sdk import WechatBasic

import door_log
from door_keyword import keyword, reply, log_text, Status, Method, Direction
from door_db import DataOperation
from settings import TOKEN


urls = (
    '/', 'Index'
)

app = web.application(urls, globals())
token = TOKEN


class Index:

    def __init__(self):
        self.response = ''
        self.wechat = None
        self.is_admin = False
        self.openid = ''
        self.message = None
        self.result = 0
        self.user_name = ''
        self.user_keyword = ''
        self.is_super_admin = False
        pass

    def GET(self):
        arg = web.input(wechat_arg=[])
        signature = arg.signature
        timestamp = arg.timestamp
        nonce = arg.nonce

        self.wechat = WechatBasic(token=token)

        if self.wechat.check_signature(signature=signature, timestamp=timestamp, nonce=nonce):
            return arg.echostr

    def POST(self):
        data = web.data()
        arg = web.input(wechat_arg=[])

        signature = arg.signature
        timestamp = arg.timestamp
        nonce = arg.nonce

        self.wechat = WechatBasic(token=token)

        if self.wechat.check_signature(signature=signature, timestamp=timestamp, nonce=nonce):
            self.wechat.parse_data(data)
            self.message = self.wechat.get_message()

        self.openid = self.message.source

        if self.message.type == 'text':
            self.result = DataOperation.check_flag(self.openid)

            #normal status and ready to receive the keyword or admin command
            if self.result == 0:
                self.get_user_info()

                if cmp(self.message.content, keyword['reset']) == 0:
                    self.resetting()
                elif cmp(self.message.content, self.user_keyword) == 0:
                    self.open_door_success()
                elif cmp(self.message.content, keyword['manage']) == 0:
                    self.managing()
                elif cmp(self.message.content, keyword['super_manage']) == 0:
                    self.super_managing()
                else:
                    self.open_door_fail()

            #resetting status and ready to receive the new keyword
            elif self.result == 1:
                self.get_user_info()
                if (self.message.content, keyword['reset']) == 0:
                    self.reset_fail()
                else:
                    self.reset_success()

            #registering status and check user's permission
            elif self.result == 2:
                permission = self.check_permission()
                if permission:
                    self.register_success()
                else:
                    self.register_fail()

            #manage status and ready to receive the command
            elif self.result == 3:
                self.get_user_info()
                if self.message.content == u'1':
                    self.choose_magic_1()
                elif self.message.content == u'2':
                    self.choose_magic_2()
                else:
                    self.choose_magic_fail()

            #if the name which is exist will be deleted
            elif self.result == 4:
                add_name = self.message.content
                exist = DataOperation.check_permission(add_name)
                if exist:
                    DataOperation.delete_user_temp(add_name, Method.NAME)
                else:
                    DataOperation.add_user(add_name, keyword['default_key'])
                DataOperation.change_flag(self.openid, Status.READY)
                self.response_and_log('magic_success')

            elif self.result == 5:
                add_name = self.message.content
                exist = DataOperation.check_admin(add_name, Method.NAME)
                if exist:
                    DataOperation.change_admin(add_name, Direction.REDUCE)
                elif exist is None:
                    self.response_and_log('super_magic_failed')
                else:
                    DataOperation.change_admin(add_name, Direction.PROMOTE)
                    self.response_and_log('magic_success')

                DataOperation.change_flag(self.openid, Status.READY)

            #initial status
            elif self.result is None:
                if cmp(self.message.content, keyword['register']) == 0:
                    self.registering()
                else:
                    self.rejecting()

        else:
            self.response = self.wechat.response_text(reply['unknown'])

        return self.response

    def resetting(self):
        DataOperation.change_flag(self.openid, Status.RESETTING)
        self.response_and_log('resetting')

    def open_door_success(self):
        #door_rpc.open_door()
        self.response_and_log('open_success')

    def get_user_info(self):
        self.user_keyword = DataOperation.get_keyword(self.openid)
        self.user_name = DataOperation.get_name(self.openid)
        self.is_admin = DataOperation.check_admin(self.openid)

    def managing(self):
        if not self.is_admin:
            self.response_and_log('permission_deny')
        else:
            DataOperation.change_flag(self.openid, Status.MANAGING)
            self.response_and_log('managing')

    def super_managing(self):
        is_super_admin = DataOperation.check_super_admin(self.openid)
        if not is_super_admin:
            self.response_and_log('permission_deny')
        else:
            DataOperation.change_flag(self, Status.SUPER_MAGIC)
            self.response_and_log('super_managing')

    def open_door_fail(self):
        self.response_and_log('open_failed')

    def reset_success(self):
        DataOperation.change_keyword(self.openid, self.message.content)
        DataOperation.change_flag(self.openid, Status.READY)
        self.response_and_log('reset')

    def reset_fail(self):
        DataOperation.change_flag(self.openid, Status.READY)
        self.response_and_log('reset_failed')

    def register_success(self):
        self.user_name = self.message.content
        DataOperation.delete_user_temp(self.openid, Method.OPENID)
        DataOperation.register_user(self.openid, self.user_name)
        self.response_and_log('registered')

    def register_fail(self):
        DataOperation.delete_user_temp(self.openid, Method.OPENID)
        self.response_and_log('register_failed')

    def registering(self):
        DataOperation.register_user_temp(self.openid, keyword['default_name'], 2, keyword['default_key'], 0)
        self.response = self.wechat.response_text(reply['registering'])

    def rejecting(self):
        self.response = self.wechat.response_text(reply['rejected'])

    def check_permission(self):
        result = DataOperation.check_permission(self.message.content)
        if result is None:
            result = False
        return result

    def choose_magic_1(self):
        self.response_and_log('manage_magic_1')
        DataOperation.change_flag(self.openid, Status.MAGIC)

    def choose_magic_2(self):
        self.response_and_log('manage_magic_2')
        DataOperation.change_flag(self.openid, Status.MAGIC)

    def choose_magic_fail(self):
        self.response_and_log('choose_magic_failed')

    def response_and_log(self, content):
        self.response = self.wechat.response_text(reply[content])
        door_log.add_log(self.user_name, self.message.content, log_text[content])

if __name__ == "__main__":
    app.run()
else:
    application = app.wsgifunc()
