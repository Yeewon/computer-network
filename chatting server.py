import select
import socket
import sys

# broadcast chat messages to all connected clients
def broadcast(input_list, server_socket, sock, message):
    for socket in input_list:
        # send the message only to peer
        if socket != server_socket and socket != sock:
            try:
                socket.send(message)
            except:
                # broken socket connection
                socket.close()
                # broken socket, remove it
                if socket in input_list:
                    input_list.remove(socket)

def chat_server(port):
    ip = '127.0.0.1'
    size = 1024

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 소켓생성
    server.bind((ip, port))  # 바인드
    server.listen(1)  # 리슨, 여기까지는 기본적인 서버 소켓 세팅
    input_list = [server]  # select 함수에서 관찰될 소켓 리스트 설정
    sd_list = []

    while True:
        # select 함수는 관찰될 read, write, except 리스트가 인수로 들어가며
        # 응답받은 read, write, except 리스트가 반환된다.
        # input_list 내에 내에 읽을 준비가 된 소켓이 있는지 감시한다.
        input_ready, write_ready, except_ready = select.select(input_list, [], [])

        # 응답받은 read 리스트 처리
        for sock in input_ready:
            # 클라이언트가 접속했으면 처리함
            if sock == server:
                if len(sd_list) <=16:
                    client, address = server.accept()
                    sd_list.append(client.fileno()) #sd를 저장한다.
                    host, port = address
                    print("Connection from host {}, port {}, socket {}".format(host, port, client.fileno()), flush=True)
                    sd_list.append(client.fileno())
                    input_list.append(client)  # input_list에 추가함으로써 데이터가 들어오는 것을 감시함
                else:
                    continue

            # 클라이언트소켓에 데이터가 들어왔으면
            else:
                message = sock.recv(size)
                if message:
                    broadcast(input_list, server, sock, message)

                # 데이터가 없는경우, 즉 클라이언트에서 소켓을 close 한경우
                else:
                    #print(sock.getpeername(), 'close', flush=True)
                    print("Connection Closed {}".format(sock.fileno()))
                    sock.close()
                    # 리스트에서 제거
                    input_list.remove(sock)

    server.close()

if __name__ == "__main__":
    port = int(input("hw3 "))
    print('Student ID : 20165161')
    print('Name : Yeewon')
    chat_server(port)





