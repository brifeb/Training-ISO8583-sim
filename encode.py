import pprint # pretty print, untuk menampilkan dict 
import iso8583
from iso8583.specs import default_ascii as spec
import datetime


# ambil jam sekarang
dt=datetime.datetime.now()
dt=dt.strftime('%m%d%H%M%S')
print(dt)
# MMDDhhmmss



sign_on_msg = {
    't': '0800',
    '7': dt,
    '11': '000001',
    '33': '777006',
    '70': '001'
}

echo_msg = {
    't': '0800',
    '7': dt,
    '11': '031380',
    '70': '301'
}

print("dict input:")
pprint.pprint(sign_on_msg)
print()


# #8220000080000000
# 8    2
# 1000 0010...
# 1234 5678...

encoded_raw, encoded = iso8583.encode(sign_on_msg, spec)
print('hasil encode: ', encoded)
print("\nhasil encode:")
pprint.pprint(encoded)
print()

# print dengan formatting
iso8583.pp(encoded, spec)
print()

# hasil encode dalam format bytearray
print(encoded_raw)
print(type(encoded_raw))