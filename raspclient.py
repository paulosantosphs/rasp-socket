import socket
import time
HOST = '127.0.0.1'  # Endereco IP do Servidor
PORT = 5000  # Porta que o Servidor esta
tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
dest = (HOST, PORT)
tcp.connect(dest)

tcp.send('id_rasp')
time.sleep(2)

temperatura = 0
umidade = 0

while 1:
    msg = str("%s;%s" % (temperatura, umidade))
    #msg.encode('utf-8')
    print msg
    tcp.send(msg)

    temperatura += 0.3
    umidade += 0.1
    time.sleep(5)

tcp.close()