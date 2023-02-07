## libs
>pip install pyiso8583

https://pyiso8583.readthedocs.io/en/latest/index.html 

# Menjalankan socket testing
## socket:
>cd socket
#### 1. Start server
> python server.py
#### 2. hit dari client
> python client.py


# Menjalankan Simulator end to end
1. Jalankan simulator bank host
> cd bank-host

> python bankserver.py

2. Jalankan Backend apps (buka terminal baru)
> cd ecom-be

> python app.py

3. Jalankan Frontend (buka terminal baru)
> cd ecom-fe

pertama kali:
> npm install

start apps
> npm start

buka browser http://localhost:3000/

lakukan transaksi, nomor kartu testing yang terdaftar:
123450000011, 123450000012, 123450000013

