import socket
import threading
import json
import sys

# 서버 설정
HOST = '127.0.0.1'  # 서버의 IP 주소 (로컬호스트)
PORT = 9999        # 서버의 포트 번호 9999로 설정

# 클라이언트 관리 딕셔너리 및 집합
# 'clients' 딕셔너리는 닉네임을 키로, 소켓 객체를 값으로 저장하여 1:1 통신에 사용합니다.
clients = {} 
# 'all_sockets' 집합은 모든 클라이언트 소켓을 저장하여 1:N 통신(브로드캐스트)에 사용합니다.
all_sockets = set()

def handle_client(client_socket):
    """
    각 클라이언트와의 통신을 전담하는 함수.
    이 함수는 새로운 클라이언트가 접속할 때마다 별도의 스레드에서 실행됩니다.
    """
    # 클라이언트의 IP 주소와 포트 번호 가져오기
    client_address = client_socket.getpeername()
    print(f"[새로운 연결] {client_address}에서 연결되었습니다.")

    username = None
    try:
        # 1. 클라이언트의 닉네임 수신
        #   클라이언트가 접속하자마자 자신의 닉네임을 JSON 형식으로 보냅니다.
        user_data = client_socket.recv(1024).decode('utf-8')
        user_info = json.loads(user_data)
        username = user_info['username']
        
        # 2. 사용자 정보 매핑 및 접속 알림
        #   닉네임과 소켓을 매핑하여 clients 딕셔너리에 저장합니다.
        #   all_sockets 집합에도 소켓을 추가하여 전체 클라이언트를 관리합니다.
        clients[username] = client_socket
        all_sockets.add(client_socket)
        
        print(f"사용자 '{username}'님이 접속했습니다.")
        # 모든 클라이언트에게 새로운 사용자 접속을 알립니다.
        broadcast_message(f"'{username}'님이 채팅에 참여했습니다.")
        
    except (json.JSONDecodeError, KeyError):
        # JSON 형식 오류 또는 'username' 키가 없을 경우
        print("잘못된 사용자 정보 형식입니다. 연결을 종료합니다.")
        client_socket.close()
        all_sockets.discard(client_socket) # 혹시 모를 경우를 대비해 소켓 제거
        return

    # 3. 메시지 수신 및 처리 루프
    try:
        while True:
            # 클라이언트로부터 메시지 수신
            message_data = client_socket.recv(1024).decode('utf-8')
            if not message_data:
                # 메시지가 없으면 연결이 끊긴 것으로 판단합니다.
                break
            
            message_info = json.loads(message_data)
            
            if 'to' in message_info:
                # 1:1 메시지인 경우, 'to' 필드를 확인하여 특정 사용자에게만 보냅니다.
                send_private_message(username, message_info['to'], message_info['message'])
            else:
                # 1:N (전체) 메시지인 경우, 모든 클라이언트에게 보냅니다.
                broadcast_message(f"[{username}] {message_info['message']}", client_socket)

    except Exception as e:
        # 통신 중 예외 발생 시 (예: 클라이언트가 강제 종료됨)
        print(f"[오류 발생] {username}: {e}")
    finally:
        # 4. 연결 종료 처리
        #   연결이 끊기면 clients 딕셔너리와 all_sockets 집합에서 해당 소켓을 제거합니다.
        print(f"[연결 종료] '{username}'님의 연결이 종료되었습니다.")
        clients.pop(username, None) # 딕셔너리에서 해당 사용자 제거
        all_sockets.discard(client_socket) # 집합에서 소켓 제거
        client_socket.close() # 소켓 닫기
        broadcast_message(f"'{username}'님이 채팅을 나갔습니다.")

def broadcast_message(message, sender_socket=None):
    """
    메시지를 모든 클라이언트에게 전송 (1:N 통신).
    """
    encoded_message = message.encode('utf-8')
    for sock in list(all_sockets): # 반복 중 요소가 변경될 수 있으므로 list()로 복사하여 사용
        if sock != sender_socket: # 메시지를 보낸 자신은 제외합니다.
            try:
                sock.sendall(encoded_message)
            except:
                # 전송 오류 발생 시 해당 소켓을 제거합니다.
                sock.close()
                all_sockets.discard(sock)

def send_private_message(from_user, to_user, message):
    """
    특정 사용자에게만 메시지를 전송 (1:1 통신).
    """
    # to_user의 닉네임으로 소켓을 찾습니다.
    to_socket = clients.get(to_user)
    if to_socket:
        full_message = f"[1:1 from {from_user}] {message}"
        try:
            to_socket.sendall(full_message.encode('utf-8'))
            print(f"'{from_user}' -> '{to_user}'에게 1:1 메시지 전송")
        except:
            # 전송 실패 시 해당 사용자가 오프라인 상태라고 판단합니다.
            print(f"'{to_user}'에게 메시지 전송 실패 (오프라인)")
    else:
        # 닉네임이 clients 딕셔너리에 없으면 오프라인 상태입니다.
        print(f"사용자 '{to_user}'는 현재 오프라인입니다.")

def start_server():
    """
    서버를 시작하고 클라이언트의 연결을 기다리는 주 루프 함수.
    """
    # TCP 소켓 생성 (IPv4, TCP)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 소켓을 지정된 IP와 포트에 바인딩
    server_socket.bind((HOST, PORT))
    # 클라이언트 연결 요청 대기
    server_socket.listen()
    print(f"서버가 {HOST}:{PORT}에서 대기 중입니다...")

    while True:
        # 클라이언트 연결 수락
        client_socket, _ = server_socket.accept()
        # 새로운 연결에 대해 별도의 스레드 생성
        client_thread = threading.Thread(target=handle_client, args=(client_socket,))
        client_thread.daemon = True # 메인 스레드 종료 시 서브 스레드도 함께 종료되도록 설정
        client_thread.start()

if __name__ == "__main__":
    start_server()