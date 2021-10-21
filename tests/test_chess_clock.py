#!/usr/bin/env python

"""Tests for `chess_clock` package."""

import time
import pytest


from chess_clock import chess_clock


@pytest.fixture
def clock():
    return chess_clock.ChessClock(60, 10)


def test_setup_clock_variables(clock):
    assert clock.base_time == clock.total_time_credit
    assert clock.remaining == clock.total_time_credit


def test_operations(clock):
    clock.start()
    assert clock.is_ticking()
    assert (clock.remaining + clock.elapsed) == clock.total_time_credit
    time.sleep(2)
    assert clock.elapsed == 2
    assert clock.remaining  == clock.total_time_credit - 2
    assert (clock.remaining + clock.elapsed) == clock.total_time_credit


def test_pause(clock):
    clock.start()
    time.sleep(3)
    assert clock.elapsed == 3
    assert clock.remaining  == clock.total_time_credit - 3
    clock.pause()
    old_elapsed = clock.elapsed
    time.sleep(2)
    assert old_elapsed == clock.elapsed


def test_invalid_operations(clock):
    with pytest.raises(RuntimeError):
        clock.pause()
    with pytest.raises(RuntimeError):
        clock.resume()
    clock.start()
    with pytest.raises(RuntimeError):
        clock.resume()
    clock.pause()
    clock.resume()


def test_increment(clock):
    clock.start()
    time.sleep(2)
    assert clock.elapsed == 2
    assert clock.remaining == clock.base_time  - 2
    clock.pause()
    assert clock.elapsed == 2
    assert clock.remaining  == clock.base_time + clock.increment - 2
