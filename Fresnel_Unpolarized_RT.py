import numpy as np
import matplotlib.pyplot as plt

# Fresnel relations for unpolarized light at an air-glass interface

# Refractive indices
n1 = 1.00       # air
n2 = 1.50       # glass

# Angle of incidence
theta_i = np.linspace(0, 89.9, 2000)
theta_i_rad = np.radians(theta_i)

# Snell's law
sin_theta_t = (n1 / n2) * np.sin(theta_i_rad)
theta_t_rad = np.arcsin(sin_theta_t)

# Fresnel amplitude reflection coefficients
rs = (
    (n1 * np.cos(theta_i_rad) - n2 * np.cos(theta_t_rad))
    / (n1 * np.cos(theta_i_rad) + n2 * np.cos(theta_t_rad))
)

rp = (
    (n2 * np.cos(theta_i_rad) - n1 * np.cos(theta_t_rad))
    / (n2 * np.cos(theta_i_rad) + n1 * np.cos(theta_t_rad))
)

# Reflectances
Rs = np.abs(rs)**2
Rp = np.abs(rp)**2

# Fresnel transmission coefficients
ts = (
    2 * n1 * np.cos(theta_i_rad)
    / (n1 * np.cos(theta_i_rad) + n2 * np.cos(theta_t_rad))
)

tp = (
    2 * n1 * np.cos(theta_i_rad)
    / (n2 * np.cos(theta_i_rad) + n1 * np.cos(theta_t_rad))
)

# Transmittances
Ts = (
    (n2 * np.cos(theta_t_rad))
    / (n1 * np.cos(theta_i_rad))
) * np.abs(ts)**2

Tp = (
    (n2 * np.cos(theta_t_rad))
    / (n1 * np.cos(theta_i_rad))
) * np.abs(tp)**2


# Unpolarized light
R = (Rs + Rp) / 2
T = (Ts + Tp) / 2


# Brewster angle
theta_B = np.degrees(np.arctan(n2 / n1))

# Reflectance at normal incidence
R_normal = ((n1 - n2) / (n1 + n2))**2


# Plotting
plt.figure(figsize=(8, 5.5))

plt.plot(
    theta_i,
    R,
    linewidth=2,
    label=r"Reflectance $R_{\rm unpol}$"
)

plt.plot(
    theta_i,
    T,
    linewidth=2,
    label=r"Transmittance $T_{\rm unpol}$"
)

# Brewster angle
plt.axvline(
    theta_B,
    linestyle="--",
    linewidth=1.5,
    label=fr"Brewster angle $\theta_B={theta_B:.1f}^\circ$"
)

# Normal-incidence reflectance
#plt.scatter(
#    [0],
#    [R_normal],
#    zorder=5
#)

#plt.annotate(
#    fr"$R(0^\circ)={R_normal:.2f}$",
#    xy=(0, R_normal),
#    xytext=(7, R_normal + 0.08),
#    arrowprops=dict(arrowstyle="->"),
#)

# Labelling
plt.xlabel(r"Angle of incidence $\theta_i$ (degrees)")
plt.ylabel("Intensity fraction")

plt.title(
    "Reflectance and Transmittance of Unpolarized Light\n"
    "at an Air–Glass Interface"
)

plt.xlim(0, 90)
plt.ylim(0, 1.05)

plt.grid(True, alpha=0.3)
plt.legend()

plt.tight_layout()

plt.show()
