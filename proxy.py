import socket
import struct

def run_socks5_proxy(host='127.0.0.1', port=8080):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen(1)
        print(f"[+] Listening on {host}:{port}")

        conn, addr = s.accept()
        print(f"[+] Accepted connection from {addr}")

        with conn:
            # === Step 1: Receive SOCKS5 greeting ===
            version, nmethods = conn.recv(2)
            methods = conn.recv(nmethods)
            print(f"[+] Received SOCKS5 greeting: version={version}, methods={methods}")

            # === Step 2: Send SOCKS5 method selection ===
            conn.sendall(b'\x05\x00')  # Version 5, no authentication

            # === Step 3: Receive SOCKS5 connection request ===
            req = conn.recv(4)
            if len(req) < 4:
                print("[-] Invalid request header")
                return

            ver, cmd, rsv, atyp = req
            if atyp == 0x01:  # IPv4
                addr = socket.inet_ntoa(conn.recv(4))
            elif atyp == 0x03:  # Domain name
                domain_len = conn.recv(1)[0]
                addr = conn.recv(domain_len).decode()
            elif atyp == 0x04:  # IPv6
                addr = socket.inet_ntop(socket.AF_INET6, conn.recv(16))
            else:
                print("[-] Unsupported address type")
                return

            port_bytes = conn.recv(2)
            dest_port = struct.unpack("!H", port_bytes)[0]

            print(f"[+] SOCKS5 request to connect to {addr}:{dest_port}")

            # === Step 4: Send SOCKS5 success response ===
            # Telling curl "connection to target succeeded"
            reply = b'\x05\x00\x00\x01'  # Version, success, reserved, IPv4
            reply += socket.inet_aton("127.0.0.1")  # BIND address (dummy)
            reply += struct.pack("!H", 8081)        # BIND port (dummy)
            conn.sendall(reply)

            # === Step 5: Send fake HTTP response ===
            response = b"HTTP/1.1 200 OK\r\nContent-Length: 5\r\n\r\nHELLO"
            conn.sendall(response)
            print("[+] Sent dummy HTTP response")

            # Wait to keep connection open for testing
            try:
                while True:
                    data = conn.recv(1024)
                    if not data:
                        break
                    print(f"[recv] {data}")
            except Exception as e:
                print(f"[!] Error: {e}")

if __name__ == '__main__':
    run_socks5_proxy()
