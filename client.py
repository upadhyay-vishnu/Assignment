import socket                   # Import socket module
import os


def file_tail(s, file_name, _dir):
    if file_name in os.listdir(_dir):
            s.send(file_name)
    else:
        f = open(_dir + '/' + file_name, 'w')
        f.close()
        s.send(file_name)
    while True:
        inp = raw_input("write the text:")
        s.send(inp)
        if not inp:
            break


def get_filename(_dir):
    all_files = os.listdir(_dir)
    if all_files:
        print "available files are "
        for _file in all_files:
            print _file, ',',
        print '\n'
    else:
        print "There is no files available"
    print "please write a name from above files or to open a new file, give a new name"

    # print os.listdir(_dir)
    file_name = raw_input("filename: ")
    print "file %s is open to write, please write the text and press enter for next line." % file_name
    return file_name


def make_connection():
    s = socket.socket()
    host = socket.gethostname()
    s.connect((host, 25000))
    return s


def main():
    _socket = make_connection()
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    _dir = BASE_DIR + '/Assignment/log'
    _file = get_filename(_dir)
    file_tail(_socket, _file, _dir)
    _socket.close()


main()
