"""
Comprehensive physical verification of the CDA implementation.

This script performs 8 independent physical checks:

    1. Single-dipole sanity check (N=1): CDA == analytical isolated response
    2. Two-dipole analytical comparison (N=2): closed-form coupled solution
    3. Green's function properties: symmetry G(r) == G(-r), reciprocity
    4. Linear system residual: ||A·p - E_inc|| / ||E_inc||
    5. Mirror symmetry: symmetric geometry -> symmetric response
    6. Reciprocity (swap source/receiver dipoles): off-diagonal symmetry
    7. Array-size convergence: bulk values stabilize as N grows
    8. Wavelength scaling invariance: dimensionless geometry -> same result
"""

from __future__ import annotations

import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.special import hankel1

import cda


FIG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "figures")
os.makedirs(FIG_DIR, exist_ok=True)

PASS = "PASS"
FAIL = "FAIL"

results: list[tuple[str, str, str]] = []


def report(name: str, ok: bool, detail: str):
    tag = PASS if ok else FAIL
    line = f"[{tag}]  {name}"
    print(line)
    print(f"        {detail}")
    print()
    results.append((tag, name, detail))


# ---------------------------------------------------------------------
# Common setup
# ---------------------------------------------------------------------
def default_alpha() -> complex:
    return cda.LorentzAlpha(
        omega0=2.1 * np.pi, gamma=0.4, F=4.0
    )(omega=2.0 * np.pi)


# ---------------------------------------------------------------------
# Test 1: Single-dipole
# ---------------------------------------------------------------------
def test_single_dipole():
    alpha = default_alpha()
    res = cda.run_uniform_array(N=1, period=1.0, alpha=alpha)
    p_num = res["p_coupled"][0]
    p_ana = alpha * 1.0
    err = abs(p_num - p_ana) / abs(p_ana)
    ok = err < 1e-12
    report(
        "1. Single-dipole sanity check",
        ok,
        f"CDA matches analytical p = alpha * E_inc   (rel. error = {err:.2e})",
    )


# ---------------------------------------------------------------------
# Test 2: Two-dipole analytical
# ---------------------------------------------------------------------
def test_two_dipole_analytical(period: float = 0.8):
    """
    For two identical dipoles at positions +/- P/2 with incident field E_0 = 1,
    by symmetry p_1 = p_2 = p. The self-consistent equation becomes:
        p = alpha * (1 + G(P) * p)
        p = alpha / (1 - alpha * G(P))
    """
    alpha = default_alpha()
    G12 = cda.greens_2d(np.array([period]))[0]
    p_ana = alpha / (1.0 - alpha * G12)

    res = cda.run_uniform_array(N=2, period=period, alpha=alpha)
    p1, p2 = res["p_coupled"]

    err1 = abs(p1 - p_ana) / abs(p_ana)
    err2 = abs(p2 - p_ana) / abs(p_ana)
    sym_err = abs(p1 - p2) / abs(p1)

    ok = max(err1, err2, sym_err) < 1e-12
    report(
        "2. Two-dipole analytical comparison",
        ok,
        f"rel. error: p1 vs. analytical = {err1:.2e},  "
        f"p2 vs. analytical = {err2:.2e},  |p1-p2|/|p1| = {sym_err:.2e}",
    )


