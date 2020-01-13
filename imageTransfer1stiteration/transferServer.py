import socket
import time

# conn: new socket object for sending and
# receiving data on connection
# address: address bound to socket

def create_connection(sock: socket, port: int, host: str) -> socket:
    sock.bind((host, port))
    sock.listen(5)
    connection, client_address = sock.accept() # accept connection returns tuple
    print("Got connection from ", client_address)
    return connection

def close_connection(conn: socket) -> None:
    conn.close()

def send_file(filename: str, conn: socket) -> None:
    f = open(filename, 'rb')
    l = f.read(1024)
    while(l):
        conn.send(l)
        l = f.read(1024)
    print("FILE SENT")
    f.close()
    conn.send(bytes("\n", 'utf-8'))

def recv_file(filename: str, conn: socket) -> None:
    with open(filename, 'wb') as f:
        while True:
            data = conn.recv(1024)
            if not data:
                break
            f.write(data)

def send_msg(message: str, conn: socket) -> None:
    conn.send(bytes(message, 'utf-8'))

def recv_msg(conn: socket, buff_size: int = 16) -> str:
    data = conn.recv(buff_size)
    received = str()
    try:
        received = str(data, 'utf-8')
    except:
        pass
    return received

if __name__ == "__main__":
    p = 52000
    s = socket.socket()
    h = "192.168.0.104"
    conn = create_connection(s, p, h)
    sent_timestamp = time.time()
    print(sent_timestamp)
    send_file("done.jpg", conn)
    print("WAITING")
    recv_timestamp = float(recv_msg(conn))
    close_connection(conn)

    w = open("imagetransferdelay.txt",'a')
    results = '{}\t\t{}\t\t{}\n'.format(sent_timestamp,recv_timestamp,recv_timestamp - sent_timestamp)
    w.write(results)
    w.close()
    
