import datetime
import socket
import time

HOST = '192.168.0.3'  # Endereco IP do Servidor
PORT = 5000  # Porta que o Servidor esta
tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
dest = (HOST, PORT)
tcp.connect(dest)

tcp.send('id_rasp')
time.sleep(2)
total = 0
contador = 1
temperatura = 0
umidade = 0

while 1:
    msg = str("%s;%s" % (temperatura, umidade))
    tcp.send(msg)

    inicio = datetime.datetime.now()
    msg = tcp.recv(1024)
    # print(msg)
    fim = datetime.datetime.now()

    tempo = fim - inicio
    tempos = tempo.total_seconds()
    total = total + tempos

    print(total)
    print(contador)
    if contador == 100:
        media = total / 100
        print(media)
        break
    temperatura += 0.3
    umidade += 0.1
    contador += 1

tcp.close()
