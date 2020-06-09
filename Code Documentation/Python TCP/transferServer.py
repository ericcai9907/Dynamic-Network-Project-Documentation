import socket
import time
import struct
import statistics
import sys
import os
#import numpy as np

# conn: new socket object for sending and
# receiving data on connection
# address: address bound to socket

def create_connection(sock: socket, port: int, host: str) -> socket:
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # solution for: "socket.error: [Errno 98] Address already in use"
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
    f.close()

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
    p = 49000
    #s = socket.socket()
    h = "127.0.0.1"
    try:
        os.remove("imagetransferdelay.txt")
    except:
        pass
    if len(sys.argv) < 4:
        print('Pass the server IP, port, image, output filename, and result output file as the sole command line argument.')
    else:
        a = "imagetransferdelay.txt"
        try:
            a = sys.argv[4]
        except:
            pass
        w = open(a,'a')
        w.write('Sent Timestamp\t\tReceived Timestamp\t\tCalculated TimeStamp\n')
        w.write('=====================================================================================\n')
        for i in range(100):
            s = socket.socket()
            conn = create_connection(s, int(sys.argv[2]), sys.argv[1])
            img_size = os.path.getsize(sys.argv[3])
            data = struct.pack('!i', img_size)
            conn.send(data)
            sent_timestamp = time.time()
            print("Sent @: ", sent_timestamp)
            send_file(sys.argv[3], conn)
            data = conn.recv(1024)
            recv_timestamp = struct.unpack('!d',data)[0]
            print("Recv @: ", recv_timestamp)
            #difference = abs(recv_timestamp - sent_timestamp)
            results = '{}\t\t{}\t\t{}\n'.format(sent_timestamp,
                                                recv_timestamp,
                                                abs(recv_timestamp - sent_timestamp))
            w.write(results)
            delay.append(abs(recv_timestamp - sent_timestamp))
            close_connection(conn)
        w.write("MEAN\t\t\t\tSTANDARD DEVIATION\t\tVARIANCE\n")
        stats = '{}\t\t{}\t\t{}\n'.format(statistics.mean(delay),
                                            statistics.stdev(delay),
                                            statistics.variance(delay))
        w.write(stats)
        w.close()