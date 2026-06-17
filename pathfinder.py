import heapq
from typing import TypeAlias
from parsing import Parser
from models import Zone

Path: TypeAlias = list[str]
HeapItem: TypeAlias = tuple[int, int, int, str, tuple[str, ...]]


class Pathfinder:
    """
    Finds valid paths between the start and end zones
    while considering zone costs and priorities.
    """
    # def calculate_path_cost(self, path: list[str]) -> int:
    #     if len(path) <= 1:
    #         return 0

    #     total_cost = 0
    #     for zone_name in path[1:]:
    #         zone_obj = self.zones[zone_name]
    #         total_cost += self.get_cost(zone_obj)

    #     return total_cost

    def __init__(self, parser: Parser) -> None:
        """
        Initialize pathfinding data and zone priority rules.
        """
        self.zones = parser.zones
        self.start = parser.start_zone
        self.end = parser.end_zone
        self.nb_drones = parser.nb_drones

        self.priority_map = {
            "normal": 1,
            "priority": 0,
            "restricted": 2,
            "start": 1,
            "end": 1
        }

    def get_cost(self, zone: Zone) -> int:
        """
        Return the movement cost of entering a zone.
        Restricted zones cost more than normal zones.
        """

        if zone.zone_type == "restricted":
            return 2
        return 1

    def get_paths(self, max_paths: int = 6) -> list[Path]:
        """
        Find up to max_paths valid paths from start to end
        using a priority-based search algorithm.
        """
        if not self.start or not self.end:
            return []

        heap: list[HeapItem] = [
            (
                0,  # cost / takolfa
                self.priority_map[self.start.zone_type],  # l2awlawiya
                1,  # lenght dial path 1 hitach kina ghir start
                self.start.name,  # zone li fiha hna
                (self.start.name,)  # paths tupe
            )
        ]

        founded_paths: list[Path] = []  # f kola kanwsel l goal we save here

        cost_margin = 3

        """cost_margin kanet dair 10 mais f map dail medum kan
        # kiakhtar lia 2 dail path walkin path tani kan kber men lawel
        # b 4 dail cost fa mli daret cost_margin ghir 3 wela mazain
        # ghadi yakhtar lia ghir path lawel li ghadi yjib lia
        # ahseb perfmonce.. :) """

        # ila darna 2 ghadi yjib lina paths mat9arbin ou
        # ou mkhaltin ghadi ndiro wait bzd

        # ou ila darna 40 ghadi yjib lina pths twa bzf -> big cost.
        best_cost: int | None = None  # None first
        #  BEST_COST kansajlo fih awel a9erb tri9 l end

        while heap and len(founded_paths) < max_paths:
            cost, priority, length, zone_name, path = heapq.heappop(heap)

            if best_cost is not None and cost > best_cost + cost_margin:
                break

            if zone_name == self.end.name:
                if best_cost is None:
                    best_cost = cost

                if list(path) not in founded_paths:
                    founded_paths.append(list(path))
                continue  # bach manchoufech neighbores dail goal

            current_zone = self.zones[zone_name]

            for neighbor in current_zone.neighbors:
                if neighbor.name in path or neighbor.zone_type == "blocked":
                    continue  # loops and blocked zone

                new_cost = cost + self.get_cost(neighbor)
                new_priority = priority + self.priority_map[neighbor.zone_type]
                new_path = path + (neighbor.name,)

                heapq.heappush(
                    heap,
                    (
                        new_cost,
                        new_priority,
                        length + 1,
                        neighbor.name,
                        new_path
                    )
                )

        return founded_paths
