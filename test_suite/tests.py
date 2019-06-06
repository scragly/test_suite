import curses


class TestStatus:
    waiting = "WAITING"
    in_progress = "IN PROGRESS"
    passed = "PASSED"
    failed = "FAILED"


class Test:
    def __init__(self, test_function, pw_generator, group_line, stdscr):
        self.callable = test_function
        self.description = test_function.__doc__[2:]
        self.index = int(test_function.__doc__[:2])
        self.line = group_line + self.index
        self.generator = pw_generator
        self.result = None
        self.value = None
        self.status = TestStatus.waiting
        self.screen = stdscr
        self.update_display()

    def __str__(self):
        return self.description

    def __repr__(self):
        return f"<Test {self.callable.__name__}>"

    def update_line(self, start, text, color):
        self.screen.addstr(self.line, start, text, color)

    def refresh_screen(self):
        curses.curs_set(0)
        self.screen.refresh()

    @property
    def display_color(self):
        colors = {
            TestStatus.waiting: curses.A_DIM,
            TestStatus.in_progress: curses.A_REVERSE | curses.color_pair(3),
            TestStatus.passed: curses.A_BOLD | curses.color_pair(2),
            TestStatus.failed: curses.A_BOLD | curses.color_pair(1)
        }
        return colors[self.status]

    def update_status(self, status):
        self.status = status
        self.update_display()

    def __call__(self):

        self.update_status(TestStatus.in_progress)

        try:
            result = self.callable()
        except Exception as e:
            result = False, type(e).__name__

        if isinstance(result, tuple):
            self.result, self.value = result
        else:
            self.result, self.value = result, result

        status = TestStatus.passed if self.result else TestStatus.failed
        self.update_status(status)
        self.update_display()

        return self.result, self.value

    def update_display(self):
        self.update_line(0,  f"{'':^74}", self.display_color)
        self.update_line(1, f"{self.status:<11}", self.display_color)
        self.update_line(14, f"{self.description:<68}", self.display_color)
        if self.value is not None:
            value = str(self.value).ljust(8)
            self.update_line(82, value, self.display_color)
        else:
            self.update_line(82, " "*8, self.display_color)
        self.refresh_screen()
