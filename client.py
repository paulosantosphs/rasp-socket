import datetime
import socket
import threading
import time

import thread

lock_medicao = threading.Lock()


def client(id):
    global tempo_client
    global cont_client

    tempo_client = 0
    cont_client = 0

    HOST = '192.168.0.3'  # Endereco IP do Servidor
    PORT = 5000  # Porta que o Servidor esta
    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    dest = (HOST, PORT)
    tcp.connect(dest)

    tcp.send('id_client')
    time.sleep(2)
    numero_ultimos_dados = 10  # para retornar os n ultimos dados medidos

    while 1:
        tcp.send(str(numero_ultimos_dados))
        inicio = datetime.datetime.now()
        msg = tcp.recv(1024)
        fim = datetime.datetime.now()
        delta = fim - inicio
        deltas = delta.total_seconds()

        # print ("Cliente %s" % id)
        # print ("%s ultimos dados:" % numero_ultimos_dados)
        msg = msg.replace('),', ');').replace('[', '').replace(']', '')
        msg = msg.split(';')
        i = 1
        for dado in msg:
            dado = dado.split(',')
            temperatura = dado[0]
            umidade = dado[1]
            # print (" %s - Temperatura: %s - Umidade: %s" % (i, temperatura, umidade))
            i += 1

        lock_medicao.acquire()
        tempo_client += deltas
        cont_client += 1
        if cont_client == 100866:
            print("Media cliente")
            print(tempo_client / cont_client)
            lock_medicao.release()
            break
        else:
            lock_medicao.release()

    print
    "acabou"
    tcp.close()


numero_de_clientes = 1000
for i in range(numero_de_clientes):
    thread.start_new_thread(client, tuple([i]))
    print
    i
    time.sleep(0.01)

while 1:
    time.sleep(1)
