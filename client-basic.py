import socket

# Pre TCP použijeme typ socket.SOCK_STREAM
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM);

# 1. Nadviazanie spojenia - CONNECT (THREE-WAY HANDSHAKE)
sock.connect(('127.0.0.1', 65432))

# 2. Pošleme správu serveru
message = "Ahoj server! Toto je test spojenia."
data = message.encode('utf-8')
sock.sendall(data)

# 3. Prijmeme odpoveď
response = sock.recv(1024)
if response:
    message = response.decode('utf-8')
    print(f"Odpoveď od servera: {message}")

# 4. Shutdown - oznámime serveru, že už nebudeme posielať
sock.shutdown(socket.SHUT_WR)

# 5. Ešte raz recv() - počkáme, kým server všetko spracuje
final_data = sock.recv(1024)
if final_data:
    message = final_data.decode('utf-8')
    print(f"Zostávajúca odpoveď: {message}")

# 6. Zatvorenie spojenia
sock.close()