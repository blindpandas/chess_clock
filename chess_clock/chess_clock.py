# coding: utf-8

import time


Seconds = int


class ChessClock:

    def __init__(self, base_time: Seconds, increment: Seconds):
        self.base_time = base_time
        self.increment = increment
        self.total_time_credit = base_time
        self._remaining = self.total_time_credit
        self.started_at = None
        self.__started_once = False

    def __repr__(self):
        if self.__started_once:
            status = "ticking" if self.is_ticking() else "paused"
        else:
            status = "not started"
        return f"<ChessClock: status={status}, elapsed={self.elapsed}, remaining={self.remaining}>"

    def is_ticking(self):
        return self.started_at is not None

    def _get_elapsed(self):
        return self.total_time_credit - self._get_remaining()

    def _get_remaining(self):
        if self.started_at is None:
            remaining = self._remaining
        else:
            remaining = self.total_time_credit - (time.monotonic() - self.started_at)
        return remaining if remaining >= 0 else 0

    @property
    def elapsed(self):
        return round(self._get_elapsed())

    @property
    def remaining(self):
        return round(self._get_remaining())

    def start(self):
        if self.__started_once:
            raise RuntimeError("Clock can only be started once.")
        self.started_at = time.monotonic()
        self.__started_once = True

    def pause(self):
        if not self.is_ticking():
            raise RuntimeError("Could not pause clock. Clock is not ticking.") 
        self.total_time_credit += self.increment
        self._remaining = self._get_remaining()
        self.started_at = None

    def resume(self):
        if self.is_ticking():
            raise RuntimeError("Could not resume clock. Clock is already ticking.") 
        elif not self.__started_once:
            raise RuntimeError("Can not resume clock. Clock has not been started.")
        self.started_at = time.monotonic()

