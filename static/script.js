const statusEl = document.getElementById('status');
const playBtn = document.getElementById('playBtn');
const stopBtn = document.getElementById('stopBtn');


function setStatus(msg) {
statusEl.textContent = msg;
}


async function startGame() {
playBtn.disabled = true;
setStatus('Starting game...');
try {
const res = await fetch('/start', { method: 'POST' });
if (res.ok) {
setStatus('Game launched! Check the turtle window.');
} else if (res.status === 409) {
const data = await res.json();
if (data.status === 'already_running') {
setStatus('Game is already running.');
} else {
setStatus('Could not start: already running.');
}
} else {
setStatus('Unexpected error while starting.');
}
} catch (e) {
console.error(e);
setStatus('Failed to reach server. Is Flask running?');
} finally {
// Re-enable so user can try again later
playBtn.disabled = false;
}
}


async function stopGame() {
stopBtn.disabled = true;
setStatus('Stopping (best-effort)...');
try {
const res = await fetch('/stop', { method: 'POST' });
if (res.ok) {
setStatus('Stop signal sent. If the turtle window is still open, close it manually.');
} else if (res.status === 409) {
setStatus('No running game to stop.');
} else {
setStatus('Unexpected error while stopping.');
}
} catch (e) {
console.error(e);
setStatus('Failed to reach server. Is Flask running?');
} finally {
stopBtn.disabled = false;
}
}


playBtn.addEventListener('click', startGame);
stopBtn.addEventListener('click', stopGame);