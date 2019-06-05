import curses


class Progress:
    line = None

    def __init__(self, total, stdscr, name=None, parent=None):
        self.total = total
        self.label = f"{name} Stage:" if name else "Total Progress:"
        self.screen = stdscr
        self.text_color = curses.A_BOLD | curses.color_pair(self.text_int)
        self.bar_color = curses.A_BOLD | curses.color_pair(self.bar_int)
        self.current = 0
        self.parent = parent
        self.update(0)

    def write(self, start, text, bar=True):
        color = self.bar_color if bar else self.text_color
        self.screen.addstr(self.line, start, text, color)
        self.screen.addstr(self.line, 17, "[", curses.A_BOLD)
        self.screen.addstr(self.line, 81, "]", curses.A_BOLD)

    def refresh(self):
        curses.curs_set(0)
        self.screen.refresh()

    def increment(self):
        self.current += 1
        self.update(self.current)
        if self.parent:
            self.parent.increment()

    def update(self, completed):
        if completed:
            bar = '|' * round(completed/self.total*64)
        else:
            bar = ''
        fraction = f"{completed:>2}/{self.total}"

        self.write(18, f"{' ' * 64}")
        self.write(18, bar, True)
        self.write(84, fraction)
        self.write(1, f"{self.label:<15}")
        self.refresh()


class GlobalProgress(Progress):
    line = 1
    text_int = 2
    bar_int = 2


class GroupProgress(Progress):
    line = 2
    text_int = 3
    bar_int = 2
