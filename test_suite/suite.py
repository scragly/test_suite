import curses
import sys

from .progress import GlobalProgress
from .groups import TestGroup


class Suite:
    def __init__(self, title, function, *test_groups):
        self.function = function
        self.title = title
        self.groups = test_groups or TestGroup.groups
        curses.wrapper(self.run)

    def run(self, stdscr):
        stdscr.keypad(True)
        stdscr.clear()
        curses.use_default_colors()
        curses.init_pair(1, curses.COLOR_RED, -1)
        curses.init_pair(2, curses.COLOR_GREEN, -1)
        curses.init_pair(3, curses.COLOR_YELLOW, -1)
        curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_CYAN)
        blue_bg = curses.color_pair(4)

        stdscr.addstr(
            0, 0, f"{self.title:^90}",
            curses.A_REVERSE | blue_bg
        )

        global_progress = GlobalProgress(18, stdscr)

        current_line = 4

        groups = []
        for Group in self.groups:
            group = Group(self.function, current_line, stdscr, global_progress)
            current_line += group.total + 2
            groups.append(group)

        for group in groups:
            group.run_tests()

        stdscr.addstr(
            current_line+2, 0,
            f"{'Tests Complete - Press Enter to Close':^90}",
            curses.A_BOLD
        )
        curses.curs_set(0)
        stdscr.refresh()

        try:
            while True:
                c = stdscr.getch()
                stdscr.addstr(0, 0, f"{c}")
                if c in [curses.KEY_ENTER, 10, ord(' '), 27]:
                    sys.exit()
        except KeyboardInterrupt:
            sys.exit()
