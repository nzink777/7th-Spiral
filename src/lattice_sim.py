import numpy as np

class LatticeSim:
    def __init__(self, num_sectors=64, A=1.0):
        self.N = num_sectors
        self.A = A
        self.phi = np.deg2rad(137.5) # Golden Angle
        
        # Initialize geometry
        self.r = self.A * np.sqrt(np.arange(1, self.N + 1) / self.N)
        self.theta = self.phi * np.arange(1, self.N + 1)
        self.H = np.zeros((self.N, self.N), dtype=complex)
        self.psi = np.ones(self.N, dtype=complex) / np.sqrt(self.N)
        
    def build_hamiltonian(self, T0=1.0, gamma0=0.5, localization_xi=0.1):
        """Constructs the non-Hermitian Hamiltonian H = T + i*Gamma."""
        for n in range(self.N):
            for m in range(self.N):
                if n == m: continue
                
                # Spatial coupling metric
                dist = np.sqrt(self.r[n]**2 + self.r[m]**2 - 
                               2 * self.r[n] * self.r[m] * np.cos(self.theta[n] - self.theta[m]))
                
                # 1. Reciprocal Hopping (T_nm)
                T_nm = T0 * np.exp(-dist / localization_xi)
                
                # 2. Non-Reciprocal Bias (i*Gamma_nm)
                # Chiral flow: n -> n+1
                gamma_nm = gamma0 if (m == n + 1) else (-gamma0 if (m == n - 1) else 0)
                
                self.H[n, m] = T_nm + (1j * gamma_nm)
        return self.H

    def solve_modes(self):
        """Calculates complex eigenvalues to find gain/loss modes."""
        return np.linalg.eigvals(self.H)

    def evolve(self, dt):
        """Time evolution: psi(t+dt) = exp(-iHt) psi(t)"""
        evolution_op = np.linalg.matrix_power(np.exp(-1j * self.H * dt), 1)
        self.psi = np.dot(evolution_op, self.psi)
        return self.psi

# Verification
if __name__ == "__main__":
    sim = LatticeSim()
    sim.build_hamiltonian()
    modes = sim.solve_modes()
    
    # Identify the highest gain mode (Imaginary part)
    max_gain_idx = np.argmax(modes.imag)
    print(f"Primary Resonance Mode (Real): {modes[max_gain_idx].real:.4f}")
    print(f"Energy Extraction Potential (Imag): {modes[max_gain_idx].imag:.4f}")
    print(f"Non-Hermitian check (Sum abs diff): {np.sum(np.abs(sim.H - sim.H.conj().T)):.4f}")
    
