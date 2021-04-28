import socket
import struct
import sys
import netifaces as ni


def myAddress(interface = 'enp0s3'):#retorna o endereco do script q esta sendo usado
	ni.ifaddresses(interface)
	ip = ni.ifaddresses(interface)[ni.AF_INET][0]['addr']
	return ip

try:
    expression = input("Entre com alguma expressao para ser resolvida: ")
    eval(expression)
except:
    print("Expressao Invalida!")
    exit(0)#fecha o programa

multicast_group = ('224.3.29.71', 10000)


# Create the datagram socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Set a timeout so the socket does not block
# indefinitely when trying to receive data.
sock.settimeout(2)#tempo de 2 segundos para receber a resposta do servidor



# Set the time-to-live for messages to 1 so they do not
# go past the local network segment.
ttl = struct.pack('b', 1)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)


 


try:
    # Send data to the multicast group
    print('Enviando expressao: {!r}'.format(expression))
    sent = sock.sendto(str.encode(expression), multicast_group)


    # Look for responses from all recipients
    print('Esperando receber resposta...')
    while True:
        try:
            data, server = sock.recvfrom(16)
        except socket.timeout:#se o tempo de resposta execeder o esperado
            print('timed out, no more responses')
            break#conexao eh fechada apos o break
        else:
            print('Resultado obitido do servidor:%s é :%s '%(server[0],data.decode()))

finally:
    print('closing socket')
    sock.close()
