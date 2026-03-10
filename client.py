import socket
import threading


def listener(s):
    while True:
        try:
            data = s.recv(1024)
            if not data:
                print("Server ukoncil spojenie")
                break
            message = data.decode('utf-8')
            print(f"Server odpovedal: {message}")
        except socket.timeout:
            print(".", end="", flush=True)
        except Exception as e:
            print(f"Chyba prijimania: {e}")
            break


def send_loop(s):
    while True:
        msg = input()
        if msg.strip().lower() in ['quit', 'exit', '']:
            print("Ukoncujem...")
            break
        try:
            s.sendall(msg.encode('utf-8'))
        except socket.timeout:
            print("Timeout posielania (5s)")
        except Exception as e:
            print(f"Chyba posielania: {e}")
            break


HOST = '127.0.0.1'
PORT = 65432


def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(5)  # socket timeout pre sendall() a pre recv()
    try:
        # 3-way handshake
        s.connect((HOST, PORT))
        print("Pripojeny k serveru, mozes pisat spravy.")
        # vlakno na prijimanie sprav
        t = threading.Thread(target=listener, args=(s,))
        t.daemon = True
        t.start()
        # send loop
        send_loop(s)
    except KeyboardInterrupt:
        print("Ukoncujem...")
    except Exception as e:
        print(f"Chyba: {e}")

    # ukoncenie spojenia
    try:
        s.shutdown(socket.SHUT_WR)
        t.join()  # cakame, kym vlakno skonci
        s.close()
        print("Spojenie ukoncene.")
    except:
        pass


if __name__ == "__main__":
    main()
