"""
02 - Multi-qubit gates and Qiskit's bit ordering.

Single-qubit gates act on one wire in isolation. Multi-qubit gates are where
qubits actually start affecting each other - this is what makes entanglement
possible.

Key gates:
  cx(control, target)        - CNOT. Flips target iff control is |1>.
  cz(control, target)        - phase-flips target iff control is |1>.
                                Symmetric in control/target, unlike cx.
  swap(a, b)                 - exchanges the states of two qubits
  ccx(c1, c2, target)        - Toffoli. Flips target iff both controls are |1>.

Ordering gotcha (important if you're coming from a hand-rolled simulator,
see deutsch-jozsa/dj-simulator.py where qubit 0 is the LEFTMOST bit of the
printed ket): Qiskit does the opposite. Qiskit's statevector and bitstrings
are little-endian - qubit 0 is the RIGHTMOST bit. |q1 q0> is the read order,
not |q0 q1>. This trips everyone up at least once, so we check it directly
below instead of just asserting it.
"""

from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector


def bell_pair():
    """H on qubit 0, then CNOT(0 -> 1). Produces (|00> + |11>) / sqrt(2)."""
    qc = QuantumCircuit(2)
    qc.h(0)
    qc.cx(0, 1)
    return qc


def probs(sv):
    """Plain {bitstring: rounded float} dict, easier to read than raw numpy output."""
    return {str(k): round(float(v), 3) for k, v in sv.probabilities_dict().items()}


def check_bit_ordering():
    """Flip only qubit 0 with an X gate and read off which ket label lights up."""
    qc = QuantumCircuit(2)
    qc.x(0)   # flip ONLY qubit 0
    # If qubit 0 is the rightmost character, flipping it alone should light
    # up "01", not "10".
    return probs(Statevector(qc))


if __name__ == "__main__":
    qc = bell_pair()
    print(qc.draw(output="text"))
    print("\nbell pair amplitudes:", probs(Statevector(qc)))

    print("\nordering check (x on qubit 0 only):", check_bit_ordering())
    print("-> qubit 0 is the RIGHTMOST character in the ket label.")

    print("\nToffoli (ccx): flips target only when both controls are |1>")
    qc2 = QuantumCircuit(3)
    qc2.x(0)
    qc2.x(1)     # both controls set to |1>
    qc2.ccx(0, 1, 2)
    print(qc2.draw(output="text"))
    print("result:", probs(Statevector(qc2)))

    # Try it yourself:
    # In check_bit_ordering(), flip qubit 1 instead of qubit 0 (qc.x(1)) and
    # predict which ket label lights up before running it - then confirm.
    # Next file uses Statevector properly to inspect amplitudes, not just
    # probabilities.
