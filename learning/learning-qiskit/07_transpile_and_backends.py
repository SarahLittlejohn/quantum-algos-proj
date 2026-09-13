"""
07 - Transpile and backends.

Every prior file used Statevector: an exact, ideal simulation with no
concept of hardware. Real quantum computers only support a small fixed set
of native gates ("basis gates") and only allow two-qubit gates between
physically-connected qubits. transpile() rewrites your circuit into an
equivalent one using only those allowed operations - the compiler step
between "the circuit you wrote" and "the circuit that can actually run".

AerSimulator is a backend that executes circuits shot by shot like real
hardware would (random outcomes from measurement, like 04's Sampler), rather
than handing you the exact state directly.

Key objects:
  transpile(qc, basis_gates=[...])   - rewrite qc using only these gate names
  transpile(qc, backend=...)         - rewrite qc for a specific backend's
                                        constraints
  AerSimulator()                     - a local backend that runs circuits
  backend.run(qc, shots=n)           - execute directly on a backend
                                        (the classic path - still supported
                                        for backends specifically, unlike the
                                        removed top-level execute() function)
"""

from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator


def bell_circuit_with_z():
    qc = QuantumCircuit(2, 2)
    qc.h(0)
    qc.cx(0, 1)
    qc.z(0)
    qc.measure([0, 1], [0, 1])
    return qc


if __name__ == "__main__":
    qc = bell_circuit_with_z()
    print("original circuit:")
    print(qc.draw(output="text"))
    print("gate names:", [instr.operation.name for instr in qc.data])

    # Restrict to a minimal universal basis: u3 (arbitrary single-qubit
    # rotation) + cx. h and z above must be rewritten in terms of these.
    restricted = transpile(qc, basis_gates=["u3", "cx"], optimization_level=1)
    print("\ntranspiled to basis_gates=['u3', 'cx']:")
    print(restricted.draw(output="text"))
    print("gate names:", [instr.operation.name for instr in restricted.data])
    assert set(i.operation.name for i in restricted.data) <= {"u3", "cx", "measure", "barrier"}
    print("sanity check passed: no h or bare z survived transpilation")

    # Now actually execute it on a simulated backend instead of reading the
    # exact statevector.
    backend = AerSimulator()
    tqc = transpile(qc, backend)
    job = backend.run(tqc, shots=1000)
    counts = job.result().get_counts()
    print(f"\nAerSimulator, 1000 shots -> {counts}")
    print("expect ~50/50 '00'/'11', same distribution Statevector predicted in 04,")
    print("but this time obtained by actually simulating shot noise, not reading amplitudes.")

    # Try it yourself:
    # Transpile bell_circuit_with_z() with basis_gates=['cz', 'sx', 'rz'] (a
    # different universal set - common on real IBM hardware) instead of
    # ['u3', 'cx'], and compare how many gates each rewrite produces via
    # restricted.size(). This closes out the basics curriculum - from here,
    # the next step is applying these building blocks to an actual algorithm.
