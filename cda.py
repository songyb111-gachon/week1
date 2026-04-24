"""
Coupled Dipole Approximation (CDA) — 2D scalar implementation
for analyzing inter-meta-atom coupling in a 1D metasurface array.

Model:
    Each meta-atom -> single point electric dipole with scalar polarizability alpha.
    Dipoles are arranged on a 1D line with period P along the x-axis.
    Incident plane wave: normal incidence, E = E0 * exp(i*k0*z), polarized out of plane.
    In 2D (we treat the line as cylindrical scatterers along y), the scalar Green's
    function is the 0th-order Hankel function of the first kind:

        G(r) = (i/4) * H0^(1)(k0 * r)

    Self-consistent equation:
        p_i = alpha_i * (E_inc_i + sum_{j != i} G(|r_i - r_j|) * p_j)

    Rearranged to matrix form:
        A_ij =  1/alpha_i           (i = j)
                -G(|r_i - r_j|)     (i != j)

        A * p = E_inc

Author: AIP Week 2 project
"""

from __future__ import annotations

from dataclasses import dataclass
import numpy as np
from scipy.special import hankel1


# ---------------------------------------------------------------------
# Basic physical constants in natural units (wavelength-normalized)
# ---------------------------------------------------------------------
# We fix k0 = 2*pi (i.e. wavelength lambda = 1). All distances are
# reported in units of the wavelength.

K0 = 2.0 * np.pi
LAMBDA = 1.0


# ---------------------------------------------------------------------
# Polarizability model: Lorentzian
# ---------------------------------------------------------------------
@dataclass
class LorentzAlpha:
    """Lorentzian polarizability as a function of frequency.

    alpha(omega) = F / (omega0^2 - omega^2 - i*gamma*omega)

    Here we use dimensionless omega where omega = 2*pi (i.e., the operating
    frequency matches lambda = 1). omega0 encodes the resonance frequency
    of the meta-atom (different meta-atom geometries -> different omega0).
    """

    omega0: float
    gamma: float = 0.2
    F: float = 1.0

    def __call__(self, omega: float = 2.0 * np.pi) -> complex:
        denom = self.omega0**2 - omega**2 - 1j * self.gamma * omega
        return self.F / denom


# ---------------------------------------------------------------------
# Green's function
# ---------------------------------------------------------------------
def greens_2d(r: np.ndarray, k0: float = K0) -> np.ndarray:
    """2D scalar free-space Green's function.

    G(r) = (i/4) * H0^(1)(k0 * r)

    Vectorized over r. Safe for r > 0. Returns a complex array.
    """
    r = np.asarray(r, dtype=float)
    return 0.25j * hankel1(0, k0 * r)


# ---------------------------------------------------------------------
# Array geometry
# ---------------------------------------------------------------------
def linear_array(N: int, period: float, center: bool = True) -> np.ndarray:
    """Return x-positions of N meta-atoms on a 1D line with given period.

    If center=True, the array is centered around x = 0.
    """
    x = np.arange(N, dtype=float) * period
    if center:
        x -= x.mean()
    return x


# ---------------------------------------------------------------------
# CDA solver
# ---------------------------------------------------------------------
def build_interaction_matrix(
    positions: np.ndarray,
    alphas: np.ndarray,
    k0: float = K0,
) -> np.ndarray:
    """Build the N x N CDA interaction matrix A.

    A_ii = 1 / alpha_i
    A_ij = -G(|r_i - r_j|)     (i != j)

    positions: shape (N,) — x-coordinates of dipoles (we assume y = 0 for all).
    alphas:    shape (N,) — complex polarizabilities.
    """
    positions = np.asarray(positions, dtype=float)
    alphas = np.asarray(alphas, dtype=complex)
    N = positions.size

    dx = positions[:, None] - positions[None, :]
    r = np.abs(dx)
    np.fill_diagonal(r, 1.0)  # placeholder; we overwrite diagonal

    A = -greens_2d(r, k0=k0)
    diag_idx = np.arange(N)
    A[diag_idx, diag_idx] = 1.0 / alphas
    return A


