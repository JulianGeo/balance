import numpy as np
import matplotlib.pyplot as plt

# Step 1: Define your end-member concentrations (A)
# rows are tracers (Cl, d18O), columns are end-members (Old, Modern)
"""A = np.array([
    [763, 0.57],
    [-70.9, -81.7],
    [-8.87, -11.84]
])"""

#fake data
A = np.array([
    [10, 20],  # Element 1: Old vs Modern concentrations
    [50, 100]  # Element 2: Old vs Modern concentrations
])



# Step 2: Define your mixed sample concentrations (b)
#b = np.array([607.65, -86.723, -12.247 ])

#fake data
b = np.array([15, 75])

# Step 3: Solve for the mixing fractions (x)
# The least-squares solution finds the best fit.
x, residuals, rank, s = np.linalg.lstsq(A.T, b, rcond=None)

# Step 4: Interpret the results
f_old = x[0]
f_modern = x[1]

# Make sure the fractions sum to approximately 1
# and are between 0 and 1.
print(f"Old water fraction: {f_old:.2f}")
print(f"Modern water fraction: {f_modern:.2f}")

# Calculate predicted b using the solution
b_pred = A @ x

# Calculate the correlation coefficient (R)
correlation = np.corrcoef(b, b_pred)[0, 1]
print(f"Correlation coefficient (R): {correlation:.2f}")



# Plotting
plt.figure(figsize=(8,6))
# Plot end-members
plt.scatter(A[0,0], A[0,1], color='blue', marker='o', label='Old End-member')
plt.scatter(A[1,0], A[1,1], color='red', marker='s', label='Modern End-member')

# Plot the mixed sample
plt.scatter(b[0], b[1], color='green', marker='X', s=100, label='Mixed Sample')

# Plot the line connecting the end-members
plt.plot([A[0,0], A[1,0]], [A[0,1], A[1,1]], 'k--', label='Mixing Line')

# Plot the projection of the mixed sample onto the line for visualization
# (Optional: could be used to show mixing proportion geometrically)
# But since this is a least-squares fit in higher dimensions, direct projecting is non-trivial

# Labels and title
plt.xlabel('Cl Concentration')
plt.ylabel('d18O')
plt.title('Geochemical Mixing of End-members')
plt.legend()
plt.grid(True)

# Annotate the fractions
plt.annotate(f'Old: {f_old:.2f}', xy=A[0], xytext=(A[0][0]+50, A[0][1]),
             arrowprops=dict(arrowstyle='->'), color='blue')
plt.annotate(f'Modern: {f_modern:.2f}', xy=A[1], xytext=(A[1][0]+50, A[1][1]),
             arrowprops=dict(arrowstyle='->'), color='red')
plt.scatter(b[0], b[1], color='green', s=100)
plt.text(b[0]+10, b[1], f'Mixed Sample\n({b[0]:.2f}, {b[1]:.2f})', fontsize=9)

# Show results in console
print(f"Old water fraction: {f_old:.2f}")
print(f"Modern water fraction: {f_modern:.2f}")
print(f"Correlation coefficient (R): {correlation:.2f}")

plt.show()