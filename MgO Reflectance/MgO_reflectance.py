import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Constants
hbar = 6.5821196e-16       # eV s

# Read the experimental optical constants of MgO
# Columns: E_eV, n, k
data = pd.read_csv("MgO_optical_constants.csv")

E = data["E_eV"].to_numpy()
n = data["n"].to_numpy()
k = data["k"].to_numpy()

# Convert photon energy to angular frequency:
# E = hbar * omega
omega = E / hbar

# Normal-incidence Fresnel reflectance from vacuum:
# R = |(n_tilde - 1)/(n_tilde + 1)|^2
# n_tilde = n + i k
R = ((n - 1)**2 + k**2) / ((n + 1)**2 + k**2)

# Plot angular frequency in units of 10^15 rad/s
omega_15 = omega / 1e15
R_percent = 100 * R

plt.figure(figsize=(8, 5.5))
plt.plot(omega_15, R_percent, "o-", markersize=3, linewidth=1.2)

plt.xlabel(r"Angular frequency $\omega$ ($10^{15}\,\mathrm{rad\,s^{-1}}$)")
plt.ylabel(r"Reflectance $R$ (\%)")
plt.title("Normal-incidence reflectance of MgO")

plt.xlim(left=0)
plt.ylim(bottom=0)
plt.grid(True, alpha=0.3)
plt.tight_layout()

plt.savefig("MgO_reflectance.png", dpi=300, bbox_inches="tight")
plt.show()
