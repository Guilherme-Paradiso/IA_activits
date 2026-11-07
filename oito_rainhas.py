def posicao_segura(tabuleiro, coluna_atual, linha_tentada):
    for coluna_ant in range(8):
        linha_ant = tabuleiro[coluna_ant]
        if linha_ant is None:        # coluna vazia (inclui a atual): ignora
            continue
        if linha_ant == linha_tentada:
            return False
        if abs(linha_ant - linha_tentada) == abs(coluna_ant - coluna_atual):
            return False
    return True

def resolver_oito_rainhas(tabuleiro_inicial):
    pilha = [list(tabuleiro_inicial)]
    nos_criados = 1 
    
    while pilha:
        tabuleiro_atual = pilha.pop()
        
        if None not in tabuleiro_atual:
            return tabuleiro_atual, nos_criados
            
        coluna_vazia = tabuleiro_atual.index(None)
        
        for linha in range(7, -1, -1):
            if posicao_segura(tabuleiro_atual, coluna_vazia, linha):
                novo_tabuleiro = list(tabuleiro_atual)
                novo_tabuleiro[coluna_vazia] = linha
                pilha.append(novo_tabuleiro)
                nos_criados += 1
                
    return None, nos_criados

def imprimir_tabuleiro(solucao, tabuleiro_inicial):

    if not solucao:
        print("Sem solução possível para este tabuleiro inicial.")
        return

    print("-" * 17)
    for linha in range(8):
        linha_visual = ""
        for coluna in range(8):
            # Se tem uma rainha nesta posição...
            if solucao[coluna] == linha:
                # Verifica se ela já estava lá desde o começo
                if tabuleiro_inicial[coluna] == linha:
                    linha_visual += "R " # Sua rainha!
                else:
                    linha_visual += "Q " # Rainha da IA
            else:
                linha_visual += ". " # Vazio
        print(linha_visual)
    print("-" * 17)



# --- TESTANDO TABULEIRO COM NENHUMA RAINHA FIXA ---
print("=== TABULEIRO COM NENHUMA RAINHA FIXA ===")
# Você não fixa nenhuma rainha
nenhuma_rainha = [None, None, None, None, None, None, None, None]
solucao_nenhuma, nos_nenhuma = resolver_oito_rainhas(nenhuma_rainha)

print(f"Nós (tentativas) da IA: {nos_nenhuma}")
imprimir_tabuleiro(solucao_nenhuma, nenhuma_rainha)

# --- TESTANDO TABULEIRO COM 1 RAINHA FIXA ---
print("=== TABULEIRO COM 1 RAINHA FIXA ===")
# Você fixa a rainha na coluna  (linha 7)
uma_rainha = [7, None, None, None, None, None, None, None]
solucao_uma, nos_uma = resolver_oito_rainhas(uma_rainha)

print(f"Nós (tentativas) da IA: {nos_uma}")
imprimir_tabuleiro(solucao_uma, uma_rainha)

# --- TESTANDO TABULEIRO COM 2 RAINHA FIXA ---
print("=== TABULEIRO COM 2 RAINHAS FIXAS ===")
# Você fixa as rainhas nas colunas 0 e 1 (linhas 2 e 6)
duas_rainhas = [2, 6, None, None, None, None, None, None]
solucao_duas, nos_duas = resolver_oito_rainhas(duas_rainhas)

print(f"Nós (tentativas) da IA: {nos_duas}")
imprimir_tabuleiro(solucao_duas, duas_rainhas)

# --- TESTANDO TABULEIRO COM 3 RAINHAS FIXAS ---
print("=== TABULEIRO COM 3 RAINHAS FIXAS ===")
# Você fixa as rainhas nas colunas 0, 1 e 2 (linhas 0, 4 e 7)
tres_rainhas = [0, 4, 7, None, None, None, None, None]
solucao_tres, nos_tres = resolver_oito_rainhas(tres_rainhas)

print(f"Nós (tentativas) da IA: {nos_tres}")
imprimir_tabuleiro(solucao_tres, tres_rainhas)