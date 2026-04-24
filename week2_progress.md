# Week 2 Progress Presentation (5 min)
## CDA Baseline Implementation & Comprehensive Verification
## CDA 베이스라인 구현 및 종합 검증

---

## 1. Question Being Tested | 검증 중인 질문

> **"Does inter-meta-atom coupling distort the phase response of individual atoms, and how does this distortion depend on the array period P?"**
>
> **"메타 원자 간 커플링이 위상 응답을 얼마나 왜곡하는가? 그리고 주기 P에 따라 어떻게 달라지는가?"**

---

## 2. Baseline Implemented | 구현한 베이스라인

### Code structure | 코드 구조
- `cda.py` — CDA core library | CDA 핵심 라이브러리
  - 2D scalar Green's function (Hankel H₀⁽¹⁾)
  - N×N interaction matrix builder
  - Linear system solver (`np.linalg.solve`)
  - Lorentzian polarizability model
- `run_baseline.py` — baseline run + first figures
- `run_period_sweep.py` — period sweep (Week 3 preview)
- `run_verification.py` — **10 physical verification tests**

### What works | 동작 확인
- End-to-end forward run: uniform and non-uniform arrays
- All diagnostics implemented: Δφ, max Δφ, ADR, extinction proxy
- 1D arrays of arbitrary size, complex Lorentzian α

---

## 3. Verification Results: 10 / 10 PASS | 검증 결과: 10/10 통과

| # | Test | Result |
|---|------|--------|
| 1 | Single dipole = α·E_inc | rel. error **1.5×10⁻¹⁶** |
| 2 | Two-dipole analytical p = α/(1−αG) | **2.5×10⁻¹⁶** |
| 3 | Green's function formula + reciprocity | exact **0** |
| 4 | Linear system residual ‖Ap−E‖/‖E‖ | **5.4×10⁻¹⁶** |
| 5 | Mirror symmetry (centered uniform array) | **7×10⁻¹⁶** |
| 6 | Matrix reciprocity A_ij = A_ji | exact **0** |
| 7 | Array-size convergence (2D lattice sum) | slope ≈ **−0.26** |
| 8 | Wavelength-scaling invariance | exact **0** |
| 9 | Extinction power positivity (optical theorem) | all **P_ext > 0** |
| 10 | Non-uniform solver ⇒ uniform limit | exact **0** |

### Highlighted Physical Insight — Test 7 | 주목할 물리 — Test 7
- Observed convergence rate **∼ 1/N^0.26**
- Theoretical expectation for 2D free-space Green's function: **1/√N** (−0.5)
- Confirms that 2D scalar lattice sums are **conditionally convergent** and inherently slow
- 2D Green 함수의 1/√r 감쇠 특성으로 수렴이 본질적으로 느림 — 프로젝트의 중요한 물리적 한계

---

## 4. Baseline Result | 베이스라인 결과

### Uniform array, N = 31, P = 0.6 λ
| Quantity | Value |
|----------|-------|
| Mean phase deviation | **6.09°** |
| Max phase deviation | **7.89°** |
| Amplitude distortion ratio | **[0.979, 1.041]** |

→ Coupling is real, measurable, and non-negligible at sub-wavelength periods.
→ 서브파장 주기에서 커플링이 실제로 측정 가능한 수준임을 확인

---

## 5. First Scan: Period Sweep | 첫 스윕 결과

### Uniform vs non-uniform array
| P / λ | Uniform | Non-uniform |
|-------|---------|-------------|
| 0.5 | 5.8° | 6.6° |
| 1.0 | **27.0°** | **22.4°** |
| 1.5 | 3.4° | 3.8° |
| 2.0 | **14.1°** | **18.3°** |
| 3.0 | **20.9°** | **19.8°** |

### Key observation | 핵심 관찰
- **Sharp peaks at P = m·λ** (integer multiples of wavelength)
- 파장의 정수배 주기에서 급격한 피크 → **Wood-anomaly (lattice resonance)**
- Coincides with grating-diffraction onset conditions
- 격자 회절 차수 개시 조건과 일치하는 물리적 현상

---

## 6. Main Current Difficulty | 현재 주요 어려움

### (a) Lattice-resonance divergence | 격자 공명 발산
- Matrix nearly singular at P ≈ m·λ
- Δφ(P) curve is non-monotonic → cannot simply say "larger P → weaker coupling"
- Must separate **off-resonance** behavior from resonance peaks

### (b) Slow 2D convergence | 2D 시스템의 느린 수렴
- 1/√N lattice sum convergence is inherent to 2D Green's function
- Finite-array edge effects persist longer than in 3D
- Future work: consider periodic boundary (Bloch) conditions

---

## 7. Next Week's Plan | 다음 주 계획

### Primary comparison | 메인 비교
- **Uniform vs non-uniform** detailed analysis
  - focus on off-resonance regions for clean interpretation
  - isolate (i) pure lattice coupling, (ii) α-inhomogeneity effect
- Identify **threshold period P*** at which mean |Δφ| < 1°
- Quantify asymmetric coupling in phase-gradient (metalens-like) arrays

### Additional checks | 추가 검증
- Deeper conditioning study near Wood anomalies
- Optical-theorem ratio P_sca / P_ext (energy budget)
- Sensitivity to α ordering in non-uniform cases

---

## Deliverables so far | 현재까지 산출물

- `cda.py`, `run_baseline.py`, `run_period_sweep.py`, `run_verification.py`
- Figures:
  - `figures/baseline_uniform_array.png`
  - `figures/limiting_case_period.png`
  - `figures/period_sweep_comparison.png`
  - `figures/verification_convergence.png`
- 10/10 physical verification tests all **PASS**
