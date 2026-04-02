import socket
import os

# Nastavenia
HOST = "0.0.0.0"  # počúva na všetkých rozhraniach
PORT = 8080  # bežný port pre testovanie


def load_file(filename="index.html"):
    """Načíta súbor a vráti jeho obsah + MIME typ"""
    if not os.path.exists(filename):
        return b"<h1>404 - Subor index.html nebol najdeny!</h1>", "text/html"

    with open(filename, "rb") as f:  # "rb" = binary mód (pre obrázky aj html)
        content = f.read()

    # Jednoduché určenie MIME typu podľa prípony
    if filename.endswith(".html") or filename.endswith(".htm"):
        mime = "text/html"
    elif filename.endswith(".css"):
        mime = "text/css"
    elif filename.endswith(".js"):
        mime = "application/javascript"
    elif filename.endswith(".png"):
        mime = "image/png"
    elif filename.endswith(".jpg") or filename.endswith(".jpeg"):
        mime = "image/jpeg"
    else:
        mime = "application/octet-stream"

    return content, mime


# === Hlavný server ===
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # užitočné pri reštarte
server.bind((HOST, PORT))
server.listen(5)

print(f"🚀 Server beží na http://{HOST if HOST != '0.0.0.0' else 'localhost'}:{PORT}")
print("Načítaj stránku v prehliadači a skús aj refresh (F5)\n")

while True:
    client, addr = server.accept()
    print(f"📡 Pripojenie z {addr}")

    # Prijať request
    request = client.recv(4096).decode("utf-8", errors="ignore")
    print("--- REQUEST (prvých 500 znakov) ---")
    print(request[:500])

    # Načítať index.html
    content, content_type = load_file("index.html")

    # Vytvoriť HTTP odpoveď
    response = f"""HTTP/1.1 200 OK\r\nContent-Type: {content_type}; charset=utf-8\r\nContent-Length: {len(content)}\r\nConnection: close\r\n\r\n""".encode("utf-8") + content

    client.send(response)
    client.close()