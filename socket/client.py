import socket
import iso8583
from iso8583.specs import default_ascii as spec

# Buat socket untuk terhubung ke server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('localhost', 5000))

# Buat pesan untuk dikirim
sign_on_msg = {
    't': '0800',
    'p': '8220000080000000',
    '1': '0400000000000000',
    '7': '0903000854',
    '11': '000001',
    '33': '777006',
    '70': '001'}

# Encode pesan ke byte
encoded_raw, encoded = iso8583.encode(sign_on_msg, spec)
print('Sending message: ', encoded_raw)
iso8583.pp(encoded, spec)

# Kirim pesan
s.sendall(encoded_raw)

# Terima balasan
data = s.recv(1024)

# Dekode pesan balasan menjadi sebuah instance ISO 8583
print(f"\n{'-' * 100}")
print('Received reply: ', data)

# Encode pesan ke byte
decode, encoded = iso8583.decode(data, spec)
iso8583.pp(decode, spec)

# Tutup koneksi
s.close()
