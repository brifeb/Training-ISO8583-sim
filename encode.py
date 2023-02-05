import iso8583
from iso8583.specs import default_ascii as spec



msg_echo = b"0800822000000000000004000000000000000903000917031380301"
msg_echo_reply = b"081082200000020000000400000000000000090300091703138000301"

decoded, encoded = iso8583.decode(msg_echo, spec)

# print dengan formatting
iso8583.pp(decoded, spec)

# print dalam format dict
print(decoded)
print(type(decoded))