import socket
from fields_check import *

# main server ip: 94.184.178.173
SERVER = "192.168.39.144"
PORT = 5050
ADDR = (SERVER, PORT)
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "DISCONNECT"


def start():
    server.listen()

    while True:
        client_connection, addr = server.accept()

        print(f'connection from {addr} is established')

        while True:
            received_data = client_connection.recv(1024)

            if received_data:
                # parse the message
                received_data = received_data.decode(FORMAT)

                print(f"received_data: {received_data}")

                parse_packet(client_connection, received_data)

                client_connection.close()

                print(f'Closed Connection from {addr}')

                break


def handle_location_data_upstream(client_connection, fields):

    GPS_LOCATION_TYPE = 1
    BASE_STATION_LOCATION_TYPE = 2
    WIFI_LOCATION_TYPE = 3

    location_type = int(fields[-2])

    first_location_data_index = 8
    last_location_data_index = -2

    location_data = fields[first_location_data_index: last_location_data_index]
    if location_type == GPS_LOCATION_TYPE:  # GPS:  @B#@|01|001|866058040049134|8888888888888888|0|032|20210204212708|37.79831273333333|117.36866|1|@E#@
        print(f'location type: GPS, data: {location_data}')

    elif location_type == BASE_STATION_LOCATION_TYPE:  # base station: @B#@|01|001|864891030973357|9722341295788832|1|99|20210204221039|60086,610,34,722,17|50021,610,34,722,7|50100,610,34,72 2,7|2|@E#@
        print(f'location type: Base Station, location data: {location_data}')

    elif location_type == WIFI_LOCATION_TYPE:  # WiFi: @B#@|01|001| 111112222233333 |8888888888888888|0|078|20200731024809|b8:f8:83:56:d6:8c,-63&c0:fd:84:01:03:68,-77&50:bd:5f: 62:55:bc,-77| 49835,209 45,000,460,69|49835,20945,000,460,69|49835,20945,000,460,69|49835,20945,000,460,69 |3|@E#@
        print(f'location type: WiFi, location data: {location_data}\n')

    send_confirmation_location_data_packet(client_connection)


def send_confirmation_location_data_packet(client_connection):
    confirmation_packet = "@B#@|01|002|111112222233333|0| 6D596C5F770100205B816CE25E0200205B816D7753BF002000330031003177019053002097608FD15B816CE279D15F3A7 5356C6067099650516C53F8 |20160729173850|@E#@"

    client_connection.send(confirmation_packet.encode(FORMAT))

    print(f"Sent data to client: {confirmation_packet}\n")


def handle_boot_scene(client_connection, fields):
    print("in handle_boot_scene")


uplink_handlers = {"001": handle_location_data_upstream,
                   "003": handle_boot_scene}



def parse_packet(client_connection, received_packet):
    fields = received_packet.split('|')

    try:
        check_fields(fields)
    except ValueError as e:
        print(f'check frame error has occurred: {e}')

        return

    category_code = fields[2]

    handler = uplink_handlers.get(category_code)
    handler(client_connection, fields)


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)
start()
