from models import Drones
from typing import List
from parsing import Parser
from models import Connections


class Sminulation:
    """
    Simulates drone movements through the network while respecting
    zone capacities and connection capacity constraints.
    """
    def __init__(
            self,
            parser: Parser,
            paths: List[List[str]]
            ) -> None:
        """
        Initialize the simulation, store network data and assign
        drones to available paths.
        """
        self.parser = parser
        self.paths = paths
        self.drones: list[Drones] = []
        self.turn_count = 0
        self._initialize_drones()

    def _initialize_drones(self) -> None:
        """
        Create all drones and distribute them across the available paths.
        """
        num_paths = len(self.paths)

        for i in range(self.parser.nb_drones):
            assigned_path = self.paths[i % num_paths]

            drone = Drones(drone_id=i + 1, path=assigned_path)
            self.drones.append(drone)

    def step(self) -> bool:
        """
        Execute a single simulation turn by moving eligible drones
        and applying zone and connection capacity rules.
        return False whenn all drone reached the destination
        otherwiseTrue
        """
        if all(drone.finished for drone in self.drones):
            return False

        self.turn_count += 1
        moves_this_turn = []
        links_used_this_turn: dict[tuple[str, str], int] = {}

        active_drones = sorted(
            [d for d in self.drones if not d.finished],
            key=lambda d: d.path_index,
            reverse=True
        )
        # we only take the dones that haven't reached the finish , and
        # sord them by the path_index (fin waslat kola wahda)

        for drone in active_drones:
            if drone.in_transit:
                drone.in_transit = False
                drone.move()
                moves_this_turn.append(
                                      f"D{drone.drone_id}-"
                                      f"{drone.current_zone_name()}"
                                      )
                continue

            next_zone_name = drone.next_zone_name()
            if not next_zone_name:
                continue

            can_move = self._check_capacity(
                                            drone,
                                            next_zone_name,
                                            links_used_this_turn
                                            )
            # 1 check for capacity connection (link)
            # 2 ckech start ou l end
            # 3 check dail capacity zone
            if can_move:
                next_zone = self.parser.zones[next_zone_name]
                z1, z2 = tuple(sorted(
                    [drone.current_zone_name(), next_zone_name]
                    ))
                conn_pair = (z1, z2)

                if next_zone.zone_type == "restricted":
                    drone.in_transit = True
                    connection_name = (
                                    f"{drone.current_zone_name()}"
                                    f"-{next_zone_name}"
                                    )
                    moves_this_turn.append(
                        f"D{drone.drone_id}-"
                        f"{connection_name}")
                else:
                    drone.move()
                    moves_this_turn.append(
                        f"D{drone.drone_id}-"
                        f"{drone.current_zone_name()}"
                        )

                links_used_this_turn[conn_pair] = (
                    links_used_this_turn.get(conn_pair, 0) + 1
                    )

        if moves_this_turn:
            print(" ".join(moves_this_turn))

        return True

    def run(self) -> None:
        """
        Run the simulation until every drone reaches the destination.
        """
        turn = 0
        while self.step():
            turn += 1

    def _get_connection(
            self,
            zone1_name: str,
            zone2_name: str
            ) -> None | Connections:
        """
        Retrieve the connection object linking the given zones.
        """
        pair = tuple(sorted([zone1_name, zone2_name]))

        for con in self.parser.connections:
            if tuple(sorted([con.zone1, con.zone2])) == pair:
                return con
        return None

    def _check_capacity(
                        self,
                        drone: Drones,
                        next_zone_name: str,
                        links_used_this_turn: dict[tuple[str, str], int]
                        ) -> bool:
        """
        Verify whether a drone can move to the next zone without
        exceeding connection or zone capacity limits.
        return bool: True if movement is allowed, otherwise False.
        """
        current_zone_name = drone.current_zone_name()  # name
        next_zone = self.parser.zones[next_zone_name]  # obj of next zone

        conn = self._get_connection(current_zone_name, next_zone_name)
        # obj for connection.
        if conn:
            c1, c2 = tuple(sorted([current_zone_name, next_zone_name]))
            conn_pair = (c1, c2)

            drones_on_link = 0
            for d in self.drones:
                if d.in_transit:
                    curr = d.current_zone_name()
                    nxt = d.next_zone_name()

                    if curr is not None and nxt is not None:
                        z1, z2 = sorted([curr, nxt])
                        if (z1, z2) == conn_pair:
                            drones_on_link += 1
            # kanchoufo wax kina chi dron f connection (selk)
            # kainin 2 dial condition
            # a- wach had drone kina f waset selk
            # b- in selk men sloka.

            drones_on_link += links_used_this_turn.get(conn_pair, 0)

            if drones_on_link >= conn.max_link_capacity:
                return False

            if next_zone.zone_type in ["start", "end"]:
                return True

            drones_in_next_zone = sum(
                1 for d in self.drones
                if d.current_zone_name() == next_zone_name and not d.in_transit
            )
            # anchoufo chhal men dron kina f next zone ou
            #  not d.in_transit makinach f waset connection (selk)

            drones_incoming = sum(
                1 for d in self.drones
                if d.in_transit and d.next_zone_name() == next_zone_name
            )
            # chhal men drone jaya l had zone but ba9a f connection

            total_future_drones = drones_in_next_zone + drones_incoming

            if total_future_drones >= next_zone.max_drones:
                return False

            return True
        return False
