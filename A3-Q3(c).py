import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks


# Given parameters
w0 = 6.4e14                  # resonance frequency (rad/s)
gamma = 0.28 * w0            # damping factor (rad/s)
wp = 7.8e16                  # plasma frequency (rad/s)

c = 3.00e8                   # speed of light (m/s)


# Frequency range
w = np.logspace(np.log10(0.01*w0), np.log10(1e4*w0), 20000)
x = w / w0


# Complex permittivity
den = (w0**2 - w**2)**2 + (gamma*w)**2

eps_r = 1 + wp**2 * (w0**2 - w**2) / den
eps_i = wp**2 * gamma * w / den


# Refractive index n and extinction coefficient kappa
# epsilon = (n + i*kappa)^2
abs_eps = np.sqrt(eps_r**2 + eps_i**2)

n = np.sqrt((abs_eps + eps_r) / 2)

kappa = np.sqrt((abs_eps - eps_r) / 2)


# Phase velocity
v_phase = c / n


# Finding local maxima and minima of n
max_n, _ = find_peaks(n, prominence=1e-3)
min_n, _ = find_peaks(-n, prominence=1e-3)


# Finding local maxima and minima of kappa
max_k, _ = find_peaks(kappa, prominence=1e-3)
min_k, _ = find_peaks(-kappa, prominence=1e-3)


# Printing extrema

print("\nLOCAL EXTREMA OF n")

for i in max_n:
    print(f"Maximum: omega = {x[i]:.6f} omega_0 "
          f"= {w[i]:.4e} rad/s, "
          f"n = {n[i]:.6f}")

for i in min_n:
    print(f"Minimum: omega = {x[i]:.6f} omega_0 "
          f"= {w[i]:.4e} rad/s, "
          f"n = {n[i]:.6f}")


print("\nLOCAL EXTREMA OF kappa")

for i in max_k:
    print(f"Maximum: omega = {x[i]:.6f} omega_0 "
          f"= {w[i]:.4e} rad/s, "
          f"kappa = {kappa[i]:.6f}")

for i in min_k:
    print(f"Minimum: omega = {x[i]:.6f} omega_0 "
          f"= {w[i]:.4e} rad/s, "
          f"kappa = {kappa[i]:.6f}")


# Plotting n and kappa

plt.figure(figsize=(10, 6))

plt.plot(x, n, label=r'$n$')
plt.plot(x, kappa, label=r'$\kappa$')

# Marking resonance frequency
plt.axvline(
    1,
    linestyle='--',
    label=r'$\omega_0$'
)


# Marking and labelling extrema of n

for i in max_n:
    plt.plot(x[i], n[i], 'o')
    plt.annotate(
        rf'$\omega={x[i]:.3f}\omega_0$',
        xy=(x[i], n[i]),
        xytext=(-70, -3),
        textcoords='offset points'
    )

for i in min_n:
    plt.plot(x[i], n[i], 'o')
    plt.annotate(
        rf'$\omega={x[i]:.3f}\omega_0$',
        xy=(x[i], n[i]),
        xytext=(-20, -15),
        textcoords='offset points'
    )


# Marking and labelling extrema of kappa

for i in max_k:
    plt.plot(x[i], kappa[i], 'o')
    plt.annotate(
        rf'$\omega={x[i]:.3f}\omega_0$',
        xy=(x[i], kappa[i]),
        xytext=(10, -3),
        textcoords='offset points'
    )

for i in min_k:
    plt.plot(x[i], kappa[i], 'o')
    plt.annotate(
        rf'$\omega={x[i]:.3f}\omega_0$',
        xy=(x[i], kappa[i]),
        xytext=(8, -20),
        textcoords='offset points'
    )


# Labels and formatting

plt.xlabel(r'Normalized frequency $\omega/\omega_0$')
plt.ylabel(r'$n,\ \kappa$')

plt.title(
    r'Real Refractive Index $n$ and Extinction Coefficient $\kappa$'
)

plt.xscale('log')
plt.xlim(0.01, 1e4)

plt.grid(True, which='both', alpha=0.3)
plt.legend()

plt.tight_layout()
plt.show()
