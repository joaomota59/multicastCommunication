#!/bash/bin
#para rodar o script eh so fazer no terminal o comando:
#bash scriptInitial.sh
#nisso as rotas e ativacao do multicast sao feitas

sudo ifconfig enp0s3 multicast
sudo route -n add -net 224.0.0.0 netmask 240.0.0.0 dev enp0s3
#inicar o send em uma maquina e o recive nas outras

#script para iniciar a configuracao do multicast

