import curses
import sys

from .progress import Progress
from .groups import TestGroup


class Suite:
    def __init__(self, title, function, *test_groups, on_finish=None):
        self.function = function
        self.title = title
        self.groups = test_groups or TestGroup.groups
        self.on_finish = on_finish
        self.screen = None
        self.results = {}
        try:
            self.screen = self.init_screen()
            self.run()
        finally:
            self.close_screen()

    def init_screen(self):
        screen = curses.initscr()
        curses.noecho()
        curses.cbreak()
        screen.keypad(1)
        curses.start_color()
        return screen

    def close_screen(self):
        if self.screen:
            self.screen.keypad(0)
        curses.echo()
        curses.nocbreak()
        curses.endwin()

    def run(self):
        self.screen.keypad(True)
        self.screen.clear()
        curses.use_default_colors()
        curses.init_pair(1, curses.COLOR_RED, -1)
        curses.init_pair(2, curses.COLOR_GREEN, -1)
        curses.init_pair(3, curses.COLOR_YELLOW, -1)
        curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_CYAN)
        curses.init_pair(5, curses.COLOR_BLACK, curses.COLOR_WHITE)

        self.screen.addstr(
            0, 0, f"{self.title:^90}", curses.color_pair(4) | curses.A_REVERSE | curses.A_BOLD
        )

        global_progress = Progress(self.screen)

        current_line = 3

        groups = []
        for Group in self.groups:
            group = Group(
                self.function, current_line, self.screen, global_progress
            )
            current_line += group.total + 2
            groups.append(group)

        for group in groups:
            results = group.run_tests()
            self.results[group.__class__.__name__] = results

        self.screen.addstr(
            current_line, 0,
            f"{'Tests Complete - Press Enter to Close':^90}",
            curses.A_BOLD
        )

        curses.curs_set(0)
        self.screen.refresh()

        if self.on_finish:
            self.on_finish(self)

        try:
            while True:
                c = self.screen.getch()
                self.screen.addstr(0, 0, f"{c}")
                if c in [curses.KEY_ENTER, 10, ord(' '), 27]:
                    sys.exit()
        except KeyboardInterrupt:
            sys.exit()
