import pprint
import iso8583
from iso8583.specs import default_ascii as spec

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


encoded_raw, encoded = iso8583.encode(sign_on_msg, spec)
print('hasil encode: ', encoded)
pprint.pprint(encoded)
print()

# print dengan formatting
iso8583.pp(encoded, spec)
print()

# hasil encode dalam format bytearray
print(encoded_raw)
print(type(encoded_raw))