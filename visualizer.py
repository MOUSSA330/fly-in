import pygame
from parsing import Parser
from simulation import Sminulation


class Visualizer:
    """
    Handles the graphical visualization of the Fly-In simulation
    using Pygame. Draws zones, connections, drones and UI controls.
    """

    def __init__(
            self,
            parser: Parser,
            sim: Sminulation,
            width: int = 1200,
            height: int = 800) -> None:
        """
        Initialize the visualization window, UI elements,
        colors, fonts and simulation references.
        """
        pygame.init()  # initialize

        self.screen = pygame.display.set_mode((width, height))  # creat window
        # library -> modul -> function

        pygame.display.set_caption("Mr Lee Moussa-Fly-In: Drone Simuation")
        # set_caption -->> liter dail window

        self.parser = parser
        self.sim = sim

        self._calculate_layout(width, height)

        self.color_map = {
            "green": (0, 255, 0),
            "yellow": (255, 255, 0),
            "red": (255, 0, 0),
            "blue": (0, 0, 255),
            "gray": (128, 128, 128),
            "orange": (255, 165, 0),
            "cyan": (0, 255, 255),

            "purple": (128, 0, 128),
            "black": (20, 20, 20),
            "brown": (139, 69, 19),
            "maroon": (128, 0, 0),
            "gold": (255, 215, 0),
            "darkred": (139, 0, 0),
            "violet": (238, 130, 238),

            "crimson": (220, 20, 60),
            "rainbow": (255, 105, 180),
            "lime": (50, 205, 50),
            "magenta": (255, 0, 255),
            "none": (200, 200, 200)  # li ma3andhom color
        }  # RGB every color kiakon bin 0 ou 255
        # we need it whene we use draw in Pygame

        self.is_panning = False
        self.last_mouse_pos = (0, 0)
# -------------------
        pygame.font.init()  # initialize l system dail lines (fonts).
        self.font = pygame.font.SysFont(None, 16)  # font object

        # font like matba3a kateteb3 lina f war9a w lhait hio
        # screen (self, screen).

        # example:
        # text_surf = self.font.render(...)
        # self.screen.blit(text_surf, ...)

        self.auto_paly = False  # auto play hia mli kankhli prgamr khdem rasoo
        self.last_turn_time = 0  # time for last turn for next turn
        self.turn_delay = 800  # time btw turns

        self.btn_play = pygame.Rect(20, 20, 100, 40)  # x, y, width , height.
        self.btn_step = pygame.Rect(130, 20, 100, 40)  # creat btn
        self.btn_quit = pygame.Rect(240, 20, 100, 40)
