import numpy as np
import yaml

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

    def find_exceptional_points(self, gamma_range=np.linspace(0, 2.0, 100)):
        """
        Sweeps gamma_0 to locate Exceptional Points (EPs).
        EPs occur where eigenvalues coalesce.
        """
        eigenvalue_history = []
        for g in gamma_range:
            self.build_hamiltonian(T0=1.0, gamma0=g, localization_xi=0.1)
            eigenvalues = np.linalg.eigvals(self.H)
            eigenvalue_history.append(eigenvalues)
        
        return gamma_range, np.array(eigenvalue_history)

    def calibrate_ep(self):
        """
        Sweeps gamma0 to find the Exceptional Point and writes to constants.yaml.
        Logic: Minimizes the distance between the two eigenvalues with the largest real parts.
        """
        gamma_range = np.linspace(0.1, 2.0, 500)
        min_diff = float('inf')
        optimal_gamma = 0
        
        for g in gamma_range:
            self.build_hamiltonian(T0=1.0, gamma0=g, localization_xi=0.1)
            evals = np.linalg.eigvals(self.H)
            
            # Sort by real part to track the two primary resonant modes
            evals = evals[np.argsort(evals.real)]
            
            # Identify the gap between the two modes closest to coalescence
            gap = np.abs(evals[1] - evals[0])
            
            if gap < min_diff:
                min_diff = gap
                optimal_gamma = g
                
        # Lock the value
        with open("constants.yaml", "w") as f:
            yaml.dump({"Axiomatic_Constant_Gamma0": float(optimal_gamma)}, f)
        
        print(f"Locked Gamma0 at: {optimal_gamma}")

# Verification
if __name__ == "__main__":
    sim = LatticeSim()
    sim.build_hamiltonian()
    modes = sim.solve_modes()
    
    print(f"Primary Resonance Mode (Real): {modes[np.argmax(modes.imag)].real:.4f}")
    print(f"Energy Extraction Potential (Imag): {modes[np.argmax(modes.imag)].imag:.4f}")
    print(f"Non-Hermitian check (Sum abs diff): {np.sum(np.abs(sim.H - sim.H.conj().T)):.4f}")
        
