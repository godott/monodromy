"""
monodromy/qlr_table.py

Precomputed descriptions of the monodromy polytope for SU(4) and PU(4).
"""

from fractions import Fraction
from typing import List

from .polytopes import make_convex_polytope


"""
Precomputed table of quantum Littlewood-Richardson coefficients for the small
quantum cohomology ring of k-planes in C^4, 0 < k < 4.  Each entry is of the
form [r, k, [*a], [*b], [*c], d], corresponding to the relation

    N_{ab}^{c, d} = 1   or   <sigma_a, sigma_b, sigma_{*c}> = q^d.

NOTE: We include only entries with a <= b in the traversal ordering used by
      `qiskit.quantum_info.monodromy.lrcalc.displacements`.

NOTE: This table can be regenerated using
      `qiskit.quantum_info.monodromy.lrcalc.regenerate_qlr_table` .
"""
#              r  k   a    b    c   d
qlr_table = [[1, 3, [0], [0], [0], 0],
             [1, 3, [0], [1], [1], 0],
             [1, 3, [0], [2], [2], 0],
             [1, 3, [0], [3], [3], 0],
             [1, 3, [1], [1], [2], 0],
             [1, 3, [1], [2], [3], 0],
             [1, 3, [1], [3], [0], 1],
             [1, 3, [2], [2], [0], 1],
             [1, 3, [2], [3], [1], 1],
             [1, 3, [3], [3], [2], 1],
             # r k    a       b       c     d
             [2, 2, [0, 0], [0, 0], [0, 0], 0],
             [2, 2, [0, 0], [1, 0], [1, 0], 0],
             [2, 2, [0, 0], [1, 1], [1, 1], 0],
             [2, 2, [0, 0], [2, 0], [2, 0], 0],
             [2, 2, [0, 0], [2, 1], [2, 1], 0],
             [2, 2, [0, 0], [2, 2], [2, 2], 0],
             [2, 2, [1, 0], [1, 0], [1, 1], 0],
             [2, 2, [1, 0], [1, 0], [2, 0], 0],
             [2, 2, [1, 0], [1, 1], [2, 1], 0],
             [2, 2, [1, 0], [2, 0], [2, 1], 0],
             [2, 2, [1, 0], [2, 1], [2, 2], 0],
             [2, 2, [1, 0], [2, 1], [0, 0], 1],
             [2, 2, [1, 0], [2, 2], [1, 0], 1],
             [2, 2, [1, 1], [1, 1], [2, 2], 0],
             [2, 2, [1, 1], [2, 0], [0, 0], 1],
             [2, 2, [1, 1], [2, 1], [1, 0], 1],
             [2, 2, [1, 1], [2, 2], [2, 0], 1],
             [2, 2, [2, 0], [2, 0], [2, 2], 0],
             [2, 2, [2, 0], [2, 1], [1, 0], 1],
             [2, 2, [2, 0], [2, 2], [1, 1], 1],
             [2, 2, [2, 1], [2, 1], [2, 0], 1],
             [2, 2, [2, 1], [2, 1], [1, 1], 1],
             [2, 2, [2, 1], [2, 2], [2, 1], 1],
             [2, 2, [2, 2], [2, 2], [0, 0], 2],
             # r k      a          b          c      d
             [3, 1, [0, 0, 0], [0, 0, 0], [0, 0, 0], 0],
             [3, 1, [0, 0, 0], [1, 0, 0], [1, 0, 0], 0],
             [3, 1, [0, 0, 0], [1, 1, 0], [1, 1, 0], 0],
             [3, 1, [0, 0, 0], [1, 1, 1], [1, 1, 1], 0],
             [3, 1, [1, 0, 0], [1, 0, 0], [1, 1, 0], 0],
             [3, 1, [1, 0, 0], [1, 1, 0], [1, 1, 1], 0],
             [3, 1, [1, 0, 0], [1, 1, 1], [0, 0, 0], 1],
             [3, 1, [1, 1, 0], [1, 1, 0], [0, 0, 0], 1],
             [3, 1, [1, 1, 0], [1, 1, 1], [1, 0, 0], 1],
             [3, 1, [1, 1, 1], [1, 1, 1], [1, 1, 0], 1]]


def ineq_from_qlr(r, k, a, b, c, d):
    """
    Generates a monodromy polytope inequality from the position of a nonzero
    quantum Littlewood-Richardson coefficient.

    See (*) in Theorem 23 of /1904.10541
    """

    # $$d - \sum_{i=1}^r \alpha_{k+i-a_i}
    #     - \sum_{i=1}^r \beta_{k+i-b_i}
    #     + \sum_{i=1}^r \delta_{k+i-c_i} \ge 0$$

    new_row = [Fraction(d),
               Fraction(0), Fraction(0), Fraction(0), Fraction(0),  # alpha's
               Fraction(0), Fraction(0), Fraction(0), Fraction(0),  # beta's
               Fraction(0), Fraction(0), Fraction(0), Fraction(0), ]  # gamma's
    for i, ai in enumerate(a):
        index = k + (i + 1) - ai  # subscript in the Biswas inequality
        offset = 0  # last entry before alpha
        new_row[index + offset] -= 1  # poke the value in
    for i, bi in enumerate(b):
        index = k + (i + 1) - bi  # subscript in the Biswas inequality
        offset = 4  # last entry before beta
        new_row[index + offset] -= 1  # poke the value in
    for i, ci in enumerate(c):
        index = k + (i + 1) - ci  # subscript in the Biswas inequality
        offset = 8  # last entry before gamma
        new_row[index + offset] += 1  # poke the value in

    # now remember that a4 = -a1-a2-a3 and so on
    new_row = [new_row[0],
               *[x - new_row[4] for x in new_row[1:4]],
               *[x - new_row[8] for x in new_row[5:8]],
               *[x - new_row[12] for x in new_row[9:12]]
               ]

    return new_row


def generate_qlr_inequalities():
    """
    Regenerates the set of monodromy polytope inequalities from the stored table
    `qlr_table` of quantum Littlewood-Richardson coefficients.
    """
    qlr_inequalities = []
    for r, k, a, b, c, d in qlr_table:
        qlr_inequalities.append(ineq_from_qlr(r, k, a, b, c, d))
        if a != b:
            qlr_inequalities.append(ineq_from_qlr(r, k, b, a, c, d))

    return qlr_inequalities


"""
This houses the monodromy polytope, the main static input of the whole calc'n.
This polytope does _not_ also contain the alcove constraints.
"""
qlr_polytope = make_convex_polytope(generate_qlr_inequalities())


def fractionify(table) -> List[List[Fraction]]:
    """
    Convenience routine for not writing Fraction() a whole bunch.

    NOTE: This can be poorly behaved if your rationals don't have exact floating
          point representations!
    """
    return [[Fraction(i) for i in j] for j in table]


"""
Inequalities defining the fundamental Weyl alcove used in monodromy polytope
calculations for SU(4).
"""
alcove = make_convex_polytope(fractionify([
    [0,  1, -1,  0, ],  # a1 - a2 >= 0
    [0,  0,  1, -1, ],  # a2 - a3 >= 0
    [0,  1,  1,  2, ],  # a3 - a4 >= 0
    [1, -2, -1, -1, ],  # a4 - (a1 - 1) >= 0
]))

"""
Inequalities defining the fundamental Weyl alcove used in monodromy polytope
calculations for PU(4).
"""
alcove_c2 = make_convex_polytope(fractionify([
    *alcove.convex_subpolytopes[0].inequalities,
    [1, -2, 0, 2, ],  # a3 + 1/2 - a1 >  0 , the C2 inequality
]))
