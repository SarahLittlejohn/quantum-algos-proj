# Learning Qiskit

Step 1 of learning Qiskit: work through the basics before applying them to an actual algorithm. Each file is self-contained — a notes block explaining the concept, minimal runnable code, and one "try it yourself" exercise at the bottom. Run them in order; each builds on the last.

Generated with the `learning-curriculum` skill (`.claude/skills/learning-curriculum/SKILL.md`).

## Basics

- [X] **1. Circuits and gates** (`01_circuits_and_gates.py`) : `QuantumCircuit`, registers, single-qubit gates (X, H, Z, Y, S, T), drawing circuits.
- [X] **2. Multi-qubit gates** (`02_multi_qubit_gates.py`) : CX/CNOT, CZ, SWAP, Toffoli, and Qiskit's little-endian qubit ordering.
- [X] **3. Statevector simulation** (`03_statevector_simulation.py`) : exact complex amplitudes via `Statevector`, `.evolve()`.
- [ ] **4. Measurement and sampling** (`04_measurement_and_sampling.py`) : classical registers, `measure()`, the `StatevectorSampler` primitive, reading counts.
- [ ] **5. Parameterized and rotation gates** (`05_parameterized_and_rotation_gates.py`) : RX/RY/RZ, `Parameter` objects, binding values.
- [ ] **6. Custom gates and oracles** (`06_custom_gates_and_oracles.py`) : packaging sub-circuits as reusable gates, rebuilding Deutsch-Jozsa's oracle test in Qiskit.
- [ ] **7. Transpile and backends** (`07_transpile_and_backends.py`) : `transpile()` to a basis gate set, running on `AerSimulator`.

## Step 2

Once the basics above are ticked off, pick a small warm-up problem to apply Qiskit to before returning to the main README's algorithm roadmap.
