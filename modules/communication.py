import socket
import time
import json
import threading


class IPv4:
    def __init__(self, ip: str, port: int):
        self.ip = ip
        self.port = port
        self.address = (ip, port)


local_ip = socket.gethostbyname(socket.getfqdn(socket.gethostname()))


def check_and_update_ip(HOST='client'):
    with open("data/ip_address.json", "r", encoding='utf-8') as f:
        data = json.load(f)

        global local_port
        local_port = data[HOST]['port']

        if HOST == 'server':
            data['server']['ip'] = local_ip
            remote_address = IPv4(data['client']['ip'], data['client']['ip'])
            Msg = Server(HOST)
        elif HOST == 'client':
            data['client']['ip'] = local_ip
            remote_address = IPv4(data['server']['ip'], data['server']['ip'])
            Msg = Client(HOST)
        else:
            pass
    # update local "ip_address.json"
    with open("data/ip_address.json", "w", encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False)
    # send msg to update remote "ip_address.json"
    Msg.send('###' + HOST + 'ip:' + local_ip)
    Msg.close()


class Server:
    def __init__(self, HOST='server'):
        self.HOST = HOST
        self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ip = socket.gethostbyname(socket.getfqdn(socket.gethostname()))
        with open("data/ip_address.json", "r", encoding='utf-8') as f:
            data = json.load(f)
            self.port = data[self.HOST]['port']
            self.name = data[self.HOST]['name']
        self.ip_port = (self.ip, self.port)

        self.tcp_socket.bind(self.ip_port)
        print('Waiting for Client to connect...')
        self.tcp_socket.listen(5)
        self.client_socket, self.client_addr = self.tcp_socket.accept()
        print(self.client_addr)

        send_thread = threading.Thread(target=self.send)
        recv_thread = threading.Thread(target=self.recv)
        send_thread.start()
        recv_thread.start()

    def send(self):
        while True:
            content = input(":")
            now_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            msg = str(now_time) + '  ' + self.name + '\n' + content
            data = self.client_socket.send(msg.encode('utf-8'))
            print(data)
            print(msg)

    def recv(self):
        while True:
            msg = self.client_socket.recv(1024)
            print(msg.decode('utf-8'))

    def close(self):
        self.client_socket.close()


class Client:
    def __init__(self, HOST='client'):
        self.HOST = HOST
        with open("data/ip_address.json", "r", encoding='utf-8') as f:
            data = json.load(f)
            server_ip = data['server']['ip']
            server_port = data['server']['port']
            self.name = data[self.HOST]['name']
        Server = IPv4(server_ip, server_port)

        self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcp_socket.connect(Server.address)

        send_thread = threading.Thread(target=self.send)
        recv_thread = threading.Thread(target=self.recv)
        send_thread.start()
        recv_thread.start()

    def send(self):
        while True:
            content = input(":")
            now_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            msg = str(now_time) + '  ' + self.name + '\n' + content
            data = self.tcp_socket.send(msg.encode('utf-8'))
            print(data)
            print(msg)

    def recv(self):
        while True:
            msg = self.tcp_socket.recv(1024)
            print(msg.decode('utf-8'))

    def close(self):
        self.tcp_socket.close()


if __name__ == '__main__':
    server = Server()