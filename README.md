# UDP file upload - Python 3 

Um sistema de upload de arquivos via UDP desenvolvido em Python 3. Um servidor UDP recebe as partes dos arquivos (1024 bytes), verifica ao final a integridade via um checksum (MD5) e armazena o arquivo em uma pasta padrão (shared/).

## Compilar/executar
  
#### Para iniciar o servidor
```
  > python3 servidor.py 
```
#### Para iniciar o cliente
```
  > python3 cliente.py 
```

## Bibliotecas
  - socket:     Este módulo fornece acesso à interface de socket BSD.

  - hashlib:    Este módulo fornece uma interface comum para muitos algoritmos de hash seguro e de resumo de mensagem.

  - os:         Este módulo fornece uma maneira de usar as funcionalidades dependentes do Sistema Operacional.

  - threading:  Este módulo constrói interfaces de threading de alto-nível no topo do módulo _thread de baixo-nível. 

  - time:       Este módulo fornece várias funções relacionadas ao tempo. 


## Exemplo de uso: Enviar o arquivo teste.png para o servidor

#### Inicie o servidor em um console
  ```
  > python3 servidor.py
```

#### Inicie o cliente em outro console
  ```
  > python3 cliente.py
```

#### Agora, no console do cliente você digita o nome do arquivo que quer enviar, e pressione Enter
  > teste.png

#### O servidor irá receber o arquivo em partes, verificar sua integridade e salvar na pasta "shared/".
