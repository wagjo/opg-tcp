import socket

HOST = '127.0.0.1'  # localhost (pre testovanie)
PORT = 65432  # ľubovoľný port > 1024

# Pre TCP použijeme typ socket.SOCK_STREAM
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 1. Viažeme socket na IP + port
sock.bind((HOST, PORT))

# 2. Začneme počúvať (5 je max počet klientov čakajúcich na pripojenie)
sock.listen(5)

# 3. Prijatie spojenia (THREE WAY HANDSHAKE)
conn, addr = sock.accept()

# Teraz máme aktívne TCP spojenie (conn)
# Môžeme posielať a prijímať dáta...

# 4. Server čaká na správu od klienta
data = conn.recv(1024)
if data:
    message = data.decode('utf-8')
    print(f"Prijaté od klienta: {message}")
    # 5. Poslanie správy naspať klientovi
    conn.sendall(data)

# 6. Zatvorenie serveru
conn.close()
sock.close()