# ---------------------------------------------------

    def _calculate_layout(
            self,
            width: int,
            height: int
            ) -> None:
        """
        Calculate scale and offsets so the entire graph
        fits and stays centered inside the window.
        """
        coords = [(z.x, z.y) for z in self.parser.zones.values()]

        max_x = max(c[0] for c in coords)  # kanakhdo akber x
        max_y = max(c[1] for c in coords)  # kanakhdo akber y
        self.max_y = max_y

        margin = 100  # masafa void j jnaab dail screen

        scale_x = (width - (2 * margin)) / (max_x if max_x > 0 else 1)
        # objctive men had ster hio na3ref chhal khasni nkaber wela nsagher-
        # les cordoni bach map kamla tadekhl f lmisaha dial screen

        # kana9so men width margin * 2 3la hsab nkhaliw lfaragh-
        # f jnab bjoj limen ou liser - ou kan9asmo 3la x bach n3arfo
        # chhal khas kola wahda dail x bach akber x tawsel l akhir blasa-
        # f map

        scale_y = (height - (2 * margin)) / (max_y if max_y > 0 else 1)
        # nafs lhaja bnisba l y bhal x marjib ghadi ykon lfou9 ou-
        # ltahet ou akber y ghadi tkon f lakher dail map..

        self.scale = min(scale_x, scale_y)
        # kankhatro asgher scale bach ndamno l map kamla-
        # tadkhel f chacha (screen).

        self.offset_x = (margin + (width - (2 * margin)
                                   - max_x * self.scale) / 2)

        # objective men hada nhaded lablasa dail minin
        # ghadi nabda rassem bax x tkon centred inside chacha.

        # width - (2 * margin) hadi hia lmisaha dail rasem after mahiadna
        # l margin men liser ou limen

        # max_x * self.scale hada hio l3ared lha9i9i dial map after
        # matab9na scale

        # (width - (2 * margin) - max_x * self.scale) -> hadi hia
        # lmisaha li b9et 1000 - 800 = 200

        # (...)/2 kan9asmo 3la 2 bach lmisaha twaze3 b linem ou liser

        self.offset_y = (margin + (height - (2 * margin)
                                   - max_y * self.scale) / 2)

    def _get_coords(self, zone_name: str) -> tuple[int, int]:
        """
        Convert a zone's logical coordinates (x, y)
        into screen coordinates used for drawing.
        """
        """
        kanhawlo l position dail zone men x, y l posistion kbir
        bach ykon dakchi matba3ed ou mafhoum.
        """
        zone = self.parser.zones[zone_name]

        x = (zone.x * self.scale) + self.offset_x
        # zoom + move drawin with saving
        # zone.x * self.scale kaber x
        # + self.offset_x e2izaha l limen/ liser
        # self.scale kiabadel lmasafa ma bin zone ou zone
        # exampl x_1 = 1 , x_2 = 2 -> 2 - 1 = 1 walkin-
        # ila drabna f * self.scale (100) -> 200 - 100 = 100.

        y = ((self.max_y - zone.y) * self.scale) + self.offset_y
        # 9leb les cordoni dail y.

        return (int(x), int(y))

    def draw_map(self) -> None:
        """
        Draw all graph connections and zones
        with their names and colors.
        """
        self.screen.fill((30, 30, 30))  # color of baground

        for conn in self.parser.connections:
            pos1 = self._get_coords(conn.zone1)
            pos2 = self._get_coords(conn.zone2)

            pygame.draw.line(self.screen, (100, 100, 100), pos1, pos2, 3)
            #  hna kanrasmo line ma bin 2 dail les condoni (x, y)

        for name, zone in self.parser.zones.items():
            pos = self._get_coords(name)

            zone_color = self.color_map.get(zone.color, self.color_map["none"])

            pygame.draw.circle(self.screen, zone_color, pos, 20)
            # kairsem l9orse colore - positoin - size

            pygame.draw.circle(self.screen, (255, 255, 255), pos, 20, 2)
            # drawing circle nafes posistion o/u size ou 2 somek dial line.

            text_surf = self.font.render(name, True, (255, 255, 255))
            # render in a function kathawel men text to photo Surface.
            # kat9ed lina taswira fiha name.

            self.screen.blit(
                text_surf,
                (pos[0] - text_surf.get_width()//2, pos[1] + 25)
                )
            # blit function ghadi dir lia Sureface obouve screen.
            # screen.blit(image, position).
            # text_surf.get_width() katrje3 lina l3aed by pixels (px).
            # pos[0] - text_surf.get_width()//2 chdina nes dail l3ard-
            # bach yabda rasem f lwaset dail rasma dail zone.

    def draw_drones(self) -> None:
        """
        Draw all drones at their current positions
        or between zones while in transit.
        """
        for drone in self.sim.drones:
            curr_pos = self._get_coords(drone.current_zone_name())

            if drone.in_transit:
                next_name = drone.next_zone_name()

                if next_name is not None:
                    next_pos = self._get_coords(next_name)
                    draw_pos = (
                        (curr_pos[0] + next_pos[0]) / 2,
                        (curr_pos[1] + next_pos[1]) / 2
                        )
                    # position btw current zone ou next zone.
                else:
                    draw_pos = curr_pos
            else:
                draw_pos = curr_pos

            pygame.draw.circle(self.screen, (255, 0, 255), draw_pos, 10)
            # dicoration.
            pygame.draw.circle(self.screen, (0, 0, 0), draw_pos, 8, 2)
            pygame.draw.circle(self.screen, (0, 0, 0), draw_pos, 6, 2)
            pygame.draw.circle(self.screen, (0, 0, 0), draw_pos, 4, 2)

            drone_text = self.font.render(
                f"D{drone.drone_id}",
                False,
                (255, 255, 0)
                )
            self.screen.blit(drone_text, (draw_pos[0] - 15, draw_pos[1] - 25))
            # ( draw_pos[0] - 15 ) move a litter to the left.
            # (draw_pos[1] - 25) move the text to up.

    def draw_ui(self) -> None:  # user Interface.
        """
        Draw simulation controls such as
        Play, Step and Quit buttons.
        """
        play_color = (0, 200, 0) if not self.auto_paly else (200, 150, 0)
        pygame.draw.rect(
            self.screen,
            play_color,
            self.btn_play,
            border_radius=10
            )
        play_text = self.font.render(
            "Pause" if self.auto_paly else "Play",
            True,
            (255, 255, 255)
            )
        self.screen.blit(
            play_text,
            (self.btn_play.x + 30, self.btn_play.y + 15)
            )

        pygame.draw.rect(
            self.screen,
            (100, 100, 100),
            self.btn_step,
            border_radius=5
            )
        step_text = self.font.render("Step (Spc)", True, (255, 255, 255))

        self.screen.blit(
                        step_text,
                        (self.btn_step.x + 25, self.btn_step.y + 15)
                        )

        pygame.draw.rect(
                        self.screen,
                        (200, 0, 0),
                        self.btn_quit,
                        border_radius=5
                        )
        quit_text = self.font.render("Quit", True, (255, 255, 255))

        self.screen.blit(
                        quit_text,
                        (self.btn_quit.x + 30, self.btn_quit.y + 15)
                        )

    def run_visualization(self) -> None:
        """
        Main visualization loop.
        Handles events, updates simulation,
        and refreshes the display.
        """
        running = True
        # i = 0
        try:
            while running:
                current_time = pygame.time.get_ticks()
                if (
                    self.auto_paly and
                    (current_time - self.last_turn_time > self.turn_delay)
                ):
                    self.sim.step()
                    self.last_turn_time = current_time
                # i += 1
                # print(i)

                for event in pygame.event.get():
                    # print(event)
                    # i = 0
                    # print(i)
                    if event.type == pygame.QUIT:
                        running = False

                    elif event.type == pygame.MOUSEWHEEL:
                        if event.y > 0:
                            # print("in")
                            self.scale *= 1.1
                        elif event.y < 0:
                            # print("out")
                            self.scale /= 1.1

                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        # print("click!!")
                        if event.button == 1:  # only lift klick!
                            # print("left klick!")
                            if self.btn_play.collidepoint(event.pos):
                                # if this point of cor (event.pos)
                                # in self.btn_play
                                self.auto_paly = not self.auto_paly
                                # reverse the value fasle <-> trye

                                self.last_turn_time = current_time
                                # start clcult 800ms from this moment.

                            elif self.btn_step.collidepoint(event.pos):
                                self.auto_paly = False
                                self.sim.step()
                                print("Step Clicked!")

                            elif self.btn_quit.collidepoint(event.pos):
                                running = False
                            else:
                                self.is_panning = True
                                self.last_mouse_pos = event.pos

                    elif event.type == pygame.MOUSEBUTTONUP:
                        # hadi hia li katkhali l click li darty-
                        # ytalgha bach t3awed dir click men jdid.
                        if event.button == 1:
                            self.is_panning = False

                    elif event.type == pygame.MOUSEMOTION:
                        if self.is_panning:
                            mouse_x, mouse_y = event.pos
                            dx = mouse_x - self.last_mouse_pos[0]
                            dy = mouse_y - self.last_mouse_pos[1]
                            self.offset_x += dx
                            self.offset_y += dy
                            self.last_mouse_pos = (mouse_x, mouse_y)

                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            self.auto_paly = False
                            self.sim.step()

                self.draw_map()
                self.draw_drones()
                self.draw_ui()
                pygame.display.flip()
        except KeyboardInterrupt:
            print("ctrl + c")
            exit(1)

        pygame.quit()
