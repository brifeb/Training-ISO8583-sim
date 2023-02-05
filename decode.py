import iso8583
from iso8583.specs import default_ascii as spec



msg_echo = b"0800822000000000000004000000000000000903000917031380301"
msg_echo_reply = b"081082200000020000000400000000000000090300091703138000301"

sign_on = b'080082200000800000000400000000000000020510072700000106777006001'

decoded, encoded = iso8583.decode(sign_on, spec)

# print dengan formatting
iso8583.pp(decoded, spec)

# print dalam format dict
print(decoded)
print(type(decoded))

mti = decoded['t']
print(f"\n\nmti = {mti}")
nmi = decoded['70']
print(f'nmi (bit 70) = {nmi}')

# check jenis apa
if nmi[0] == '0':
    if nmi[1:] == '01':
        print("SIGN ON")