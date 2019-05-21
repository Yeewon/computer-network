import socket
import os
import sys
#파일의 크기를 찾아 반환하는 함수
def find_length(response):
    length_index = response.find('Content-Length:')
    connection_index = response.find('Connection:')
    content = response[length_index:connection_index - 4]
    content = content.split()
    length=int(content[1])
    return length

print("Student ID : 20165161")
print("Name : Yeewon Jung")
input = input()
cmd = input.split()

hostname = cmd[1]
portnum = int(cmd[2])
filename = cmd[3]
down_filename = filename.split('/')[3]

client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect((hostname,portnum))

request = "GET {} HTTP/1.0\r\n" \
            "Host: {}\r\n\r\n" \
            "User-agent: HW1/1.0\r\n\r\n" \
            "ID: 20165161 \r\n\r\n" \
            "Name: Yeewon Jung\r\n\r\n" \
            "Connection: close".format(filename,hostname)

client.send(request.encode())
response = b''
while True:
    content = client.recv(1024)
    if not content:break
    response += content
    file_content = response.split(b'\r\n\r\n')
    file_length = find_length(str(response))
print("Total Size {} bytes".format(file_length))
f = open(down_filename,'wb')
f.write(file_content[1])
print("Download Complete: {}, {}/{}".format(down_filename, file_length, file_length))
f.close()



















