import socket


class client:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.HOST = "5.151.91.119"
        self.PORT = 50001
        self.data = self.connect_to_server()
        # CLIENT VARIABLES

    def connect_to_server(self):
        try:
            self.client.connect((self.HOST, self.PORT))
            return self.client.recv(2048).decode()
            # WHEN CONNECTING TO SERVER SEND AND RECEIVE DATA

        except:
            print("ERRRROR")
            pass
            # IF THERE IS AN ERROR PASS

    def send_data(self, data):
        try:
            self.client.send(str.encode(data))
            return self.client.recv(2048).decode()
            # SEND DATA AND THEN RECEIVE DATA BACK

        except socket.error as e:
            # IF THERE IS AN ERROR
            str(e)

    def send_data_no_return(self, data):
        try:
            self.client.send(str.encode(data))
            # SEND DATA WITHOUT RECEIVING

        except socket.error as e:
            # IF THERE IS AN ERROR
            str(e)

    def return_data(self):
        return self.data
        # GETS INITIAL DATA WHEN A PLAYER FIRST CONNECTS

