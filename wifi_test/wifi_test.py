import socket

ip_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
ip_socket.connect(("8.8.8.8", 80))
localIP = ip_socket.getsockname()[0]
print("Got local IP from 8.8.8.8:", localIP)

tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_socket.bind((localIP, 8081));

def function():
    print("Waiting BroadCast...")
    bc_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    bc_socket.bind(('', 8080))
    _, (machineIP, _) = bc_socket.recvfrom(8080)
    print("Got machine's local address:", machineIP)

    print("Send local IP to machine", localIP)
    bc_socket.connect((machineIP, 8080))
    bc_socket.send(localIP.encode())
    print("Done")

    print("Open Socket Server with port", localIP, 8081)
    tcp_socket.listen();

    print("Waiting machine...")
    conn, addr = tcp_socket.accept()
    conn.settimeout(1.0)
    print("Connected to machine: ", addr)

    while True:
        try:
            data = conn.recv(1024)
        except socket.timeout:
            break
        msg = data.decode()
        print(data.decode())

while True:
    function()
