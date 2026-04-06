import { useEffect, useState } from "react";
import "./App.css";

// 🔥 BACKEND PRODUCCIÓN
const API_URL = "https://api-productos-p7k5.onrender.com";

function App() {
  const [productos, setProductos] = useState([]);
  const [categorias, setCategorias] = useState([]);
  const [categoriaSeleccionada, setCategoriaSeleccionada] = useState(null);
  const [busqueda, setBusqueda] = useState("");
  const [carrito, setCarrito] = useState([]);
  const [mostrarCarrito, setMostrarCarrito] = useState(false);
  const [mensaje, setMensaje] = useState("");

  // 🔥 CARGAR CATEGORÍAS
  useEffect(() => {
    fetch(`${API_URL}/categorias/`)
      .then((res) => res.json())
      .then((data) => setCategorias(data))
      .catch(() => console.log("Error cargando categorías"));
  }, []);

  // 🔥 CARGAR PRODUCTOS
  useEffect(() => {
    const url = busqueda
      ? `${API_URL}/productos/?search=${busqueda}`
      : `${API_URL}/productos/`;

    fetch(url)
      .then((res) => res.json())
      .then((data) => setProductos(data))
      .catch(() => console.log("Error cargando productos"));
  }, [busqueda]);

  // 🛒 AGREGAR
  const agregarAlCarrito = (producto) => {
    setCarrito((prev) => {
      const existe = prev.find((p) => p.id === producto.id);

      if (existe) {
        return prev.map((p) =>
          p.id === producto.id ? { ...p, cantidad: p.cantidad + 1 } : p,
        );
      }

      return [...prev, { ...producto, cantidad: 1 }];
    });

    setMensaje("Producto agregado 🛒");
    setTimeout(() => setMensaje(""), 2000);
  };

  // ➕
  const aumentar = (id) => {
    setCarrito((prev) =>
      prev.map((p) => (p.id === id ? { ...p, cantidad: p.cantidad + 1 } : p)),
    );
  };

  // ➖
  const disminuir = (id) => {
    setCarrito((prev) =>
      prev
        .map((p) => (p.id === id ? { ...p, cantidad: p.cantidad - 1 } : p))
        .filter((p) => p.cantidad > 0),
    );
  };

  // ❌
  const eliminar = (id) => {
    setCarrito((prev) => prev.filter((p) => p.id !== id));
  };

  // 💰 TOTAL
  const total = carrito.reduce(
    (acc, item) => acc + item.precio * item.cantidad,
    0,
  );

  // 🔥 FINALIZAR COMPRA (GUARDA EN BACKEND)
  const finalizarCompra = async () => {
    if (carrito.length === 0) {
      alert("El carrito está vacío");
      return;
    }

    try {
      const response = await fetch(`${API_URL}/pedidos/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          productos: carrito,
          total: total,
        }),
      });

      if (!response.ok) {
        throw new Error("Error al guardar pedido");
      }

      alert("Pedido guardado correctamente 🎉");

      setCarrito([]);
      setMostrarCarrito(false);
    } catch (error) {
      alert("Error al guardar el pedido");
    }
  };

  // 🔍 FILTRO
  const productosFiltrados = categoriaSeleccionada
    ? productos.filter((p) => {
        const catId =
          p.categoria_id || p.id_categoria || (p.categoria && p.categoria.id);

        return catId === categoriaSeleccionada;
      })
    : productos;

  return (
    <div className="container">
      {/* HEADER */}
      <div className="header">
        <h1>Mi Tienda 🛒</h1>

        <div className="carrito-info" onClick={() => setMostrarCarrito(true)}>
          🛒 {carrito.length}
        </div>
      </div>

      {/* BUSCADOR */}
      <input
        type="text"
        placeholder="Buscar producto..."
        className="search"
        value={busqueda}
        onChange={(e) => setBusqueda(e.target.value)}
      />

      {/* MENSAJE */}
      {mensaje && <div className="mensaje">{mensaje}</div>}

      {/* CATEGORÍAS */}
      <div className="categorias">
        <button onClick={() => setCategoriaSeleccionada(null)}>Todos</button>

        {categorias.map((cat) => (
          <button key={cat.id} onClick={() => setCategoriaSeleccionada(cat.id)}>
            {cat.nombre}
          </button>
        ))}
      </div>

      {/* PRODUCTOS */}
      <div className="grid">
        {productosFiltrados.map((p) => {
          const imgUrl = p.imagen
            ? `${API_URL}/images/${p.imagen}`
            : "https://via.placeholder.com/200";

          return (
            <div className="card" key={p.id}>
              <img src={imgUrl} alt={p.nombre || "producto"} className="img" />

              <h2>{p.nombre}</h2>
              <p>${p.precio}</p>

              <button onClick={() => agregarAlCarrito(p)}>Comprar</button>
            </div>
          );
        })}
      </div>

      {/* CARRITO */}
      {mostrarCarrito && (
        <div className="modal">
          <div className="modal-content">
            <h2>🛒 Tu carrito</h2>

            {carrito.length === 0 ? (
              <p>Vacío</p>
            ) : (
              carrito.map((item) => (
                <div key={item.id} className="item-carrito">
                  <span>
                    {item.nombre} x {item.cantidad}
                  </span>

                  <div className="acciones">
                    <button onClick={() => disminuir(item.id)}>➖</button>
                    <button onClick={() => aumentar(item.id)}>➕</button>
                    <button onClick={() => eliminar(item.id)}>❌</button>
                  </div>
                </div>
              ))
            )}

            <h3>Total: ${total}</h3>

            <button onClick={finalizarCompra}>Finalizar compra 💳</button>

            <button onClick={() => setMostrarCarrito(false)}>Cerrar</button>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
