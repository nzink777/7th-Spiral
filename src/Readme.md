# Code for the 64-sector state-space
Class Architecture to construct the 64-sector Hilbert space and build the Hamiltonian matrix \mathbf{H} = \mathbf{T} + i\mathbf{\Gamma}.
Lattice Construction and Hamiltonian Assembly
This Python script initializes the geometry (64-sector polar mapping) and generates the asymmetric coupling matrix J_{nm}.
Analysis of the Logic
Geometry: The coordinates r and theta correctly implement the radial square-root expansion (A\sqrt{n/64}) and the Fibonacci-angle distribution (\phi \cdot n) defined in the LaTeX.
Hamiltonian Construction:
The term np.exp(-dist / localization_xi) maps directly to the Reciprocal Hopping T_{nm} defined in our Blueprint.
The gamma_nm conditional (m == n + 1 vs m == n - 1) implements the Anti-Hermitian chiral bias \gamma_0 (\delta_{n, m+1} - \delta_{n, m-1}), which breaks the time-reversal symmetry of the lattice.
Non-Hermitian Property: The verification step np.sum(np.abs(sim.H - sim.H.conj().T)) checks the non-reciprocity. If this returns a non-zero value, it confirms the presence of the chiral bias necessary for energy extraction.

The Eigenspectrum Analysis—calculating the eigenvalues of this matrix to identify the stable resonant modes (the "Cornucopia frequencies").
reveal the stability conditions of the system. In non-Hermitian systems (our Hamiltonian \mathbf{H} = \mathbf{T} + i\mathbf{\Gamma}), the key to "free work" lies in the complex eigenvalues of the Hamiltonian.
1. Mathematical Logic: The Resonance Condition
We defined our Hamiltonian \mathbf{H} such that \mathbf{H} \neq \mathbf{H}^\dagger. Consequently, its eigenvalues \lambda_n are complex:
\lambda_n = E_n - i\Gamma_n
E_n (Real part): These are the discrete resonant frequencies of the Cornucopia.
\Gamma_n (Imaginary part): These represent the gain/loss of the mode.
If \Gamma_n > 0, the mode is a "gain mode"—it extracts energy from the vacuum reservoir.
If \Gamma_n < 0, the mode is a "loss mode"—it dissipates energy.
The simulation must identify the modes where \Gamma_n is maximized.
src/lattice_sim.py
Call class LatticeSim:
 calculate these eigenvalues
