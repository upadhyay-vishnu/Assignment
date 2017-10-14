import os
from socket import *
from threading import Thread
from concurrent.futures import ProcessPoolExecutor as Pool

pool = Pool(4)


def file_server(address, _dir):
    sock = socket(AF_INET, SOCK_STREAM)
    sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    sock.bind(address)
    sock.listen(5)
    print "starting server"
    while True:
        client, addr = sock.accept()
        print("Connection", addr)
        filename = client.recv(1024)
        filename = _dir + '/' + filename
        print filename
        read_n_lines(filename, n=10)
        Thread(target=listenToClient, args=(client, addr, filename)).start()
    sock.close()


def write_to_file(filename, text):
    with open(filename, 'a') as w:
        w.write(text)
        w.write('\n')
    read_n_lines(filename, 1)
    return text


def read_n_lines(filename, n=10):
    lines = []
    with open(filename, "r") as f:
        f.seek(0, 2)           # Seek @ EOF
        fsize = f.tell()        # Get Size
        f.seek(max(fsize - 1024, 0), 0)  # Set pos @ last n chars
        lines = f.readlines()
    lines = lines[-n:]
    for line in lines:
        print line.strip()


def listenToClient(client, address, filename):
    try:
        file_handler(client, filename)
    except Exception:
        client.close()
        return False


def file_handler(client, filename):
    while True:
        req = client.recv(10240)
        if not req:
            break
        text = str(req)
        pool.submit(write_to_file, filename, text)
        # future.result()
        # # print "this is result: %s" % result
        # resp = str(result).encode('ascii') + b'\n'
        # client.send(resp)
    print("Closed", client)


if __name__ == "__main__":
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    _dir = BASE_DIR + '/Assignment/log'
    file_server(('', 25000), _dir)
