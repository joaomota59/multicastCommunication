import socket
import struct
import sys
import netifaces as ni
import time


def myAddress(interface = 'enp0s3'):#Funcao que descobre o ip do servidor
    ni.ifaddresses(interface)
    ip = ni.ifaddresses(interface)[ni.AF_INET][0]['addr']
    return ip

def answerClient(expressao):#resposta para o cliente
    return str(eval(expressao))#retorna o resultado da expressao passada	

multicast_group = '224.3.29.71'
server_address = ('', 10000)


# Create the socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind to the server address
sock.bind(server_address)

# Tell the operating system to add the socket to
# the multicast group on all interfaces.
group = socket.inet_aton(multicast_group)
mreq = struct.pack('4sL', group, socket.INADDR_ANY)
sock.setsockopt(socket.IPPROTO_IP,socket.IP_ADD_MEMBERSHIP,mreq)

listaDeServidores = [] #vetor com 


# Receive/respond loop
while True:
    print('Esperando mensagem do cliente\n')
    data, addressCLient = sock.recvfrom(1024)#pega a msg e endereco do cliente
    try:#pega o ip do cliente e tira ele da lista de servidores
        del(listaDeServidores[listaDeServidores.index(addressCLient[0])])
    except:#se o cliente ja estiver sido deletado da lista...
        pass
    print('Recebida a entrada: {} --- do cliente {}'.format(data, addressCLient[0]))

    #print('sending acknowledgement to', address)
    #sock.sendto(b'ack-2', addressCLient) #aqui que devolte a resposta para o cliente


    ###inicio comunicacao entre os servidores####

    ###inicio configuracoes do socket dos servidores####
    ####Faz as config para os servidores poderem enviar e receber mensagens###
    multicast_group_servers = ('224.0.0.1',10001)
    sockServer = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sockServer.settimeout(0.2)
    ttl2 = struct.pack('b', 1)
    sockServer.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl2)
    try:	
        sockServer.bind(('', 10001))
        group2 = socket.inet_aton(multicast_group_servers[0])
        mreq2 = struct.pack('4sL', group, socket.INADDR_ANY)
        sockServer.setsockopt(socket.IPPROTO_IP,socket.IP_ADD_MEMBERSHIP,mreq2)
	###fim configuracoes de socket####

        messageServer = b'server on-line!'#mensagem que um servidor vai mandar p outro
    
        sockServer.sendto(messageServer,multicast_group_servers)
        time.sleep(1)
        while True:
            print('Esperando feedback dos servidores\n')
            try:
                data2, addressServer = sockServer.recvfrom(1024)#pega o dado e o endereco dos servidores
            except socket.timeout:
                print("Tempo excedido!")
                break
            else:
                print('Recebida a resposta: {} --- do servidor {}'.format(data2, addressServer[0]))
                listaDeServidores.append(int(addressServer[0].replace(".","")))
    finally:
        sockServer.close()
        print("Lista de servidores",listaDeServidores)
        ipDesteServidor = myAddress()
        print("IP deste servidor", ipDesteServidor)
        if(min(listaDeServidores)==int(ipDesteServidor.replace(".",""))):
            print("Este servidor, tem o menor IP, ira responder o Cliente")
            resposta = answerClient(data.decode())
            sock.sendto(str.encode(resposta), addressCLient)#envia a resposta para o cliente
        listaDeServidores=[]#limpa a lista de servidores dps que terminar a execucao
    ###fim comunicacao entre os servidores####
