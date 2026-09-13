"""
04 - Measurement and sampling.

Every file so far inspected the exact quantum state directly (amplitudes,
probabilities) - something a real quantum computer can never show you.
A real device only gives you classical bits from measuring, and measuring
is destructive and random: each shot collapses the state to one outcome,
drawn according to the probabilities from 03_statevector_simulation.py.

Note on API version: older Qiskit tutorials use `execute(qc, backend)` or
`backend.run(qc)`. Both are deprecated. Qiskit 2.x's supported path is the
"primitives" interface - here, StatevectorSampler, an exact (noise-free)
local sampler.

Key objects:
  qc.measure(qubit, clbit)          - measure qubit, store result in clbit
  StatevectorSampler()              - a local, exact sampling primitive
  sampler.run([qc], shots=n)        - submit a job, get many shots at once
  job.result()[0].data.<creg>.get_counts()
                                     - {bitstring: count} for register <creg>
"""

from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorSampler


def bell_pair_with_measurement():
    qc = QuantumCircuit(2, 2, name="bell")
    qc.h(0)
    qc.cx(0, 1)
    qc.measure([0, 1], [0, 1])   # measure qubit i into classical bit i
    return qc


if __name__ == "__main__":
    qc = bell_pair_with_measurement()
    print(qc.draw(output="text"))

    sampler = StatevectorSampler()
    job = sampler.run([qc], shots=1000)
    result = job.result()

    # The classical register was created unnamed by QuantumCircuit(2, 2),
    # so Qiskit defaults its name to "c" - that's the attribute to read off.
    counts = result[0].data.c.get_counts()
    print(f"\n1000 shots of a Bell pair -> counts: {counts}")
    print("expect roughly 50/50 split between '00' and '11', nothing else,")
    print("because the Bell state has zero amplitude on '01' and '10'.")

    total = sum(counts.values())
    assert total == 1000
    assert set(counts) <= {"00", "11"}   # no other outcome should ever appear
    print("\nsanity check passed: only '00' and '11' occurred, counts sum to 1000")

    # Try it yourself:
    # Change bell_pair_with_measurement() to measure only qubit 0 (drop
    # qubit 1's measure call and give it 1 classical bit instead of 2).
    # Predict the counts dict shape before running: what happens to a qubit
    # that's entangled with an unmeasured partner?
    # Next file introduces gates that take a continuous parameter instead of
    # a fixed operation - rotation gates.
