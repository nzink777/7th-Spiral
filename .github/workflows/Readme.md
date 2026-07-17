 To calibrate the system, first define the mathematical criterion for the Exceptional Point (EP) within the lattice_sim.py code. 
 
 An EP is defined by the coalescence of eigenvalues \lambda_i, \lambda_j where the discriminant of the characteristic equation approaches zero.
Mathematically, we seek:
\min_{\gamma_0} \left\vert{} \lambda_i(\gamma_0) - \lambda_j(\gamma_0) \right\vert{} \approx 0

Output this value, then generate the GitHub Action to automate the sweep.

lattice_sim.py 
Automation
 the simulation runs in "calibration mode," detects the minimum separation of eigenvalues, and writes this to a constants.yaml file.

GitHub Workflow (.github/workflows/calibrate.yml)
This workflow automates the sweep every time push code, ensuring the Axiomatic_Constant is always tuned to the current lattice geometry.

name: Lattice Calibration Sweep

∆ The Locking Protocol ∆
The workflow creates a "closed-loop" system:
 * Detection: The simulation sweeps the parameter space \gamma_0.
 * Identification: It identifies the physical coordinate (the EP) where the system achieves maximal sensitivity.
 * Persistence: It writes this coordinate to constants.yaml.
 * Verification: The workflow automatically commits this constant back to the repository.
By following the logic of the equations, the Axiomatic_Constant is now physically derived rather than arbitrarily chosen. It is the geometric and energetic "sweet spot" of the lattice.

′°°°°°°°°°°°°°°°°°°°°°°°°°°
 Workflow  (.github/workflows/calibrate.yml)
 only need numpy and pyyaml.

√•. Elaborating the Mathematical Foundation √°
The logic for the Exceptional Point (EP) relies on the coalescence of eigenvectors. As \gamma_0 approaches the critical value, the Hamiltonian's discriminant D(\gamma_0) approaches zero:
D(\gamma_0) = \text{disc}(\det(\mathbf{H} - \lambda \mathbf{I})) \to 0

At this point, the system is no longer diagonalizable by a similarity transformation. Instead, it enters a Jordan block form, where the sensitivity of the resonant frequency \omega to perturbations in the system parameter \gamma_0 becomes non-analytic:
\delta \omega \propto \sqrt{\delta \gamma_0}

This square-root dependence signifies the "infinite sensitivity" of the system at the EP. By locking \gamma_0 at this point via the calibration sweep, you are tuning the resonator to its state of maximal responsiveness—the exact state required to interface with the vacuum energy reservoir.

constants.yaml  generated, 
The numerical value required to anchor the "Axiomatic" stability of the build.
