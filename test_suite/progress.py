import curses
import itertools


class Progress:
    default_line = 1

    def __init__(self, stdscr, label="Total:", parent=None, total=0, line=0):
        self.total = total
        self.label = label
        self.screen = stdscr
        self.current = 0
        self.parent = parent
        self.line = line or self.default_line
        self.chunks = []
        self.update()

    def write(self, start, end, text, color):
        fill = ' ' * (end - start - len(text))
        self.screen.addstr(self.line, start, f"{text}{fill}", color)

    def write_bar(self):
        bar_start = 13
        bar_end = 79
        bar_length = bar_end - bar_start - 1
        bar_color = curses.color_pair(5)

        self.write(bar_start, bar_start+1, '[', bar_color)
        self.write(bar_end, bar_end+2, ']', bar_color)

        if not self.total:
            self.write(bar_start, bar_end, ' ', bar_color)
            return

        for i, value in enumerate(self.iter_bar(bar_length)):
            if value is None:
                color = bar_color
            elif value:
                color = curses.color_pair(2)
            else:
                color = curses.color_pair(1)
            start = i + bar_start + 1
            self.write(start, start, ' ', color | curses.A_REVERSE)

    def iter_bar(self, stretching_to):
        # thanks a million to MIkusaba for this section

        # pad values
        n_to_pad = self.total - len(self.chunks)
        padded_values = itertools.chain(
            self.chunks, itertools.repeat(None, n_to_pad)
        )

        # basically more_itertools.divide
        q, r = divmod(stretching_to, self.total)
        for i, v in enumerate(padded_values):
            start = (i * q) + (i if i < r else r)
            stop = ((i + 1) * q) + (i + 1 if i + 1 < r else r)
            for _ in range(start, stop):
                yield v

    def write_fraction(self):
        fraction_start = 81
        fraction_end = 90
        fraction_color = curses.color_pair(5)
        passed = sum(self.chunks)
        fraction = f" {passed}/{self.total}"
        self.write(fraction_start, fraction_end, fraction, fraction_color)

    def write_label(self):
        label_start = 0
        label_end = 17
        label_color = curses.color_pair(5)
        self.write(label_start, label_end, f" {self.label}", label_color)

    def refresh(self):
        curses.curs_set(0)
        self.screen.refresh()

    def increment(self, passed=True):
        self.chunks.append(passed)
        self.current += 1
        self.update()
        if self.parent:
            self.parent.increment(passed)

    def update(self):
        self.write_label()
        self.write_bar()
        self.write_fraction()
        self.refresh()
