# servidor.py
# Código servidor de um sistema de upload de arquivos via UDP. Um servidor UDP recebe as partes dos arquivos
# (1024 bytes), verifica ao final a integridade via um checksum (MD5) e armazena o arquivo em uma pasta padrão (shared/).
# Autor: Lucas Souza Santos 
# Data de Criação: 10/08/2020
# Ultima atualização: 14/08/2020

import socket
import hashlib

UDP_IP = "127.0.0.1"
UDP_PORT = 5005

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

# Esta função recebe um arquivos via socket udp, verifica a integridade
# e os salva no diretório /shared
def recebe():

  while (True):
    arquivo = b''   # Concatenar as partes do arquivo aqui
    numPacote = 0   # Numero do pacote que acabou de chegar
    qtdPacotes = 0  # Quantidade de pacotes que irão chegar
    
    hash_md5 = hashlib.md5()

    while(True):
      data, addr = sock.recvfrom(1024)
      # Descobre a quantidade total de pacotes e o nome do arquivo
      if(numPacote == 0):
        nome = data.decode('utf-8').split('|')[-1]
        qtdPacotes = round(int(data.decode('utf-8').split('|')[0])/1024 + 2 +0.5)
      
      # Verifica se o pacote que chegou é o último
      elif(numPacote == qtdPacotes -1):
        md5 = data.decode('utf-8')  # Pega hash md5
        break
      
      else:
        arquivo += data             # Concatena as partes do arquivo
        hash_md5.update(data)       # Atualiza md5
      
      numPacote += 1
      pass

    # Verifica integridade do arquivo comparando o hash md5 gerado
    # com o hash md5 que veio no último pacote
    if(hash_md5.hexdigest() == md5):
      print(nome + " Recebido e salvo na pasta shared/")
      sock.sendto("0".encode('utf-8'), addr)  # Envia status de recebimento do arquivo

      # Transforma as partes do arquivo em um só, gravando no diretório shared/
      with open('shared/' + nome, 'wb') as chunk_file:
        chunk_file.write(arquivo)

    else:
      print("Problemas com a integridade do arquivo " + nome)
      sock.sendto("1".encode('utf-8'), addr)  # Envia status de recebimento do arquivo

def main():
  recebe()

main()