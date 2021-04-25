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

multicast_group_servers = ('224.3.29.72',10000)


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

# Receive/respond loop
while True:
    print('Esperando mensagem do cliente\n')
    data, addressCLient = sock.recvfrom(1024)

    print('received {} bytes from {}'.format(len(data), addressCLient))
    print(data)

    #print('sending acknowledgement to', address)
    #sock.sendto(b'ack-2', addressCLient) arqui que devolte a resposta para o cliente
    sock.sendto(b'server',multicast_group_servers)
    print('Esperando feedback dos servidores\n')
    data, addressCLient = sock.recvfrom(1024)
    print(data)
