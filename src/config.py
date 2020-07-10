class EmailConfig:
    SENDER_EMAIL = 'mr.robot.steals.your.data@gmail.com'
    SENDER_PASS = '...' # TODO set here pass

    RECEIVER_EMAIL_LIST = ['kovinevmv@gmail.com']


class ConnectionConfig:
    HOST_API = 'http://192.168.8.1'

    CHECK_ONLY_WHEN_WIFI = False
    CHECKED_LIST_OF_WIFI_ESSID = ["Local System"] # TODO set here


class OtherConfig:
    ENABLE_LOGGING = True
    MODEM_PHONE_NUMBER = '+79992295925'
    CACHE_PATH = '/home/venom/Desktop/git/HuaweiSMS/cache'


class EmailStylingConfig:
    NIGHT_THEME = True
    EMAIL_SUBJECT = 'Incoming SMS from Huawei Modem'
    EMAIL_HEADER = 'New messages'


emailConfig = EmailConfig()
connectionConfig = ConnectionConfig()
otherConfig = OtherConfig()
emailStylingConfig = EmailStylingConfig()