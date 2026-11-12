"""Restart-point experiments for failed LLM agent runs.

Subpackages:
    envs         Environment adapters that reset a task and step through it.
    replay       Replays logged actions up to a restart step and checks observations.
    agents       Model clients and the loop that continues a run after a restart.
    attribution  Methods that predict which step of a failed run went wrong.
    metrics      Repair success, token cost and confidence intervals.
"""

__version__ = "0.0.1"
