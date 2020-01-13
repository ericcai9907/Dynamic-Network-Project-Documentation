import socket
import time
import struct
import statistics
#import numpy as np

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
    delay = []
    p = 54000
    s = socket.socket()
    h = "169.234.19.57"
    conn = create_connection(s, p, h)
    w = open("imagetransferdelay.txt",'a')
    for i in range(4):
        sent_timestamp = time.time()
        print("Sent @: ", sent_timestamp)
        send_file("lol.jpg", conn)
        data = conn.recv(1024)
        recv_timestamp = struct.unpack('!d',data)[0]
        print("Recv @: ", recv_timestamp)
        results = '{}\t\t{}\t\t{}\n'.format(sent_timestamp,
                                            recv_timestamp,
                                            recv_timestamp - sent_timestamp)
        w.write(results)
        delay.append(sent_timestamp - recv_timestamp)
    close_connection(conn)
    w.write("MEAN\t\t\t\tSTANDARD DEVIATION\t\tVARIANCE\n")
    stats = '{}\t\t{}\t\t{}\n'.format(statistics.mean(delay),
                                        statistics.stdev(delay),
                                        statistics.variance(delay))
    w.write(stats)
    w.close()
    
