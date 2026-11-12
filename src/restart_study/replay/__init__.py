"""Trajectory replay.

Loads a failed trajectory, replays its logged actions up to a chosen restart step,
and verifies that each observation matches the log before the agent continues.
"""
