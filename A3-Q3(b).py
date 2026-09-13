import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks

# Given parameters
w0 = 6.4e14                  # resonance frequency (rad/s)
gamma = 0.28 * w0            # damping factor (rad/s)
wp = 7.8e16                  # plasma frequency (rad/s)


# Frequency range
# Logarithmic scale
w = np.logspace(np.log10(0.01*w0), np.log10(1e4*w0), 20000)


# Complex permittivity
# epsilon = epsilon_r + i epsilon_i
den = (w0**2 - w**2)**2 + (gamma*w)**2

eps_r = 1 + wp**2 * (w0**2 - w**2) / den
eps_i = wp**2 * gamma * w / den

# Normalized frequency
x = w / w0


# Finding local maxima and minima

# epsilon_r
max_r, _ = find_peaks(eps_r)
min_r, _ = find_peaks(-eps_r)

# epsilon_i
max_i, _ = find_peaks(eps_i)
min_i, _ = find_peaks(-eps_i)


# Printing extrema

print("\nLOCAL EXTREMA OF epsilon_r")

for i in max_r:
    print(f"Maximum: omega = {x[i]:.6f} omega_0 "
          f"= {w[i]:.4e} rad/s, "
          f"epsilon_r = {eps_r[i]:.6f}")

for i in min_r:
    print(f"Minimum: omega = {x[i]:.6f} omega_0 "
          f"= {w[i]:.4e} rad/s, "
          f"epsilon_r = {eps_r[i]:.6f}")


print("\nLOCAL EXTREMA OF epsilon_i")

for i in max_i:
    print(f"Maximum: omega = {x[i]:.6f} omega_0 "
          f"= {w[i]:.4e} rad/s, "
          f"epsilon_i = {eps_i[i]:.6f}")

for i in min_i:
    print(f"Minimum: omega = {x[i]:.6f} omega_0 "
          f"= {w[i]:.4e} rad/s, "
          f"epsilon_i = {eps_i[i]:.6f}")


# Plotting

plt.figure(figsize=(10, 6))

plt.plot(x, eps_r, label=r'$\epsilon_r$')
plt.plot(x, eps_i, label=r'$\epsilon_i$')

# Mark resonance frequency omega_0
plt.axvline(
    1,
    linestyle='--',
    label=r'$\omega_0$'
)


# Marking and labelling extrema of epsilon_r

for i in max_r:
    plt.plot(x[i], eps_r[i], 'o')
    plt.annotate(
        rf'$\omega={x[i]:.3f}\omega_0$',
        xy=(x[i], eps_r[i]),
        xytext=(-70, -3),
        textcoords='offset points'
    )

for i in min_r:
    plt.plot(x[i], eps_r[i], 'o')
    plt.annotate(
        rf'$\omega={x[i]:.3f}\omega_0$',
        xy=(x[i], eps_r[i]),
        xytext=(10, -3),
        textcoords='offset points'
    )


# Marking and labelling extrema of epsilon_i

for i in max_i:
    plt.plot(x[i], eps_i[i], 'o')
    plt.annotate(
        rf'$\omega={x[i]:.3f}\omega_0$',
        xy=(x[i], eps_i[i]),
        xytext=(-70, -3),
        textcoords='offset points'
    )

for i in min_i:
    plt.plot(x[i], eps_i[i], 'o')
    plt.annotate(
        rf'$\omega={x[i]:.3f}\omega_0$',
        xy=(x[i], eps_i[i]),
        xytext=(0, 0),
        textcoords='offset points'
    )


# Labels and formatting

plt.xlabel(r'Normalized frequency $\omega/\omega_0$')
plt.ylabel(r'$\epsilon_r\text{ , } \epsilon_i$')
plt.title(
    r'Real and Imaginary Parts of Complex Permittivity'
)

plt.xscale('log')
plt.xlim(0.01, 1e4)

plt.grid(True, which='both', alpha=0.3)
plt.legend()

plt.tight_layout()
plt.show()