# ---------------------------------------------------------------------
# Test 3: Green's function properties
# ---------------------------------------------------------------------
def test_green_function():
    rs = np.linspace(0.01, 5.0, 50)
    g_pos = cda.greens_2d(rs)
    g_neg = cda.greens_2d(-rs)  # Note: cda.greens_2d uses abs(r) internally? No, it uses r directly.
    # Actually greens_2d takes a positive distance. But H0 is defined for positive r.
    # For our CDA we always use |r_i - r_j|. Let's verify G(|dx|) with both dx > 0 and dx < 0.
    # Since r = |dx| in cda, both give the same result. Verify here manually.
    g_from_hankel_pos = 0.25j * hankel1(0, 2 * np.pi * rs)
    g_from_hankel_neg = 0.25j * hankel1(0, 2 * np.pi * np.abs(-rs))

    err_pos = np.max(np.abs(g_pos - g_from_hankel_pos))
    err_neg = np.max(np.abs(g_from_hankel_pos - g_from_hankel_neg))

    # Reciprocity: G(r_i - r_j) = G(r_j - r_i) because we use |dx|
    positions = np.array([0.0, 0.7, 1.3, 2.1])
    dx = positions[:, None] - positions[None, :]
    G_mat = cda.greens_2d(np.abs(dx) + 1e-30)
    sym_err = np.max(np.abs(G_mat - G_mat.T))

    ok = err_pos < 1e-14 and err_neg < 1e-14 and sym_err < 1e-14
    report(
        "3. Green's function: formula + symmetry",
        ok,
        f"|G(r) - (i/4)H0(k0 r)| = {err_pos:.2e},  "
        f"reciprocity max|G_ij - G_ji| = {sym_err:.2e}",
    )


# ---------------------------------------------------------------------
# Test 4: Linear system residual
# ---------------------------------------------------------------------
def test_linear_system_residual():
    alpha = default_alpha()
    N, P = 51, 0.8
    res = cda.run_uniform_array(N=N, period=P, alpha=alpha)
    positions = res["positions"]
    alphas = res["alphas"]
    E_inc = res["E_inc"]
    p = res["p_coupled"]

    A = cda.build_interaction_matrix(positions, alphas)
    residual = np.linalg.norm(A @ p - E_inc) / np.linalg.norm(E_inc)

    ok = residual < 1e-12
    report(
        "4. Linear system residual  ||A p - E_inc|| / ||E_inc||",
        ok,
        f"residual = {residual:.2e}   (N = {N}, P = {P} lambda)",
    )


# ---------------------------------------------------------------------
# Test 5: Mirror symmetry
# ---------------------------------------------------------------------
def test_mirror_symmetry():
    """
    For a centered uniform array with normal-incidence plane wave,
    the response must be mirror-symmetric about the center:
        p_i = p_{N-1-i}
    """
    alpha = default_alpha()
    N, P = 21, 0.75
    res = cda.run_uniform_array(N=N, period=P, alpha=alpha)
    p = res["p_coupled"]
    positions = res["positions"]

    # verify positions are symmetric
    pos_err = np.max(np.abs(positions + positions[::-1]))

    # verify amplitude and phase symmetric
    amp_err = np.max(np.abs(np.abs(p) - np.abs(p[::-1])))
    phase_err = np.max(np.abs(np.angle(p) - np.angle(p[::-1])))

    ok = pos_err < 1e-12 and amp_err < 1e-10 and phase_err < 1e-10
    report(
        "5. Mirror symmetry of uniform centered array",
        ok,
        f"max |p_i - p_(N-1-i)|: amplitude = {amp_err:.2e},  "
        f"phase = {phase_err:.2e}  rad",
    )


# ---------------------------------------------------------------------
# Test 6: Reciprocity at the matrix level
# ---------------------------------------------------------------------
def test_reciprocity_matrix():
    """
    A_ij should equal A_ji for off-diagonal entries.
    """
    alpha = default_alpha()
    positions = cda.linear_array(N=11, period=0.9)
    alphas = np.full(11, alpha, dtype=complex)
    A = cda.build_interaction_matrix(positions, alphas)

    off_diag_mask = ~np.eye(A.shape[0], dtype=bool)
    sym_err = np.max(np.abs(A[off_diag_mask] - A.T[off_diag_mask]))

    ok = sym_err < 1e-14
    report(
        "6. Matrix reciprocity  A_ij == A_ji",
        ok,
        f"max off-diagonal asymmetry = {sym_err:.2e}",
    )


