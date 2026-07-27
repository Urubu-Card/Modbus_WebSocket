const ws = new WebSocket("ws://127.0.0.1:8000/ws/plant/");
/* ws.onmessage = (e) => console.log("Recebido:", e.data);
ws.onopen = () => console.log("Conectado!"); */

let paragrafo = document.getElementById("data");



ws.onmessage = (e) => {
 
    let dados = JSON.parse(e.data)
    paragrafo.textContent = dados.Registro_0
};
