OBJETIVO = (0, 1, 2,
            3, 4, 5,
            6, 7, 8)


def vizinhos(tab):
    """Devolve todos os tabuleiros possíveis movendo o quadro branco 1 vez."""
    pos = tab.index(0)                    # posição (0 a 8) onde está o branco
    linha = pos // 3                      # em qual linha o branco está (0, 1 ou 2)
    coluna = pos % 3                      # em qual coluna o branco está (0, 1 ou 2)

    movimentos = []                       # lista de (nome da ação, nova posição do branco)
    if linha > 0:
        movimentos.append(("Cima", pos - 3))       # só sobe se não estiver na linha de cima
    if linha < 2:
        movimentos.append(("Baixo", pos + 3))      # só desce se não estiver na linha de baixo
    if coluna > 0:
        movimentos.append(("Esquerda", pos - 1))   # só vai à esquerda se não estiver na borda esquerda
    if coluna < 2:
        movimentos.append(("Direita", pos + 1))    # só vai à direita se não estiver na borda direita

    resultado = []
    for acao, nova_pos in movimentos:
        lista = list(tab)                                    # copia o tabuleiro (tupla vira lista)
        lista[pos], lista[nova_pos] = lista[nova_pos], lista[pos]   # troca o branco com a peça vizinha
        resultado.append((acao, tuple(lista)))               # guarda a ação e o novo tabuleiro
    return resultado


def busca_largura(inicial):
    """BFS: devolve a lista de passos (ação, tabuleiro) e quantos estados foram gerados."""
    fila = [(inicial, [])]                # cada item da fila: (tabuleiro, passos feitos até ele)
    visitados = {inicial}                 # PODA: tabuleiros que já apareceram não entram de novo

    while fila:                           # enquanto ainda houver tabuleiros para testar
        tab, passos = fila.pop(0)         # tira o PRIMEIRO da fila (quem chegou antes sai antes)

        if tab == OBJETIVO:               # teste de objetivo: chegou na ordem certa?
            return passos, len(visitados)

        for acao, novo in vizinhos(tab):  # testa cada movimento possível do branco
            if novo not in visitados:     # só continua se esse tabuleiro for novo
                visitados.add(novo)       # marca como já visto
                fila.append((novo, passos + [(acao, novo)]))   # entra no FIM da fila

    return None, len(visitados)           # a fila acabou e não achou: não tem solução


def mostrar(tab):
    """Desenha o tabuleiro em 3 linhas, trocando o 0 por X."""
    for i in (0, 3, 6):
        print("   ", " ".join("X" if n == 0 else str(n) for n in tab[i:i + 3]))


PUZZLES = {
    "Puzzle 1": (4, 6, 2, 8, 1, 3, 7, 5, 0),
    "Puzzle 2": (6, 4, 2, 8, 1, 3, 7, 5, 0),
    "Puzzle 3 (escolha)": (3, 1, 2, 4, 0, 8, 6, 5, 7),
    "Puzzle 4 (escolha)": (3, 2, 0, 7, 1, 5, 4, 6, 8),
}

if __name__ == "__main__":
    for nome, inicial in PUZZLES.items():
        print("=====", nome, "=====")
        print("Tabuleiro inicial:")
        mostrar(inicial)
        passos, gerados = busca_largura(inicial)
        if passos is None:
            print(f"SEM SOLUÇÃO. A busca testou todos os {gerados} tabuleiros possíveis.")
        else:
            for n, (acao, tab) in enumerate(passos, 1):
                print(f"Passo {n}: mover o branco para {acao}")
                mostrar(tab)
            print(f"Total de passos: {len(passos)} | Estados gerados: {gerados}")
        print()