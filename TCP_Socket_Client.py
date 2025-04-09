
import socket
import os
import hashlib
import requests

# Function to calculate the SHA-1 hash of a file
def calculate_hash(file_path):
    sha1 = hashlib.sha1()
    with open(file_path, 'rb') as f:
        while True:
            data = f.read(65536)
            if not data:
                break
            sha1.update(data)
    return sha1.hexdigest()

# Function to send Session Id to the server and receive the image
def receive_image(session_id):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        server_address = ('192.168.1.221', 65440)
        client_socket.connect(server_address)

        client_socket.sendall(session_id.encode())

        image_size = int.from_bytes(client_socket.recv(4), byteorder='big')
        
        image_data = b''
        while len(image_data) < image_size:
            data = client_socket.recv(9999)
            if not data:
                break
            image_data += data

        with open('Cool_Image.png', 'wb') as f:
            f.write(image_data)

        imageHash = calculate_hash('Cool_Image.png')


        payload = {"imageHash": imageHash}
        headers = {'Session-Id': session_id, 'Content-Type': 'application/json', 'Accept': '*/*'}
        response = requests.post('http://192.168.1.221:65400/validate-image-hash', json=payload, headers=headers)

        if response.status_code == 204:
            print("Image hash validation successful.")
        else:
            print("Image hash validation failed.")

session_id = '1F196B2E-46FA-4B07-98C3-E9F9D6495E16'
receive_image(session_id)
