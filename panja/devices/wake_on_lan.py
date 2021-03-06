import os
import socket
import struct


class WakeOnLan():
    BROADCAST_IP = '255.255.255.255'
    DEFAULT_PORT = 9

    def __init__(self, name, mac):
        self.name = name
        self.mac = mac
        self.state = False

    def update(self):
        ping = os.system("ping -c 1 " + self.name)
        self.state = 1 if ping == 0 else 0

    #####################HACK#########################
    #######Make this class behave like a switch#######
    #Must change the GUI to display different devices#
    def toggle(self):
        self.send_packet()
    ##################################################

    def create_magic_packet(self, macaddress):
        if len(macaddress) == 12:
            pass
        elif len(macaddress) == 17:
            sep = macaddress[2]
            macaddress = macaddress.replace(sep, '')
        else:
            raise ValueError('Incorrect MAC address format')

        # Pad the synchronization stream
        data = b'FFFFFFFFFFFF' + (macaddress * 16).encode()
        send_data = b''

        # Split up the hex values in pack
        for i in range(0, len(data), 2):
            send_data += struct.pack(b'B', int(data[i: i + 2], 16))
        return send_data


    def send_packet(self):
        packet = self.create_magic_packet(self.mac)

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        sock.connect((self.BROADCAST_IP, self.DEFAULT_PORT))

        sock.send(packet)

        sock.close()
