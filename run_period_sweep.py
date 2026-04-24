"""
Week 3 preparation: period sweep comparison.

    Sweep the array period P and plot mean phase deviation vs P
    for both uniform and non-uniform arrays.

Also produces a figure overlaying uniform vs. non-uniform behavior —
the main controlled comparison for Week 3.
"""

from __future__ import annotations

import os
import numpy as np
import matplotlib.pyplot as plt

import cda
from run_baseline import (
    DEFAULT_OMEGA,
    DEFAULT_OMEGA0,
    DEFAULT_GAMMA,
    DEFAULT_F,
    default_alpha,
    FIG_DIR,
)


def sweep_uniform(periods: np.ndarray, N: int = 21) -> np.ndarray:
    """Mean phase deviation over period, uniform array (identical alpha)."""
    alpha = default_alpha()
    out = np.zeros_like(periods)
    for i, P in enumerate(periods):
        res = cda.run_uniform_array(N=N, period=P, alpha=alpha)
        out[i] = np.degrees(res["mean_phase_dev"])
    return out


def sweep_nonuniform(
    periods: np.ndarray,
    N: int = 21,
    omega0_min: float = 2.00 * np.pi,
    omega0_max: float = 2.20 * np.pi,
) -> np.ndarray:
    """Mean phase deviation over period, non-uniform array.

    Each meta-atom has a different resonance frequency omega0, distributed
    linearly across the array. This mimics a typical phase-gradient design
    where each meta-atom has a different geometry.
    """
    omega = DEFAULT_OMEGA
    omega0_array = np.linspace(omega0_min, omega0_max, N)
    alphas = np.array([
        cda.LorentzAlpha(omega0=w0, gamma=DEFAULT_GAMMA, F=DEFAULT_F)(omega=omega)
        for w0 in omega0_array
    ], dtype=complex)

    out = np.zeros_like(periods)
    for i, P in enumerate(periods):
        positions = cda.linear_array(N, P)
        res = cda.run_nonuniform_array(positions=positions, alphas=alphas)
        out[i] = np.degrees(res["mean_phase_dev"])
    return out


def main():
    periods = np.linspace(0.5, 3.0, 40)
    N = 21

    print(f"Running period sweep: N={N}, {len(periods)} periods...")
    dev_uniform = sweep_uniform(periods, N=N)
    dev_nonuniform = sweep_nonuniform(periods, N=N)

    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.plot(periods, dev_uniform, "o-", color="#1A478A",
            label="Uniform array (identical α)", markersize=4)
    ax.plot(periods, dev_nonuniform, "s-", color="#C0392B",
            label="Non-uniform array (graded α)", markersize=4)
    ax.axhline(0, color="k", lw=0.5)
    ax.set_xlabel(r"period $P$ (in units of $\lambda$)")
    ax.set_ylabel(r"mean phase deviation $\overline{|\Delta\varphi|}$ (deg)")
    ax.set_title(
        f"Coupling-induced phase distortion vs. period  (N = {N})"
    )
    ax.grid(alpha=0.3)
    ax.legend()
    fig.tight_layout()
    fig_path = os.path.join(FIG_DIR, "period_sweep_comparison.png")
    fig.savefig(fig_path, dpi=150)
    plt.close(fig)

    print(f"Figure saved: {fig_path}")
    print()
    print(f"{'P/lambda':>10} | {'Uniform (deg)':>14} | {'Non-uniform (deg)':>18}")
    print("-" * 52)
    for P, du, dn in zip(periods, dev_uniform, dev_nonuniform):
        print(f"{P:>10.3f} | {du:>14.3f} | {dn:>18.3f}")


if __name__ == "__main__":
    main()
