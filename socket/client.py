import socket
import time
import iso8583
from iso8583.specs import default_ascii as spec

# Buat socket untuk terhubung ke server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('localhost', 5000))

# Buat pesan untuk dikirim
sign_on_msg = {
    't': '0800',
    '7': '0903000854',
    '11': '000001',
    '33': '777006',
    '70': '001'}
echo_msg = {
    't': '0800',
    '7': '0903000917',
    '11': '031380',
    '70': '301'
}

#TODO: Kirim Sign On terlebih dahulu, jika approve (bit 39 = 00) lanjut ke echo test


while True:
    # Encode pesan ke byte
    encoded_raw, encoded = iso8583.encode(echo_msg, spec)
    print('Sending message: ', encoded_raw)
    iso8583.pp(encoded, spec)

    # Kirim pesan
    s.sendall(encoded_raw)

    # Terima balasan
    data = s.recv(1024)

    # Dekode pesan balasan menjadi sebuah instance ISO 8583
    print(f"\n{'-' * 70}")
    print('Received reply: ', data)

    # Encode pesan ke byte
    decode, encoded = iso8583.decode(data, spec)
    iso8583.pp(decode, spec)

    time.sleep(5) # tunggu sebelum kirim pesan selanjutnya

# Tutup koneksi
s.close()
