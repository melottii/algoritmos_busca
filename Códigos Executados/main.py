import random

import time
from collections import deque
from drive.MyDrive.Faculdade.IA.Trabalho_1.Resources.viewer import MazeViewer
from math import inf, sqrt


"""
    Aluno: Matheus Xavier Melotti
    Data: 18/10/2023
"""


def gera_labirinto(n_linhas, n_colunas, inicio, goal):
    # cria labirinto vazio
    labirinto = [[0] * n_colunas for _ in range(n_linhas)]

    # adiciona celulas ocupadas em locais aleatorios de
    # forma que 50% do labirinto esteja ocupado
    numero_de_obstaculos = int(0.40 * n_linhas * n_colunas)
    for _ in range(numero_de_obstaculos):
        linha = random.randint(0, n_linhas - 1)
        coluna = random.randint(0, n_colunas - 1)
        labirinto[linha][coluna] = 1

    # remove eventuais obstaculos adicionados na posicao
    # inicial e no goal
    labirinto[inicio.y][inicio.x] = 0
    labirinto[goal.y][goal.x] = 0

    return labirinto


def total_time(tempo_final):
    if tempo_final < 60:
        tempo_segundos = round(tempo_final, 2)
        mensagem = f'{tempo_segundos} segundos'
    elif 60 < tempo_final < 3600:
        tempo_minutos = tempo_final / 60
        tempo_minutos = round(tempo_minutos, 2)
        mensagem = f'{tempo_minutos} minutos'
    else:
        tempo_horas = tempo_final / 3600
        tempo_horas = round(tempo_horas, 2)
        mensagem = f'{tempo_horas} horas'
    return mensagem


class Celula:
    def __init__(self, y, x, anterior, custo):
        self.y = y
        self.x = x
        self.anterior = anterior
        self.custo = custo

    def __lt__(self, other):
        return self.custo < other.custo


def distancia(celula_1, celula_2):
    dx = celula_1.x - celula_2.x
    dy = celula_1.y - celula_2.y
    return sqrt(dx ** 2 + dy ** 2)


def esta_contido(lista, celula):
    for elemento in lista:
        if (elemento.y == celula.y) and (elemento.x == celula.x):
            return True
    return False


def custo_caminho(caminho):
    if len(caminho) == 0:
        return inf

    custo_total = 0
    for i in range(1, len(caminho)):
        custo_total += distancia(caminho[i].anterior, caminho[i])

    return custo_total


def obtem_caminho(goal):
    caminho = []

    celula_atual = goal
    while celula_atual is not None:
        caminho.append(celula_atual)
        celula_atual = celula_atual.anterior

    # o caminho foi gerado do final para o
    # comeco, entao precisamos inverter.
    caminho.reverse()

    return caminho


def celulas_vizinhas_livres(celula_atual, labirinto):
    # generate neighbors of the current state
    vizinhos = [Celula(y=celula_atual.y - 1, x=celula_atual.x - 1, anterior=celula_atual, custo=0),
                Celula(y=celula_atual.y + 0, x=celula_atual.x - 1, anterior=celula_atual, custo=0),
                Celula(y=celula_atual.y + 1, x=celula_atual.x - 1, anterior=celula_atual, custo=0),
                Celula(y=celula_atual.y - 1, x=celula_atual.x + 0, anterior=celula_atual, custo=0),
                Celula(y=celula_atual.y + 1, x=celula_atual.x + 0, anterior=celula_atual, custo=0),
                Celula(y=celula_atual.y + 1, x=celula_atual.x + 1, anterior=celula_atual, custo=0),
                Celula(y=celula_atual.y + 0, x=celula_atual.x + 1, anterior=celula_atual, custo=0),
                Celula(y=celula_atual.y - 1, x=celula_atual.x + 1, anterior=celula_atual, custo=0), ]

    # seleciona as celulas livres
    vizinhos_livres = []
    for v in vizinhos:
        # verifica se a celula esta dentro dos limites do labirinto
        if (v.y < 0) or (v.x < 0) or (v.y >= len(labirinto)) or (v.x >= len(labirinto[0])):
            continue
        # verifica se a celula esta livre de obstaculos.
        if labirinto[v.y][v.x] == 0:
            vizinhos_livres.append(v)

    return vizinhos_livres


