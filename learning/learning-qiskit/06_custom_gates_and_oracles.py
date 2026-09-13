"""
06 - Custom gates and oracles.

Every gate so far has been a Qiskit built-in. Real circuits are built by
packaging a sub-circuit into a single reusable gate, then treating it as a
black box inside a bigger circuit - exactly the role an "oracle" plays in
Deutsch-Jozsa: a black box that computes a function, used without caring how.

This mirrors deutsch-jozsa/dj-simulator.py's phase_oracle(f), but built from
real Qiskit gates instead of a numpy sign-flip array, and using the same two
test cases as that file's own sanity check: a constant oracle (identity) and
the simplest possible balanced oracle (Z on qubit 0, i.e. f(x) = x_0).

Note, same caveat as dj-simulator.py: a *general* balanced oracle (arbitrary
truth table) needs an ancilla qubit and phase kickback via CX gates. That
construction is left for later - both files stick to oracles simple enough
to write down directly.

Key objects:
  qc.to_gate(label=...)     - freeze a sub-circuit into one reusable gate
  qc.append(gate, qubits)   - insert a custom gate into a bigger circuit
"""

from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector


def oracle_constant(k):
    """f(x) = 0 for all x: no operation at all."""
    qc = QuantumCircuit(k, name="const")
    return qc.to_gate()


def oracle_balanced_z0(k):
    """f(x) = x_0: exactly half the inputs get phase-flipped. A single Z gate."""
    qc = QuantumCircuit(k, name="bal_z0")
    qc.z(0)
    return qc.to_gate()


def deutsch_jozsa(k, oracle_gate):
    """H on every qubit, one oracle call, H on every qubit - same structure
    as dj-simulator.py's deutsch_jozsa(), now built from real Qiskit gates."""
    qc = QuantumCircuit(k)
    qc.h(range(k))
    qc.append(oracle_gate, range(k))
    qc.h(range(k))
    return qc


def verdict(qc):
    p_all_zero = Statevector(qc).probabilities_dict().get("0" * qc.num_qubits, 0.0)
    return "constant" if p_all_zero > 1 - 1e-9 else "balanced"


if __name__ == "__main__":
    k = 2

    qc_const = deutsch_jozsa(k, oracle_constant(k))
    print(qc_const.draw(output="text"))
    print(f"constant oracle -> {verdict(qc_const)}\n")

    qc_bal = deutsch_jozsa(k, oracle_balanced_z0(k))
    print(qc_bal.draw(output="text"))
    print(f"balanced oracle (Z on q0) -> {verdict(qc_bal)}\n")

    assert verdict(qc_const) == "constant"
    assert verdict(qc_bal) == "balanced"
    print("sanity check passed: matches dj-simulator.py's own constant/balanced verdicts")

    # Try it yourself:
    # Write oracle_balanced_z1(k) that applies Z to qubit 1 instead of qubit 0
    # (f(x) = x_1), run it through deutsch_jozsa(3, ...) with k=3, and confirm
    # verdict() still says "balanced" even though the oracle acts on a
    # different qubit than before.
    # Next file runs circuits like these on a simulated *backend* instead of
    # reading the exact statevector - the last step before real hardware.
