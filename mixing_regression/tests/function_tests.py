import numpy as np


def test_linealg_solver_ideal():
    print("Running ideal test case for np.linalg.solve...")
    # Test case for np.linalg.solve

    # Coefficient matrix
    A = np.array([[3, 1], [1, 2]])
    # Right hand side vector
    b = np.array([9, 8])
    x = np.linalg.solve(A, b)
    print("Solution x:", x)
    expected_x = np.array([2, 3])
    assert np.allclose(x, expected_x), f"Expected {expected_x}, but got {x}"


def test_linealg_solver():
    print("Running test case for np.linalg.solve...")
    # Test case for np.linalg.solve

    # Coefficient matrix
    A = np.array([[2, 4], [1, 2]])
    # Right hand side vector
    b = np.array([1, 16000])
    x = np.linalg.solve(A, b)
    print("Solution x:", x)


test_linealg_solver_ideal()
test_linealg_solver()
