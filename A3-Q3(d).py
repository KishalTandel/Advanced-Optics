import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks


# ---------------------------------------------------------
# Given parameters
# ---------------------------------------------------------
w0 = 6.4e14                  # resonance frequency (rad/s)
gamma = 0.28 * w0            # damping factor (rad/s)
wp = 7.8e16                  # plasma frequency (rad/s)

c = 3.00e8                   # speed of light (m/s)


# ---------------------------------------------------------
# Frequency range
# ---------------------------------------------------------
# Logarithmic scale, same range as the n-kappa plot
x = np.logspace(np.log10(0.01), np.log10(1e4), 100000)
w = x * w0


# ---------------------------------------------------------
# Complex permittivity
# epsilon = epsilon_r + i epsilon_i
# ---------------------------------------------------------
den = (w0**2 - w**2)**2 + (gamma*w)**2

eps_r = 1 + wp**2 * (w0**2 - w**2) / den
eps_i = wp**2 * gamma * w / den


# ---------------------------------------------------------
# Complex refractive index
# epsilon = (n + i*kappa)^2
# ---------------------------------------------------------
abs_eps = np.sqrt(eps_r**2 + eps_i**2)

n = np.sqrt((abs_eps + eps_r) / 2)

# Numerically stable expression for kappa:
# eps_i = 2*n*kappa
kappa = eps_i / (2*n)


# ---------------------------------------------------------
# Reflectivity and interface transmittance
# ---------------------------------------------------------
R = ((n - 1)**2 + kappa**2) / ((n + 1)**2 + kappa**2)

T = 4*n / ((n + 1)**2 + kappa**2)


# ---------------------------------------------------------
# Effectively absorption-free region
# ---------------------------------------------------------
# Absorption coefficient:
# alpha = 2*omega*kappa/c
#
# At sufficiently high frequency kappa -> 0,
# so absorption becomes negligible.
#
# Numerical criterion used only to identify the
# effectively absorption-free region for plotting.

kappa_threshold = 1e-3

absorption_free = kappa < kappa_threshold

# Plot T only in the absorption-free region
T_plot = T.copy()
T_plot[~absorption_free] = np.nan


# ---------------------------------------------------------
# Find boundaries of absorption-free region
# kappa = threshold
# ---------------------------------------------------------
difference = kappa - kappa_threshold

crossings = np.where(
    np.diff(np.sign(difference)) != 0
)[0]


print("\nBoundaries of effectively absorption-free region:")

for i in crossings:

    x1, x2 = x[i], x[i+1]
    y1, y2 = difference[i], difference[i+1]

    xb = x1 - y1 * (x2 - x1) / (y2 - y1)
    wb = xb * w0

    print(
        f"omega/omega0 = {xb:.6f}, "
        f"omega = {wb:.6e} rad/s"
    )


# ---------------------------------------------------------
# Plot
# ---------------------------------------------------------
plt.figure(figsize=(10, 6))

# Reflectivity everywhere
plt.plot(
    x, R,
    label='Reflectivity $R$',
    linewidth=2
)

# Transmittance only in absorption-free region
plt.plot(
    x, T_plot,
    label='Transmittance $T$',
    linewidth=2
)


# Shade absorbing region
plt.fill_between(
    x,
    0,
    1,
    where=~absorption_free,
    alpha=0.20,
    label=r'Absorbing region ($\kappa$ not negligible)'
)


# Resonance frequency
plt.axvline(
    1,
    linestyle='--',
    linewidth=1.5,
    label=r'Resonance $\omega_0$'
)


# Boundary of absorption-free region
#for i in crossings:

#    x1, x2 = x[i], x[i+1]
#    y1, y2 = difference[i], difference[i+1]

#    xb = x1 - y1 * (x2 - x1) / (y2 - y1)

#    plt.axvline(
#        xb,
#        linestyle=':',
#        linewidth=1.2
#    )


# Labels
plt.xlabel(r'Normalized frequency $\omega/\omega_0$')
plt.ylabel(r'$R,\ T$')
plt.title('Reflectivity and Transmittance')

plt.xscale('log')
plt.xlim(0.01, 1e4)
plt.ylim(0, 1.05)

plt.grid(True, which='both', alpha=0.3)
plt.legend()

plt.tight_layout()
plt.show()
