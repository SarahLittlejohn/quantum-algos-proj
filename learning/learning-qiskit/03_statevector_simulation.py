"""
03 - Statevector simulation.

02_multi_qubit_gates.py already used Statevector to read off probabilities.
This file goes one level deeper: the full complex amplitudes, not just their
squared magnitudes - the thing your dj-simulator.py builds by hand with
numpy tensors. Statevector is Qiskit's built-in equivalent: no measurement,
no randomness, just "what is the exact quantum state after these gates".

Key objects:
  Statevector.from_label("00")   - construct a basis state directly
  Statevector(qc)                 - evolve |00...0> through a circuit
  sv.evolve(qc)                   - evolve an existing statevector further
  sv.data                         - the raw complex amplitude array
  sv.probabilities_dict()         - |amplitude|^2 per bitstring (seen already)
"""

import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector


def show_amplitudes(sv, label=""):
    """Print every basis state with a non-negligible amplitude."""
    print(label)
    n = sv.num_qubits
    for i, amp in enumerate(sv.data):
        if abs(amp) > 1e-9:
            bitstring = format(i, f"0{n}b")
            print(f"  |{bitstring}>  amp {amp.real:+.3f}{amp.imag:+.3f}j   prob {abs(amp) ** 2:.3f}")
    print()


if __name__ == "__main__":
    # Start from an explicit basis state, same idea as zero_state(k) in
    # dj-simulator.py, but Qiskit gives you the constructor directly.
    sv0 = Statevector.from_label("00")
    show_amplitudes(sv0, "starting state |00>")

    # Evolve it step by step with .evolve(), rather than building one circuit
    # up front - useful for inspecting a computation mid-flight.
    step1 = QuantumCircuit(2)
    step1.h(0)
    sv1 = sv0.evolve(step1)
    show_amplitudes(sv1, "after H on qubit 0")

    step2 = QuantumCircuit(2)
    step2.cx(0, 1)
    sv2 = sv1.evolve(step2)
    show_amplitudes(sv2, "after CX(0 -> 1) -> Bell pair")

    # Sanity check against hand computation: a Bell pair should be exactly
    # (|00> + |11>) / sqrt(2), i.e. amplitude 1/sqrt(2) on each, zero phase.
    expected = 1 / np.sqrt(2)
    assert abs(sv2.data[0].real - expected) < 1e-9   # |00>
    assert abs(sv2.data[3].real - expected) < 1e-9   # |11>
    print(f"sanity check passed: both amplitudes equal 1/sqrt(2) = {expected:.3f}")

    # Try it yourself:
    print("My task...")
    sv_singlet = Statevector.from_label("01")
    sv_singlet1 = sv_singlet.evolve(step1)
    show_amplitudes(sv_singlet1, "after H on qubit 0")
    stepCNOT = QuantumCircuit(2)
    stepCNOT.cx(0,1)
    sv_singlet2 = sv_singlet1.evolve(stepCNOT)
    show_amplitudes(sv_singlet2, "after CNOT")
    stepX = QuantumCircuit(2)
    stepX.x(0)
    sv_singlet3 = sv_singlet2.evolve(stepX)
    show_amplitudes(sv_singlet3, "after X on qubit 0")


    # Build the state (|01> - |10>) / sqrt(2) (the singlet state) by starting
    # from Statevector.from_label("01"), applying H to qubit 0, then CX(0 -> 1),
    # then a X somewhere to flip the sign on the right term. Print the
    # amplitudes and check the signs match what you'd compute by hand.
    # Next file adds measurement - turning this exact state into random
    # classical outcomes, the way a real quantum computer would.
