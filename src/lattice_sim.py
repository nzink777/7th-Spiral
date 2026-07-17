import numpy as np

class LatticeSim:
    def __init__(self, num_sectors=64, scaling_factor=1.0):
        self.N = num_sectors
        self.A = scaling_factor
        self.phi = np.deg2rad(137.5) # Golden angle
        
        # Geometry initialization
        self.r = self.A * np.sqrt(np.arange(1, self.N + 1) / self.N)
        self.theta = self.phi * np.arange(1, self.N + 1)
        
        # State vector (Probability amplitudes)
        self.psi = np.ones(self.N, dtype=complex) / np.sqrt(self.N)
        
        self.H = np.zeros((self.N, self.N), dtype=complex)
        
    def build_hamiltonian(self, T0=1.0, gamma0=0.5, localization_xi=0.1):
        """
        Constructs the non-Hermitian Hamiltonian: H = T + i*Gamma
        T_nm: Reciprocal hopping (Hermitian)
        i*Gamma_nm: Non-reciprocal bias (Anti-Hermitian)
        """
        for n in range(self.N):
            for m in range(self.N):
                if n == m:
                    continue # On-site energy assumed 0 for simplicity
                
                # Euclidean distance in polar coordinates
                dist = np.sqrt(self.r[n]**2 + self.r[m]**2 - 
                               2 * self.r[n] * self.r[m] * np.cos(self.theta[n] - self.theta[m]))
                
                # 1. Reciprocal Hopping (T_nm)
                T_nm = T0 * np.exp(-dist / localization_xi)
                
                # 2. Non-Reciprocal Bias (i*Gamma_nm)
                # Chiral flow: n -> n+1
                gamma_nm = gamma0 if (m == n + 1) else (-gamma0 if (m == n - 1) else 0)
                
                # Assemble J_nm
                self.H[n, m] = T_nm + (1j * gamma_nm)
        
        return self.H

    def evolve(self, dt):
        """
        Time evolution using the non-Hermitian Hamiltonian
        d(psi)/dt = -i * H * psi
        """
        evolution_op = np.exp(-1j * self.H * dt)
        self.psi = np.dot(evolution_op, self.psi)
        return self.psi

# Verification
if __name__ == "__main__":
    sim = LatticeSim()
    sim.build_hamiltonian()
    print(f"Hamiltonian shape: {sim.H.shape}")
    print(f"Non-Hermitian component check (H - H.conj.T):")
    print(np.sum(np.abs(sim.H - sim.H.conj().T))) # Should be non-zero due to i*Gamma
