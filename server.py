import datetime
import mysql.connector
import socket
import thread
import threading

HOST = ''  # Endereco IP do Servidor
PORT = 5000  # Porta que o Servidor esta

lock = threading.Lock()

def mysqlConnect():
    global mydb
    global mycursor
    try:
        mydb = mysql.connector.connect(host='localhost',
                                       database='rasp',
                                       user='rasp',
                                       password='123456',
                                       autocommit=False)
        if mydb.is_connected():
            print('Connected to MySQL database')
            mycursor = mydb.cursor()

    except mysql.connector.Error as e:
        print("Can't connect to MySQL", datetime.datetime.now())


def conectado(con, cliente):
    print 'Conectado por', cliente

    msg = con.recv(1024)
    if msg == 'id_rasp':
        print cliente, msg
        while True:
            msg = con.recv(1024)
            if not msg: break
            print 'Rasp: ', cliente, msg

            msg = str(msg).split(';')
            temperatura = float(msg[0])
            umidade = float(msg[1])

            sql = "INSERT INTO `temperatura_umidade` (`data`, `temperatura`, `umidade`) VALUES (%s,%s,%s)"
            val = (datetime.datetime.now(), temperatura, umidade)

            lock.acquire() #Tranca acesso ao recurso do BD
            mycursor.execute(sql, val)
            mydb.commit()
            lock.release() #Libera acesso ao recurso do BD

    else:
        if msg == 'id_client':
            print cliente, msg
            while True:
                msg = con.recv(1024)
                if not msg: break
                print 'Cliente: ', cliente, msg
                numero = int(msg)

                lock.acquire()  # Tranca acesso ao recurso do BD
                mycursor.execute("SELECT temperatura,umidade FROM temperatura_umidade order by id desc limit %s" % (numero))
                myresult = mycursor.fetchall()
                lock.release()  # Libera acesso ao recurso do BD

                con.send(str(myresult))


    print 'Finalizando conexao do cliente', cliente
    con.close()
    thread.exit()


tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

orig = (HOST, PORT)

tcp.bind(orig)
tcp.listen(1)


mysqlConnect()

while True:
    con, cliente = tcp.accept()
    thread.start_new_thread(conectado, tuple([con, cliente]))

tcp.close()
mydb.close()
