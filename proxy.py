import socket
import threading

LISTEN_PORT = 5672
RABBITMQ_HOST = 'rabbitmq'
RABBITMQ_PORT = 5672

def handle_connection(client_sock):
    print(f"[!] Conexión entrante desde {client_sock.getpeername()}")
    
    try:
        rabbit_sock = socket.create_connection((RABBITMQ_HOST, RABBITMQ_PORT))
    except Exception as e:
        print(f"[!] Error al conectar a RabbitMQ: {e}")
        client_sock.close()
        return

    def forward(src, dst):
        try:
            while True:
                data = src.recv(4096)
                if not data:
                    break
                print(f"📦 Datos: {data}")
                dst.sendall(data)
        except Exception as e:
            print(f"[!] Error al redirigir: {e}")
        finally:
            src.close()
            dst.close()

    threading.Thread(target=forward, args=(client_sock, rabbit_sock)).start()
    threading.Thread(target=forward, args=(rabbit_sock, client_sock)).start()

def start_proxy():
    proxy_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    proxy_sock.bind(('0.0.0.0', LISTEN_PORT))
    proxy_sock.listen(5)
    print(f"[+] Proxy escuchando en {LISTEN_PORT} y redirigiendo a {RABBITMQ_HOST}:{RABBITMQ_PORT}")

    while True:
        client_sock, _ = proxy_sock.accept()
        threading.Thread(target=handle_connection, args=(client_sock,)).start()

if __name__ == "__main__":
    start_proxy()
