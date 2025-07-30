import leitor_instancias 
import os
import simulated_annealing
import iterated_local_search

# 1. Dicionário com as soluções ótimas conhecidas
"""
SOLUCOES_OTIMAS = {
    's000.kp': 23674,
    's001.kp': 34777,
    's002.kp': 87868
}
"""
# 2. Outro dicionário com as soluções ótimas conhecidas
SOLUCOES_OTIMAS = {
    'knapPI_1_100_1000_1': 9147,
    'knapPI_1_500_1000_1': 28857,
    'f8_l-d_kp_23_10000': 9767
}

# 2. Função que calcula o Gap Relativo, conforme a fórmula do TP2
def calcular_gap(lucro_otimo, lucro_heuristica):
    """Calcula o gap relativo percentual."""
    if lucro_otimo == 0:
        return float('inf') # Evita divisão por zero
    # Fórmula do TP2: Gap(%) = ((z* - z_heur) / z*) * 100
    gap = ((lucro_otimo - lucro_heuristica) / lucro_otimo) * 100
    return gap

def main():
    """
    Função principal que orquestra a execução do programa.
    """
    print("--- Iniciando o resolvedor para o Problema da Mochila ---")

    # caminho das pastas --- teste 1
    """instancias_para_testar = [
        'kplib/00Uncorrelated/n00050/R01000/s000.kp',
        'kplib/02StronglyCorrelated/n00100/R01000/s001.kp',
        'kplib/01WeaklyCorrelated/n00200/R01000/s002.kp'
    ]
    """
    # caminho das pastas --- teste 2 -------------------------------->aqui
    instancias_para_testar = [
        'kplib/large_scale/knapPI_1_100_1000_1',
        'kplib/large_scale/knapPI_1_500_1000_1',
        'kplib/low-dimensional/f8_l-d_kp_23_10000'
    ]

    # Itera sobre cada instância da lista
    for caminho in instancias_para_testar: 
        nome_arquivo = os.path.basename(caminho)
        print(f"\n--- Processando instância: {nome_arquivo} ---")
        
        instancia_atual = leitor_instancias.carregar_instancia_kplib(caminho)
        
        if instancia_atual:
            print(f"Dados carregados: Capacidade={instancia_atual['capacidade']}, Itens={instancia_atual['n_itens']}")
            
            # Pega o valor ótimo do nosso dicionário
            lucro_otimo = SOLUCOES_OTIMAS.get(nome_arquivo)
            
            if lucro_otimo is not None:
                print(f"Valor Ótimo Conhecido: {lucro_otimo}")

                # --- Execução do Simulated Annealing ---
                resultado_sa = simulated_annealing.executar(instancia_atual)
                # 3. Calcula e imprime o Gap para o SA
                gap_sa = calcular_gap(lucro_otimo, resultado_sa['lucro'])
                print(f"-> Tempo SA: {resultado_sa['tempo']:.4f}s | Lucro Encontrado SA: {resultado_sa['lucro']} | Gap Relativo SA: {gap_sa:.2f}%")
                
                print("-" * 20) # Linha separadora para clareza

                # --- Execução do Iterated Local Search ---
                resultado_ils = iterated_local_search.executar(instancia_atual)
                # 3. Calcula e imprime o Gap para o ILS
                gap_ils = calcular_gap(lucro_otimo, resultado_ils['lucro'])
                print(f"-> Tempo ILS: {resultado_ils['tempo']:.4f}s | Lucro Encontrado ILS: {resultado_ils['lucro']} | Gap Relativo ILS: {gap_ils:.2f}%")

            else:
                print(f"AVISO: Solução ótima para '{nome_arquivo}' não foi definida no dicionário SOLUCOES_OTIMAS.")

        else:
            print(f"Falha ao carregar a instância. Pulando para a próxima.")

# Garante que a função main() seja chamada quando o script for executado
if __name__ == "__main__":
    main()