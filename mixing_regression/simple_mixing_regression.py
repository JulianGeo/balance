import numpy as np
from typing import Tuple, Dict, Optional, Union


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

    def calculate_mixing_fraction(self, mixed_sample: Dict[str, float], element: str):
        idx = self.elements.index(element)

        # Create the coefficient matrix
        A = np.array([[1, 1], [self.C1[idx], self.C2[idx]]])

        # Create the right-hand side vector
        b = np.array([1, mixed_sample[element]])  # f1 + f2 = 1, f1*C1 + f2*C2 = Cm

        try:
            # Solve using numpy's linear algebra solver
            f1, f2 = np.linalg.solve(A, b)
            return f1, f2
        except np.linalg.LinAlgError:
            raise ValueError(f"Cannot solve mixing model for elements {element}")

    def calculate_all(self, mixed_sample: Dict[str, float]) -> Dict:
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
            elem = self.elements[i]
            key = f"{elem}"

            try:
                f1, f2 = self.calculate_mixing_fraction(mixed_sample, elem)

                results[key] = {
                    "fraction_end_member1": f1,
                    "fraction_end_member2": f2,
                    "elements_used": (elem),
                }

            except (ValueError, np.linalg.LinAlgError) as e:
                results[key] = {
                    "error": str(e),
                    "elements_used": (elem),
                }

        return results


# Example usage
def example_usage():
    reservoir = {
        "Cl": 744,
        "Li": 1.19,
        "B": 7.47,
        "Na": 483,
        "Ca": 84,
        "Mg": 49.2,
        "SO4": 168,
        "HCO3": 409,
    }
    freshwater = {
        "Cl": 1.42,
        "Li": 0.01,
        "B": 0.04,
        "Na": 17.94,
        "Ca": 12.4,
        "Mg": 12.12,
        "SO4": 1.44,
        "HCO3": 139.08,
    }

    # Create mixing model
    model = NumpyMixingModel(reservoir, freshwater)

    mixed_sample = {
        "Cl": 602,
        "Li": 0.63,
        "B": 7.182,
        "Na": 462.07,
        "Ca": 64.4,
        "Mg": 123.24,
        "SO4": 16.8,
        "HCO3": 1088.85,
    }

    print("Mixed sample concentrations:")
    for elem, conc in mixed_sample.items():
        print(f"{elem}: {conc:.1f}")

    # All elements
    print("\n3. All element pair results:")
    pairwise_results = model.calculate_all(mixed_sample)
    for pair, result in pairwise_results.items():
        if "error" not in result:
            print(
                f"{pair}: f1 = {result['fraction_end_member1']:.3f}, f2 = {result['fraction_end_member2']:.3f})"
            )


if __name__ == "__main__":
    example_usage()
