import socket
import time
import datetime
import iso8583
from iso8583.specs import default_ascii as spec
import sys

def rekuest_payment(card_number, amount):

    # Beri nama terminal dari argumen 
    terminal_id = "ONLINE02"
    print("terminal_id:", terminal_id)

    # Buat socket untuk terhubung ke server
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('localhost', 5000))

    # ambil jam sekarang
    dt_now = datetime.datetime.now()
    dt_now = dt_now.strftime('%m%d%H%M%S')
    print(f"Datetime now: {dt_now}")

    # formatting amount:
    trx_amount = f"{amount:010d}00"
    print('trx_amount', trx_amount)

    # format iso8583 message
    msg_payment = {
        't': '0200',
        '2': card_number,
        '3': '401010',
        '4': trx_amount,
        '7': dt_now,
        '11': '000001',
        '12': dt_now[4:],
        '13': dt_now[:4],
        '15': dt_now[:4],
        '18': '6010',
        '32': '03008',
        '37': f"{dt_now[:4]}00000012",
        '41': terminal_id,
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
    rc = decode['39']

    if mti == "0210":    
        print(f'Response code: {rc}')
        if rc == "00":
            print("PAYMENT APPROVED")
        else:
            print("PAYENT FAILED")
    
    return rc


    # jika approve, 

    # Tutup koneksi
    s.close()


