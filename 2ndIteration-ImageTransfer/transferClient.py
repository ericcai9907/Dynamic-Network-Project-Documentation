import socket
import time
import struct
import sys

def connect_to(sock: socket, port: int, host: str) -> None:
    ''' Establishes a connection to a server, given hostname, port #, and a
        socket '''
    sock.connect((host,port))
    print("Got connection from (",host, ",", port,")")

def close_connection(sock: socket) -> None:
    ''' Closes connection(s) given a socket '''
    sock.close()

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

def recv_file(filename: str, filesize: int, conn: socket) -> None:
    with open(filename, 'wb') as f:
        while filesize > 0:
            data = conn.recv(1024)
            if not data:
                break
            #print(repr(data))
            f.write(data)
            filesize = filesize - 1024


if __name__ == "__main__":
    host = "127.0.0.1"
    port = 49000
    if len(sys.argv) != 4:
        print('Pass the server IP, port, image, and output filename as the sole command line argument.')
    else:
        for i in range(4):
            #fname = 'download_{}'.format(i) make multiple files instead of 1
            sock = socket.socket()
            connect_to(sock, int(sys.argv[2]) + i, sys.argv[1])
            data = sock.recv(1024)
            img_size = struct.unpack('!i', data)[0]
            fname = sys.argv[3]
            recv_file(fname + '_' + str(i), img_size, sock)
            recv_timestamp = time.time()
            data = struct.pack('!d',recv_timestamp)
            sock.send(data)
            print("Recv @: ", recv_timestamp)
            print("Done receiving file")
            close_connection(sock)

    


