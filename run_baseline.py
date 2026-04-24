"""
Week 2 Baseline Run:
    1. Demonstrate that the CDA code runs end-to-end.
    2. Sanity check: for a single isolated dipole, CDA result must match
       the analytical isolated response p = alpha * E_inc.
    3. Produce one baseline figure: phase deviation across the array at a
       typical period.
    4. Produce one scalar diagnostic: mean phase deviation.

All outputs are saved to the ./figures/ directory.
"""

from __future__ import annotations

import os
import numpy as np
import matplotlib.pyplot as plt

import cda

FIG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "figures")
os.makedirs(FIG_DIR, exist_ok=True)


# ---------------------------------------------------------------------
# 1. Single-dipole sanity check
# ---------------------------------------------------------------------
DEFAULT_OMEGA = 2.0 * np.pi        # operating frequency (lambda = 1)
DEFAULT_OMEGA0 = 2.1 * np.pi       # resonance frequency (close, but detuned)
DEFAULT_GAMMA = 0.4
DEFAULT_F = 4.0


def default_alpha() -> complex:
    """Reference polarizability used throughout Week 2 baseline."""
    return cda.LorentzAlpha(
        omega0=DEFAULT_OMEGA0, gamma=DEFAULT_GAMMA, F=DEFAULT_F
    )(omega=DEFAULT_OMEGA)


def sanity_check_single_dipole() -> dict:
    """For N=1, the CDA result must exactly equal alpha * E_inc."""
    alpha = default_alpha()

    result = cda.run_uniform_array(N=1, period=1.0, alpha=alpha, E0=1.0 + 0j)

    p_num = result["p_coupled"][0]
    p_ana = alpha * 1.0  # analytical isolated response

    err_abs = abs(p_num - p_ana)
    err_rel = err_abs / abs(p_ana)

    print("=" * 60)
    print("Sanity Check 1: Single isolated dipole")
    print("=" * 60)
    print(f"  alpha (complex)     = {alpha:.6e}")
    print(f"  p (CDA numerical)   = {p_num:.6e}")
    print(f"  p (analytical)      = {p_ana:.6e}")
    print(f"  |error|             = {err_abs:.3e}")
    print(f"  relative error      = {err_rel:.3e}")
    print()

    return {
        "alpha": alpha,
        "p_num": p_num,
        "p_ana": p_ana,
        "err_abs": err_abs,
        "err_rel": err_rel,
    }


# ---------------------------------------------------------------------
# 2. Large-period limiting case
# ---------------------------------------------------------------------
def sanity_check_large_period(N: int = 21) -> dict:
    """As P -> infinity, coupled phase should converge to isolated phase."""
    alpha = default_alpha()

    periods = np.array([0.6, 1.0, 2.0, 5.0, 10.0, 20.0])
    mean_devs = []
    for P in periods:
        res = cda.run_uniform_array(N=N, period=P, alpha=alpha)
        mean_devs.append(res["mean_phase_dev"])
    mean_devs = np.array(mean_devs)

    print("=" * 60)
    print("Sanity Check 2: Large-period limit")
    print("=" * 60)
    for P, d in zip(periods, mean_devs):
        print(f"  P = {P:5.2f} lambda   ->   mean |Dphi| = {np.degrees(d):7.3f} deg")
    print()

    return {"periods": periods, "mean_devs": mean_devs}


