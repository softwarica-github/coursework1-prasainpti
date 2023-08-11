import socket
import threading
import os

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def scan_tcp_port(target_host, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((target_host, port))
        if result == 0:
            print(f"Port {port} (TCP) on {target_host} is open.")
        else:
            print(f"Port {port} (TCP) on {target_host} is closed.")
        sock.close()
    except:
        print(f"An error occurred while scanning port {port} (TCP) on {target_host}.")

def scan_udp_port(target_host, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(1)
        sock.sendto(b'', (target_host, port))
        data, addr = sock.recvfrom(1024)
        print(f"Port {port} (UDP) on {target_host} is open.")
        sock.close()
    except:
        print(f"Port {port} (UDP) on {target_host} is closed.")

def range_port_scan(target_host, port_start, port_end, scan_tcp=True, scan_udp=False):
    print(f"Scanning ports {port_start} to {port_end} on {target_host}...\n")
    for port in range(port_start, port_end + 1):
        if scan_tcp:
            t = threading.Thread(target=scan_tcp_port, args=(target_host, port))
            t.start()
        if scan_udp:
            t = threading.Thread(target=scan_udp_port, args=(target_host, port))
            t.start()

def ping_ip(target_host):
    try:
        response = os.system("ping -c 1 " + target_host)
        if response == 0:
            print(f"Host {target_host} is reachable.")
        else:
            print(f"Host {target_host} is unreachable.")
    except Exception as e:
        print("Error occurred:", e)

def banner_grabbing(target_host, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)
        sock.connect((target_host, port))
        sock.send(b'GET / HTTP/1.1\r\n')
        banner = sock.recv(1024)
        print(f"Banner for port {port} on {target_host}:\n{banner.decode()}")
        sock.close()
    except:
        print(f"Could not grab banner for port {port} on {target_host}.")

if __name__ == "__main__":
    while True:
        clear_screen()
        print("Menu:")
        print("1. Individual Port Scan (TCP/UDP)")
        print("2. Range Port Scan (TCP/UDP)")
        print("3. Ping the IP Address")
        print("4. Banner Grabbing (TCP)")
        print("5. Exit")

        choice = input("Enter your choice (1/2/3/4/5): ")

        if choice == "1":
            target_host = input("Enter the target IP address or domain name: ")
            port = int(input("Enter the port to scan: "))
            scan_tcp_port(target_host, port)
            scan_udp_port(target_host, port)
            input("Press Enter to continue...")

        elif choice == "2":
            target_host = input("Enter the target IP address or domain name: ")
            port_start = int(input("Enter the starting port: "))
            port_end = int(input("Enter the ending port: "))
            scan_tcp = input("Scan TCP ports? (Y/N): ").lower() == 'y'
            scan_udp = input("Scan UDP ports? (Y/N): ").lower() == 'y'
            range_port_scan(target_host, port_start, port_end, scan_tcp, scan_udp)
            input("Press Enter to continue...")

        elif choice == "3":
            target_host = input("Enter the IP address or domain name to ping: ")
            ping_ip(target_host)
            input("Press Enter to continue...")

        elif choice == "4":
            target_host = input("Enter the target IP address or domain name: ")
            port = int(input("Enter the port to grab the banner from: "))
            banner_grabbing(target_host, port)
            input("Press Enter to continue...")

        elif choice == "5":
            print("Exiting...")
            break

        else:
            print("Invalid choice. Please try again.")
            input("Press Enter to continue...")
