import "./App.css";
import { useState } from "react";
import axios from "axios";

const products = [
    {
        id: 1,
        nama: "Sepeda Fixie",
        harga: 2500000,
        stok: 1,
        img: "https://www.sepeda.me/wp-content/uploads/2020/09/Custom-Frame-Pursuit-Yamaguchi.jpg",
    },
    {
        id: 2,
        nama: "Sepeda BMX",
        harga: 1900000,
        stok: 1,
        img: "https://www.sepeda.me/wp-content/uploads/2018/11/Sepeda-BMX-Thumbnail.jpg",
    },
    {
        id: 3,
        nama: "Balance Bike",
        harga: 800000,
        stok: 1,
        img: "https://www.sepeda.me/wp-content/uploads/2019/01/Balance_Bike.jpg",
    },
];

function Product({ data }) {
    return (
        <div>
            <h1>{data.nama}</h1>
            <p>Rp. {data.harga}</p>
            <img src={data.img} width={100} />
        </div>
    );
}

function App() {
    const [halaman, setHalaman] = useState("home");
    const [selectedProduct, setSelectedProduct] = useState();
    const [cardnumber, setCardnumber] = useState("");
    const [status, setStatus] = useState("");

    let handleBeli = (beliProduk) => {
        setHalaman("pembayaran");
        setSelectedProduct(beliProduk);
    };

    let handleBayar = async (bayarProduk) => {
        // request ke be,
        const response = await axios.post("http://127.0.0.1:5001/api/", {
            card: cardnumber,
            produk: bayarProduk,
        });

        console.log("response", response);

        // product, data kartu ( nomor kartu)
        let responsecode = response.data.rc;
        if (responsecode === "00") {
            setStatus("Berhasil rc:" + responsecode);
        } else {
            setStatus("Gagal \nrc:" + responsecode);
        }

        setHalaman("done");
    };

    return (
        <div className="App">
            <h1>Toko Sepeda</h1>

            {halaman === "home" && (
                <>
                    <h2>Daftar Produk:</h2>

                    {products.map((produk, i) => (
                        <div className="Produk" key={i}>
                            <Product data={produk} />
                            <p>
                                <button onClick={() => handleBeli(produk)}>
                                    BELI
                                </button>
                            </p>
                        </div>
                    ))}
                </>
            )}

            {halaman === "pembayaran" && (
                <>
                    <nav onClick={() => setHalaman("home")}> &lt; back </nav>
                    <h2>Pembayaran</h2>
                    <div className="Produk">
                        <Product data={selectedProduct} />
                        <div className="detail">
                            <hr />
                            <h3>Metode Pembayaran:</h3>
                            <hr />
                            <h4>Transfer Bank:</h4>
                            <p>BNI 003003003</p>
                            <p>BCA 001001001</p>
                            <p>Selahkan melakukan pembayaran dan konfirmasi</p>
                            <hr />
                            <h4>Debit Online:</h4>
                            Masukkan nomor kartu:
                            <input
                                value={cardnumber}
                                onChange={(value) => {
                                    setCardnumber(value.target.value);
                                }}
                            />
                            <p>
                                <button
                                    onClick={() => handleBayar(selectedProduct)}
                                >
                                    BAYAR
                                </button>
                            </p>
                        </div>
                    </div>
                </>
            )}
            {halaman === "done" && (
                <>
                    <nav onClick={() => setHalaman("home")}> &lt; home </nav>
                    <h2>Status Pembayaran</h2>
                    <h1>{status}</h1>
                </>
            )}
        </div>
    );
}

export default App;
