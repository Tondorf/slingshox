from tcpserver import TCPServer


class GameServer(TCPServer):
    def __init__(self, host, port):
        super(GameServer, self).__init__(host, port)

        for msg in ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']:
            self._broadcast_messages.append(msg)

    def _on_new_client(self, client_id):
        print(f'New client: {client_id}')

    def _on_client_message(self, message, client_id):
        print(f'Received from client {client_id}', message)
