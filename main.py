import networkx as nx
import matplotlib.pyplot as plt


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

            # Adiciona o nó com sua duração como atributo
            G.add_node(codigo, nome=nome, duracao=int(duracao))

            # Adiciona arestas ao grafo baseadas nas dependências
            for dep in dependencias:
                if dep:  # Verifica se a dependência não está vazia
                    # Adiciona a aresta com o peso
                    G.add_edge(dep, codigo, weight=int(
                        G.nodes[dep]['duracao']))

    return G


def encontrar_caminho_critico_bellman_ford(G):
    # Encontrar o(s) nó(s) inicial(is) (nós sem predecessores)
    no_inicial = [n for n in G.nodes() if G.in_degree(n) == 0]

    if not no_inicial:
        raise ValueError("O grafo não tem um nó inicial válido.")

    # Inicializa distâncias com valores negativos infinitos (para maximizar)
    distancias = {node: float('-inf') for node in G.nodes()}
    predecessores = {node: None for node in G.nodes()}

    # Define a distância inicial para todos os nós sem predecessores
    for inicio in no_inicial:
        distancias[inicio] = G.nodes[inicio]['duracao']

    # Relaxamento das arestas N-1 vezes (onde N é o número de nós)
    for _ in range(len(G.nodes()) - 1):
        for node in G.nodes():
            for vizinho in G.successors(node):
                peso_aresta = G.nodes[vizinho]['duracao']
                nova_dist = distancias[node] + peso_aresta

                if nova_dist > distancias[vizinho]:
                    distancias[vizinho] = nova_dist
                    predecessores[vizinho] = node

    # Detectar ciclos negativos (não esperamos ter no caminho crítico)
    for node in G.nodes():
        for vizinho in G.successors(node):
            peso_aresta = G.nodes[vizinho]['duracao']
            if distancias[node] + peso_aresta > distancias[vizinho]:
                raise ValueError("O grafo contém um ciclo de peso negativo.")

    # Encontrar o nó final com maior distância
    max_node = max(distancias, key=distancias.get)

    # Reconstruir o caminho crítico
    caminho_critico = []
    while max_node is not None:
        caminho_critico.append(max_node)
        max_node = predecessores[max_node]

    caminho_critico.reverse()
    return caminho_critico, distancias[caminho_critico[-1]]


def desenhar_grafo_caminho_critico(G, caminho_critico, nome_arquivo="grafo_critico.png"):
    plt.figure(figsize=(12, 8))

    # Cria um subgrafo contendo apenas os nós e arestas do caminho crítico
    subgrafo = G.subgraph(caminho_critico).copy()

    # Cria o layout para a visualização
    pos = nx.spring_layout(subgrafo, seed=123)

    # Cria um conjunto de arestas do caminho crítico
    path_edges = [(caminho_critico[i], caminho_critico[i+1])
                  for i in range(len(caminho_critico) - 1)]

    # Define as cores dos nós e arestas para destacar o caminho crítico
    node_colors = ['lightgreen' for node in subgrafo.nodes()]
    edge_colors = ['red' for edge in path_edges]

    # Desenha os nós e as arestas do subgrafo contendo o caminho crítico
    nx.draw(subgrafo, pos, with_labels=True, node_size=2000, node_color=node_colors,
            edge_color=edge_colors, font_size=10, font_weight='bold', arrows=True)

    plt.title("Caminho Crítico Destacado no Grafo")

    # Salva o gráfico em um arquivo de imagem
    plt.savefig(nome_arquivo)
    plt.close()  # Fecha a figura para evitar sobreposição em novos gráficos


def main():
    while True:
        arquivo = input("Informe o arquivo (0 para sair): ")
        if arquivo == '0':
            break
        try:
            print("Processando ...")
            G = carregar_grafo(arquivo)  # Carrega o grafo do arquivo CSV
            caminho_critico, tempo_minimo = encontrar_caminho_critico_bellman_ford(
                G)  # Encontra o caminho crítico

            # Exibe o caminho crítico e o tempo mínimo
            print("\nCaminho Crítico:\n")
            for tarefa in caminho_critico:
                print(f"- {G.nodes[tarefa]['nome']}")

            print(f"\nTempo Mínimo: {tempo_minimo}\n")

            # Gera um nome de arquivo para salvar a imagem
            nome_arquivo = "grafo_caminho_critico.png"
            # Desenha o grafo com o caminho crítico destacado e salva como imagem
            desenhar_grafo_caminho_critico(G, caminho_critico, nome_arquivo)
            print(f"Gráfico salvo como {nome_arquivo}")
        except Exception as e:
            print(f"\nErro ao processar o arquivo: {e}\n")


if __name__ == "__main__":
    main()
