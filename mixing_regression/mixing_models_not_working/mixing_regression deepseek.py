import numpy as np
from typing import Tuple, Dict, Optional, Union

# TODO: entender el método bien
# TODO: ojo clave normalizar la data porque altos valores como el Cl opacan mucho los bajos


class NumpyMixingModel:
    """
    A robust two-end-member mixing model using numpy for geochemical calculations.
    """

    def __init__(self, end_member1: Dict[str, float], end_member2: Dict[str, float]):
        """
        Initialize with two end-members.

        Parameters:
        -----------
        end_member1: dict with element names as keys and concentrations as values
        end_member2: dict with element names as keys and concentrations as values
        """
        self.end_member1 = end_member1
        self.end_member2 = end_member2
        self.elements = list(end_member1.keys())

        # Verify both end-members have the same elements
        if set(end_member1.keys()) != set(end_member2.keys()):
            raise ValueError("End-members must have the same elements")

        # Convert to numpy arrays for efficient computation
        self.C1 = np.array([end_member1[elem] for elem in self.elements])
        self.C2 = np.array([end_member2[elem] for elem in self.elements])

        # Calculate concentration differences
        self.delta_C = self.C1 - self.C2

    def calculate_mixing_fraction(
        self, mixed_sample: Dict[str, float], element1: str, element2: str
    ) -> Tuple[float, float]:
        """
        Calculate mixing fraction using two specific elements.

        Parameters:
        -----------
        mixed_sample: dict with concentrations of the mixed sample
        element1: first element to use for calculation
        element2: second element to use for calculation

        Returns:
        --------
        tuple: (fraction from end_member1, fraction from end_member2)
        """
        # Get indices of the selected elements
        idx1 = self.elements.index(element1)
        idx2 = self.elements.index(element2)

        # Create the coefficient matrix
        A = np.array([[1, 1], [self.C1[idx1], self.C2[idx1]]])

        # Create the right-hand side vector
        Cm = np.array([mixed_sample[element1], mixed_sample[element2]])
        b = np.array([1, Cm[0]])  # f1 + f2 = 1, f1*C1 + f2*C2 = Cm

        try:
            # Solve using numpy's linear algebra solver
            f1, f2 = np.linalg.solve(A, b)
            return f1, f2
        except np.linalg.LinAlgError:
            raise ValueError(
                f"Cannot solve mixing model for elements {element1}-{element2}"
            )

    def calculate_optimal_mix(
        self, mixed_sample: Dict[str, float]
    ) -> Tuple[float, float, dict]:
        """
        Calculate optimal mixing fraction using all available elements with error minimization.

        Parameters:
        -----------
        mixed_sample: dict with concentrations of the mixed sample

        Returns:
        --------
        tuple: (optimal f1, optimal f2, statistics)
        """
        # Convert mixed sample to numpy array
        Cm = np.array([mixed_sample[elem] for elem in self.elements])

        # Use least squares approach: minimize sum of squared errors
        # Equation: f1 * (C1 - C2) = Cm - C2
        # Rearranged: f1 * delta_C = Cm - C2

        delta_Cm = Cm - self.C2

        # Solve using least squares: f1 = (delta_C · delta_Cm) / (delta_C · delta_C)
        numerator = np.dot(self.delta_C, delta_Cm)
        denominator = np.dot(self.delta_C, self.delta_C)

        if abs(denominator) < 1e-12:
            raise ValueError("End-members are too similar - cannot calculate mixing")

        f1_optimal = numerator / denominator
        f2_optimal = 1 - f1_optimal

        # Calculate statistics
        predicted_Cm = f1_optimal * self.C1 + f2_optimal * self.C2
        residuals = Cm - predicted_Cm
        rmse = np.sqrt(np.mean(residuals**2))
        r_squared = 1 - np.sum(residuals**2) / np.sum((Cm - np.mean(Cm)) ** 2)

        stats = {
            "rmse": rmse,
            "r_squared": r_squared,
            "residuals": dict(zip(self.elements, residuals)),
            "predicted": dict(zip(self.elements, predicted_Cm)),
        }

        return f1_optimal, f2_optimal, stats

    def calculate_all_pairwise(self, mixed_sample: Dict[str, float]) -> Dict:
        """
        Calculate mixing fractions using all possible element pairs.

        Parameters:
        -----------
        mixed_sample: dict with mixed sample concentrations

        Returns:
        --------
        dict: results for each element pair with statistics
        """
        results = {}

        for i in range(len(self.elements)):
            for j in range(i + 1, len(self.elements)):
                elem1, elem2 = self.elements[i], self.elements[j]
                pair_key = f"{elem1}-{elem2}"

                try:
                    f1, f2 = self.calculate_mixing_fraction(mixed_sample, elem1, elem2)

                    # Calculate error for this pair
                    predicted_Cm = f1 * self.C1 + f2 * self.C2
                    actual_Cm = np.array([mixed_sample[e] for e in self.elements])
                    error = np.sqrt(np.mean((actual_Cm - predicted_Cm) ** 2))

                    results[pair_key] = {
                        "fraction_end_member1": f1,
                        "fraction_end_member2": f2,
                        "rmse": error,
                        "elements_used": (elem1, elem2),
                    }

                except (ValueError, np.linalg.LinAlgError) as e:
                    results[pair_key] = {
                        "error": str(e),
                        "elements_used": (elem1, elem2),
                    }

        return results

    def sensitivity_analysis(
        self,
        mixed_sample: Dict[str, float],
        noise_level: float = 0.01,
        n_iterations: int = 1000,
    ) -> Dict:
        """
        Perform Monte Carlo sensitivity analysis with added noise.

        Parameters:
        -----------
        mixed_sample: dict with mixed sample concentrations
        noise_level: relative noise level (default: 1%)
        n_iterations: number of Monte Carlo iterations

        Returns:
        --------
        dict: sensitivity analysis results
        """
        f1_values = []

        for _ in range(n_iterations):
            # Add random noise to mixed sample concentrations
            noisy_sample = {}
            for elem, conc in mixed_sample.items():
                noise = np.random.normal(0, noise_level * conc)
                noisy_sample[elem] = conc + noise

            try:
                f1, f2, _ = self.calculate_optimal_mix(noisy_sample)
                f1_values.append(f1)
            except ValueError:
                continue

        if not f1_values:
            raise ValueError("All sensitivity analysis iterations failed")

        f1_values = np.array(f1_values)

        return {
            "mean_f1": np.mean(f1_values),
            "std_f1": np.std(f1_values),
            "min_f1": np.min(f1_values),
            "max_f1": np.max(f1_values),
            "confidence_95": (
                np.percentile(f1_values, 2.5),
                np.percentile(f1_values, 97.5),
            ),
            "n_successful": len(f1_values),
        }


