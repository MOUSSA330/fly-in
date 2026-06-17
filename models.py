from typing import List


class Zone:
    """
    Represents a graph node (zone) with its position,
    properties and neighboring zones.
    """
    def __init__(
            self,
            name: str,
            x: int,
            y: int,
            zone_type: str = "normal",
            color: str = "none",
            max_drones: int = 1) -> None:
        """
        Initialize a zone with coordinates, type,
        color, capacity and neighbors list.
        """
        self.name = name
        self.x = x
        self.y = y
        self.zone_type = zone_type
        self.color = color
        self.max_drones = max_drones

        self.neighbors: List[Zone] = []  # Adjancency List its name in alghos
        # its mian hada Graph
        # its mein ana 3andi zonz a martabta b 2 dail neibord
        # b ou c matalan


class Connections:
    """
    Represents an undirected connection between
    two zones with a link capacity.
    """
    def __init__(
            self,
            zone1: str,
            zone2: str,
            max_link_capacity: int = 1
            ) -> None:
        """
        Initialize a connection between two zones
        and define its maximum capacity.
        """
        self.zone1 = zone1
        self.zone2 = zone2
        self.max_link_capacity = max_link_capacity


class Drones:
    """
    Represents a drone moving through
    a predefined path in the graph.
    """
    def __init__(self, drone_id: int, path: List[str]) -> None:
        """
        Initialize a drone with its identifier,
        path and movement state.
        """
        self.drone_id = drone_id
        self.path = path
        self.path_index = 0  # fin wselna f had path
        self.finished = False  # wax wsalna l end wla mazal

        self.in_transit = False  # wax hna kainin waset connection(slek)
        # self.waited_turns = 0  # chhal me turn w han knastnaw

    def current_zone_name(self) -> str:
        """
        Return the name of the zone
        where the drone is currently located.
        """
        return self.path[self.path_index]

    def next_zone_name(self) -> str | None:
        """
        Return the next zone in the path,
        or None if the drone reached the end.
        """
        if self.path_index + 1 >= len(self.path):
            return None
        return self.path[self.path_index + 1]

    def move(self) -> None:
        """
        Move the drone one step forward
        along its assigned path.
        """
        self.path_index += 1
        if self.path_index == len(self.path) - 1:
            self.finished = True
