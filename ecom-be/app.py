import time
import pprint
from flask import Flask, request, render_template
import iso8583
from iso8583.specs import default_ascii as spec
import json

from  tohostbank import rekuest_payment

app = Flask(__name__)
@app.route('/api/', methods=['POST'])
def api_handler():
    # Mengambil pesan dari Frontend
    data = request.get_data()
    data = data.decode('utf8').replace("'", '"')
    print('data:', data, type(data))

    # format ke json
    data_json = json.loads(data)
    print('data_json', data_json, type(data_json))

    # ambil data produk yang dibeli
    produk = data_json['produk']
    pprint.pprint(produk)

    # ambil amount trx
    amount = produk['harga']
    print('trax amount', amount)

    # ambil data nomor kartu
    card_number = data_json['card']
    print("card_number", card_number)


    rc = "00"
    try:
        # send rekuest ke host bank
        rc = rekuest_payment(card_number, amount)
    except Exception as e:
        print(f"GAGAL kirim, error: {e}")
        # jika gagal, kembalikan dengan response code 91 (host down)
        rc = "91"

    # kirim kembali response hasil transaksi ke Frontend

    return {
        'rc': rc
    }



if __name__ == '__main__':
    app.run(port=5001, debug=True)
