from models import Zone
from models import Connections


class Parser:
    """
    Parses a Fly-In configuration file and builds
    zones, connections and simulation settings.
    """
    def __init__(self, path_file: str) -> None:
        """
        Initialize parser data structures and validation rules.
        """
        self.path_file = path_file

        self.nb_drones = 0

        self.start_zone: Zone | None = None
        self.end_zone: Zone | None = None

        self.zones: dict[str, Zone] = {}

        self.connections: list[Connections] = []
        self.connection_pairs: set[tuple[str, str]] = set()
        # search is fast then list.

        self.used_coords: set[tuple[int, int]] = set()
        # check deplicat coordoni.

        self.allowed_colors = [
            "green", "yellow", "red", "blue", "gray", "orange", "cyan",
            "purple", "black", "brown", "maroon", "gold", "darkred",
            "violet", "crimson", "rainbow", "lime", "magenta", "none"
        ]

        self.valid_zones = ["normal", "blocked", "restricted", "priority"]

    def parser(self) -> None:
        """
        Read the configuration file and parse all sections
        while validating the input format.
        """
        try:
            with open(self.path_file, "r") as f:
                first = True

                for line_number, line in enumerate(f, start=1):
                    line = line.strip()
                    if not line or line.startswith('#'):
                        continue

                    elif first:
                        self.parse_nb_dron(line, line_number)
                        first = False

                    elif line.startswith("start_hub:"):
                        if self.start_zone is not None:
                            raise ValueError(
                                f"Error in line {line_number}"
                                " There must be exactly one start_hub:")
                        self.parse_start(line, line_number)

                    elif line.startswith("end_hub:"):
                        if self.end_zone is not None:
                            raise ValueError(
                                f"Error in line {line_number}"
                                " There must be exactly one end_hub:")
                        self.parse_end(line, line_number)

                    elif line.startswith("hub:"):
                        self.parse_hub(line, line_number)

                    elif line.startswith("connection:"):
                        self.parse_connection(line, line_number)

                    else:
                        raise ValueError(
                            f"unknow this line {line!r}"
                            f" in number {line_number}")
                    # print(line)
                # print(self.zones.keys())
        except BaseException as e:
            print(e)
            exit(1)

    def parse_nb_dron(self, line: str, line_number: int) -> None:
        """
        Parse and validate the number of drones.
        """
        if not line.startswith("nb_drones"):
            raise ValueError(
                f"Error in {line_number}: "
                f"first line must be 'nb_drones: '"
            )
        values = line.split(":")
        if len(values) != 2:
            raise ValueError(
                f"Error in line {line_number}"
                f" expect input like 'key : value' "
            )
        value = values[1].strip()
        if not value.isdigit() or int(value) <= 0:
            raise ValueError(
                f"Error line {line_number}: "
                f"invalid number of drones"
            )
        self.nb_drones = int(value)

    def parse_start(
            self,
            line: str,
            line_number: int
            ) -> None:
        """
        Parse and create the start hub zone.
        """
        content = line[len("start_hub:"):].strip()
        # print(content)

        parts = content.split(maxsplit=3)

        if len(parts) < 3:
            raise ValueError(
                f"Error in line {line_number}"
                "expect structure 'start_hub: <name> <x> <y> [metadata]'")

        name = parts[0]
        if "-" in name or " " in name:
            raise ValueError(
                f"Error line {line_number}: invalid zone name"
            )

        try:
            x = int(parts[1])
            y = int(parts[2])

        except ValueError:
            raise ValueError(f"Error in line {line_number} "
                             "cordinat must be integer ")
        if (x, y) in self.used_coords:
            raise ValueError(
                f"Error in line {line_number}: "
                f"Coordinates ({x}, {y}) are already used by another zone"
            )
        self.used_coords.add((x, y))

        if len(parts) == 4:
            metadata = parts[3]
            if not (metadata.startswith("[") and metadata.endswith("]")):
                raise ValueError(f"Error in line {line_number}: "
                                 "metadata must be enclosed in []")
        else:
            metadata = ""

        color = "none"
        max_drones = 1
        zone_type = "normal"

        metadata = metadata[1:-1]
        tags = metadata.split()

        if len(tags) > 3:
            raise ValueError(
                            f"Error in lin {line_number}: "
                            "expect maximum 3 attributes "
                            "'color=... max_drones=...zone=...'"
                            )
        for a in tags:
            if "=" not in a:
                raise ValueError(
                                f"Error in line {line_number} "
                                "expect'color=<value> max_drones=<number>'"
                                )
            key, value = a.split("=", 1)

            if key.strip() == "zone":
                if value not in self.valid_zones:
                    raise ValueError(
                        f"Error in line {line_number} "
                        f"invalid zone type expect {self.valid_zones}"
                    )

                if value == "blocked":
                    raise ValueError(
                        f"Error in line {line_number} "
                        f"invalid zone type start must be normal zone!"
                    )

                zone_type = value

            elif key == "color":
                if value not in self.allowed_colors:
                    raise ValueError(
                        f"Error in line {line_number}: "
                        f"Invalid color '{value}'. Allowed colors are: "
                        f"{', '.join(self.allowed_colors)}"
                    )
                color = value
            elif key == "max_drones":
                try:
                    max_drones = int(value)
                    if max_drones <= 0 or max_drones < self.nb_drones:
                        raise ValueError
                except ValueError:
                    raise ValueError(
                        f"Error in {line_number} "
                        "max_drones must be  valid integer"
                        " and be exact number of drones"
                                     )
            else:
                raise ValueError(
                    f"Error in line {line_number} "
                    "expect keys just 'color' and max_drones"
                    "i'm not entrresi about type of zone this is"
                    "start zone"
                    )

        zone = Zone(
            name=name,
            x=x,
            y=y,
            zone_type=zone_type,
            color=color,
            max_drones=max_drones
        )

        self.start_zone = zone
        self.zones[name] = zone
