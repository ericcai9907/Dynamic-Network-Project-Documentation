import socket
import time
import struct

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

def recv_file(filename: str, conn: socket) -> None:
    with open(filename, 'wb') as f:
        while True:
            try:
                if str(data, 'utf-8') == "\n":
                    break
            except:
                pass
            data = conn.recv(1024)
            #print(repr(data))
            if not data:
                print("BREAK")
                break
            f.write(data)
        print("OUTSIDE WHILE LOOP")


if __name__ == "__main__":
    host = "169.234.5.252"
    port = 52000
    sock = socket.socket()
    connect_to(sock, port, host)
    for i in range(4):
        #fname = 'download_{}'.format(i) make multiple files instead of 1
        fname = "download.jpg"
        recv_file(fname, sock)
        recv_timestamp = time.time()
        data = struct.pack('!d',recv_timestamp)
        print("Recv @: ", recv_timestamp)
        print("Done receiving file")
        sock.sendall(data)
    close_connection(sock)

    


