"""
test/xx_decompose/test_weyl.py

Tests for monodromy/xx_decompose/weyl.py .
"""

import qiskit
from qiskit.quantum_info.operators import Operator

import ddt
import unittest

from itertools import permutations
import random

from monodromy.static.matrices import *
from monodromy.xx_decompose.weyl import *

epsilon = 0.001


@ddt.ddt
class TestMonodromyWeyl(unittest.TestCase):
    """Check Weyl action routines."""

    def __init__(self, *args, seed=42, **kwargs):
        super().__init__(*args, **kwargs)
        random.seed(seed)
        np.random.seed(seed)

    def test_reflections(self):
        """Check that reflection circuits behave as expected."""
        for name in reflection_options.keys():
            coordinate = [random.random() for _ in range(3)]
            reflected_coordinate, reflection_circuit, reflection_phase = \
                apply_reflection(name, coordinate)
            original_matrix = canonical_matrix(*coordinate)
            reflected_matrix = canonical_matrix(*reflected_coordinate)
            reflect_matrix = Operator(reflection_circuit).data
            with np.printoptions(precision=3, suppress=True):
                print(name)
                print(reflect_matrix.conjugate().transpose(1, 0) @ original_matrix @ reflect_matrix)
                print(reflected_matrix * reflection_phase)
            self.assertTrue(np.all(
                np.abs(reflect_matrix.conjugate().transpose(1, 0) @ original_matrix @ reflect_matrix
                       - reflected_matrix * reflection_phase)
                < epsilon
            ))

    def test_shifts(self):
        """Check that shift circuits behave as expected."""
        for name in shift_options.keys():
            coordinate = [random.random() for _ in range(3)]
            shifted_coordinate, shift_circuit, shift_phase = apply_shift(
                name, coordinate
            )
            original_matrix = canonical_matrix(*coordinate)
            shifted_matrix = canonical_matrix(*shifted_coordinate)
            shift_matrix = Operator(shift_circuit).data
            with np.printoptions(precision=3, suppress=True):
                print(name)
                print(original_matrix @ shift_matrix)
                print(shifted_matrix * shift_phase)
            self.assertTrue(np.all(
                np.abs(original_matrix @ shift_matrix
                       - shifted_matrix * shift_phase)
                < epsilon
            ))

    def test_rotations(self):
        """Check that rotation circuits behave as expected."""
        for permutation in permutations([0, 1, 2]):
            coordinate = [random.random() for _ in range(3)]
            rotation_circuit = canonical_rotation_circuit(
                permutation[0], permutation[1]
            )
            original_matrix = canonical_matrix(*coordinate)
            rotation_matrix = Operator(rotation_circuit).data
            rotated_matrix = canonical_matrix(
                coordinate[permutation[0]],
                coordinate[permutation[1]],
                coordinate[permutation[2]],
            )
            self.assertTrue(np.all(
                np.abs(rotation_matrix.conjugate().transpose(1, 0) @ original_matrix @ rotation_matrix
                       - rotated_matrix)
                < epsilon
            ))