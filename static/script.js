/*const ws = new WebSocket("ws://127.0.0.1:8000/ws/plant/");
 ws.onmessage = (e) => console.log("Recebido:", e.data);
ws.onopen = () => console.log("Conectado!"); */
const token="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzg1Njg3NzY4LCJpYXQiOjE3ODU2OTg4MjgsImp0aSI6ImU0ZGNiOGJiNDVkMTQyMWU5N2QzODY0N2E4YzcyODk2IiwidXNlcl9pZCI6IjEifQ.2x3LEsPt5yttqcaUL8WPD0ZC4Zj6QamV8xbuYSMkLMI";
let ws = new WebSocket(`ws://127.0.0.1:8000/ws/plant/CLPULTRAMASTERBLASTER/?token=${token}`);
ws.onmessage = (e) => console.log("Recebido:", e.data);
ws.onopen = () => console.log("Conectado!");
ws.onerror = (e) => console.log("Erro:", e);


let paragrafo = document.getElementById("data");

console.log()

ws.onmessage = (e) => {
 
    console.log(e.data)

    let dados = JSON.parse(e.data)
    paragrafo.textContent = dados.nivel
};
