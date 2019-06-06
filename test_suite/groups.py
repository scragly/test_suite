import curses
import inspect

from .tests import Test
from .progress import Progress


class TestGroup:
    name = None
    progress_line = 2
    groups = []

    def __init_subclass__(cls, **kwargs):
        TestGroup.groups.append(cls)

    def __init__(self, function, line, stdscr, global_progress):
        self.function = function
        self.screen = stdscr
        self.line = line
        self.passed = 0
        self.completed = 0
        self.tests = self.get_tests()
        self.total = len(self.tests)
        self.progress = Progress(
            stdscr, f"{self.name}:", global_progress, self.total, self.line
        )
        global_progress.total += self.total
        # self.update_display()

    def get_tests(self):
        members = (m[1] for m in inspect.getmembers(self, self.is_test))
        tests = []
        for test in members:
            tests.append(Test(test, self.function, self.line, self.screen))
        tests.sort(key=lambda t: t.index)
        return tests

    @classmethod
    def count_tests(cls):
        return len(inspect.getmembers(cls, cls.is_test))

    def update_line(self, start, text, color):
        self.screen.addstr(self.line, start, text, color)

    def refresh_screen(self):
        curses.curs_set(0)
        self.screen.refresh()

    @staticmethod
    def is_test(member):
        return inspect.ismethod(member) and member.__name__.startswith('test_')

    def run_tests(self):
        for test in self.tests:
            result, value = test()
            self.completed += 1
            if result:
                self.passed += 1
                self.progress.increment(True)
            else:
                self.progress.increment(False)

            test.update_display()
            # self.update_display()

    @property
    def display_color(self):
        if self.completed < self.total:
            return curses.A_BOLD | curses.A_REVERSE
        elif self.passed == self.total:
            return curses.A_BOLD | curses.color_pair(2) | curses.A_REVERSE
        else:
            return curses.A_BOLD | curses.color_pair(1) | curses.A_REVERSE

    def update_display(self):
        stage_line_txt = f"{self.name} Requirements"
        self.update_line(0, f"{stage_line_txt:^90}", self.display_color)
