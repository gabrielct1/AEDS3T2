import networkx as nx
import matplotlib.pyplot as plt

# Função para carregar o grafo do arquivo CSV
def carregar_grafo(arquivo):
    G = nx.DiGraph()  # Cria um grafo direcionado

    # Abre o arquivo CSV para leitura
    with open(arquivo, 'r', encoding='utf-8') as f:
        next(f)  # Pular o cabeçalho do CSV
        for linha in f:
            partes = linha.strip().split(',')
            if len(partes) < 5:
                print(f"Formato incorreto na linha: {linha.strip()}")
                continue  # Pular linhas com formato incorreto
            codigo, nome, periodo, duracao, dependencias = partes
            dependencias = dependencias.split(';') if dependencias else []
            
            # Adiciona arestas ao grafo baseadas nas dependências
            for dep in dependencias:
                if dep:  # Verifica se a dependência não está vazia
                    G.add_edge(dep, codigo, weight=1)  # Adiciona a aresta com peso padrão (1)

    return G

# Função para encontrar o caminho crítico no grafo
def encontrar_caminho_critico(G):
    topo = list(nx.topological_sort(G))  # Ordenação topológica dos nós
    comprimento = {}  # Dicionário para armazenar o comprimento do caminho até cada nó
    predecessores = {}  # Dicionário para armazenar o predecessor de cada nó
    
    for node in topo:
        comprimento[node] = 0
        predecessores[node] = None

    # Calcula o comprimento do caminho crítico
    for node in topo:
        for succ in G.successors(node):
            peso = G[node][succ]['weight']
            if comprimento[node] + peso > comprimento.get(succ, 0):
                comprimento[succ] = comprimento[node] + peso
                predecessores[succ] = node

    # Encontra o nó com o comprimento máximo
    max_node = max(comprimento, key=comprimento.get)
    caminho_critico = []
    while max_node is not None:
        caminho_critico.append(max_node)
        max_node = predecessores[max_node]

    caminho_critico.reverse()  # Inverte a lista para obter o caminho do início ao fim
    return caminho_critico, comprimento[caminho_critico[-1]]

# Função para desenhar o grafo com destaque para o caminho crítico
def desenhar_grafo(G, caminho_critico):
    pos = nx.spring_layout(G, seed=123)  # Layout para a visualização do grafo
    plt.figure(figsize=(12, 8))
    
    # Cria um conjunto de arestas do caminho crítico para destacá-las
    path_edges = set((caminho_critico[i], caminho_critico[i+1]) for i in range(len(caminho_critico) - 1))
    edge_colors = ['red' if (u, v) in path_edges else 'black' for u, v in G.edges()]
    node_colors = ['lightgreen' if node in caminho_critico else 'lightblue' for node in G.nodes()]

    # Desenha o grafo com os nós e arestas destacados
    nx.draw(G, pos, with_labels=True, node_size=2000, node_color=node_colors, edge_color=edge_colors, font_size=10, font_weight='bold', arrows=True)
    plt.title("Grafo de Dependências com Caminho Crítico Destacado")
    plt.show()

# Função principal
def main():
    while True:
        arquivo = input("Informe o arquivo (0 para sair): ")
        if arquivo == '0':
            break
        try:
            print("Processando ...")
            G = carregar_grafo(arquivo)  # Carrega o grafo do arquivo CSV
            caminho_critico, tempo_minimo = encontrar_caminho_critico(G)  # Encontra o caminho crítico
            
            # Exibe o caminho crítico e o tempo mínimo
            print("Caminho Crítico:")
            for tarefa in caminho_critico:
                print(f"- {tarefa}")

            print(f"Tempo Mínimo: {tempo_minimo}")

            desenhar_grafo(G, caminho_critico)  # Desenha o grafo com o caminho crítico destacado
        except Exception as e:
            print(f"Erro ao processar o arquivo: {e}")

if __name__ == "__main__":
    main()
