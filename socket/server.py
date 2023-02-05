import time
import socket
import iso8583
from iso8583.specs import default_ascii as spec

# Buat socket untuk mendengarkan koneksi masuk
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('localhost', 5000))
s.listen(1)
print("server started")

sign_on_respond = {
    't': '0810',
    '7': '0903000854',
    '11': '000001',
    '39': '00',
    '70': '001'
}
echo_msg_respond = {
    't': '0810',
    '7': '0903000917',
    '11': '031380',
    '39': '00',
    '70': '301'
}

while True:
    print('wait..')
    # Tunggu koneksi masuk
    conn, addr = s.accept()
    print('Connected by', addr)

    while True:
        try:
            # Terima pesan masuk
            data = conn.recv(1024)
            print('Received message:', data)

            if data:
                # Dekode pesan masuk
                decoded, encoded = iso8583.decode(data, spec)
                iso8583.pp(decoded, spec)

                # Proses pesan ISO 8583
                # (validasi, autentikasi, pemrosesan database, dll.)
                time.sleep(1)  # simulate 3s processing

                mti = decoded["t"]


                # Periksa apakah tipe pesan adalah 0800
                if mti == '0800':
                    net_msg_type = decoded["70"]

                    # Buat pesan balasan
                    if net_msg_type == '001':
                        print("SIGN ON")
                        reply = sign_on_respond
                    elif net_msg_type == '301':
                        print("ECHO TEST")
                        reply = echo_msg_respond

                    print(f"\n{'=' * 50}")
                    print('Sending reply: ')
                    # Encode pesan balasan ke byte
                    encode_raw, encoded = iso8583.encode(reply, spec)
                    print('message encode_raw: ', encode_raw)

                    # Kirim balasan
                    conn.sendall(encode_raw)
            else:
                break
        except ConnectionResetError:
            break
    # Tutup koneksi
    conn.close()
