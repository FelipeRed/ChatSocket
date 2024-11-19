import socket as sock
import threading

def broadcast(mensagem, remetente=None):
    # Função que envia uma mensagem para para todos os usuários 
    for cliente in clientes_conectados:
        if cliente != remetente:
            try:
                cliente['socket'].sendall(mensagem.encode())
            except:
                remover_cliente(cliente)

def unicast(mensagem, destinatario):
    #def que cria o sistema de unicast, enviando apenas para um usuário específico
    for cliente in clientes_conectados:
        #se o cliente tem o nome em destinatarios ele retorna sua mensagem
        if cliente['nome'] == destinatario:
            try:
                cliente['socket'].sendall(mensagem.encode())
                return True
            except:
                remover_cliente(cliente)
                return False
    return False

def multicast(mensagem, destinatarios):
    for destinatario in destinatarios:
        unicast(mensagem, destinatario)

def remover_cliente(cliente):
    if cliente in clientes_conectados:
        clientes_conectados.remove(cliente)
        print(f"Cliente {cliente['nome']} desconectado.")
        broadcast(f"SISTEMA: {cliente['nome']} saiu do chat.")

def receber_dados(sock_conn, endereco):
    nome = sock_conn.recv(50).decode()

    cliente = {'socket': sock_conn, 'nome': nome, 'endereco': endereco}
    clientes_conectados.append(cliente)
    
    print(f"Conexão com sucesso com {nome} : {endereco}")
    broadcast(f"\nSISTEMA: {nome} entrou no chat.", cliente['socket'])
   
    while True:
        try:
            mensagem = sock_conn.recv(1024).decode()
            
            if mensagem.startswith("/unicast"):
                
                _, destinatario, msg = mensagem.split(" ", 2)
                #if para unicast onde ele encontra o usuario
                if unicast(f"[Privado de {nome}] {msg}", destinatario):
                    sock_conn.sendall(f"[Privado para {destinatario}] {msg}".encode())
                #se não ele retorna o print da mensagem não encontrada
                else:
                    sock_conn.sendall(f"SISTEMA: Usuário {destinatario} não encontrado.".encode())

            elif mensagem.startswith("/multicast"):
                partes = mensagem.split(" ")

                if ":" in partes:  # Verifica se existe dois pontos na mensagem
                    indice = partes.index(":")  # Encontra o índice do ":"

                    destinatarios = partes[1:indice]  # Destinatários são todos os itens entre o /multicast e o ":"
                    
                    # Mensagem é tudo o que vem no índice após o ":"
                    msg = ' '.join(partes[indice+1:])  # Junta todas as palavras usando um espaço em branco " "
                    
                    multicast(f"[Grupo de {nome}] {msg}", destinatarios)
            else:
                broadcast(f"{nome}: {mensagem}", sock_conn)
        except:
            remover_cliente(cliente)
            break


clientes_conectados = []

# HOST = '127.0.0.1'
HOST = '192.168.1.100'
PORTA = 9999

socket_server = sock.socket(sock.AF_INET, sock.SOCK_STREAM)
socket_server.bind((HOST, PORTA))
socket_server.listen()

print(f"O servidor {HOST}:{PORTA} está aguardando conexões...")

while True:
    sock_conn, ender = socket_server.accept()
    thread_cliente = threading.Thread(target=receber_dados, args=[sock_conn, ender])
    thread_cliente.start()