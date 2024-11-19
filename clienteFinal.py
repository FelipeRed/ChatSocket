import socket as sock
import threading

def receber_mensagens():
    while True:
        try:
            mensagem = socket_cliente.recv(1024).decode()
            print(mensagem)
        except:
            print("Erro ao receber mensagem ou conexão encerrada.")
            break


HOST = (input('Digite o Host: ')) 
PORTA = int(input('Digite a Porta: ')) 

# HOST = '127.0.0.1'  # IP DO SERVIDOR
# PORTA = 9999  # PORTA DO SERVIDOR

# Criamos o socket do cliente
socket_cliente = sock.socket(sock.AF_INET, sock.SOCK_STREAM)

# Solicita conexão ao servidor (HOST,PORTA)
socket_cliente.connect((HOST, PORTA))

print("INICIANDO CHAT")
nome = input("Informe seu nome para entrar no chat:\n")

# Antes de entrar no loop enviamos o nome
socket_cliente.sendall(nome.encode())

# Iniciando thread para receber mensagens
thread_recebimento = threading.Thread(target=receber_mensagens)
thread_recebimento.start()

# Loop principal para envio de mensagens
while True:
    mensagem = input('')
    if mensagem.lower() == '/sair':
        socket_cliente.close()
        print("Chat encerrado.")
        break
    socket_cliente.sendall(mensagem.encode())