# ---------------------------------------------------------------------
# 3. Baseline figure: phase deviation across a uniform array
# ---------------------------------------------------------------------
def baseline_figure(N: int = 31, period: float = 0.6) -> dict:
    """Produce a baseline figure showing the coupled response of a uniform array.

    Shows:
      - phase deviation Delta phi_i vs atom index
      - amplitude distortion ratio vs atom index
    """
    alpha = default_alpha()

    result = cda.run_uniform_array(N=N, period=period, alpha=alpha)
    positions = result["positions"]
    phase_dev = np.degrees(result["phase_dev"])
    adr = cda.amplitude_distortion_ratio(result["p_coupled"], result["p_isolated"])
    mean_dev = np.degrees(result["mean_phase_dev"])
    max_dev = np.degrees(result["max_phase_dev"])

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4.2))

    ax1.plot(positions, phase_dev, "o-", color="#C0392B")
    ax1.axhline(0, color="k", lw=0.5)
    ax1.set_xlabel(r"atom position $x$ (in units of $\lambda$)")
    ax1.set_ylabel(r"phase deviation $\Delta\varphi$ (deg)")
    ax1.set_title(
        f"Phase deviation — uniform array\n"
        f"N = {N}, P = {period:.2f}"
        + r"$\lambda$"
        + f",   mean |$\\Delta\\varphi$| = {mean_dev:.2f}°"
    )
    ax1.grid(alpha=0.3)

    ax2.plot(positions, adr, "s-", color="#1A478A")
    ax2.axhline(1, color="k", lw=0.5)
    ax2.set_xlabel(r"atom position $x$ (in units of $\lambda$)")
    ax2.set_ylabel(r"amplitude ratio $|p_{\rm coup}|/|p_{\rm iso}|$")
    ax2.set_title("Amplitude distortion ratio")
    ax2.grid(alpha=0.3)

    fig.tight_layout()
    fig_path = os.path.join(FIG_DIR, "baseline_uniform_array.png")
    fig.savefig(fig_path, dpi=150)
    plt.close(fig)

    print("=" * 60)
    print(f"Baseline figure: N={N}, P={period} lambda")
    print("=" * 60)
    print(f"  mean |Dphi|  = {mean_dev:7.3f} deg")
    print(f"  max  |Dphi|  = {max_dev:7.3f} deg")
    print(f"  ADR range    = [{adr.min():.4f}, {adr.max():.4f}]")
    print(f"  saved to     : {fig_path}")
    print()

    return {
        "mean_dev_deg": mean_dev,
        "max_dev_deg": max_dev,
        "adr_min": float(adr.min()),
        "adr_max": float(adr.max()),
        "fig_path": fig_path,
    }


# ---------------------------------------------------------------------
# 4. Limiting-case figure: mean phase deviation vs period
# ---------------------------------------------------------------------
def limiting_case_figure(N: int = 21) -> dict:
    """Plot mean phase deviation as a function of period P.

    Expected: Delta phi -> 0 as P -> infinity (isolated-limit).
    """
    alpha = default_alpha()

    periods = np.linspace(0.5, 10.0, 40)
    mean_devs = []
    for P in periods:
        res = cda.run_uniform_array(N=N, period=P, alpha=alpha)
        mean_devs.append(np.degrees(res["mean_phase_dev"]))
    mean_devs = np.array(mean_devs)

    fig, ax = plt.subplots(figsize=(7, 4.2))
    ax.plot(periods, mean_devs, "o-", color="#1A478A", markersize=4)
    ax.axhline(0, color="k", lw=0.5)
    ax.set_xlabel(r"period $P$ (in units of $\lambda$)")
    ax.set_ylabel(r"mean $|\Delta\varphi|$ (deg)")
    ax.set_title(
        f"Limiting-case check: mean phase deviation vs period (N={N})"
    )
    ax.grid(alpha=0.3)
    fig.tight_layout()
    fig_path = os.path.join(FIG_DIR, "limiting_case_period.png")
    fig.savefig(fig_path, dpi=150)
    plt.close(fig)

    print("=" * 60)
    print("Limiting-case figure saved:")
    print(f"  {fig_path}")
    print(f"  Dphi at  P=0.5 : {mean_devs[0]:7.3f} deg")
    print(f"  Dphi at  P=10  : {mean_devs[-1]:7.3f} deg")
    print()

    return {
        "periods": periods,
        "mean_devs": mean_devs,
        "fig_path": fig_path,
    }


# ---------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------
if __name__ == "__main__":
    sanity_check_single_dipole()
    sanity_check_large_period(N=21)
    baseline_figure(N=31, period=0.6)
    limiting_case_figure(N=21)
    print("Week 2 baseline complete. See ./figures/ for plots.")
