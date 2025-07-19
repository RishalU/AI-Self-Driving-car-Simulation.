// === Supercharged main.js: Full Visual Makeover ===
const canvas = document.getElementById("canvas");
const ctx = canvas.getContext("2d");
canvas.width = 800;
canvas.height = 600;

const laneLeftX = 140; // was 125
const laneWidth = 100;
const laneCenters = [190, 290, 390, 490, 590]; // shifted 15px right

const centerY = canvas.height / 2;

let car = null;
let traffic = [];
let laneOffsetY = 0;
let frameCount = 0;
let dodged = 0;

const socket = new WebSocket("ws://127.0.0.1:8000/ws");
socket.onmessage = (event) => {
    const data = JSON.parse(event.data);
    car = data.car;
    traffic = data.traffic;
    draw();
};

function draw() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    if (!car) return;

    frameCount++;
    const offsetY = centerY - car.y;
    laneOffsetY += 5;
    if (laneOffsetY >= 30) laneOffsetY = 0;

    // ==== ROAD & ENVIRONMENT ====
    // Background roadside (side soil)
    ctx.fillStyle = "#a77751";
    ctx.fillRect(0, 0, laneLeftX - 10, canvas.height);
    ctx.fillRect(laneLeftX + laneWidth * 5 + 10, 0, canvas.width - (laneLeftX + laneWidth * 5 + 10), canvas.height);

    // Bushes
    ctx.fillStyle = "#e2c336";
    for (let i = 0; i < 10; i++) {
        const y = (i * 80 + laneOffsetY * 2) % canvas.height;
        ctx.beginPath();
        ctx.arc(laneLeftX - 25, y, 6, 0, Math.PI * 2);
        ctx.arc(laneLeftX + laneWidth * 5 + 25, y, 6, 0, Math.PI * 2);
        ctx.fill();
    }

    // Road center gradient
    const roadGradient = ctx.createLinearGradient(0, 0, 0, canvas.height);
    roadGradient.addColorStop(0, "#2d2d2d");
    roadGradient.addColorStop(1, "#1a1a1a");
    ctx.fillStyle = roadGradient;
    ctx.fillRect(laneLeftX - 10, 0, laneWidth * 5 + 20, canvas.height);

    // Lane lines (scrolling)
    ctx.strokeStyle = "#aaa";
    ctx.lineWidth = 2;
    ctx.setLineDash([15, 15]);
    ctx.lineDashOffset = -laneOffsetY;
    for (let i = 0; i <= 5; i++) {
        const x = laneLeftX + i * laneWidth;
        ctx.beginPath();
        ctx.moveTo(x, 0);
        ctx.lineTo(x, canvas.height);
        ctx.stroke();
    }
    ctx.setLineDash([]);

    // ==== TRAFFIC ====
    traffic.forEach(t => {
        const tx = t.x;
        const ty = t.y + offsetY;
        ctx.save();
        ctx.translate(tx, ty);

        const typeSeed = Math.floor(t.y) % 3;
        let w = 20, h = 40;
        let bodyColor = "red";

        if (typeSeed === 0) {
            w = 20; h = 40; bodyColor = "#cc3333"; // Car
        } else if (typeSeed === 1) {
            w = 20; h = 60; bodyColor = "#880000"; // Truck
        } else {
            w = 10; h = 30; bodyColor = "#ff6611"; // Bike
        }

        ctx.fillStyle = bodyColor;
        ctx.fillRect(-w / 2, -h / 2, w, h);

        ctx.fillStyle = "#fcc";
        ctx.fillRect(-w / 2 + 2, -h / 2 + 2, w - 4, 8);

        ctx.fillStyle = "white";
        ctx.fillRect(-w / 2 + 2, -h / 2, 3, 5);
        ctx.fillRect(w / 2 - 5, -h / 2, 3, 5);

        ctx.fillStyle = "orange";
        ctx.fillRect(-w / 2 + 2, h / 2 - 5, 3, 5);
        ctx.fillRect(w / 2 - 5, h / 2 - 5, 3, 5);

        ctx.restore();
    });

    // ==== PLAYER CAR ====
    ctx.save();
    ctx.translate(car.x, centerY);

    ctx.fillStyle = "#33cc33";
    ctx.fillRect(-10, -20, 20, 40);

    ctx.fillStyle = "#9f9";
    ctx.fillRect(-8, -18, 16, 10);

    ctx.fillStyle = "white";
    ctx.fillRect(-8, -20, 3, 5);
    ctx.fillRect(5, -20, 3, 5);

    ctx.fillStyle = "red";
    ctx.fillRect(-8, 15, 3, 5);
    ctx.fillRect(5, 15, 3, 5);

    ctx.fillStyle = "#222";
    ctx.fillRect(-11, -18, 3, 12);
    ctx.fillRect(8, -18, 3, 12);
    ctx.fillRect(-11, 6, 3, 12);
    ctx.fillRect(8, 6, 3, 12);

    ctx.restore();

    // Sensor arcs (WiFi look)
    ctx.strokeStyle = "aqua";
    ctx.lineWidth = 1;
    for (let i = 1; i <= 3; i++) {
        ctx.beginPath();
        ctx.arc(car.x, centerY - 20 - i * 15, i * 10, Math.PI, 2 * Math.PI);
        ctx.stroke();
    }

}
