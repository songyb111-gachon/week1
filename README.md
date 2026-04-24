# Coupled Dipole Approximation for Metasurface Phase Analysis

AIP Mini Project — Week 1 ~ Week 4

## Research Question

> **"How does the phase distortion caused by inter-meta-atom coupling increase as the array period decreases?"**

## Model

Each meta-atom is modeled as a point electric dipole with a scalar polarizability `α`.
Dipoles are arranged on a 1D line with period `P` and interact via the 2D free-space
scalar Green's function `G(r) = (i/4) H₀⁽¹⁾(k₀ r)`. The self-consistent
equation for the dipole moments is:

```
A · p = E_inc
```

with `A_ii = 1/α_i` and `A_ij = -G(|r_i − r_j|)` for `i ≠ j`.

## Files

| File | Description |
|------|-------------|
| `cda.py` | Core CDA library: Green's function, interaction matrix, solver, Lorentzian polarizability |
| `run_baseline.py` | Week 2 baseline: single-dipole sanity check + uniform-array figure |
| `run_period_sweep.py` | Period sweep comparison (uniform vs non-uniform) |
| `make_pptx.py` | Week 1 proposal PPT generator |
| `week1_proposal.md` | Week 1 proposal text (minimal) |
| `week1_proposal_full.md` | Week 1 proposal text (full version) |
| `week1_script.md` | Week 1 presentation script |
| `week2_progress.md` | Week 2 progress report |
| `week2_script.md` | Week 2 presentation script |

## Requirements

- Python 3.10+
- `numpy`
- `scipy`
- `matplotlib`
- `python-pptx` (for PPT generation)
- `Pillow`, `lxml` (python-pptx dependencies)

Install:

```bash
pip install numpy scipy matplotlib python-pptx
```

## Usage

### Run Week 2 baseline & validation

```bash
python run_baseline.py
```

Outputs:
- `figures/baseline_uniform_array.png` — phase deviation & amplitude ratio
- `figures/limiting_case_period.png` — mean phase deviation vs period

### Run period sweep

```bash
python run_period_sweep.py
```

Outputs:
- `figures/period_sweep_comparison.png` — uniform vs. non-uniform array

### Generate Week 1 PPT

```bash
python make_pptx.py
```

Outputs:
- `week1_proposal_v2.pptx`

## Key Results (Week 2)

- Single-dipole sanity check passes at machine precision (rel. error ~ 1e-16)
- At P = 0.6 λ, N = 31 uniform array: mean |Δφ| ≈ 6°, max ≈ 8°
- Clear **lattice-resonance peaks** observed at P = m · λ (integer multiples)
- Non-uniform array (graded polarizability) shows additional phase distortion
  outside resonance regions — main topic for Week 3 comparison

## Project Schedule

| Week | Goal |
|------|------|
| 1 | Project proposal |
| 2 | Baseline implementation + sanity check |
| 3 | Controlled comparison (uniform vs non-uniform, period dependence) |
| 4 | Verification (optical theorem, convergence) + final presentation |
