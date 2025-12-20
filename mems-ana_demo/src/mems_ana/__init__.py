# -*- coding: utf-8 -*-
"""
mems_ana

Lightweight, explainable (schematic) MEMS analysis utilities.
Not FEM. Purpose is to "see the shape" and compare tendencies.
"""

from .ferroelectric import make_branches, make_closed_loop

__all__ = [
    "make_branches",
    "make_closed_loop",
]
