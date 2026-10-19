const symbols = ["🍒", "🍋", "🍊", "🔔", "💎", "7️⃣", "🌟", "🃏"];
const weights = [10, 8, 6, 4, 2, 1, 1, 2];
const values = {"🍒": 1, "🍋": 2, "🍊": 3, "🔔": 5, "💎": 10, "7️⃣": 50};

let balance = 1000;
let multiplier = 1;
let freeSpins = 0;

const balanceEl = document.getElementById('balance');
const multEl = document.getElementById('mult');
const betInput = document.getElementById('bet');
const spinBtn = document.getElementById('spinBtn');
const msgEl = document.getElementById('msg');
const gridEl = document.getElementById('grid');

// --- SISTEMA DE ÁUDIO ---
const sounds = {
    spin: new Audio('https://assets.mixkit.co/active_storage/sfx/2003/2003-preview.mp3'),
    stop: new Audio('https://assets.mixkit.co/active_storage/sfx/2571/2571-preview.mp3'),
    win: new Audio('https://assets.mixkit.co/active_storage/sfx/2017/2017-preview.mp3'),
    lose: new Audio('https://assets.mixkit.co/active_storage/sfx/251/251-preview.mp3'),
    scatter: new Audio('https://assets.mixkit.co/active_storage/sfx/2019/2019-preview.mp3')
};

// Ajusta volume e loop
sounds.spin.loop = true;
Object.values(sounds).forEach(s => s.volume = 0.5);

function playSound(name) {
    sounds[name].currentTime = 0;
    sounds[name].play().catch(e => console.log("Áudio bloqueado pelo browser"));
}

// Inicializa a Grid 3x3
for (let i = 0; i < 9; i++) {
    const reel = document.createElement('div');
    reel.className = 'reel';
    reel.innerText = symbols[0];
    gridEl.appendChild(reel);
}
const reels = document.querySelectorAll('.reel');

function getRandomSymbol() {
    const totalWeight = weights.reduce((a, b) => a + b, 0);
    let random = Math.random() * totalWeight;
    for (let i = 0; i < symbols.length; i++) {
        if (random < weights[i]) return symbols[i];
        random -= weights[i];
    }
    return symbols[0];
}

function speak(text) {
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = 'pt-BR';
    window.speechSynthesis.speak(utterance);
}

function toggleModal() {
    const m = document.getElementById('modal');
    m.style.display = m.style.display === 'flex' ? 'none' : 'flex';
}

async function spin() {
    const bet = parseInt(betInput.value);
    if (isNaN(bet) || bet <= 0) {
        msgEl.innerText = "Aposta inválida!";
        return;
    }
    if (bet > balance && freeSpins === 0) {
        msgEl.innerText = "Saldo insuficiente!";
        return;
    }

    if (freeSpins > 0) {
        freeSpins--;
        msgEl.innerText = `Giro Grátis! Restam: ${freeSpins}`;
    } else {
        balance -= bet;
        balanceEl.innerText = balance;
    }
    
    spinBtn.disabled = true;
    msgEl.className = "message";

    // Inicia sons de giro
    playSound('spin');
    
    reels.forEach(reel => {
        reel.classList.add('spinning');
        reel.classList.remove('wild');
    });

    const spinInterval = setInterval(() => {
        reels.forEach(reel => {
            if (!reel.classList.contains('stopped')) reel.innerText = getRandomSymbol();
        });
    }, 100);

    const finalGrid = [];
    for (let col = 0; col < 3; col++) {
        await new Promise(resolve => setTimeout(resolve, 600 + col * 600));
        
        // Para o som de giro e toca o stop
        sounds.spin.pause();
        playSound('stop');

        for (let row = 0; row < 3; row++) {
            const index = row * 3 + col;
            const res = getRandomSymbol();
            finalGrid.push({index, res});
            reels[index].classList.remove('spinning');
            reels[index].classList.add('stopped');
            reels[index].innerText = res;
            if (res === "🃏") reels[index].classList.add('wild');
        }
    }
    clearInterval(spinInterval);

    const resultFlat = new Array(9).fill("");
    finalGrid.forEach(item => resultFlat[item.index] = item.res);
    const matrix = [
        [resultFlat[0], resultFlat[1], resultFlat[2]],
        [resultFlat[3], resultFlat[4], resultFlat[5]],
        [resultFlat[6], resultFlat[7], resultFlat[8]]
    ];

    let totalWin = 0;
    let scatterCount = 0;

    for (let i = 0; i < 3; i++) {
        const win = checkLine(matrix[i], bet);
        if (win > 0) totalWin += win;
    }
    for (let i = 0; i < 3; i++) {
        const col = [matrix[0][i], matrix[1][i], matrix[2][i]];
        const win = checkLine(col, bet);
        if (win > 0) totalWin += win;
    }

    resultFlat.forEach(s => { if(s === "🌟") scatterCount++; });

    if (scatterCount >= 3) {
        freeSpins += 10;
        msgEl.innerText = "🌟 10 GIROS GRÁTIS ATIVADOS! 🌟";
        playSound('scatter');
        speak("Incrível! Você ganhou dez giros grátis!");
    }

    if (totalWin > 0) {
        const finalPrize = totalWin * multiplier;
        balance += finalPrize;
        balanceEl.innerText = balance;
        multiplier++;
        multEl.innerText = multiplier;
        
        const msg = `JACKPOT! Você ganhou ${finalPrize.toFixed(2)} dólares!`;
        msgEl.innerText = `💥 ${msg} 💥`;
        msgEl.className = "message win";
        playSound('win');
        speak(msg);
        confetti({ particleCount: 150, spread: 70, origin: { y: 0.6 } });
    } else {
        multiplier = 1;
        multEl.innerText = multiplier;
        msgEl.innerText = "💀 A casa venceu. Tenta de novo!";
        msgEl.className = "message lose";
        playSound('lose');
        speak("Você falhou!");
    }

    setTimeout(() => {
        reels.forEach(reel => reel.classList.remove('stopped'));
        spinBtn.disabled = false;
    }, 500);
}

function checkLine(line, bet) {
    const filtered = line.filter(s => s !== "🃏");
    if (filtered.length === 0) return bet * 10;
    const first = filtered[0];
    const allSame = filtered.every(s => s === first);
    if (allSame && values[first]) return bet * values[first];
    return 0;
}

spinBtn.addEventListener('click', spin);