def breadth_first_search(labirinto, inicio, goal, viewer):
    fronteira = deque()
    expandidos = set()
    fronteira.append(inicio)
    goal_encontrado = None
    while (len(fronteira) > 0) and (goal_encontrado is None):
        no_atual = fronteira.popleft()
        vizinhos = celulas_vizinhas_livres(no_atual, labirinto)
        for v in vizinhos:
            if v.y == goal.y and v.x == goal.x:
                goal_encontrado = v
                break
            else:
                if (not esta_contido(expandidos, v)) and (not esta_contido(fronteira, v)):
                    fronteira.append(v)
        expandidos.add(no_atual)
    viewer.update(generated=fronteira,
                  expanded=expandidos)
    caminho = obtem_caminho(goal_encontrado)
    custo = custo_caminho(caminho)
    return caminho, custo, expandidos


def depth_first_search(labirinto, inicio, goal, viewer):
    fronteira = deque()
    expandidos = set()
    fronteira.append(inicio)
    goal_encontrado = None
    while (len(fronteira) > 0) and (goal_encontrado is None):
        no_atual = fronteira.pop()
        vizinhos = celulas_vizinhas_livres(no_atual, labirinto)
        for v in vizinhos:
            if v.y == goal.y and v.x == goal.x:
                goal_encontrado = v
                break
            else:
                if (not esta_contido(expandidos, v)) and (not esta_contido(fronteira, v)):
                    fronteira.append(v)
        expandidos.add(no_atual)
    viewer.update(generated=fronteira,
                  expanded=expandidos)
    caminho = obtem_caminho(goal_encontrado)
    custo = custo_caminho(caminho)
    return caminho, custo, expandidos


def menor_star(lista,destino):
    d = destino
    for i in lista:
        if d == destino:
            d = i
        elif distancia(d,destino)> distancia(i,destino):
            d = i
    return d


def a_star_search(labirinto, inicio, goal, viewer):
    fronteira = deque()
    expandidos = set()
    fronteira.append(inicio)
    goal_encontrado = None
    while (len(fronteira) > 0) and (goal_encontrado is None):
        no_atual = menor_star(fronteira, goal)
        fronteira.remove(no_atual)
        vizinhos = celulas_vizinhas_livres(no_atual, labirinto)
        for v in vizinhos:
            if v.y == goal.y and v.x == goal.x:
                goal_encontrado = v
                break
            else:
                if (not esta_contido(expandidos, v)) and (not esta_contido(fronteira, v)):
                    fronteira.append(v)
        expandidos.add(no_atual)
    viewer.update(generated=fronteira,
                  expanded=expandidos)
    caminho = obtem_caminho(goal_encontrado)
    custo = custo_caminho(caminho)
    return caminho, custo, expandidos


def uniform_cost_search(labirinto, inicio, goal, viewer):
    fronteira = deque()
    expandidos = set()
    fronteira.append(inicio)
    goal_encontrado = None
    no_atual = inicio
    caminhos = []
    while (len(fronteira) > 0) and (goal_encontrado is None):
        for n in fronteira:
            if distancia(n, inicio) <= distancia(no_atual, inicio):
                no_atual = n
            else:
                no_atual = fronteira[0]
        fronteira.remove(no_atual)
        vizinhos = celulas_vizinhas_livres(no_atual, labirinto)
        for v in vizinhos:
            if v.y == goal.y and v.x == goal.x:
                goal_encontrado = v
                caminhos.append(goal_encontrado)
            else:
                if (not esta_contido(expandidos, v)) and (not esta_contido(fronteira, v)):
                    fronteira.append(v)
        expandidos.add(no_atual)
    viewer.update(generated=fronteira,
                  expanded=expandidos)
    caminho = obtem_caminho(goal_encontrado)
    custo = custo_caminho(caminho)
    return caminho, custo, expandidos


