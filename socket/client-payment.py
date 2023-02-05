import socket
import time
import datetime
import iso8583
from iso8583.specs import default_ascii as spec
import sys


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


# rekuest pembelian pulsa

amount = '000001000000'

msg_payment = {
    't': '0200',
    '2': '6271230000000001',
    '4': amount,
    '7': dt_now,
    '11': '000001',
    '12': dt_now[4:],
    '13': dt_now[:4],
    '15': dt_now[:4],
    '18': '6010',
    '32': '03008',
    '37': f"{dt_now[:4]}00000012",
    '41': terminal_id,
    '48': '015200308111050746',
    '49': '360',
    '61': '123456',
    '102': '12345678910'

}


# encode dari dict ke msg
encoded_raw, encoded = iso8583.encode(msg_payment, spec)

# kirim ke server
s.sendall(encoded_raw)
print(f'rekuest payment: {encoded_raw}')
iso8583.pp(encoded, spec)


# terima balasan
data_respond = s.recv(1024)
print("terima balasan", data_respond)

# decode data_respond
decode, encoded = iso8583.decode(data_respond, spec)
# print(decode)
iso8583.pp(encoded, spec)

# cek message 0210
mti = decode['t']
if mti == "0210":

    rc = decode['39']
    print(f'Response code: {rc}')
    if rc == "00":
        print("PAYMENT APPROVED")
    else:
        print("PAYENT FAILED")


# jika approve, 

# Tutup koneksi
s.close()


