import sys
import datetime

reload(sys)
sys.setdefaultencoding('utf-8')


def add_log(username, user_message, user_behav):
    print "enter add log"
    dt = datetime.datetime.now()
    dt = dt.strftime('%Y-%m-%d %H:%M:%S')
    log_file = open("../log/user.log", "a+")
    log_line = username + u":" + user_message + u"r:" + user_behav + dt + "\n"
    log_file.write(log_line)
    print "write success"
    log_file.close()
    print "close success"
