MIN_POR_KM = 2        # trem a 30 km/h = 1 km a cada 2 minutos
TROCA = 5             # minutos gastos a cada mudança de linha

# Trechos do mapa: (estação, estação, distância real em km, linha). As cores foram lidas do mapa do PDF.
TRECHOS = [
    ("E1", "E2", 11, "Azul"),     ("E2", "E3", 9, "Azul"),      ("E3", "E4", 7, "Azul"),
    ("E4", "E5", 14, "Azul"),     ("E5", "E6", 3, "Azul"),
    ("E10", "E2", 4, "Amarela"),  ("E2", "E9", 11, "Amarela"),  ("E9", "E8", 10, "Amarela"),
    ("E8", "E5", 33, "Amarela"),  ("E5", "E7", 2, "Amarela"),
    ("E11", "E9", 14, "Vermelha"), ("E9", "E3", 10, "Vermelha"), ("E3", "E13", 19, "Vermelha"),
    ("E12", "E8", 7, "Verde"),    ("E8", "E4", 16, "Verde"),    ("E4", "E13", 12, "Verde"),
    ("E13", "E14", 5, "Verde"),
]

# Distância em linha reta (km) entre as estações E1 até E14 (tabela do PDF).
# A linha 0 é a E1, a linha 1 é a E2, e assim por diante (o mesmo para as colunas).
RETA = [
    [0, 11, 20, 27, 40, 43, 39, 28, 18, 10, 18, 30, 30, 32],
    [11, 0, 9, 16, 29, 32, 28, 19, 11, 4, 17, 23, 21, 24],
    [20, 9, 0, 7, 20, 22, 19, 15, 10, 11, 21, 21, 13, 18],
    [27, 16, 7, 0, 13, 16, 12, 13, 13, 18, 26, 21, 11, 17],
    [40, 29, 20, 13, 0, 3, 2, 21, 25, 31, 38, 27, 16, 20],
    [43, 32, 22, 16, 3, 0, 4, 23, 28, 33, 41, 30, 17, 20],
    [39, 28, 19, 12, 2, 4, 0, 22, 25, 29, 38, 28, 13, 17],
    [28, 19, 15, 13, 21, 23, 22, 0, 9, 22, 18, 7, 25, 30],
    [18, 11, 10, 13, 25, 28, 25, 9, 0, 13, 12, 12, 23, 28],
    [10, 4, 11, 18, 31, 33, 29, 22, 13, 0, 20, 27, 20, 23],
    [18, 17, 21, 26, 38, 41, 38, 18, 12, 20, 0, 15, 35, 39],
    [30, 23, 21, 21, 27, 30, 28, 7, 12, 27, 15, 0, 31, 37],
    [30, 21, 13, 11, 16, 17, 13, 25, 23, 20, 35, 31, 0, 5],
    [32, 24, 18, 17, 20, 20, 17, 30, 28, 23, 39, 37, 5, 0],
]


def numero(estacao):
    """Transforma 'E7' em 6 (a posição dela na tabela RETA)."""
    return int(estacao[1:]) - 1


def heuristica(estacao, destino):
    """h: estimativa do tempo que falta = linha reta até o destino x 2 minutos por km."""
    return RETA[numero(estacao)][numero(destino)] * MIN_POR_KM


def vizinhos(estacao):
    """Lista os trechos que saem da estação: (estação vizinha, km, linha)."""
    lista = []
    for a, b, km, linha in TRECHOS:
        if a == estacao:
            lista.append((b, km, linha))
        if b == estacao:
            lista.append((a, km, linha))
    return lista


def a_estrela(origem, destino):
    """Devolve o caminho [(estação, linha), ...] e o tempo total em minutos."""
    # Cada item da fronteira: (f, g, estação, linha em que estou, caminho até aqui)
    fronteira = [(heuristica(origem, destino), 0, origem, None, [(origem, None)])]
    melhor_g = {(origem, None): 0}        # menor tempo já achado para chegar em cada (estação, linha)

    while fronteira:
        item = min(fronteira, key=lambda x: x[0])    # pega o item com MENOR f = g + h
        fronteira.remove(item)
        f, g, estacao, linha, caminho = item

        if g > melhor_g[(estacao, linha)]:           # já achei um jeito mais rápido: ignora este
            continue

        if estacao == destino:                       # teste de objetivo
            return caminho, g

        for viz, km, nova_linha in vizinhos(estacao):
            troca = 0
            if linha is not None and nova_linha != linha:   # mudou de linha: paga 5 minutos
                troca = TROCA
            novo_g = g + km * MIN_POR_KM + troca            # tempo gasto até a vizinha
            estado = (viz, nova_linha)
            if estado not in melhor_g or novo_g < melhor_g[estado]:   # só vale se for mais rápido
                melhor_g[estado] = novo_g
                novo_f = novo_g + heuristica(viz, destino)
                fronteira.append((novo_f, novo_g, viz, nova_linha, caminho + [estado]))

    return None, None


def resumo(origem, destino):
    """Calcula e devolve os dados da viagem: estações, linhas usadas, trocas e tempo total."""
    caminho, tempo = a_estrela(origem, destino)
    estacoes = [e for e, _ in caminho]
    trocas = []                                       # onde houve mudança de linha
    for i in range(2, len(caminho)):
        if caminho[i][1] != caminho[i - 1][1]:
            trocas.append((caminho[i - 1][0], caminho[i - 1][1], caminho[i][1]))
    return estacoes, trocas, tempo


def mostrar(origem, destino):
    if origem == destino:
        print(f"{origem} -> {destino}: você já está no destino (0 minutos).")
        return
    estacoes, trocas, tempo = resumo(origem, destino)
    print(f"Origem: {origem} | Destino: {destino}")
    print("Caminho mais rápido:", " -> ".join(estacoes))
    print("Mudanças de linha:", len(trocas))
    for est, de, para in trocas:
        print(f"   troca em {est}: linha {de} para linha {para}")
    print(f"Tempo total: {tempo} minutos ({tempo - 5 * len(trocas)} de viagem + {5 * len(trocas)} de trocas)")


def ler_estacao(texto):
    while True:
        e = input(texto).strip().upper()
        if e.startswith("E") and e[1:].isdigit() and 1 <= int(e[1:]) <= 14:
            return e
        print("Estação inválida. Digite de E1 até E14.")


if __name__ == "__main__":
    origem = ler_estacao("Estação de origem (E1 a E14): ")
    destino = ler_estacao("Estação de destino (E1 a E14): ")
    mostrar(origem, destino)
    print()
    if input("Mostrar TODAS as combinações de estações? (s/n): ").strip().lower() == "s":
        for i in range(1, 15):
            for j in range(i + 1, 15):
                mostrar(f"E{i}", f"E{j}")
                print()