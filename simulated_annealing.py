import random
import time
import math 

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

# ---  Função para gerar uma solução vizinha ---
def gerar_vizinho(solucao_atual, itens, capacidade):
    """Gera uma solução vizinha válida trocando um bit aleatoriamente."""
    vizinho = solucao_atual[:] # Cria uma cópia da solução
    
    # Tenta gerar um vizinho válido em até N tentativas
    for _ in range(len(itens)): 
        posicao_troca = random.randint(0, len(itens) - 1)
        vizinho[posicao_troca] = 1 - vizinho[posicao_troca] # Inverte o bit

        _, peso_vizinho = calcular_valor_solucao(vizinho, itens)
        
        # Se o vizinho for válido, retorna. Senão, desfaz a troca e tenta de novo.
        if peso_vizinho <= capacidade:
            return vizinho
        else:
            vizinho[posicao_troca] = 1 - vizinho[posicao_troca] # Desfaz

    return solucao_atual # Se não encontrar vizinho válido, retorna a original

def executar(instancia):
    """
    Executa o algoritmo Simulated Annealing para uma instância do problema.
    """
    print("Executando Simulated Annealing...")
    inicio = time.time()

    # --- Parâmetros do Simulated Annealing ---
    temperatura_inicial = 1000
    temperatura_final = 1
    taxa_resfriamento = 0.995
    iteracoes_por_temperatura = 100 # Número de vizinhos a explorar por temperatura
    
    itens = instancia['itens']
    capacidade = instancia['capacidade']

    # --- 1. Geração da Solucao Inicial ---
    solucao_atual = gerar_solucao_inicial(itens, capacidade)
    lucro_atual, _ = calcular_valor_solucao(solucao_atual, itens)
    
    # Guarda a melhor solução encontrada até agora
    melhor_solucao = solucao_atual[:]
    melhor_lucro = lucro_atual
    
    temperatura = temperatura_inicial
    
    # --- Loop principal do Simulated Annealing ---
    while temperatura > temperatura_final:
        for _ in range(iteracoes_por_temperatura):
            # 2. Geração de um vizinho
            vizinho = gerar_vizinho(solucao_atual, itens, capacidade)
            lucro_vizinho, _ = calcular_valor_solucao(vizinho, itens)

            # 3. Decidir se aceita o vizinho
            diferenca_lucro = lucro_vizinho - lucro_atual

            if diferenca_lucro > 0: # Se o vizinho é melhor, aceita
                solucao_atual = vizinho[:]
                lucro_atual = lucro_vizinho
            else:
                # Se for pior, aceita com uma probabilidade
                probabilidade = math.exp(diferenca_lucro / temperatura)
                if random.random() < probabilidade:
                    solucao_atual = vizinho[:]
                    lucro_atual = lucro_vizinho
            
            # Atualiza a melhor solução encontrada
            if lucro_atual > melhor_lucro:
                melhor_solucao = solucao_atual[:]
                melhor_lucro = lucro_atual
        
        # 4. Resfriamento da temperatura
        temperatura *= taxa_resfriamento

    fim = time.time()
    tempo_execucao = fim - inicio
    
    print(f"Melhor solução encontrada pelo SA: Lucro = {melhor_lucro}")
    print(f"Tempo de execução do SA: {tempo_execucao:.4f} segundos")

    # Retorna a MELHOR solução encontrada
    return {
        'solucao': melhor_solucao,
        'lucro': melhor_lucro,
        'tempo': tempo_execucao
    }