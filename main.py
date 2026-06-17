import sys
from parsing import Parser
from pathfinder import Pathfinder
from simulation import Sminulation
from visualizer import Visualizer


def main() -> int:
    if len(sys.argv) != 2:
        print("Missing path file")
        exit(1)

    file_path = sys.argv[1]

    pars = Parser(file_path)
    pars.parser()

    # for a, b in pars.zones.items():
    #     lst = []
    #     for c in b.neighbors:
    #         lst.append(c.name)
    #     print(a, "->", lst)

    pathfinder = Pathfinder(pars)
    paths = pathfinder.get_paths(max_paths=4)

    if not paths:
        print("Error: No paths available to distribute.")
        exit(1)

    print("\n", len(paths), "\n")

    sim = Sminulation(pars, paths)
    # sim.run()

    vis = Visualizer(pars, sim)
    vis.run_visualization()
    print(f"\ntotal turns: {sim.turn_count}")

    # path = pathfinder.get_paths(max_paths=6)
    # print(f" number is {len(path)}\n")

    # for i, p in enumerate(path, start=1):
    #     cost = pathfinder.calculate_path_cost(p)
    #     print(f"way nuber is  {i} cost is : {cost} Turns):")
    #     print(" -> ".join(p))
    #     print()

    return 0


main()
