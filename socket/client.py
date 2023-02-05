import socket
import time
import datetime
import iso8583
from iso8583.specs import default_ascii as spec
import sys

def request_payment():
    print("pembelian")

# Beri nama terminal dari argumen 
terminal_id = "TERM0001"
print('Jumlah argument:', len(sys.argv))
print('Argumen:', sys.argv)

if len(sys.argv) > 1:
    print('Argumen pertama:', sys.argv[1])
    terminal_id = sys.argv[1]

# Buat socket untuk terhubung ke server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('localhost', 5000))

# ambil jam sekarang
dt_now = datetime.datetime.now()
dt_now = dt_now.strftime('%m%d%H%M%S')
print(f"Datetime now: {dt_now}")

signed_on = False

# Buat pesan untuk dikirim
sign_on_msg = {
    't': '0800',
    '7': dt_now,
    '11': '000001',
    '33': '777006',
    '41': terminal_id,
    '70': '001'}

echo_msg = {
    't': '0800',
    '7': dt_now,  # datetime
    '11': '031380',
    '41': terminal_id,
    '70': '301'
}

# TODO: Kirim Sign On terlebih dahulu, jika approve (bit 39 = 00) lanjut ke echo test
# encode dari dict ke msg
encoded_raw, encoded = iso8583.encode(sign_on_msg, spec)

# kirim ke server
s.sendall(encoded_raw)

# terima balasan
data_respond = s.recv(1024)
print("terima balasan", data_respond)
#b'081082200000020000000400000000000000090300085400000100001'

# decode data_respond
decode, encoded = iso8583.decode(data_respond, spec)
print(decode)
# {'t': '0810', 'p': '8220000002000000', '1': '0400000000000000', '7': '0903000854', '11': '000001', '39': '00', '70': '001'}

# cek message 0810
mti = decode['t']
if mti == "0810":
    # cek nmi = 301
    nmi = decode['70']
    if nmi == "001":
        print("signon")
        # cek response code
        rc = decode['39']
        print(f'Response code: {rc}')
        if rc == "00":
            signed_on = True
        else:
            signed_on = False


# jika approve, lanjutkan echo

if signed_on:
    print("SIGNED ON, CONTINUE ECHO TEST")
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

        request_payment()

        time.sleep(5)  # tunggu sebelum kirim pesan selanjutnya

# Tutup koneksi
s.close()