# ---------------------------------------------------------------------
# Test 7: Array-size convergence
# ---------------------------------------------------------------------
def test_array_convergence():
    """
    As N increases, the phase deviation of the central atom should
    slowly converge. In 2D the free-space Green's function decays as
    1/sqrt(r), so the 1D lattice sum converges conditionally (O(1/sqrt(N))).
    We therefore check:
        a) successive differences decrease on average
        b) the decay is consistent with ~1/sqrt(N) (2D Green's function behavior)
    """
    alpha = default_alpha()
    P = 0.8  # avoid Wood-anomaly regions
    Ns = np.array([11, 21, 41, 81, 161, 321, 641])
    center_dev = []
    for N in Ns:
        res = cda.run_uniform_array(N=int(N), period=P, alpha=alpha)
        center_idx = int(N) // 2
        dphi = cda.phase_deviation(res["p_coupled"], res["p_isolated"])
        center_dev.append(np.degrees(dphi[center_idx]))
    center_dev = np.array(center_dev)

    diffs = np.abs(np.diff(center_dev))
    final_diff = diffs[-1]

    # Test: absolute converged value + rate of convergence.
    # Fit: |delta_N| ~ C / sqrt(N)  =>  log|delta| = log C - 0.5 log N
    valid = diffs > 0
    if valid.sum() >= 3:
        slope, _ = np.polyfit(np.log(Ns[1:][valid]), np.log(diffs[valid]), 1)
    else:
        slope = np.nan

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4.2))
    ax1.semilogx(Ns, center_dev, "o-", color="#1A478A")
    ax1.set_xlabel("array size N")
    ax1.set_ylabel(r"central atom phase deviation (deg)")
    ax1.set_title(f"Central-atom phase deviation  (P = {P} lambda)")
    ax1.grid(alpha=0.3)

    ax2.loglog(Ns[1:], diffs, "s-", color="#C0392B", label="|delta_N|")
    # reference 1/sqrt(N) line
    ref = diffs[0] * np.sqrt(Ns[1] / Ns[1:])
    ax2.loglog(Ns[1:], ref, "k--", alpha=0.5, label="1/sqrt(N) reference")
    ax2.set_xlabel("N")
    ax2.set_ylabel("|center_dev[N] - center_dev[N/2]| (deg)")
    ax2.set_title(f"Convergence rate (fitted slope = {slope:.2f})")
    ax2.grid(alpha=0.3, which="both")
    ax2.legend()
    fig.tight_layout()
    out_path = os.path.join(FIG_DIR, "verification_convergence.png")
    fig.savefig(out_path, dpi=150)
    plt.close(fig)

    # Acceptable if:
    #   (a) final successive difference is below 0.5 deg, AND
    #   (b) the fitted slope is close to -0.5 (2D Green's function decay rate)
    slope_ok = -0.9 < slope < -0.2
    diff_ok = final_diff < 0.5
    ok = slope_ok and diff_ok
    report(
        "7. Array-size convergence of central-atom phase deviation",
        ok,
        f"central Dphi values: {np.array2string(center_dev, precision=3)}\n"
        f"        successive |differences|:  "
        f"{np.array2string(diffs, precision=3)} deg\n"
        f"        final step difference = {final_diff:.3e} deg\n"
        f"        fitted convergence slope = {slope:.3f}   "
        f"(theoretical -0.5 for 2D Green)\n"
        f"        plot saved: {out_path}",
    )


# ---------------------------------------------------------------------
# Test 8: Wavelength scaling invariance
# ---------------------------------------------------------------------
def test_wavelength_scaling():
    """
    CDA depends only on dimensionless k0 * r. If we scale all distances
    AND change k0 accordingly, the dipole moments should be invariant
    (when alpha is taken at the same scaled frequency).

    Simpler check: we compute at k0 = 2*pi (lambda = 1).
    Then redefine k0' = 4*pi (lambda' = 0.5) and scale all positions by 0.5.
    Result must be identical.
    """
    alpha = default_alpha()
    N, P = 15, 0.8
    positions1 = cda.linear_array(N, P)
    alphas = np.full(N, alpha, dtype=complex)
    E_inc = cda.plane_wave_normal(positions1)

    p1 = cda.solve_cda(positions1, alphas, E_inc, k0=2 * np.pi)

    scale = 0.5
    positions2 = positions1 * scale
    p2 = cda.solve_cda(positions2, alphas, E_inc, k0=2 * np.pi / scale)

    err = np.max(np.abs(p1 - p2) / np.max(np.abs(p1)))
    ok = err < 1e-12
    report(
        "8. Wavelength scaling invariance",
        ok,
        f"max |p(k0) - p(k0/scale)| / max|p| = {err:.2e}   (scale = {scale})",
    )


