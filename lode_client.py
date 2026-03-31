import socket
import struct
import json
import sys

# Rovnaký protokol ako na serveri
def send_message(sock: socket.socket, msg: dict):
    data = json.dumps(msg).encode("utf-8")
    length = struct.pack("!I", len(data))
    sock.sendall(length + data)

def recv_message(sock: socket.socket) -> dict | None:
    header = b""
    while len(header) < 4:
        chunk = sock.recv(4 - len(header))
        if not chunk:
            return None
        header += chunk
    length = struct.unpack("!I", header)[0]

    data = b""
    while len(data) < length:
        chunk = sock.recv(length - len(data))
        if not chunk:
            return None
        data += chunk
    return json.loads(data.decode("utf-8"))


def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("127.0.0.1", 12345))
    print("✅ Pripojený na server!")

    name = input("Zadaj svoje meno: ").strip()

    while True:
        try:
            x_str = input("\nZadaj X (0-9) alebo 'q' pre koniec: ").strip().lower()
            if x_str == 'q':
                break
            x = int(x_str)
            y = int(input("Zadaj Y (0-9): ").strip())

            msg = {"type": "guess", "x": x, "y": y, "player": name}
            send_message(client, msg)

            resp = recv_message(client)
            if resp:
                if resp["type"] == "result":
                    if resp.get("hit"):
                        print(f"🔥 ZÁSah na ({x},{y})! Tvoje skóre: {resp['score']}")
                    else:
                        print(f"💧 Miss na ({x},{y}). Skóre: {resp.get('score', 0)}")
                elif resp["type"] == "error":
                    print("❌ Chyba:", resp["msg"])
        except ValueError:
            print("Musíš zadať čísla!")
        except:
            print("Spojenie prerušené.")
            break

    client.close()
    print("Koniec hry.")

if __name__ == "__main__":
    main()