def main():
    seed = 0
    random.seed(seed)
    n_linhas = 25
    n_colunas = 25
    start = Celula(y=0, x=0, anterior=None, custo=0)
    goal = Celula(y=n_linhas - 1, x=n_colunas - 1, anterior=None, custo=0)

    """
    O labirinto sera representado por uma matriz (lista de listas)
    em que uma posicao tem 0 se ela eh livre e 1 se ela esta ocupada.
    """
    labirinto = gera_labirinto(n_linhas, n_colunas, start, goal)

    viewer = MazeViewer(labirinto, start, goal, step_time_miliseconds=20, zoom=40)

    # ----------------------------------------
    # BFS Search
    # ----------------------------------------

    start_time_bfs = time.time()
    viewer._figname = "BFS"
    caminho_bfs, custo_total_bfs, expandidos_bfs = breadth_first_search(labirinto, start, goal, viewer)
    end_time_bfs = total_time(time.time() - start_time_bfs)
    if len(caminho_bfs) == 0:
        print("Goal é inalcançavel neste labirinto.")
    print(f"BFS:"
          f"\tTempo de execução: {end_time_bfs}.\n"
          f"\tCusto total do caminho: {custo_total_bfs}.\n"
          f"\tNumero de passos: {len(caminho_bfs) - 1}.\n"
          f"\tNumero total de nos expandidos: {len(expandidos_bfs)}.\n\n"
          )

    viewer.update(path=caminho_bfs, view=True)
    viewer.pause()

    # ----------------------------------------
    # DFS Search
    # ----------------------------------------
    """
        start_time_dfs = time.time()
        viewer._figname = "DFS"
        caminho_dfs, custo_total_dfs, expandidos_dfs = depth_first_search(labirinto, start, goal, viewer)
        end_time_dfs = total_time(time.time() - start_time_dfs)
        if len(caminho_dfs) == 0:
            print("Goal é inalcançável neste labirinto.")
        print(f"DFS:"
              f"\tTempo de execução: {end_time_dfs}.\n"
              f"\tCusto total do caminho: {custo_total_dfs}.\n"
              f"\tNumero de passos: {len(caminho_dfs) - 1}.\n"
              f"\tNumero total de nós expandidos: {len(expandidos_dfs)}.\n\n")
        viewer.update(path=caminho_dfs, view=True)
        viewer.pause()
    """
    # ----------------------------------------
    # A-Star Search
    # ----------------------------------------
    """
        start_time_ast = time.time()
        viewer._figname = "AST"
        caminho_ast, custo_total_ast, expandidos_ast = a_star_search(labirinto, start, goal, viewer)
        if len(caminho_ast) == 0:
            print("Goal é inalcançável neste labirinto.")
        print(f"AST:"
              f"\tTempo de execução: {total_time(time.time() - start_time_ast)}.\n"
              f"\tCusto total do caminho: {custo_total_ast}.\n"
              f"\tNumero de passos: {len(caminho_ast) - 1}.\n"
              f"\tNumero total de nós expandidos: {len(expandidos_ast)}.\n\n")
        viewer.update(path=caminho_ast, view=True)
        viewer.pause()
    """
    # ----------------------------------------
    # Uniform Cost Search (Obs: opcional)
    # ----------------------------------------
    """
        start_time_ucs = time.time()
        viewer._figname = "UCS"
        caminho_ucs, custo_total_ucs, expandidos_ucs = uniform_cost_search(labirinto, start, goal, viewer)
        if len(caminho_ucs) == 0:
            print("Goal é inalcançável neste labirinto.")
        print(f"UCS:"
              f"\tTempo de execução: {total_time(time.time() - start_time_ucs)}.\n"
              f"\tCusto total do caminho: {custo_total_ucs}.\n"
              f"\tNumero de passos: {len(caminho_ucs) - 1}.\n"
              f"\tNumero total de nós expandidos: {len(expandidos_ucs)}.\n\n")
        viewer.update(path=caminho_ucs, view=True)
        viewer.pause()
    """


if __name__ == "__main__":
    main()