# ---------------------------------------- end

    def parse_end(self, line: str, line_number: int) -> None:
        """
        Parse and create the end hub zone
        """
        content = line[len("end_hub:"):].strip()

        parts = content.split(maxsplit=3)

        if len(parts) < 3:
            raise ValueError(
                f"Error in line {line_number}"
                "expect structure 'start_hub: <name> <x> <y> [metadata]'")

        name = parts[0]
        if "-" in name or " " in name:
            raise ValueError(
                f"Error line {line_number}: invalid zone name"
            )

        try:
            x = int(parts[1])
            y = int(parts[2])

            # if x < 0 or y < 0:
            #     raise ValueError(f"Error in line {line_number} "
            #                      "cordinat must be positive integer ")
        except ValueError:
            raise ValueError(f"Error in line {line_number} "
                             "cordinat must be integer ")

        # check les cordoni
        if (x, y) in self.used_coords:
            raise ValueError(
                f"Error in line {line_number}: "
                f"Coordinates ({x}, {y}) are already used by another zone"
            )
        self.used_coords.add((x, y))

        if len(parts) == 4:
            metadata = parts[3]
            if not (metadata.startswith("[") and metadata.endswith("]")):
                raise ValueError(f"Error in line {line_number}: "
                                 "metadata must be enclosed in []")
        else:
            metadata = ""

        color = "none"
        max_drones = self.nb_drones
        zone_type = "normal"

        metadata = metadata[1:-1]
        tags = metadata.split()

        if len(tags) > 3:
            raise ValueError(
                            f"Error in lin {line_number}: "
                            "expect maximum 2 attributes "
                            "'color=... max_drones=...'"
                            )
        for a in tags:
            if "=" not in a:
                raise ValueError(f"Error in line {line_number} "
                                 "expect'color=<value> max_drones=<number>'")
            key, value = a.split("=", 1)

            if key.strip() == "zone":
                if value not in self.valid_zones:
                    raise ValueError(
                        f"Error in line {line_number} "
                        f"invalid zone type expect {self.valid_zones}"
                    )
                zone_type = value

            elif key == "color":
                if value not in self.allowed_colors:
                    raise ValueError(
                        f"Error in line {line_number}: "
                        f"Invalid color '{value}'. Allowed colors are: "
                        "{', '.join(self.allowed_colors)}"
                    )
                color = value
            elif key == "max_drones":
                try:
                    max_drones = int(value)
                    if max_drones <= 0 or max_drones < self.nb_drones:
                        raise ValueError
                except ValueError:
                    raise ValueError(
                        f"Error in line {line_number} "
                        "max_drones must be  valid integer"
                        " and must be equal max drones"
                                     )
            else:
                raise ValueError(
                    f"Error in line {line_number} "
                    "expect keys just 'color' and max_drones")

        zone = Zone(
            name=name,
            x=x,
            y=y,
            zone_type=zone_type,
            color=color,
            max_drones=max_drones
        )

        self.end_zone = zone
        self.zones[name] = zone

    def parse_hub(self, line: str, line_number: int) -> None:
        """
        Parse and create a regular hub with its metadata.
        """
        content = line[len("hub:"):].strip()

        parts = content.split(maxsplit=3)

        if len(parts) < 3:
            raise ValueError(
                f"Error in line {line_number}"
                "expect structure 'start_hub: <name> <x> <y> [metadata]'")

        name = parts[0]
        if "-" in name or " " in name:
            raise ValueError(
                f"Error line {line_number}: invalid zone name"
            )

        try:
            x = int(parts[1])
            y = int(parts[2])

        except ValueError:
            raise ValueError(f"Error in line {line_number} "
                             "cordinat must be integer ")

        # check les cordoni
        if (x, y) in self.used_coords:
            raise ValueError(
                f"Error in line {line_number}: "
                f"Coordinates ({x}, {y}) are already used by another zone"
            )
        self.used_coords.add((x, y))

        if len(parts) == 4:
            metadata = parts[3]
            if not (metadata.startswith("[") and metadata.endswith("]")):
                raise ValueError(f"Error in line {line_number}: "
                                 "metadata must be enclosed in []")
        else:
            metadata = ""

        zone_type = "normal"
        color = "none"
        max_drones = 1

        metadata = metadata[1:-1]
        tags = metadata.split()

        if len(tags) > 3:
            raise ValueError(
                            f"Error in line {line_number}: "
                            "expect maximum 3 attributes "
                            "respect stucture -> "
                            "'zone=... color=... max_drones=...'"
                            )
        for a in tags:
            if "=" not in a:
                raise ValueError(f"Error in line {line_number} "
                                 "expect'color=<value> max_drones=<number>'")
            key, value = a.split("=", 1)

            if key.strip() == "zone":
                if value not in self.valid_zones:
                    raise ValueError(
                        f"Error in line {line_number} "
                        f"invalid zone type expect {self.valid_zones}"
                    )
                zone_type = value
            elif key == "color":
                if value not in self.allowed_colors:
                    raise ValueError(
                        f"Error in line {line_number}: "
                        f"Invalid color '{value}'. Allowed colors are: "
                        "{', '.join(self.allowed_colors)}"
                    )
                color = value
            elif key == "max_drones":
                try:
                    max_drones = int(value)
                    if max_drones <= 0:
                        raise ValueError
                except ValueError:
                    raise ValueError(
                        f"Error in {line_number} "
                        "max_drones must be valid integer"
                                    )
            else:
                raise ValueError(
                    f"Error in line {line_number} "
                    "expect keys just 'color' and 'max_drones' and 'zone' ")

        zone = Zone(
            name=name,
            x=x,
            y=y,
            zone_type=zone_type,
            color=color,
            max_drones=max_drones
        )

        self.zones[name] = zone

    def parse_connection(self, line: str, line_number: int) -> None:
        """"
        Parse and create a connection between two zones
        while validating capacities and graph rules.
        """
        content = line[len("connection:"):].strip()

        parts = content.split(maxsplit=1)

        if len(parts) == 0:
            raise ValueError(
                            f"Error in line {line_number} "
                            "excpect ' <name1>-<name2> [metadata]'"
                            )

        basic = parts[0]

        if len(parts) == 2:
            metadata = parts[1]
            if not (metadata.startswith("[") and metadata.endswith("]")):
                raise ValueError(
                                f"Error in line {line_number}: "
                                "metadata must be enclosed in []"
                                )
            metadata = metadata[1:-1]
        else:
            metadata = ""

        if "-" not in basic:
            raise ValueError(
                f"Error in line {line_number}: invalid connection "
                "expect connection: <zone1>-<zone2> [metadata]"
            )

        zone1, zone2 = basic.split("-", 1)
        zone1 = zone1.strip()
        zone2 = zone2.strip()

        if zone1 not in self.zones or zone2 not in self.zones:
            raise ValueError(
                f"Line {line_number}: undefined zone in connection"
            )

        z1, z2 = tuple(sorted([zone1, zone2]))
        pair = (z1, z2)

        if pair in self.connection_pairs:
            raise ValueError(
                f"Error in line {line_number}: duplicate connection"
            )

        max_link_capacity = 1

        tags = metadata.split()
        if len(tags) > 1:
            raise ValueError(
                f"Error in line {line_number}: "
                "expect maximum 1 attribute 'max_link_capacity=...'"
            )

        for tag in tags:
            if "=" not in tag:
                raise ValueError(
                    f"Error in line {line_number}: "
                    "expect structure max_link_capacity=..."
                )

            key, value = tag.split("=", 1)

            if key == "max_link_capacity":
                try:
                    max_link_capacity = int(value)
                except ValueError:
                    raise ValueError(
                        f"Error in line {line_number}: "
                        "max_link_capacity must be a valid integer"
                    )

                if max_link_capacity <= 0:
                    raise ValueError(
                        f"Error in line {line_number}: "
                        "max_link_capacity must be positive int"
                    )
            else:
                raise ValueError(
                    f"Line {line_number}: invalid metadata key '{key}'"
                )

        connections = Connections(
            zone1=zone1,
            zone2=zone2,
            max_link_capacity=max_link_capacity
        )

        self.zones[zone1].neighbors.append(self.zones[zone2])
        self.zones[zone2].neighbors.append(self.zones[zone1])

        # here i just respected Undirected Graph how look :)
        # if i have connctio A-B
        # so i do A.neighbors = [B] and B.neibhbors = [A]
        # so i can go from a to b and b to a
        # and in Zone class i do self.neighbors = [] it's Adjacency List.
        # it's Undirected Graph.

        self.connections.append(connections)
        self.connection_pairs.add(pair)
