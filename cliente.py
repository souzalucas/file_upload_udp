# cliente.py
# Código cliente de um sistema de upload de arquivos via UDP. Um servidor UDP recebe as partes dos arquivos
# (1024 bytes), verifica ao final a integridade via um checksum (MD5) e armazena o arquivo em uma pasta padrão (shared/).
# Autor: Lucas Souza Santos 
# Data de Criação: 10/08/2020
# Ultima atualização: 14/08/2020

import socket
import os
import hashlib
import time
import threading

UDP_IP = "127.0.0.1"
UDP_PORT = 5005
addr = (UDP_IP, UDP_PORT)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Esta funão mostra uma barra de progresso conforma o arquivo é transferido
def barraProgresso(iteracao, total, prefixo = '', sufixo = '', decimais = 1, tamanho = 100, preenchido = '█'):

    porcentagem = ("{0:." + str(decimais) + "f}").format(100 * (iteracao / float(total)))
    tamanhoPreenchido = int(tamanho * iteracao // total)
    barra = preenchido * tamanhoPreenchido + '-' * (tamanho - tamanhoPreenchido)
    print('\r%s |%s| %s%% %s' % (prefixo, barra, porcentagem, sufixo), end = '\r')
    # Imprimir nova linha ao concluir
    if iteracao == total: 
        print()

# Esta função envia arquivos para um servidor via sockets udp
def envia():
    print("Para enviar o arquivo é só escrever o nome e pressionar Enter! (1 arquivo por vez)\n")

    while(True):
        hash_md5 = hashlib.md5()
        # print(hash_md5)
        nome = input()                   # Pega o nome do arquivo

        if(os.path.isfile(nome)):                                       # Arquivo existe?
            tam = os.path.getsize(nome)                                 # Tamanho do arquivo
            sock.sendto((str(tam) + "|" + nome).encode('utf-8'), addr)  # Enviando no primeiro pacote o tamanho e nome do arquivo

            with open(nome, "rb") as a:
                i = 0
                for chunk in iter(lambda: a.read(1024), b""):           # Lendo arquivo em partes (1024 bytes)
                    hash_md5.update(chunk)                              # Atualizando md5
                    sock.sendto(chunk, addr)                            # Enviando parte do arquivo
                    barraProgresso(i, round(tam/1024 + 2 +0.5), prefixo = 'Progresso:', sufixo = 'Completo', tamanho = 50)
                    i += 1
                    time.sleep(0.01)

            sock.sendto(hash_md5.hexdigest().encode('utf-8'), addr)     # Enviando hash md5 por último
            barraProgresso(i+2, round(tam/1024 + 2 +0.5), prefixo = 'Progresso:', sufixo = 'Completo', tamanho = 50)

        else:
            print("Arquivo inexistente!")

# Esta função recebe o status do recebimento do arquivo pelo servidor
def recebe():
    while(True):
        data, addr = sock.recvfrom(1024)
        status = data.decode('utf-8')
        if(status == "0"):
            print("Sucesso no envio!\n")
        else:
            print("Problema com a integridade do arquivo!\n")


def main():
    # Cria uma thread para cada funcionalidade do programa
    thread_envia = threading.Thread(target=envia)
    thread_recebe = threading.Thread(target=recebe)

    # Inicia as threads criadas, para serem executadas paralelamente
    thread_envia.start()
    thread_recebe.start()

main()