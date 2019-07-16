from socket import *
import threading
from definitions import IMAGES_PATH
from kivy.app import App
from kivy.config import Config
from jim import JimClient
from client_log_config import logging


cli_log = logging.getLogger('client')

enable_tracing = False

def esc_markup(msg):
    return (msg.replace('&', '&amp;')
            .replace('[', '&bl;')
            .replace(']', '&br;'))




# class ChatClient(protocol.Protocol):
#     def connectionMade(self):
#         self.transport.write('CONNECT')
#         self.factory.app.on_connect(self.transport)
#
#     def dataReceived(self, data):
#         self.factory.app.on_message(data)


# class ChatClientFactory(protocol.ClientFactory):
#     protocol = ChatClient
#
#     def __init__(self, app):
#         self.app = app

class Client(JimClient):
    def __init__(self, login, host, port):
        super().__init__(login)
        self.blockSize = 0
        self.host = host
        self.port = port
        self.connected = False
        self.chat_list = []
        self.online_users = []
        self.logon()
        self.active_chat = ''

    def logon(self):
        sock = socket(AF_INET, SOCK_STREAM)
        print('Connecting to %s:%s' % (self.host, self.port))
        cli_log.info('Connecting to %s:%s' % (self.host, self.port))
        try:
            sock.connect((self.host, self.port))
        except ConnectionRefusedError:
            cli_log.critical('Unable to connect to %s:%s' % (self.host, self.port))
            return
        except OSError as err:
            cli_log.critical('OS error: {0}'.format(err))
            return
        else:
            cli_log.info('Connected to %s:%s' % (self.host, self.port))
        msg = self.presence()
        sock.send(msg)  # Отправить сообщение presence
        print('presence message sent')
        data = sock.recv(1024)
        print('data=', data)
        msg_list = self.unpack(data)
        for msg in msg_list:
           print(msg['alert'])
        self.connected = True


class ChatApp(App):
    def connect(self):
        host = self.root.ids.server.text
        self.nick = self.root.ids.nickname.text
        print('-- connecting to ' + host)
        msg_client = Client(self.nick, host, 7777)



    def disconnect(self):
        print('-- disconnecting')
        if self.conn:
            self.conn.loseConnection()
            del self.conn
        self.root.current = 'login'
        self.root.ids.chat_logs.text = ''

    def send_msg(self):
        msg = self.root.ids.message.text
        self.conn.write('{0}:{1}'.format(self.nick, msg))
        self.root.ids.chat_logs.text += (
            '\t[b][color=2980b9]{}:[/color][/b] {}\n'
                .format(self.nick, esc_markup(msg)))
        self.root.ids.message.text = ''

    def on_connect(self, conn):
        print('-- connected')
        self.conn = conn
        self.root.current = 'chatroom'

    def on_message(self, msg):
        self.root.ids.chat_logs.text += '\t' + msg + '\n'


if __name__ == '__main__':
    Config.set('graphics', 'width', '600')
    Config.set('graphics', 'height', '900')

    ChatApp().run()



















# from kivy.app import App
# from kivy.uix.gridlayout import GridLayout
# from kivy.uix.label import Label
# from kivy.uix.textinput import TextInput
# class Login_Screen(GridLayout):
#    def __init__(self, **kwargs):
#        super(Login_Screen, self).__init__(**kwargs)
#        self.cols = 2
#        self.add_widget(Label(text='User Name'))
#        self.username = TextInput(multiline=False)
#        self.add_widget(self.username)
#        self.add_widget(Label(text='password'))
#        self.password = TextInput(password=True, multiline=False)
#        self.add_widget(self.password)
# class AppKivy(App):
#    def build(self):
#        return Login_Screen()
# if __name__ == '__main__':
#    AppKivy().run()