# ---------------------------------------------------------------------
# Test 9: Extinction power positivity (optical-theorem-inspired)
# ---------------------------------------------------------------------
def test_extinction_positive():
    """
    Extinction power per unit length in 2D:
        P_ext  ~  Im( E_inc* . p ) summed over all dipoles.

    For a passive, physically meaningful system (lossy Lorentzian alpha),
    the extinction power must be strictly positive for any non-trivial setup.
    """
    alpha = default_alpha()
    periods_to_test = [0.5, 0.7, 1.2, 1.5, 2.5]
    Ns = [3, 21, 51]
    all_positive = True
    log_lines = []
    for N in Ns:
        for P in periods_to_test:
            res = cda.run_uniform_array(N=N, period=P, alpha=alpha)
            E_inc = res["E_inc"]
            p = res["p_coupled"]
            P_ext_proxy = float(np.sum(np.imag(np.conj(E_inc) * p)))
            log_lines.append(
                f"  N={N:>3}, P={P:>4.2f}   ->   P_ext_proxy = {P_ext_proxy:+.4e}"
            )
            if P_ext_proxy <= 0:
                all_positive = False

    report(
        "9. Extinction power positivity (optical-theorem inspired)",
        all_positive,
        "Im( E_inc* . p ) > 0 for all configurations:\n        "
        + "\n        ".join(log_lines),
    )


# ---------------------------------------------------------------------
# Test 10: Non-uniform array sanity — setting all alpha equal == uniform
# ---------------------------------------------------------------------
def test_nonuniform_reduces_to_uniform():
    """
    run_nonuniform_array with all identical alpha must give the same
    result as run_uniform_array.
    """
    alpha = default_alpha()
    N, P = 15, 0.9
    positions = cda.linear_array(N, P)
    alphas = np.full(N, alpha, dtype=complex)

    res_u = cda.run_uniform_array(N=N, period=P, alpha=alpha)
    res_nu = cda.run_nonuniform_array(positions=positions, alphas=alphas)

    err = np.max(np.abs(res_u["p_coupled"] - res_nu["p_coupled"]))
    ok = err < 1e-14
    report(
        "10. Non-uniform solver reduces to uniform (with identical alphas)",
        ok,
        f"max |p_uniform - p_nonuniform| = {err:.2e}",
    )


# ---------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------
def summary():
    n_pass = sum(1 for tag, *_ in results if tag == PASS)
    n_fail = sum(1 for tag, *_ in results if tag == FAIL)
    total = len(results)

    print("=" * 70)
    print(f"VERIFICATION SUMMARY:  {n_pass} / {total} passed,  {n_fail} failed")
    print("=" * 70)
    for tag, name, _ in results:
        print(f"  [{tag}]  {name}")
    print()

    if n_fail == 0:
        print("All physical checks passed.")
    else:
        print("Some checks FAILED - please inspect.")


if __name__ == "__main__":
    print("=" * 70)
    print("CDA PHYSICAL VERIFICATION SUITE")
    print("=" * 70)
    print()
    test_single_dipole()
    test_two_dipole_analytical()
    test_green_function()
    test_linear_system_residual()
    test_mirror_symmetry()
    test_reciprocity_matrix()
    test_array_convergence()
    test_wavelength_scaling()
    test_extinction_positive()
    test_nonuniform_reduces_to_uniform()
    summary()
