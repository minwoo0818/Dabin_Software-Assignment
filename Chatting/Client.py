import socket
import threading
import json
import sys

# 서버 설정
HOST = '127.0.0.1'  # 서버의 IP 주소
PORT = 9999        # 서버의 포트 번호

def receive_messages(client_socket):
    """
    서버로부터 메시지를 수신하는 스레드.
    이 함수는 별도의 스레드에서 실행되어 메시지를 실시간으로 받습니다.
    """
    while True:
        try:
            # 메시지 수신 (1024바이트)
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                # 받은 메시지를 화면에 출력
                print(message)
            else:
                # 메시지가 없으면 연결이 끊긴 것으로 판단
                break
        except:
            # 오류 발생 시 (예: 서버가 종료됨)
            print("서버 연결이 끊겼습니다.")
            break
    # 스레드 종료
    sys.exit()

def start_client():
    """
    클라이언트를 시작하고 메시지를 전송하는 주 루프 함수.
    """
    # TCP 소켓 생성
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        # 서버에 연결 시도
        client_socket.connect((HOST, PORT))
    except ConnectionRefusedError:
        print("서버에 연결할 수 없습니다. 서버가 실행 중인지 확인하세요.")
        return

    print("서버에 연결되었습니다.")
    
    # 1. 닉네임 입력 및 서버로 전송
    nickname = input("닉네임을 입력하세요: ")
    # JSON 형식으로 닉네임 데이터를 만들어 서버로 보냅니다.
    client_socket.sendall(json.dumps({'username': nickname}).encode('utf-8'))

    # 메시지 수신을 위한 스레드 시작
    # 이 스레드는 사용자가 메시지를 입력하는 동안에도 실시간으로 메시지를 받습니다.
    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    receive_thread.daemon = True
    receive_thread.start()
    
    # 2. 메시지 전송 루프
    while True:
        # 사용자로부터 메시지 입력 받기
        message = input()
        if message.lower() == 'quit':
            break
        
        # 3. 메시지 형식에 따라 1:1 또는 1:N 메시지 생성
        if message.startswith("/to"):
            # "/to 닉네임 메시지 내용" 형식으로 1:1 메시지 생성
            try:
                parts = message.split(' ', 2)
                recipient = parts[1]
                content = parts[2]
                payload = {'to': recipient, 'message': content}
            except IndexError:
                print("잘못된 형식입니다. '/to 닉네임 메시지' 형식으로 입력하세요.")
                continue
        else:
            # 1:N 메시지인 경우, 'to' 필드 없이 메시지 내용만 담습니다.
            payload = {'message': message}
            
        try:
            # JSON 형식으로 메시지를 서버에 전송
            client_socket.sendall(json.dumps(payload).encode('utf-8'))
        except:
            print("메시지 전송에 실패했습니다.")
            break
            
    # 4. 클라이언트 소켓 닫기
    client_socket.close()

if __name__ == "__main__":
    start_client()