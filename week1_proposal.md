# Week 1 Proposal Presentation (5 min)
## Effect of Inter-Meta-Atom Coupling on Phase Response: Coupled Dipole Approximation
## 메타 원자 간 커플링이 위상 응답에 미치는 영향: Coupled Dipole Approximation

---

## 1. Research Context | 연구 배경

- In metasurface design, each meta-atom is typically treated as **isolated**
- 메타서페이스 설계 시 각 메타 원자를 **독립적(isolated)** 으로 가정

- In reality, adjacent meta-atoms are **electromagnetically coupled**, distorting the phase response
- 실제로는 인접 원자 간 **전자기 커플링**이 존재하여 위상 응답이 왜곡됨

- As the period decreases, coupling strengthens → mismatch between design and actual performance
- 주기가 작을수록 커플링이 강해져, 설계와 실제 성능 사이 불일치 발생

---

## 2. Research Question | 연구 질문

> **"How does the phase distortion caused by inter-meta-atom coupling increase as the array period decreases?"**
>
> **"배열 주기가 줄어들수록 메타 원자 간 커플링에 의한 위상 왜곡이 어떻게 증가하는가?"**

---

## 3. Track A — Build a New Simulation | 시뮬레이션 직접 구축

- Implement a Coupled Dipole Approximation (CDA) simulation from scratch in Python
- CDA 시뮬레이션을 Python으로 처음부터 구현

- Directly code the Green's function + N×N linear system solver
- Green 함수 + N×N 선형 시스템 풀이를 직접 코딩

---

## 4. Model | 모델

- Each meta-atom modeled as a point dipole | 각 메타 원자를 점 쌍극자로 모델링:
  - $p_i = \alpha_i \, E_{\text{loc},i}$

- Local electric field | 국소 전기장:
  - $E_{\text{loc},i} = E_{\text{inc},i} + \sum_{j \neq i} G(r_{ij}) \, p_j$

- Green's function | Green 함수:
  - $G(r) = \frac{i}{4} H_0^{(1)}(k_0 r)$

- Combined into matrix form | 행렬 형태로 결합:
  - $\mathbf{A}\,\mathbf{p} = \mathbf{E}_{\text{inc}}$ → solve linear system | 선형 시스템 풀이

| Item | Description | 항목 | 내용 |
|------|-------------|------|------|
| State variable | Dipole moment $p_i$ (complex) | 상태 변수 | 쌍극자 모멘트 $p_i$ (복소수) |
| Parameters | Period P, polarizability α (Lorentzian), wavelength λ | 파라미터 | 주기 P, 분극률 α (Lorentzian), 파장 λ |
| Boundary condition | Normal-incidence plane wave, finite 1D array | 경계 조건 | 평면파 정상 입사, 유한 1D 배열 |

---

## 5. Input / Output | 입출력

**Input | 입력**: Wavelength λ, array period P (0.5λ ~ 2.0λ), number of meta-atoms N, polarizability α

**Output | 출력**: Dipole phase $\arg(p_i)$ of each atom, phase deviation from isolated case $\Delta\varphi_i$

---

## 6. Metric | 측정 지표

- **Mean phase deviation | 평균 위상 편차**:
  - $\overline{\Delta\varphi} = \frac{1}{N}\sum|\arg(p_i^{\text{coupled}}) - \arg(p_i^{\text{isolated}})|$

- Plot $\overline{\Delta\varphi}(P)$ vs period P → quantify coupling effect
- 주기 P에 대해 $\overline{\Delta\varphi}(P)$ 를 플롯 → 커플링 영향 정량화

---

## 7. Success Criteria | 성공 기준

1. CDA code runs and computes dipole moments | CDA 코드가 동작하여 쌍극자 모멘트를 계산
2. Extract phase deviation: isolated vs coupled | 고립 vs 커플링 위상 편차 추출
3. Complete $\overline{\Delta\varphi}(P)$ graph over period sweep | 주기 스윕에 따른 $\overline{\Delta\varphi}(P)$ 그래프 완성
4. Verify convergence $\Delta\varphi \to 0$ as $P \to \infty$ | P → ∞ 극한에서 $\Delta\varphi \to 0$ 수렴 확인
