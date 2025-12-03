
// Connect WebSocket
const ws = new WebSocket(`ws://${location.host}/ws`);





const yawEl = document.getElementById('yaw');
const pitchEl = document.getElementById('pitch');
const rollEl = document.getElementById('roll');
const dtEl = document.getElementById('dt');

// --- Three.js scene ---
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(60, window.innerWidth / window.innerHeight, 0.1, 100);
camera.position.set(0, 0, 4);

const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setSize(window.innerWidth, window.innerHeight);
document.body.appendChild(renderer.domElement);

const cube = new THREE.Mesh(
  new THREE.BoxGeometry(1, 1, 1),
  new THREE.MeshStandardMaterial({ color: 0x66ccff, metalness: 0.1, roughness: 0.6 })
);
scene.add(cube);

const light = new THREE.DirectionalLight(0xffffff, 1.0);
light.position.set(3, 3, 3);
scene.add(light);
scene.add(new THREE.AmbientLight(0xffffff, 0.3));

// Correct rotation order; we'll apply Euler angles in Y (yaw), X (pitch), Z (roll).
cube.rotation.order = 'YXZ'; // three.js stores rotations via quaternion internally. [2](https://threejs.org/manual/en/matrix-transformations.html)[3](https://threejs.org/docs/)

let latest = { yaw: 0, pitch: 0, roll: 0 };
ws.onopen = () => console.log("✅ WebSocket connected");
ws.onclose = () => console.log("❌ WebSocket closed");
ws.onerror = (err) => console.error("WebSocket error:", err);
ws.onmessage = (evt) => {
  const d = JSON.parse(evt.data);
  latest = d;
  yawEl.textContent = d.yaw.toFixed(1);
  pitchEl.textContent = d.pitch.toFixed(1);
  rollEl.textContent = d.roll.toFixed(1);
  dtEl.textContent = d.dt_ms;
};

function animate() {
  requestAnimationFrame(animate);
  // Degrees -> radians
  cube.rotation.y = latest.yaw * Math.PI / 180;
  cube.rotation.x = latest.pitch * Math.PI / 180;
  cube.rotation.z = latest.roll * Math.PI / 180;
  renderer.render(scene, camera);
}
animate();

window.addEventListener('resize', () => {
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
});
