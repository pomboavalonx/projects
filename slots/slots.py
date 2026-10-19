import random
import time
import sys
import os

# --- CONFIGURAÇÕES DO CASINO ---
SIMBOLOS = ["🍒", "🍋", "🍊", "🔔", "💎", "7️⃣"]
VALORES = {"🍒": 10, "🍋": 20, "🍊": 30, "🔔": 50, "💎": 100, "7️⃣": 500}
PESOS = [10, 8, 6, 4, 2, 1]

def speak(text):
    """Integração com a voz da Nébula via edge-tts e mpv."""
    cmd = f'edge-tts --voice pt-BR-FranciscaNeural --text "{text}" --write-media resp.mp3 && mpv resp.mp3'
    os.system(cmd)

def clear_screen():
    os.system('clear')

def get_terminal_width():
    try:
        return os.get_terminal_size().columns
    except OSError:
        return 80

def center_text(text):
    width = get_terminal_width()
    return text.center(width)

def spin_grid():
    return [[random.choices(SIMBOLOS, weights=PESOS, k=1)[0] for _ in range(3)] for _ in range(3)]

def animate_grid_spin(final_grid):
    """Animação estática usando coordenadas absolutas do cursor."""
    # Salvamos a posição atual do cursor
    sys.stdout.write("\033[s") 
    
    for i in range(20):
        current_grid = [[None for _ in range(3)] for _ in range(3)]
        for col in range(3):
            if (col == 0 and i > 8) or (col == 1 and i > 13) or (col == 2 and i > 17):
                for row in range(3):
                    current_grid[row][col] = final_grid[row][col]
            else:
                for row in range(3):
                    current_grid[row][col] = random.choice(SIMBOLOS)
        
        border = "╔════════════════════╗"
        footer = "╚════════════════════╝"
        
        grid_rows = []
        for row in range(3):
            grid_rows.append(f"║  {current_grid[row][0]}  │  {current_grid[row][1]}  │  {current_grid[row][2]}  ║")

        frame = [border, grid_rows[0], grid_rows[1], grid_rows[2], footer]
        
        # Volta para a posição salva e redesenha sem pular linha
        sys.stdout.write("\033[u") 
        output = "\n".join([center_text(line) for line in frame])
        sys.stdout.write(output + "\n")
        sys.stdout.flush()
        
        time.sleep(0.1 if i < 12 else 0.2)
    
    # Restaura o cursor para a linha abaixo da máquina para o próximo input
    sys.stdout.write("\033[5B") 

def calcular_premio(grid, aposta):
    for row in grid:
        if row[0] == row[1] == row[2]:
            return aposta * (VALORES[row[0]] / 10)
    for col in range(3):
        if grid[0][col] == grid[1][col] == grid[2][col]:
            return aposta * (VALORES[grid[0][col]] / 10)
    return 0

def main():
    saldo = 1000
    clear_screen()
    
    print("\n\n")
    print(center_text("🌌 NEBULA CASINO 🌌"))
    print(center_text("━━━━━━━━━━━━━━━━━━━━━━━━━━━━"))
    print(center_text(f"Saldo Inicial: ${saldo}"))
    print(center_text("🍒 🍋 🍊 🔔 💎 7️⃣"))
    print("\n")
    
    # Placeholder da máquina
    print(center_text("╔════════════════════╗"))
    print(center_text("║  _  │  _  │  _  ║"))
    print(center_text("║  _  │  _  │  _  ║"))
    print(center_text("║  _  │  _  │  _  ║"))
    print(center_text("╚════════════════════╝"))
    print("\n")

    while saldo > 0:
        try:
            prompt = f"💰 Saldo: ${saldo} | Aposta (0 p/ sair): "
            aposta = int(input(center_text(prompt) + " "))
            if aposta == 0: break
            if aposta > saldo:
                print(center_text("❌ Aposta maior que o saldo!"))
                continue
            if aposta < 0:
                print(center_text("❌ Aposta negativa? Nem fodendo."))
                continue
        except ValueError:
            print(center_text("❌ Digita um número, porra!"))
            continue

        saldo -= aposta
        print(center_text("\n🎰 Girando a sorte... "))
        
        final_grid = spin_grid()
        animate_grid_spin(final_grid)

        premio = calcular_premio(final_grid, aposta)
        
        if premio > 0:
            msg_vitoria = f"Jackpot! Você ganhou {premio:.2f} dólares!"
            print(center_text(f"\n💥 {msg_vitoria} 💥"))
            saldo += premio
            speak(msg_vitoria)
        else:
            print(center_text("\n💀 A casa venceu. Tenta de novo, otário."))
            speak("Você falhou!")

    print(center_text(f"\n\nJogo encerrado. Saldo final: ${saldo}"))
    if saldo <= 0:
        print(center_text("Você faliu. Volta quando tiver dinheiro! 💸"))
        speak("Você faliu completamente. Que patético!")

if __name__ == "__main__":
    main()
