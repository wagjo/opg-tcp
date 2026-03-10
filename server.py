import socket
import threading


def handle_client(conn, addr):
    conn.settimeout(5)  # connection timeout pre recv()
    print(f"Klient pripojený: {addr}")
    while True:
        try:
            data = conn.recv(1024)
            if not data:
                print(f"Klient {addr} ukončil spojenie.")
                try:
                    conn.sendall(b"Prajem pekny den")
                    conn.shutdown(socket.SHUT_WR)
                except:
                    pass
                break
            print(f"Sprava od {addr}: {data.decode('utf-8')}")
            conn.sendall(data)
        except socket.timeout:
            print(".", end="", flush=True)
        except Exception as e:
            print(f"Chyba s {addr}: {e}")
            break
    conn.close()


HOST = '127.0.0.1'
PORT = 65432


def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.settimeout(0.2)  # socket timeout pre accept()
    s.listen()
    print(f"Server bezi na {HOST}:{PORT}, cakam na klientov")
    try:
        while True:
            try:
                conn, addr = s.accept()
                thread = threading.Thread(target=handle_client, args=(conn, addr))
                thread.daemon = True
                thread.start()
            except socket.timeout:
                #print(".", end="", flush=True)
                continue
            except Exception as e:
                print(f"Chyba servera: {e}")
                break
    except KeyboardInterrupt:
        print("Server ukončený Ctrl+C")
    s.close()


if __name__ == "__main__":
    main()
