import time
from flask import Flask, request, render_template
import iso8583
from iso8583.specs import default_ascii as spec

app = Flask(__name__)


@app.route('/api/iso8583', methods=['POST'])
def iso8583_handler():
    # Mengambil pesan ISO 8583 dari body permintaan HTTP
    print('request:', request)
    iso_request = request.get_data()
    print('iso_request:', iso_request)

    # Dekode pesan masuk
    decoded, encoded = iso8583.decode(iso_request, spec)
    print('Received message:', iso_request)
    iso8583.pp(decoded, spec)

    # Proses pesan ISO 8583
    # (validasi, autentikasi, pemrosesan database, dll.)

    mti = decoded["t"]

    # Periksa apakah tipe pesan adalah 0800
    if mti == '0800':
        # Buat pesan balasan
        reply = {
            't': '0810',
            'p': '8220000002000000',
            '1': '0400000000000000',
            '7': '0903000854',
            '11': '000001',
            '39': '00',
            '70': '001'
        }

        # time.sleep(1)  # simulate 1s processing

        print(f"\n{'=' * 100}")
        print('Sending reply: ')
        # Encode pesan balasan ke byte
        encode_raw, encoded = iso8583.encode(reply, spec)
        print('message encode_raw: ', encode_raw)

    # Membuat pesan respon ISO 8583
    iso_response = encode_raw

    return {
        'data': iso_response.decode('utf-8')
    }


@app.route('/')
def index():
    return render_template('client.html')

if __name__ == '__main__':
    app.run(port=5001)
