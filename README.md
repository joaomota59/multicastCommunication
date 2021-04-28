# Comunicação multicast - Tutorial

## Instalação das máquinas virtuais

* Criar uma máquina no VM VirtualBox para ser o cliente
* Criar duas ou mais máquinas no VM VirtualBox para servirem como Servidores

***

## Configurações no terminal
* Ao criar cada máquina virtual faça os comandos, no terminal de cada máquina:
1. sudo apt-get update
2. sudo apt-get install net-tools


***

## Configurações necessárias

* Ao abrir o VM VirtualBox, ir em Arquivo > Preferências > Rede > Acrescentar uma nova Rede Nat (Obs: Colocar configuração como segue abaixo!).
![configuraçao Rede NAT](https://i.imgur.com/Z7HTBtE.png)
* Em seguida, selecione uma máquina virtual criada, clique com o botão direito, vá em configurações, selecione a Rede Nat que foi criada no processo anterior, assim como nas imagens abaixo(OBS: Fazer isso para cada máquina virtual que foi criada!).
![Configuração da máquina virtual](https://imgur.com/pmHrYMJ.png)
![Seleção da configuração de Rede Nat Criada](https://imgur.com/T8KwCuE.png)
* Em seguida, é necessário ativar o multicast e sua rota, para isso, no terminal de cada máquina, digite: bash scriptInitial.sh
<br> esse comando acima realizará toda essa ativação necessária.


***

## Rodando o Script
1. Rode primeiro em cada máquina(servidor) o arquivo server.py, para isso digite no terminal python3 server.py
2. Em seguida, na máquina cliente, rode o arquivo client.py, para isso digite no terminal python3 client.py
3. Entre com uma expressão aritmética na máquina cliente, em seguida, o servidor de menor IP irá dizer a resposta desta expressão!

***

## Script em Ação
* Com a entrada passada no cliente, é retomado para ele o resultado da expressão passada, assim como mostra o exemplo da imagem abaixo:
![Servidores respondendo ao cliente](https://imgur.com/Q4hliz6.png)
