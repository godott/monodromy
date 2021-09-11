"""
test/xx_decompose/test_circuits.py

Tests for monodromy/xx_decompose/circuits.py .
"""

import qiskit

import ddt
import unittest

import random

import numpy as np

from qiskit.quantum_info.synthesis.weyl import weyl_coordinates

from monodromy.xx_decompose.circuits import *
from monodromy.static.matrices import canonical_matrix, rz_matrix

epsilon = 0.001


@ddt.ddt
class TestMonodromyCircuits(unittest.TestCase):
    """Check circuit synthesis step routines."""

    def __init__(self, *args, seed=42, **kwargs):
        super().__init__(*args, **kwargs)
        random.seed(seed)
        np.random.seed(seed)

    def _generate_xxyy_test_case(self):
        source_coordinate = [random.random(), random.random(), 0.0]
        source_coordinate = [
            source_coordinate[0] * np.pi / 8,
            source_coordinate[1] * source_coordinate[0] * np.pi / 8,
            0.0
        ]
        interaction = [random.random() * np.pi / 8]
        z_angles = [random.random() * np.pi / 8, random.random() * np.pi / 8]
        prod = (
                canonical_matrix(*source_coordinate) @
                np.kron(rz_matrix(z_angles[0]), rz_matrix(z_angles[1])) @
                canonical_matrix(interaction[0], 0., 0.)
        )
        target_coordinate = weyl_coordinates(prod)

        self.assertAlmostEqual(target_coordinate[-1], 0.0, delta=epsilon)

        return source_coordinate, interaction, target_coordinate

    def test_decompose_xxyy(self):
        """
        Test that decompose_xxyy_into_xxyy_xx correctly recovers decompositions.
        """

        for _ in range(100):
            source_coordinate, interaction, target_coordinate = \
                self._generate_xxyy_test_case()

            r, s, u, v, x, y = decompose_xxyy_into_xxyy_xx(
                target_coordinate[0], target_coordinate[1],
                source_coordinate[0], source_coordinate[1],
                interaction[0]
            )

            prod = (
                np.kron(rz_matrix(r), rz_matrix(s)) @
                canonical_matrix(*source_coordinate) @
                np.kron(rz_matrix(u), rz_matrix(v)) @
                canonical_matrix(interaction[0], 0., 0.) @
                np.kron(rz_matrix(x), rz_matrix(y))
            )
            expected = canonical_matrix(*target_coordinate)
            self.assertTrue(np.all(np.abs(prod - expected) < epsilon))

    def test_xx_circuit_step(self):
        for _ in range(100):
            source_coordinate, interaction, target_coordinate = \
                self._generate_xxyy_test_case()

            source_embodiment = qiskit.QuantumCircuit(2)
            source_embodiment.append(qiskit.extensions.UnitaryGate(
                canonical_matrix(*source_coordinate)
            ), [0, 1])
            interaction_embodiment = qiskit.QuantumCircuit(2)
            interaction_embodiment.append(qiskit.extensions.UnitaryGate(
                canonical_matrix(*interaction)
            ), [0, 1])

            prefix_circuit, affix_circuit = \
                itemgetter("prefix_circuit", "affix_circuit")(
                    xx_circuit_step(source_coordinate,
                                    interaction[0],
                                    target_coordinate,
                                    interaction_embodiment)
                )

            target_embodiment = qiskit.QuantumCircuit(2)
            target_embodiment.compose(prefix_circuit, inplace=True)
            target_embodiment.compose(source_embodiment, inplace=True)
            target_embodiment.compose(affix_circuit, inplace=True)
            self.assertTrue(np.all(np.abs(
                qiskit.quantum_info.operators.Operator(target_embodiment).data
                - canonical_matrix(*target_coordinate)) < epsilon))