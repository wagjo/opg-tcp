import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("www.example.com", 80))

request = ("GET / HTTP/1.0\r\n"
           "Host: www.example.com\r\n"
           "User-Agent: curl/8.5.0\r\n"
           "Accept: */*\r\n"
           "Connection: close\r\n"
           "\r\n")

# request = ("GET /faqs/ HTTP/1.1\r\n"
#            "Host: www.faqs.org\r\n"
#            "User-Agent: curl/8.7.1\r\n"
#            "Connection: close\r\n"
#            "Accept: */*\r\n\r\n")

s.send(request.encode("utf-8"))
s.settimeout(2)
response = b""
try:
    while True:
        data = s.recv(4096)
        if not data:
            break
        response += data
except TimeoutError:
    pass

print(response.decode("utf-8", errors="ignore"))
s.close()