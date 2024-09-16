import socket
import struct

def wake_on_lan(mac_address):
    # Validate MAC address format
    if len(mac_address) == 17:
        sep = mac_address[2]
        mac_address = mac_address.replace(sep, '')
    elif len(mac_address) != 12:
        raise ValueError("Incorrect MAC address format")

    # Create magic packet
    magic_packet = b'\xff' * 6 + bytes.fromhex(mac_address) * 16

    # Send packet
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        s.sendto(magic_packet, ('<broadcast>', 9))

if __name__ == "__main__":
    raspberry_pi_mac = "XX:XX:XX:XX:XX:XX"
    
    try:
        wake_on_lan(raspberry_pi_mac)
        print(f"Wake-on-LAN packet sent to {raspberry_pi_mac}")
    except Exception as e:
        print(f"Error: {e}")
