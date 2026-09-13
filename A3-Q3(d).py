import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks


# Given parameters
w0 = 6.4e14                  # resonance frequency (rad/s)
gamma = 0.28 * w0            # damping factor (rad/s)
wp = 7.8e16                  # plasma frequency (rad/s)


# Frequency range
x = np.linspace(0.01, 3.0, 100000)    # x = omega / omega0
w = x * w0


# Complex permittivity
# epsilon = epsilon_r + i epsilon_i
den = (w0**2 - w**2)**2 + (gamma*w)**2

eps_r = 1 + wp**2 * (w0**2 - w**2) / den
eps_i = wp**2 * gamma * w / den


# Complex refractive index: n + i*kappa
abs_eps = np.sqrt(eps_r**2 + eps_i**2)

n = np.sqrt((abs_eps + eps_r) / 2)
kappa = np.sqrt((abs_eps - eps_r) / 2)


# Reflectivity at vacuum-material interface
R = ((n - 1)**2 + kappa**2) / ((n + 1)**2 + kappa**2)

# Interface transmittance:
# R + T_interface = 1
# (This is NOT transmission through a finite slab.)
T = 4*n / ((n + 1)**2 + kappa**2)


# Absorption-dominated region
# Criterion: kappa > n
absorption_region = kappa > n

# Do not plot T in the absorption-dominated region
T_plot = T.copy()
T_plot[absorption_region] = np.nan


# Finding local maxima/minima of R
max_indices, _ = find_peaks(R)
min_indices, _ = find_peaks(-R)

print("\nLocal maxima of R:")
for i in max_indices:
    print(f"omega/omega0 = {x[i]:.6f}, "
          f"omega = {w[i]:.6e} rad/s, "
          f"R = {R[i]:.6f}")

print("\nLocal minima of R:")
for i in min_indices:
    print(f"omega/omega0 = {x[i]:.6f}, "
          f"omega = {w[i]:.6e} rad/s, "
          f"R = {R[i]:.6f}")


# Finding boundaries of kappa = n
difference = kappa - n
crossings = np.where(np.diff(np.sign(difference)) != 0)[0]

print("\nBoundaries of absorption-dominated region (kappa = n):")

for i in crossings:
    # Linear interpolation for better boundary estimate
    x1, x2 = x[i], x[i+1]
    y1, y2 = difference[i], difference[i+1]

    xb = x1 - y1 * (x2 - x1) / (y2 - y1)
    wb = xb * w0

    print(f"omega/omega0 = {xb:.6f}, "
          f"omega = {wb:.6e} rad/s")


# Plotting
plt.figure(figsize=(10, 6))

plt.plot(x, R, label='Reflectivity R', linewidth=2)
plt.plot(x, T_plot, label='Transmittance T', linewidth=2)

# Shading absorption-dominated region
plt.fill_between(
    x, 0, 1,
    where=absorption_region,
    alpha=0.20,
    label=r'Absorption-dominated ($\kappa>n$)'
)

# Marking resonance frequency
plt.axvline(
    1,
    linestyle='--',
    linewidth=1.5,
    label=r'Resonance $\omega_0$'
)

# Marking boundaries
for i in crossings:
    x1, x2 = x[i], x[i+1]
    y1, y2 = difference[i], difference[i+1]

    xb = x1 - y1 * (x2 - x1) / (y2 - y1)

    plt.axvline(
        xb,
        linestyle=':',
        linewidth=1.2
    )


# Labels and formatting
plt.xlabel(r'Normalized frequency $\omega/\omega_0$')
plt.ylabel(r'$R, T$')
plt.title('Reflectivity and Transmittance')

plt.xlim(0, 3)
plt.ylim(0, 1.05)

plt.grid(True, alpha=0.3)
plt.legend()
plt.tight_layout()

plt.show()
