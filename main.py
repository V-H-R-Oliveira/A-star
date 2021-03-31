from json import load
from operator import itemgetter
from sys import stderr


def read_json(path: str):
    with open(path, 'r') as f:
        return load(f)


def a_star(graph_path: str, heuristics_path: str, begin: str, goal: str):
    graph = read_json(graph_path)
    heuristics = read_json(heuristics_path)

    if begin not in graph or goal not in graph:
        print(f'{begin} ou {goal} não se encontram representados no grafo', file=stderr)
        return False, [], 0

    if begin == goal:
        return True, [begin, goal], graph[begin][goal]

    queue = [(begin, 0, heuristics[begin], begin)]
    visited = [begin]
    total_cost = [0]
    i = 0
    # debug = 5

    while len(queue) != 0:
        # if i == debug:
        #     break
        node, value, heuristic, parent = queue.pop(0)
        print(f'[{i}] Current: {node}-{value}-{heuristic}')

        if node == goal:
            last = visited[-1]

            if parent == last:
                visited.append(node)
                total_cost.append(value)
            else:
                visited[-1] = node
                total_cost[-1] = value

            print('Finish', visited, total_cost)
            return True, visited, sum(total_cost)

        for neighbor in graph[node]:
            if any((neighbor == i[0] for i in queue)):
                # print(neighbor, 'is in queue')
                element = list(filter(lambda key: key[0] == neighbor, queue))[0]
                _, previous_cost, previous_heuristic, _ = element
                new_cost = graph[node][neighbor] + value

                if new_cost < previous_cost:
                    new_heuristic = new_cost + heuristics[neighbor]
                    # print(
                    #     f'Replace {neighbor} previous cost {previous_cost} by {new_cost} and replace the previous heuristic {previous_heuristic} by {new_heuristic}')
                    queue.remove(element)
                    queue.append((neighbor, new_cost, new_heuristic, node))
                    continue

            if neighbor in visited:
                continue

            # print(neighbor, graph[node][neighbor], heuristics[neighbor], graph[node][neighbor] + heuristics[neighbor],
            #       value)
            new_cost = graph[node][neighbor] + value
            new_heuristic = new_cost + heuristics[neighbor]
            queue.append((neighbor, new_cost, new_heuristic, node))

        if node not in visited:
            print(f'[{i}] Processed', node, value)
            total_cost.append(value)
            visited.append(node)

        queue.sort(key=itemgetter(2))
        print(f'[{i}] Queue state:', queue)
        i += 1

    return False, [], 0


def main():
    start = 'arad'
    goal = 'bucharest'

    # start = 'S'
    # goal = 'E'
    has_path, path, cost = a_star('graph2.json', 'heuristics2.json', start, goal)

    if not has_path:
        print(f'Não existe um caminho válido entre {start} e {goal}')
        return

    print(f"Melhor caminho entre {start} e {goal}: {'->'.join(path)}\nCusto: {cost} unidades de distância")


if __name__ == '__main__':
    main()
