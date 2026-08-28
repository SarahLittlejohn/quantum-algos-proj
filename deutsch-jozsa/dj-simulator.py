"""
Deutsch-Jozsa on a from-scratch state vector simulator.

Convention: the state is a complex array of shape (2,) * k, one axis per qubit.
Axis j is qubit j. Qubit 0 is the leftmost bit of the printed ket, so
psi[b0, b1, ..., b_{k-1}] is the amplitude of |b0 b1 ... b_{k-1}>.

The oracle is applied as a direct phase multiplication rather than as a
reversible circuit with a scratch qubit. Phase kickback is assumed, not
demonstrated: see the note at the bottom.
"""

import numpy as np

# --- gates -------------------------------------------------------------

H = np.array([[1, 1], [1, -1]], dtype=complex) / np.sqrt(2)
X = np.array([[0, 1], [1, 0]], dtype=complex)
Z = np.array([[1, 0], [0, -1]], dtype=complex)
I = np.eye(2, dtype=complex)


# --- simulator core ----------------------------------------------------

def zero_state(k):
    """|00...0>: 2**k amplitudes, all zero except the all-zeros basis state."""
    psi = np.zeros((2,) * k, dtype=complex)   # (2,) * k is tuple repetition
    psi[(0,) * k] = 1.0                       # (0,) * k indexes psi[0, 0, ..., 0]
    return psi


def apply_gate(psi, gate, target):
    """Apply a 2x2 gate to one qubit, leaving the others untouched.

    Contract the gate's column index against axis `target`. tensordot puts the
    surviving gate axis at position 0, so moveaxis rotates it back to `target`
    and axis j means qubit j again. For target 0 the moveaxis is a no-op.
    """
    out = np.tensordot(gate, psi, axes=([1], [target]))
    return np.moveaxis(out, 0, target)


def probabilities(psi):
    """Measurement probabilities, flattened to ravel order."""
    return np.abs(psi.ravel()) ** 2


def show(psi, label=""):
    """Print the non-negligible amplitudes, labelled by bitstring."""
    k = psi.ndim
    print(label)
    for i, amp in enumerate(psi.ravel()):
        if abs(amp) > 1e-9:                   # not == 0: floats leave residue
            # index i in ravel order IS the bitstring, zero-padded to width k
            print(f"  |{i:0{k}b}>  amp {amp.real:+.3f}   prob {abs(amp)**2:.3f}")
    print()


# --- oracles -----------------------------------------------------------

def phase_oracle(f):
    """Build an oracle.

    f is a length-2**k array of 0/1 in ravel order. The oracle multiplies
    amplitude x by (-1)**f(x), which is elementwise multiplication by a
    vector of signs.
    """
    signs = (-1.0) ** np.asarray(f)

    def oracle(psi):
        return psi * signs.reshape(psi.shape)

    return oracle


def constant_f(k, value=0):
    """f(x) = value for every x. Balanced count 2**k of one output."""
    return np.full(2 ** k, value, dtype=int)


def balanced_f(k, rng=None):
    """A random balanced f: exactly half the inputs map to 1."""
    rng = np.random.default_rng(rng)
    f = np.array([0] * (2 ** (k - 1)) + [1] * (2 ** (k - 1)))
    rng.shuffle(f)
    return f


# --- the algorithm -----------------------------------------------------

def deutsch_jozsa(k, oracle):
    """H on every qubit, one oracle call, H on every qubit."""
    psi = zero_state(k)
    for q in range(k):
        psi = apply_gate(psi, H, q)
    psi = oracle(psi)
    for q in range(k):
        psi = apply_gate(psi, H, q)
    return psi


def verdict(psi):
    """All amplitude on |00...0> means constant; anything else means balanced.

    The interference is exact, so this is a decision, not an estimate.
    """
    p_all_zero = probabilities(psi)[0]
    return "constant" if p_all_zero > 1 - 1e-9 else "balanced"


# --- examples ----------------------------------------------------------

if __name__ == "__main__":

    for k in (2, 3):
        print(f"===== k = {k} =====\n")

        f = constant_f(k, value=0)
        psi = deutsch_jozsa(k, phase_oracle(f))
        show(psi, f"constant   f = {''.join(map(str, f))}   ->  {verdict(psi)}")

        f = balanced_f(k, rng=0)
        psi = deutsch_jozsa(k, phase_oracle(f))
        show(psi, f"balanced   f = {''.join(map(str, f))}   ->  {verdict(psi)}")

    # Sanity check: the structured balanced oracle, f(x) = x_0,
    # is just a Z on qubit 0. Same verdict, but a linear function.
    psi = deutsch_jozsa(2, lambda p: apply_gate(p, Z, 0))
    show(psi, f"balanced, linear (Z on q0)   ->  {verdict(psi)}")