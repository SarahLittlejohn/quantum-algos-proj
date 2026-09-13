"""
01 - Circuits and gates.

A QuantumCircuit is Qiskit's basic unit of work: a sequence of gates applied
to qubits, plus (optionally) classical bits to store measurement results
later. This file only builds and draws circuits - no simulation yet, that's
03_statevector_simulation.py. The goal here is just: what are the pieces,
and how do you assemble them.

Key objects:
  QuantumRegister(n)      - a named block of n qubits
  ClassicalRegister(n)    - a named block of n classical bits
  QuantumCircuit(q, c)    - ties registers together into one circuit
  qc.<gate>(qubit)        - append a gate; gates read top to bottom in the
                            drawing, same order they're applied in

Gates used below (single-qubit):
  x   - bit-flip (NOT).                 |0> -> |1>
  h   - Hadamard, equal superposition.  |0> -> (|0> + |1>) / sqrt(2)
  z   - phase-flip. Leaves |0> alone, sends |1> -> -|1>
  y   - bit-flip and phase-flip combined
  s   - quarter phase turn (S = sqrt(Z))
  t   - eighth phase turn (T = sqrt(S))
"""

from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister


def build_example_circuit():
    q = QuantumRegister(2, name="q")
    c = ClassicalRegister(2, name="c")
    qc = QuantumCircuit(q, c)

    qc.h(0)   # put qubit 0 into superposition
    qc.x(1)   # flip qubit 1 from |0> to |1>
    qc.z(0)   # phase-flip qubit 0 (invisible here - no interference yet to reveal it)
    return qc


if __name__ == "__main__":
    qc = build_example_circuit()
    print(qc.draw(output="text"))

    print(f"\nnum_qubits={qc.num_qubits}  num_clbits={qc.num_clbits}  depth={qc.depth()}")
    print("gate sequence:", [instr.operation.name for instr in qc.data])

    # Try it yourself:
    # Add a `s` gate on qubit 1 right after the x gate, redraw the circuit,
    # and check that qc.data now lists 4 gates instead of 3 in the order
    # you added them. Then move on to 02_multi_qubit_gates.py to see how
    # qubits start interacting with each other instead of sitting alone.
