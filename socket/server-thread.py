import socket
import threading
import iso8583
from iso8583.specs import default_ascii as spec
import time


# template message
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

def handle_client(conn, client_address):
    while True:
        try:
            # Terima data dari client
            data = conn.recv(1024)

            if data:
                print('Menerima data dari', client_address, ':', data.decode())

                # Dekode pesan masuk
                decoded, encoded = iso8583.decode(data, spec)
                iso8583.pp(decoded, spec)

                # Proses pesan ISO 8583
                # (validasi, autentikasi, pemrosesan database, dll.)
                time.sleep(1)  # simulate 1s processing

                mti = decoded["t"]
                print(f'mti{mti}')

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
                    print(f"\n{'-' * 50}")
                    print('Sending reply: ')

          

                elif mti == '0200':
                    print("echo back 0200")

                    decoded['t'] = '0210'
                    decoded['39'] = '12'
                    reply = decoded

                # Encode pesan balasan ke byte
                encode_raw, encoded = iso8583.encode(reply, spec)
                print('message encode_raw: ', encode_raw)

                # Kirim data kembali ke client
                conn.sendall(encode_raw)


            else:
                break
        except:
            break

    # Tutup koneksi
    conn.close()

# Inisialisasi socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Ikat socket ke alamat IP dan port tertentu
server_address = ('localhost', 5000)
s.bind(server_address)

# Listen untuk koneksi masuk
s.listen(1)

# Terima koneksi
print('Menunggu koneksi...')
while True:
    conn, client_address = s.accept()
    print('Koneksi diterima dari', client_address)
    t = threading.Thread(target=handle_client, args=(conn, client_address))
    t.start()
