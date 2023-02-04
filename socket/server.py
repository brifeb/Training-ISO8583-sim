import time
import socket
import iso8583
from iso8583.specs import default_ascii as spec

# Buat socket untuk mendengarkan koneksi masuk
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('localhost', 5000))
s.listen(1)
print("server started")

# Tunggu koneksi masuk
while True:
    conn, addr = s.accept()
    print('Connected by', addr)

    # Terima pesan masuk
    data = conn.recv(1024)

    # Dekode pesan masuk
    decoded, encoded = iso8583.decode(data, spec)
    print('Received message:', data)
    iso8583.pp(decoded, spec)

    # Proses pesan ISO 8583
    # (validasi, autentikasi, pemrosesan database, dll.)

    mti = decoded["t"]

    # Periksa apakah tipe pesan adalah 0800
    if mti == '0800':
        # Buat pesan balasan
        reply = {
            't': '0810',
            'p': '8220000002000000',
            '1': '0400000000000000',
            '7': '0903000854',
            '11': '000001',
            '39': '00',
            '70': '001'
        }

        time.sleep(3)  # simulate 3s processing

        print(f"\n{'=' * 100}")
        print('Sending reply: ')
        # Encode pesan balasan ke byte
        encode_raw, encoded = iso8583.encode(reply, spec)
        print('message encode_raw: ', encode_raw)

        # Kirim balasan
        conn.sendall(encode_raw)

    # Tutup koneksi
    conn.close()
