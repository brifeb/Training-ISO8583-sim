import requests
import iso8583
from iso8583.specs import default_ascii as spec


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

# Encode pesan ISO 8583 ke format string
data = encoded_raw

# Kirim pesan ISO 8583 sebagai payload HTTP
url = 'http://localhost:5001/api/iso8583'
headers = {'Content-Type': 'application/octet-stream'}
response = requests.post(url, headers=headers, data=data)

# Cek status respon HTTP
if response.status_code == 200:
    print('Pesan ISO 8583 berhasil dikirim!')
    data = response.text
    data_utf8 = bytearray(data, encoding='utf8')
    # Dekode pesan balasan menjadi sebuah instance ISO 8583
    print(f"\n{'-' * 100}")
    print('Received reply: ', data_utf8)

    # Encode pesan ke byte
    decode, encoded = iso8583.decode(data_utf8, spec)
    iso8583.pp(decode, spec)
else:
    print('Gagal mengirim pesan ISO 8583, status kode:', response.status_code)