# Utility functions
def create_mixing_line(
    C1: np.ndarray, C2: np.ndarray, n_points: int = 100
) -> np.ndarray:
    """
    Create a mixing line between two end-members.

    Parameters:
    -----------
    C1: concentrations of end member 1
    C2: concentrations of end member 2
    n_points: number of points along the mixing line

    Returns:
    --------
    array: mixing line points (n_points x n_elements)
    """
    fractions = np.linspace(0, 1, n_points)
    mixing_line = np.outer(fractions, C1) + np.outer(1 - fractions, C2)
    return mixing_line


def calculate_mixing_using_ratios(
    C1_A: float, C1_B: float, C2_A: float, C2_B: float, Cm_A: float, Cm_B: float
) -> Tuple[float, float]:
    """
    Simple function for two-element mixing using numpy.
    """
    # Create matrices
    A = np.array([[1, 1], [C1_A, C2_A]])
    b = np.array([1, Cm_A])

    try:
        f1, f2 = np.linalg.solve(A, b)
        return f1, f2
    except np.linalg.LinAlgError:
        raise ValueError("Cannot solve mixing model - end-members may be too similar")


# Example usage
def example_usage():
    # Define end members
    # seawater = {'Na': 10700, 'Cl': 19350, 'Ca': 411, 'Mg': 1290}
    # freshwater = {'Na': 8, 'Cl': 10, 'Ca': 15, 'Mg': 4}

    seawater = {"Cl": 744, "Li": 1.19, "B": 7.47}
    freshwater = {"Cl": 1.42, "Li": 0.01, "B": 0.04}

    # Create mixing model
    model = NumpyMixingModel(seawater, freshwater)

    # Create a mixed sample (30% seawater, 70% freshwater)
    """mixed_sample = {
        'Na': 10700 * 0.3 + 8 * 0.7,
        'Cl': 19350 * 0.3 + 10 * 0.7,
        'Ca': 411 * 0.3 + 15 * 0.7,
        'Mg': 1290 * 0.3 + 4 * 0.7
    }"""

    # End-member concentrations (Cl, Li, B)
    """A = np.array([
        [744, 1.19, 7.47],   # Old
        [1.42, 0.01, 0.04]  # Modern
    ])"""

    mixed_sample = {
        "Cl": 602,
        "Li": 0.63,
        "B": 7.182,
    }

    print("Mixed sample concentrations:")
    for elem, conc in mixed_sample.items():
        print(f"{elem}: {conc:.1f}")

    # 1. Calculate using specific elements
    print("\n1. Using specific elements (Na-Cl):")
    try:
        f1, f2 = model.calculate_mixing_fraction(mixed_sample, "Na", "Cl")
        print(f"Seawater fraction: {f1:.3f}")
        print(f"Freshwater fraction: {f2:.3f}")
    except ValueError as e:
        print(f"Error: {e}")

    # 2. Optimal mixing using all elements
    print("\n2. Optimal mixing using all elements:")
    f1_opt, f2_opt, stats = model.calculate_optimal_mix(mixed_sample)
    print(f"Optimal seawater fraction: {f1_opt:.3f}")
    print(f"Optimal freshwater fraction: {f2_opt:.3f}")
    print(f"RMSE: {stats['rmse']:.2f}")
    print(f"R²: {stats['r_squared']:.3f}")

    # 3. All pairwise combinations
    print("\n3. All element pair results:")
    pairwise_results = model.calculate_all_pairwise(mixed_sample)
    for pair, result in pairwise_results.items():
        if "error" not in result:
            print(
                f"{pair}: f1 = {result['fraction_end_member1']:.3f} (RMSE: {result['rmse']:.2f})"
            )

    # 4. Sensitivity analysis
    print("\n4. Sensitivity analysis (1% noise):")
    sensitivity = model.sensitivity_analysis(mixed_sample, noise_level=0.01)
    print(f"Mean f1: {sensitivity['mean_f1']:.3f} ± {sensitivity['std_f1']:.3f}")
    print(
        f"95% confidence: [{sensitivity['confidence_95'][0]:.3f}, {sensitivity['confidence_95'][1]:.3f}]"
    )

    return model, mixed_sample


if __name__ == "__main__":
    model, mixed_sample = example_usage()
