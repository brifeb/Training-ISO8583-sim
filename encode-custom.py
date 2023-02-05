import pprint # pretty print, untuk menampilkan dict 
import iso8583
from iso8583.specs import default_ascii as spec
import datetime

pprint.pprint(spec)

custom_spec = spec

custom_spec['11'] = {
    'data_enc': 'ascii',
    'desc': 'Testing edit custom STAN',
    'len_enc': 'ascii',
    'len_type': 0,
    'max_len': 8
}

sign_on_msg = {
    't': '0800',
    '11': '00000199',
    '33': '777006',
    '70': '001'
}

print("dict input:")
pprint.pprint(sign_on_msg)
print()


encoded_raw, encoded = iso8583.encode(sign_on_msg, custom_spec)
print('hasil encode: ', encoded)
print("\nhasil encode:")
pprint.pprint(encoded)
print()

# print dengan formatting
iso8583.pp(encoded, custom_spec)
print()

# hasil encode dalam format bytearray
print(encoded_raw)
print(type(encoded_raw))