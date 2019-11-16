from tcpserver import TCPServer


class GameServer(TCPServer):
    def __init__(self, host, port):
        super(GameServer, self).__init__(host, port)

    def _on_new_client(self, client_id):
        print(f'New client: {client_id}')

    def _on_client_message(self, message, client_id):
        print(f'Received from client {client_id}', message)

    def _generate_broadcast_messages(self):
        return ['a', 'b', 'c']
