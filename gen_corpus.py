import socket
import struct
import os
import glob

DELIMITER = b"-=^..^=-"
INPUT_DIR = "input_responses"
OUTPUT_DIR = "output"

os.makedirs(OUTPUT_DIR, exist_ok=True)

def load_responses():
    """Loads all files from the input_responses directory"""
    files = sorted(glob.glob(os.path.join(INPUT_DIR, "*")))
    return [open(f, "rb").read() for f in files]

def run_socks5_proxy(host='127.0.0.1', port=8080):
    responses = load_responses()
    print(f"[+] Loaded {len(responses)} responses.")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen(1)
        print(f"[+] Listening on {host}:{port}")

        conn, addr = s.accept()
        print(f"[+] Accepted connection from {addr}")

        with conn:
            session_data = b""

            # Step 1: Receive greeting
            greeting = conn.recv(2)
            if len(greeting) < 2:
                return
            version, nmethods = greeting
            methods = conn.recv(nmethods)
            session_data += greeting + methods
            print(f"[+] SOCKS5 greeting: version={version}, methods={methods}")

            # Step 2: Send method selection
            conn.sendall(b'\x05\x00')  # No authentication
            session_data += b'\x05\x00'

            # Step 3: Receive connection request
            req = conn.recv(4)
            session_data += req
            if len(req) < 4:
                print("[-] Invalid request header")
                return

            ver, cmd, rsv, atyp = req
            if atyp == 0x01:
                addr = socket.inet_ntoa(conn.recv(4))
                session_data += socket.inet_aton(addr)
            elif atyp == 0x03:
                domain_len = conn.recv(1)[0]
                domain = conn.recv(domain_len)
                addr = domain.decode()
                session_data += bytes([domain_len]) + domain
            elif atyp == 0x04:
                addr = socket.inet_ntop(socket.AF_INET6, conn.recv(16))
                session_data += socket.inet_pton(socket.AF_INET6, addr)
            else:
                print("[-] Unsupported address type")
                return

            port_bytes = conn.recv(2)
            dest_port = struct.unpack("!H", port_bytes)[0]
            session_data += port_bytes
            print(f"[+] SOCKS5 connect request to {addr}:{dest_port}")

            # Step 4: Send success response
            reply = b'\x05\x00\x00\x01' + socket.inet_aton("127.0.0.1") + struct.pack("!H", 8081)
            conn.sendall(reply)
            session_data += reply

            # Step 5: Send responses from input_responses/
            for idx, payload in enumerate(responses):
                conn.sendall(payload + DELIMITER)
                print(f"[+] Sent response #{idx + 1} ({len(payload)} bytes + delimiter)")
                session_data += payload + DELIMITER

            # Save session input for AFL reproduction
            outfile = os.path.join(OUTPUT_DIR, f"session_{os.getpid()}.bin")
            with open(outfile, "wb") as f:
                f.write(session_data)
                print(f"[+] Saved session input to {outfile}")

            '''
            # Optionally keep the connection alive
            try:
                while True:
                    data = conn.recv(1024)
                    if not data:
                        break
                    print(f"[recv] {data}")
            except Exception as e:
                print(f"[!] Error: {e}")
            '''

if __name__ == '__main__':
    run_socks5_proxy()

