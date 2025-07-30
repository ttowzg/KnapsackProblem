import os

def carregar_instancia_kplib(caminho_arquivo):
    """
    Lê um arquivo de instância do Problema da Mochila do repositório kplib.
    """
    if not os.path.exists(caminho_arquivo):
        print(f"Erro: Arquivo não encontrado em '{caminho_arquivo}'")
        return None

    with open(caminho_arquivo, 'r') as f:
        linhas = f.readlines()

    linhas = [linha for linha in linhas if linha.strip()]

    # Verifica se o arquivo não está vazio após a limpeza
    if not linhas:
        print(f"Erro: O arquivo '{caminho_arquivo}' está vazio ou contém apenas linhas em branco.")
        return None

    
    # Lê o número de itens e a capacidade
    try:
        n_itens = int(linhas[0].strip())
        capacidade = int(linhas[1].strip())
    except (ValueError, IndexError):
        print(f"Erro: Formato inválido no cabeçalho do arquivo '{caminho_arquivo}'. Verifique se as duas primeiras linhas contêm números.")
        return None
    
    itens = []
    # Lê os itens (lucro e peso)
    for i in range(2, n_itens + 2):
        try:
            lucro, peso = map(int, linhas[i].strip().split())
            itens.append({'lucro': lucro, 'peso': peso})
        except (ValueError, IndexError):
            print(f"Erro: Formato inválido na linha {i+1} do arquivo '{caminho_arquivo}'.")
            return None
            
    return {
        'nome': os.path.basename(caminho_arquivo),
        'n_itens': n_itens,
        'capacidade': capacidade,
        'itens': itens
    }
"""
# --- Bloco de Teste ---
if __name__ == "__main__":
    print("--- Testando o módulo leitor_instancias.py de forma isolada ---")
    
    # Este caminho precisa ser corrigido aqui também para o teste isolado funcionar no Windows
    caminho_de_teste = 'kplib/00Uncorrelated/n00050/R01000/s000.kp'
    instancia_teste = carregar_instancia_kplib(caminho_de_teste)

    if instancia_teste:
        print("Módulo de leitura funcionando corretamente!")
        print(f"Nome da instância: {instancia_teste['nome']}")

        """