def solve_cda(
    positions: np.ndarray,
    alphas: np.ndarray,
    E_inc: np.ndarray,
    k0: float = K0,
) -> np.ndarray:
    """Solve A p = E_inc for dipole moments p (coupled response)."""
    A = build_interaction_matrix(positions, alphas, k0=k0)
    return np.linalg.solve(A, E_inc)


def isolated_response(alphas: np.ndarray, E_inc: np.ndarray) -> np.ndarray:
    """Dipole moments if each meta-atom were isolated: p = alpha * E_inc."""
    return np.asarray(alphas, dtype=complex) * np.asarray(E_inc, dtype=complex)


# ---------------------------------------------------------------------
# Incident field helpers
# ---------------------------------------------------------------------
def plane_wave_normal(positions: np.ndarray, E0: complex = 1.0 + 0j) -> np.ndarray:
    """Normal-incidence plane wave evaluated at y = 0: E_inc = E0 (uniform)."""
    return np.full(positions.shape, E0, dtype=complex)


# ---------------------------------------------------------------------
# Diagnostics
# ---------------------------------------------------------------------
def phase_deviation(p_coupled: np.ndarray, p_isolated: np.ndarray) -> np.ndarray:
    """Phase deviation per dipole, wrapped to (-pi, pi]."""
    dphi = np.angle(p_coupled) - np.angle(p_isolated)
    return np.angle(np.exp(1j * dphi))  # wrap


def mean_phase_deviation(p_coupled: np.ndarray, p_isolated: np.ndarray) -> float:
    """Mean absolute phase deviation (radians)."""
    return float(np.mean(np.abs(phase_deviation(p_coupled, p_isolated))))


def max_phase_deviation(p_coupled: np.ndarray, p_isolated: np.ndarray) -> float:
    return float(np.max(np.abs(phase_deviation(p_coupled, p_isolated))))


def amplitude_distortion_ratio(
    p_coupled: np.ndarray, p_isolated: np.ndarray
) -> np.ndarray:
    return np.abs(p_coupled) / np.abs(p_isolated)


# ---------------------------------------------------------------------
# Convenience: end-to-end run for a uniform 1D array
# ---------------------------------------------------------------------
def run_uniform_array(
    N: int,
    period: float,
    alpha: complex,
    E0: complex = 1.0 + 0j,
    k0: float = K0,
):
    """Run CDA for a uniform 1D array. Returns a dict of results."""
    positions = linear_array(N, period)
    alphas = np.full(N, alpha, dtype=complex)
    E_inc = plane_wave_normal(positions, E0=E0)

    p_coupled = solve_cda(positions, alphas, E_inc, k0=k0)
    p_iso = isolated_response(alphas, E_inc)

    return {
        "positions": positions,
        "alphas": alphas,
        "E_inc": E_inc,
        "p_coupled": p_coupled,
        "p_isolated": p_iso,
        "phase_dev": phase_deviation(p_coupled, p_iso),
        "mean_phase_dev": mean_phase_deviation(p_coupled, p_iso),
        "max_phase_dev": max_phase_deviation(p_coupled, p_iso),
    }


def run_nonuniform_array(
    positions: np.ndarray,
    alphas: np.ndarray,
    E0: complex = 1.0 + 0j,
    k0: float = K0,
):
    """Run CDA for a non-uniform 1D array (each dipole may have different alpha)."""
    positions = np.asarray(positions, dtype=float)
    alphas = np.asarray(alphas, dtype=complex)
    E_inc = plane_wave_normal(positions, E0=E0)

    p_coupled = solve_cda(positions, alphas, E_inc, k0=k0)
    p_iso = isolated_response(alphas, E_inc)

    return {
        "positions": positions,
        "alphas": alphas,
        "E_inc": E_inc,
        "p_coupled": p_coupled,
        "p_isolated": p_iso,
        "phase_dev": phase_deviation(p_coupled, p_iso),
        "mean_phase_dev": mean_phase_deviation(p_coupled, p_iso),
        "max_phase_dev": max_phase_deviation(p_coupled, p_iso),
    }
