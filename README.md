# quantum-algos-proj

Working through the major quantum algorithms one at a time, with a small self-contained project for each. The aim is understanding rather than coverage: derive the maths first, then build something that makes the mechanism visible.

A secondary constraint is tool variety. Each project uses a different part of the ecosystem (NumPy from scratch, Qiskit, Cirq, PennyLane, Stim, Q#) so the learning isn't tied to one framework's abstractions.

Each algorithm lives in its own numbered folder.

## Core list

- [X] **1. Deutsch-Jozsa** : first proof of quantum advantage on a contrived problem. Oracle generator: pick constant or balanced, circuit reveals it in one query.
- [ ] **2. Bernstein-Vazirani** : extracting a hidden bitstring in one query. "Guess my secret" game, quantum player wins in 1 shot vs n classical queries.
- [ ] **3. Quantum walks** : ballistic vs diffusive spreading. 1D Hadamard walk against the classical version, then walks on graphs.
- [ ] **4. Grover's algorithm** : quadratic speedup on unstructured search. Sudoku or graph-colouring solver with a custom oracle.
- [ ] **5. Simon's algorithm** : exponential speedup, the conceptual bridge to Shor. Includes the classical post-processing (solving the linear system over GF(2)).
- [ ] **6. Quantum phase estimation** : the workhorse subroutine behind Shor and HHL. Eigenvalues of small unitaries, precision vs ancilla count.
- [ ] **7. Stabiliser codes** (3-qubit, Shor, Steane) : how logical qubits are protected. Noise sandbox with tunable error rates, logical vs physical error rate.
- [ ] **8. QAOA** : variational approach to combinatorial problems. Max-Cut on random graphs, approximation ratio vs circuit depth p.
- [ ] **9. VQE** : hybrid quantum-classical eigensolvers. H2 dissociation curve, comparing ansatze and optimisers.
- [ ] **10. Amplitude estimation** : quadratic speedup for Monte Carlo. Option pricing or pi estimation, benchmarked against classical MC.
- [ ] **11. Quantum kernel methods** : feature maps in Hilbert space. Kernel-target alignment: which datasets actually benefit?
- [ ] **12. Variational quantum classifiers** : trainable quantum circuits. Small image classifier, investigating barren plateaus as qubit count grows.
- [ ] **13. Shor's algorithm** : exponential speedup, breaks RSA. Factor 15, 21, 35 end to end, then resource estimates for RSA-2048.
- [ ] **14. Trotter-Suzuki / Hamiltonian simulation** : the original motivation for quantum computers. Spin chain simulation, Trotter error vs step size.
- [ ] **15. HHL** : linear systems, heavily caveated. Implement for a 2x2 system, then write up why the caveats usually kill the advantage.
- [ ] **16. Quantum PCA** : density matrix exponentiation. Toy covariance data, stress-testing the assumptions.
- [ ] **17. QGANs** : generative modelling with quantum circuits. Learn a simple distribution, compare against a classical GAN.
- [ ] **18. Surface codes** : the leading fault-tolerance route. Build a decoder (MWPM via NetworkX), plot threshold behaviour.
- [ ] **19. Magic state distillation** : non-Clifford gates fault-tolerantly. Simulate the 15-to-1 protocol, output error vs input error.
- [ ] **20. BB84 / E91** : quantum cryptography rather than computation. Simulate a QKD channel with an eavesdropper, detect them via error rate.

## Extensions

Gaps identified after drafting the main list. Not necessarily in order, and some are write-ups rather than code.

### Foundational primitives

- [ ] Teleportation and superdense coding
- [ ] CHSH / Bell inequality violation
- [ ] Quantum Fourier transform as its own object

### Missing subroutines

- [ ] Amplitude amplification (general form)
- [ ] Quantum counting
- [ ] Iterative / Kitaev phase estimation
- [ ] Hidden subgroup problem (write-up)

### The modern framework

- [ ] Block encoding, LCU, qubitisation, QSVT
- [ ] qDRIFT and post-Trotter simulation

### Practical / NISQ

- [ ] Classical shadows
- [ ] Error mitigation (ZNE, PEC, symmetry verification)
- [ ] Gottesman-Knill and stabiliser simulation
- [ ] Solovay-Kitaev and gate synthesis

### Alternative models

- [ ] Adiabatic / quantum annealing
- [ ] Measurement-based (cluster state) computing
- [ ] Boson sampling / random circuit sampling

### Error correction beyond the surface code

- [ ] qLDPC codes (e.g. bivariate bicycle)
- [ ] Colour codes
