# -*- coding: utf-8 -*-
def enum(**enums):
    return type('Enum', (), enums)

Status = enum(READY=0, RESETTING=1, REGISTERING=2, MANAGERING=3, MAGIC=4)
Method = enum(OPENID=0, NAME=1)

keyword = {
    'reset': u'我需要全新的咒语',
    'register': u'让我进入这个神奇的世界',
    'default_key': u'芝麻开门',
    'default_name': u'我叫小强',
    'manage': u'我可是个高级魔法师',
}

reply = {
    'open_success': u'咒语生效，门已打开',
    'open_failed': u'咒语无效，门仍关闭',
    'registering': u'想要进入神奇的办公室，在确认你已经获得高级魔法师的许可后，请报上你的真名(请将姓名填写正确，这关乎你是否能进入魔法世界)',
    'registered': u'原来是你啊，你可以说开门咒语了',
    'reset_failed': u'嗯，不行，这一条是禁咒',
    'resetting': u'说下你的新咒语吧',
    'reset': u'好的，你的新咒语已经记下了',
    'rejected': u'噢，你好像还不是个魔法师吧',
    'unknown': u'对不起，我听不懂你在说什么',
    'permission_deny': u'你的修为还不够哦',
    'register_failed': u'哦哦，你没被高级魔法师认可哦！',
    'managing': u'高级魔法师欢迎你,你有如下两种高级魔法：1.许可新的魔法师 2.删除你已经许可的魔法师。请输入你要施展的魔法编号',
    'manage_magic_1': u'输入你许可的魔法师姓名(请将姓名填写正确，这关乎他是否能进入魔法世界)',
    'manage_magic_2': u'输入你要删除许可的魔法师姓名(请将姓名填写正确，填错了可删除不了)',
    'choose_magic_failed': u'魔法释放失败，你选择你还不会的魔法:(',
    'magic_success': u'施法成功'
}

log_text = {
    'resetting': u'正在重置',
    'open_success': u'已开门',
    'open_failed': u'开门失败',
    'reset_failed': u'重置失败',
    'reset': u'已重置',
    'registered': u'已注册',
    'permission_deny': u'试图变成高级魔法师失败',
    'managing': u'变身成高级魔法师',
    'register_failed': u'试图注册失败',
    'manage_magic_1': u'准备许可新的魔法师',
    'manage_magic_2': u'准备删除已许可的魔法师',
    'choose_magic_failed': u'魔法选择失败',
    'magic_success': u'施法成功'
}


