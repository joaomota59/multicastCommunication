import socket
import struct
import sys
import netifaces as ni


def myAddress(interface = 'enp0s3'):
    ni.ifaddresses(interface)
    ip = ni.ifaddresses(interface)[ni.AF_INET][0]['addr']
    return ip

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
sock.setsockopt(
    socket.IPPROTO_IP,
    socket.IP_ADD_MEMBERSHIP,
    mreq)

listaDeServidores = ['192.168.100.4','192.168.100.5','192.168.100.6','192.168.100.7']


# Receive/respond loop
while True:
    print('Esperando mensagem do cliente\n')
    data, addressCLient = sock.recvfrom(1024)#pega a msg e endereco do cliente
    try:#pega o ip do cliente e tira ele da lista de servidores
        del(listaDeServidores[listaDeServidores.index(addressCLient[0])])
    except:#se o cliente ja estiver sido deletado da lista...
        pass
    print(listaDeServidores)
    print('Recebida a entrada: {} --- do cliente {}'.format(data, addressCLient[0]))

    #print('sending acknowledgement to', address)
    #sock.sendto(b'ack-2', addressCLient) arqui que devolte a resposta para o cliente


    ###inicio comunicacao entre os servidores####

    ###inicio configuracoes do socket dos servidores####
    sockServer = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sockServer.settimeout(0.2)
    ttl = struct.pack('b', 1)
    sockServer.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)	
    multicast_group_servers = ('224.3.29.72',10000)
    ###fim configuracoes de socket####


    messageServer = b'server on-line!'#mensagem que um servidor vai mandar p outro
    
    sockServer.sendto(messageServer,multicast_group_servers)
    print('Esperando feedback dos servidores\n')
    data, addressServer = sockServer.recvfrom(1024)#pega o dado e o endereco do servidor que respondeu
    print(data)
    ###fim comunicacao entre os servidores####
