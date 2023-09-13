import socket
import cv2
import pickle
import struct
import requests

def start_streaming():
    request1 = requests.get("ENTER COMMAND")
    print(request1.text)
    if request1.text == '1':
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Specify the server IP address and port.
        server_ip = 'ENTER YOUR SERVER IP'
        server_port = 'ENTER YOUR SERVER PORT WITHOUT QUOTATION MARKS'

        # Connect to the server.
        client_socket.connect((server_ip, server_port))
        print('Socket connected to server:', server_ip, 'port:', server_port)

        vid = cv2.VideoCapture(0)
        vid.set(3, 640)  # Width
        vid.set(4, 480)  # Height

        # Set desired frame rate (e.g., 30 frames per second)
        vid.set(cv2.CAP_PROP_FPS, 20)
        while vid.isOpened():
            success, frame = vid.read()
            if not success:
                break

            # Serialize the frame.
            data = pickle.dumps(frame)

            # Pack the serialized frame into a message with length information.
            message = struct.pack("Q", len(data)) + data

            # Send the message to the server.
            try:
                client_socket.sendall(message)
            except:
                pass
            if cv2.waitKey(10) == 13:
                break

        client_socket.close()
        cv2.destroyAllWindows()

start_streaming()
