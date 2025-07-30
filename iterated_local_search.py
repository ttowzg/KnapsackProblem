import random
import time

def calcular_valor_solucao(solucao, itens):
    """Calcula o lucro e o peso total de uma solução."""
    lucro_total = 0
    peso_total = 0
    for i, item in enumerate(itens):
        if solucao[i] == 1:
            lucro_total += item['lucro']
            peso_total += item['peso']
    return lucro_total, peso_total

def gerar_solucao_inicial(itens, capacidade):
    """Gera uma solução inicial aleatória, mas válida."""
    solucao = [0] * len(itens)
    peso_atual = 0
    indices_disponiveis = list(range(len(itens)))
    random.shuffle(indices_disponiveis)
    for i in indices_disponiveis:
        if peso_atual + itens[i]['peso'] <= capacidade:
            solucao[i] = 1
            peso_atual += itens[i]['peso']
    return solucao

def gerar_vizinho(solucao_atual, itens, capacidade):
    """Gera uma solução vizinha válida trocando um bit aleatoriamente."""
    vizinho = solucao_atual[:]
    for _ in range(len(itens)): 
        posicao_troca = random.randint(0, len(itens) - 1)
        vizinho[posicao_troca] = 1 - vizinho[posicao_troca]
        _, peso_vizinho = calcular_valor_solucao(vizinho, itens)
        if peso_vizinho <= capacidade:
            return vizinho
        else:
            vizinho[posicao_troca] = 1 - vizinho[posicao_troca]
    return solucao_atual

def busca_local(solucao_atual, itens, capacidade, max_iter_sem_melhora=100):
    """
    Melhora uma solução explorando sua vizinhança até atingir um ótimo local.
    """
    melhor_solucao = solucao_atual[:]
    melhor_lucro, _ = calcular_valor_solucao(melhor_solucao, itens)
    
    for _ in range(max_iter_sem_melhora):
        vizinho = gerar_vizinho(melhor_solucao, itens, capacidade)
        lucro_vizinho, _ = calcular_valor_solucao(vizinho, itens)

        if lucro_vizinho > melhor_lucro:
            melhor_solucao = vizinho[:]
            melhor_lucro = lucro_vizinho

    return melhor_solucao, melhor_lucro

# ---Função de Perturbação ---
def perturbar_solucao(solucao_atual, itens, capacidade, forca_perturbacao):
    """
    Aplica uma perturbação na solução, trocando um número de bits.
    """
    solucao_perturbada = solucao_atual[:]
    
    # Inverte um número de bits igual à força da perturbação
    posicoes_para_trocar = random.sample(range(len(itens)), forca_perturbacao)
    for pos in posicoes_para_trocar:
        solucao_perturbada[pos] = 1 - solucao_perturbada[pos]

    # Garante que a solução ainda é válida. Se não for, retorna a original.
    _, peso_total = calcular_valor_solucao(solucao_perturbada, itens)
    if peso_total > capacidade:
        return solucao_atual # Retorna a original se a perturbação a invalidou
        ''
    return solucao_perturbada

def executar(instancia):
    """
    Executa o algoritmo Iterated Local Search para uma instância do problema.
    """
    print("Executando Iterated Local Search...")
    inicio = time.time()

    # --- Parâmetros do ILS ---
    max_iteracoes_ils = 1000
    forca_perturbacao = 3 # Quantos itens serão trocados na perturbação
    
    itens = instancia['itens']
    capacidade = instancia['capacidade']

    # --- 1. Geração da Solução Inicial ---
    solucao_inicial = gerar_solucao_inicial(itens, capacidade)
    
    # --- 2. Aplica a Busca Local para encontrar o primeiro ótimo local ---
    melhor_solucao_geral, melhor_lucro_geral = busca_local(solucao_inicial, itens, capacidade)
    
    # --- Loop principal do ILS ---
    for i in range(max_iteracoes_ils):
        # 3. Perturbação: "Chacoalha" a melhor solução encontrada até agora
        solucao_perturbada = perturbar_solucao(melhor_solucao_geral, itens, capacidade, forca_perturbacao)

        # 4. Busca Local: Começa a busca a partir da solução perturbada
        nova_solucao, novo_lucro = busca_local(solucao_perturbada, itens, capacidade)

        # 5. Critério de Aceitação: Se a nova solução for melhor, atualiza
        if novo_lucro > melhor_lucro_geral:
            melhor_solucao_geral = nova_solucao[:]
            melhor_lucro_geral = novo_lucro
            print(f"ILS Iteração {i+1}: Novo melhor lucro encontrado = {melhor_lucro_geral}")


    fim = time.time()
    tempo_execucao = fim - inicio
    
    print(f"Melhor solução encontrada pelo ILS: Lucro = {melhor_lucro_geral}")
    print(f"Tempo de execução do ILS: {tempo_execucao:.4f} segundos")

    return {
        'solucao': melhor_solucao_geral,
        'lucro': melhor_lucro_geral,
        'tempo': tempo_execucao
    }