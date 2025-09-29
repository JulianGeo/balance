import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# End-member concentrations (Cl, Li, B)
"""A = np.array([
    [744, 1.19, 7.47],   # Old
    [1.42, 0.01, 0.04]  # Modern
])"""

#Fake data
A = np.array([
    [20, 100, 200],   # Old
    [10, 50, 100]  # Modern
])

# Mixed sample concentrations
#b = np.array([602, 0.63, 7.182]) #Real
#b = np.array([400, 0.6, 4 ]) #Hypothetical

#Fake data
b = np.array([15, 75, 150 ]) 

# Solve for mixing fractions
x, residuals, rank, s = np.linalg.lstsq(A.T, b, rcond=None)
f_old = x[0]
f_modern = x[1]

# Predicted concentrations
b_pred = A.T @ x

# Compute correlation coefficient
correlation = np.corrcoef(b, b_pred)[0, 1]

# 3D Plot
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

# Plot end-members
ax.scatter(A[0,0], A[0,1], A[0,2], color='blue', s=50, label='Old End-member')
ax.scatter(A[1,0], A[1,1], A[1,2], color='red', s=50, label='Modern End-member')

# Plot mixed sample
ax.scatter(b[0], b[1], b[2], color='green', s=100, label='Mixed Sample')

# Draw line between the end-members
ax.plot([A[0,0], A[1,0]],
        [A[0,1], A[1,1]],
        [A[0,2], A[1,2]],
        color='black', linestyle='--', label='Mixing Line')

# Set labels
ax.set_xlabel('Cl Concentration')
ax.set_ylabel('Li Concentration')
ax.set_zlabel('B Concentration')
ax.set_title('Geochemical Mixing in 3D Space')
ax.legend()

# Annotate fractions
ax.text(A[0,0], A[0,1], A[0,2], f'Old ({f_old:.2f})', color='blue')
ax.text(A[1,0], A[1,1], A[1,2], f'Modern ({f_modern:.2f})', color='red')
ax.text(b[0], b[1], b[2], f'Mixed', color='green', fontsize=9)

# Show plot
plt.show()

# Print results
print(f"Old water fraction: {f_old:.2f}")
print(f"Modern water fraction: {f_modern:.2f}")
print(f"Correlation coefficient (R): {correlation:.2f}")
