from cfg import build_cfg
from isomorphism import find_isomorphism
from parser import parse_file
from traversal import dfs, unreachable_blocks
from visualization import draw_cfg

'''Можно поменять для анализа других REIL программ'''
# FILE1 = 'examples/file1.rail'
# FILE2 = 'examples/not_isomorphic.rail'

FILE1 = 'examples/totient.reil'
FILE2 = ''


def show_cfg(graph):
    print('Граф потока управления:')
    for node, neighbors in graph.edges.items():
        print(f'B{node} -> {[f'B{n}' for n in neighbors]}')


def main():
    file1 = FILE1
    print(f'Первый REIL-файл: {file1}')
    file2 = FILE2
    print(f'Второй REIL-файл: {file2}')

    first = build_cfg(parse_file(file1))

    print('========== CFG 1 ==========')
    show_cfg(first)

    print('DFS:', dfs(first))
    print('Недостижимые:', unreachable_blocks(first))

    draw_cfg(first, 'CFG первой программы')

    if file2:
        second = build_cfg(parse_file(file2))

        print('========== CFG 2 ==========')
        show_cfg(second)

        print('DFS:', dfs(second))
        print('Недостижимые:', unreachable_blocks(second))

        draw_cfg(second, 'CFG второй программы')

        mapping = find_isomorphism(first, second)

        if mapping is None:
            print('Графы не изоморфны')
        else:
            print('Графы изоморфны')
            print('Соответствие вершин:', mapping)


if __name__ == '__main__':
    main()
