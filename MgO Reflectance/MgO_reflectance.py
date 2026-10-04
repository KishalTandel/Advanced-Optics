import pandas as pd
import matplotlib.pyplot as plt

# Read the data from the CSV file
csv_file = 'MgO_optical_constants.csv'
df = pd.read_csv(csv_file)

# Plot reflectance versus angular frequency
plt.figure(figsize=(8.5, 5.5))

plt.plot(
    df['omega_1e15_rad_s'],
    df['R_percent'],
    marker='o',
    linewidth=1.4,
    markersize=3.5
)

plt.xlabel(r'Angular frequency, $\omega$ ($10^{15}$ rad s$^{-1}$)')
plt.ylabel('Reflectance, R (%)')
plt.title('Single-crystal MgO: normal-incidence reflectance')

plt.grid(True, alpha=0.25)
plt.tight_layout()

# Save the figure
#plt.savefig(
#    'MgO_reflectance_Roessler_Walker.png',
#    dpi=300,
#    bbox_inches='tight'
#)

plt.show()
