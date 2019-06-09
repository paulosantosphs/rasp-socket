import socket
import time
import thread

def client(id):
    HOST = '127.0.0.1'  # Endereco IP do Servidor
    PORT = 5000  # Porta que o Servidor esta
    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    dest = (HOST, PORT)
    tcp.connect(dest)

    tcp.send('id_client')
    time.sleep(2)
    numero_ultimos_dados = 10 #para retornar os n ultimos dados medidos

    while 1:
        tcp.send(str(numero_ultimos_dados))
        msg = tcp.recv(1024)
        print ("Cliente %s" % id)
        print ("%s ultimos dados:" % numero_ultimos_dados)
        msg = msg.replace('),',');').replace('[','').replace(']','')
        msg = msg.split(';')
        i = 1
        for dado in msg:
            dado = dado.split(',')
            temperatura = dado[0]
            umidade = dado[1]
            print (" %s - Temperatura: %s - Umidade: %s" % (i, temperatura, umidade))
            i += 1
        #time.sleep(1)
    tcp.close()

numero_de_clientes = 100
for i in range(numero_de_clientes):
    thread.start_new_thread(client, tuple([i]))
    time.sleep(10)
