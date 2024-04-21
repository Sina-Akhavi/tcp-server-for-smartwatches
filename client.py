import socket

SERVER = "192.168.39.144"
PORT = 5050
ADDR = (SERVER, PORT)
FORMAT = "utf-8"

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def send_to_server():
    # location data
    data = "@B#@|01|001|866058040049134|8888888888888888|0|032|20210204212708|37.79831273333333|117.36866|1|@E#@"
    # data = "@B#@|01|001|111112222233333|8888888888888888|1|55|20160715150323 | 1c:fa:68:13:a5:b4,-87&1c:fa:68:13:a5:b5,-61 | 49835,209 45,000, 460 ,69&49835,20945,000,460,69&49835,20945,000,460,69 | 3|@E#@"
    # data = "@B#@|01|001|864891030973357|9722341295788832|1|99|20210204221039|60086,610,34,722,17|50021,610,34,722,7|50100,610,34,72 2,7|2|@E#@"

    # uplink boot data packet
    # data = "@B#@|01|003|111112222233333|8888888888888888|1.0.1|0|14|20160715150323|125.48276|37.615124|3|@E#@"

    client.send(data.encode(FORMAT))
    print("Sent data to the server")


def receive_data():
    data = client.recv(1024).decode(FORMAT)
    print(f"Received data from server: {data}\n")


send_to_server()
receive_data()

client.close()
