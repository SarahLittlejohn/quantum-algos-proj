"""
05 - Parameterized and rotation gates.

H, X, Z etc. are fixed operations - always the same matrix. Rotation gates
take a continuous angle and sweep smoothly between outcomes, which is what
variational algorithms (VQE, QAOA, and friends) are built out of. Qiskit
lets you build a circuit with a symbolic Parameter and bind an actual number
in later, so you can build the circuit's structure once and reuse it for
many angles - e.g. when a classical optimizer is searching over angles.

Key objects:
  rx(theta, q), ry(theta, q), rz(theta, q)
                                  - rotate qubit q by angle theta (radians)
                                    around the X, Y, or Z axis of the Bloch
                                    sphere
  Parameter("name")               - a symbolic placeholder for an angle
  qc.assign_parameters({p: value})
                                  - substitute a real number for a Parameter,
                                    returns a new bound circuit (does not
                                    mutate qc)
"""

import numpy as np
from qiskit import QuantumCircuit
from qiskit.circuit import Parameter
from qiskit.quantum_info import Statevector


def ry_circuit(theta):
    qc = QuantumCircuit(1)
    qc.ry(theta, 0)   # symbolic or concrete angle, same call either way
    return qc


if __name__ == "__main__":
    # RY(theta) on |0> gives cos(theta/2)|0> + sin(theta/2)|1> - a smooth
    # dial between |0> (theta=0) and |1> (theta=pi).
    for theta in (0, np.pi / 2, np.pi):
        sv = Statevector(ry_circuit(theta))
        p0 = sv.probabilities_dict().get("0", 0.0)
        print(f"theta={theta:.3f}  P(|0>)={p0:.3f}  (expected cos^2(theta/2)={np.cos(theta / 2) ** 2:.3f})")

    print()

    # Build the circuit's structure once with a symbolic Parameter, bind
    # different angles into it afterward without rebuilding the circuit.
    theta = Parameter("theta")
    template = QuantumCircuit(1)
    template.ry(theta, 0)
    print("template (unbound):")
    print(template.draw(output="text"))

    for value in (0.0, np.pi / 2, np.pi):
        bound = template.assign_parameters({theta: value})
        p0 = Statevector(bound).probabilities_dict().get("0", 0.0)
        print(f"bound theta={value:.3f}  P(|0>)={p0:.3f}")

    # Try it yourself:
    # Add a second Parameter `phi` and an rz(phi, 0) gate to `template` after
    # the ry. Bind both parameters at once with
    # template.assign_parameters({theta: ..., phi: ...}) and confirm the
    # probabilities are unaffected by phi (rz only changes phase, and a
    # single-qubit Z-rotation phase is invisible to a Z-basis measurement).
    # Next file uses circuits like this as *building blocks* inside larger
    # circuits - custom gates and oracles.
