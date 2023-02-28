import json

from app.models.enums.data_format_enum import DataFormatEnum
from app.services.impl.khwopa_service import KhwopaService
from app.services import db_service
import socket
from app.settings import configs

blockchain_settings = configs.blockchain_settings


def main() -> None:
    khwopa_service = KhwopaService()
    # khwopa_service.init_genesis_block()
    # khwopa_service.add_block('ram to shyam :3 btc')
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.bind((blockchain_settings.host, blockchain_settings.port))
    serversocket.listen(1)

    print(f'Blockchain listening at {blockchain_settings.host}:{blockchain_settings.port}')
    while True:
        # establish a connection
        client_socket, addr = serversocket.accept()

        print("Got a connection from %s" % str(addr))
        data = client_socket.recv(2024).decode()
        content_length_index = data.find('Content-Length') + len('Content-Length')
        content_length = int(data[content_length_index + 2:content_length_index + 2 + 2])
        actual_data = data[-content_length:]
        khwopa_service.add_block(actual_data)
        # client_socket.sendall(b'Hello from the server!')
        client_socket.close()


if __name__ == '__main__':
    main()
