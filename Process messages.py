from socket import*
import os
import codecs
import sys

def check_bytes(content):
    x = content.encode('utf-8')
    return len(x)

def main(portnum):
    with socket(AF_INET,SOCK_STREAM) as serverSocket:
        serverSocket.bind(('', portnum))
        serverSocket.listen(1)

        while(True):
            connectionSocket, addr = serverSocket.accept()
            data = connectionSocket.recv(1024)
            if data == b'':
                continue
            else:
                data_list = data.decode('utf-8')
                print(data_list)

                data_list = data_list.split()
                filename = data_list[1].replace('/', '')

                if not os.path.isfile(filename):
                    print('Server Error : No such file .' + data_list[1] + '!')
                    response = "HTTP/1.0 404 NOT FOUND\r\n" \
                               "Connection: close\r\n" \
                               "ID: 20165161\r\n" \
                               "Name: Yeewon Jung\r\n" \
                               "Content-Length: 0\r\n" \
                               "Content-Type: text/html\r\n\r\n"
                    connectionSocket.send(response.encode())

                    connectionSocket.close()

                else:
                    statinfo = os.stat(filename)  # file의 바이트수 check.
                    cont_length = statinfo.st_size

                    response = "HTTP/1.0 200 OK\r\n" \
                               "Connection: close\r\n" \
                               "ID: 20165161\r\n" \
                               "Name: Yeewon Jung\r\n" \
                               "Content-Length: {}\r\n" \
                               "Content-Type: text/html\r\n\r\n".format(cont_length)
                    connectionSocket.send(response.encode())
                    f = codecs.open(filename, 'r')
                    content = f.read()
                    f.close()

                    connectionSocket.send(content.encode())
                    print('finish {} {}'.format(cont_length,check_bytes(content)))
                    print()
                    connectionSocket.close()


if __name__ == '__main__':
    print("Student ID : 20165161")
    print("Name : Yeewon Jung")
    main(int(sys.argv[1]))





