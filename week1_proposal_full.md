# Week 1 Proposal Presentation
## Effect of Inter-Meta-Atom Coupling on Phase Response: Coupled Dipole Approximation
## 메타 원자 간 상호작용이 위상 응답에 미치는 영향: Coupled Dipole Approximation 기반 분석

---

## Slide 1: Research Context | 연구 배경

### Fundamental assumption in metasurface design | 메타서페이스 설계의 기본 가정
- Metasurfaces are 2D arrays of sub-wavelength nanostructures (meta-atoms)
- 메타서페이스는 서브파장 나노구조(메타 원자)의 2D 배열
- Each meta-atom is typically treated as **isolated** during the design process
- 설계 시 각 메타 원자를 **독립적(isolated)** 으로 취급하는 것이 일반적
- Individual scattering properties (phase, amplitude) are computed first, then applied to the array
- 즉, 개별 메타 원자의 산란 특성(위상, 진폭)을 먼저 계산하고, 이를 배열에 그대로 적용

### The Problem: Coupling Effect | 문제: 상호작용(Coupling) 효과
- In reality, meta-atoms are **electromagnetically coupled** to each other
- 실제로 메타 원자들은 서로 **전자기적으로 커플링**됨
- Light scattered by one meta-atom impinges on adjacent ones, altering their response
- 한 메타 원자가 산란한 빛이 인접 메타 원자에 입사하여 응답을 변화시킴
- This coupling strengthens as the spacing (period) decreases
- 메타 원자 간 간격(주기)이 작을수록 이 상호작용이 강해짐
- This causes **mismatch** between the designed and actual performance
- 이로 인해 설계와 실제 성능 사이에 **불일치**가 발생할 수 있음

### Why it matters | 왜 중요한가?
- Phase precision is critical in high-efficiency metalenses, holograms, etc.
- 고효율 메타렌즈, 홀로그램 등에서 위상 정밀도가 핵심
- Phase distortion from coupling can degrade focusing efficiency and beam quality
- 커플링으로 인한 위상 왜곡이 초점 효율, 빔 품질을 저하시킬 수 있음
- Quantitative understanding of coupling enables more accurate metasurface design
- 커플링 효과를 정량적으로 이해하면, 보다 정확한 메타서페이스 설계가 가능

---

## Slide 2: Research Question | 연구 질문

> **"How much does electromagnetic coupling between meta-atoms distort the phase response of individual atoms? How does this distortion increase as the array period decreases?"**
>
> **"메타 원자 간 전자기 커플링이 개별 원자의 위상 응답을 얼마나 왜곡하는가? 배열 주기가 줄어들수록 이 왜곡은 어떻게 증가하는가?"**

### Sub-questions | 세부 질문
1. How different is the phase response of an isolated meta-atom vs. one embedded in an array?
   고립된 메타 원자의 위상 응답과 배열 내 메타 원자의 위상 응답은 얼마나 다른가?
2. How does the phase deviation change as the period P varies from λ/2 to 2λ?
   주기(P)가 λ/2에서 2λ로 변할 때 위상 편차가 어떻게 변화하는가?
3. Does the coupling effect differ between uniform arrays (identical atoms) and non-uniform arrays (varying atoms)?
   균일 배열(동일 원자)과 비균일 배열(서로 다른 원자)에서 커플링 효과가 다른가?
4. Is there a threshold period below which coupling cannot be ignored?
   커플링 효과를 무시해도 괜찮은 주기의 임계값이 존재하는가?

---

## Slide 3: Track Selection | 프로젝트 트랙 선택

### Track A: Build a New Simulation | 시뮬레이션 직접 구축
- Implement Coupled Dipole Approximation (CDA) simulation **from scratch**
- CDA 시뮬레이션을 **처음부터 직접 구현**
- Python + NumPy/SciPy based
- Python + NumPy/SciPy 기반
- Directly code the dipole model + Green's function + linear system solver
- 쌍극자 모델 + Green 함수 + 선형 시스템 풀이를 직접 코딩

---

## Slide 4: Physical Model | 물리 모델

### Coupled Dipole Approximation (CDA)

Each meta-atom $i$ is modeled as a **point electric dipole**:
각 메타 원자 $i$를 **점 전기 쌍극자**로 모델링:

$$\mathbf{p}_i = \alpha_i \, \mathbf{E}_{\text{loc},i}$$

- $\mathbf{p}_i$: induced dipole moment of the $i$-th meta-atom | $i$번째 메타 원자의 유도 쌍극자 모멘트
- $\alpha_i$: polarizability of the $i$-th meta-atom | $i$번째 메타 원자의 분극률
- $\mathbf{E}_{\text{loc},i}$: local electric field at position $i$ | $i$번째 위치에서의 국소 전기장

### Local Electric Field | 국소 전기장

$$\mathbf{E}_{\text{loc},i} = \mathbf{E}_{\text{inc},i} + \sum_{j \neq i} \mathbf{G}(\mathbf{r}_i, \mathbf{r}_j) \, \mathbf{p}_j$$

- $\mathbf{E}_{\text{inc},i}$: incident plane wave field at position $i$ | 입사 평면파가 $i$번 위치에 만드는 전기장
- $\mathbf{G}(\mathbf{r}_i, \mathbf{r}_j)$: free-space dipole Green's function (tensor) | 자유 공간 쌍극자 Green 함수 (텐서)
- The second term represents **coupling from other meta-atoms** | 두 번째 항이 **다른 메타 원자들로부터의 커플링**

### Free-space Green's Function (2D scalar simplification) | 자유 공간 Green 함수 (2D 스칼라 단순화)

$$G(r_{ij}) = \frac{i}{4} H_0^{(1)}(k_0 \, r_{ij})$$

- $H_0^{(1)}$: Hankel function of the first kind (0th order) | 제1종 Hankel 함수 (0차)
- $k_0 = 2\pi / \lambda$
- $r_{ij} = |\mathbf{r}_i - \mathbf{r}_j|$

### 3D Tensor Green's Function (full vectorial) | 3D 텐서 Green 함수

$$\mathbf{G}(\mathbf{r}) = \frac{e^{ik_0 r}}{4\pi r}\left[\left(1 + \frac{ik_0 r - 1}{k_0^2 r^2}\right)\mathbf{I} + \left(\frac{3 - 3ik_0 r - k_0^2 r^2}{k_0^2 r^2}\right)\frac{\mathbf{r}\otimes\mathbf{r}}{r^2}\right]$$

(Start with scalar 2D model; extend to 3D tensor if time permits)
(구현 시 스칼라 2D 모델로 시작하고, 여력이 되면 3D 텐서로 확장)

### Linear System | 선형 시스템

Combining all dipoles | 모든 쌍극자에 대해 결합하면:

$$\sum_j \left(\frac{\delta_{ij}}{\alpha_j} - G_{ij}(1-\delta_{ij})\right) p_j = E_{\text{inc},i}$$

Matrix form | 행렬 형태:

$$\mathbf{A} \, \mathbf{p} = \mathbf{E}_{\text{inc}}$$

$$A_{ij} = \begin{cases} 1/\alpha_i & \text{if } i = j \\ -G(\mathbf{r}_i, \mathbf{r}_j) & \text{if } i \neq j \end{cases}$$

→ Solve the $N \times N$ linear system for all dipole moments $\mathbf{p}$
→ $N \times N$ 선형 시스템을 풀어 모든 쌍극자 모멘트 $\mathbf{p}$를 구함

---

## Slide 5: Polarizability Model | 분극률 모델

### Lorentzian Polarizability | Lorentzian 분극률

The resonant response of a meta-atom is described by the Lorentz model:
메타 원자의 공진 응답을 Lorentz 모델로 기술:

$$\alpha(\omega) = \frac{F}{\omega_0^2 - \omega^2 - i\gamma\omega}$$

- $\omega_0$: resonance frequency | 공진 주파수
- $\gamma$: damping rate (linewidth) | 감쇠율
- $F$: oscillator strength | 진동자 강도

### Geometry → Polarizability Mapping | 기하학적 파라미터 → 분극률 매핑
- Varying the meta-atom size (width, height) shifts $\omega_0$
- 메타 원자의 크기(폭, 높이)를 변화시키면 $\omega_0$이 이동
- This shift changes the transmission phase at a given wavelength
- $\omega_0$의 변화로 특정 파장에서의 투과 위상이 달라짐
- Meta-atoms with different $\omega_0$ are arranged to form a phase profile
- 서로 다른 $\omega_0$을 가진 메타 원자를 배열에 배치하여 위상 프로파일 구성

---

## Slide 6: Simulation Input / Output | 시뮬레이션 입출력

### Input | 입력
| Parameter | Symbol | Value / Range | 파라미터 | 값 / 범위 |
|-----------|--------|---------------|----------|-----------|
| Wavelength | λ | Normalized to design wavelength | 파장 | 설계 파장 기준 정규화 |
| Array period | P | 0.5λ ~ 2.0λ (sweep) | 배열 주기 | 0.5λ ~ 2.0λ (스윕) |
| Number of meta-atoms | N | 1D: 20~100 | 메타 원자 수 | 1D: 20~100개 |
| Polarizability | α | Lorentzian model | 분극률 | Lorentzian 모델 |
| Resonance frequency | ω₀ | May vary per atom | 공진 주파수 | 원자마다 다를 수 있음 |
| Incident wave | E_inc | Plane wave (normal incidence) | 입사파 | 평면파 (정상 입사) |

### Output | 출력
- Induced dipole moment $p_i$ of each meta-atom (complex) | 각 메타 원자의 유도 쌍극자 모멘트 $p_i$ (복소수)
- **Phase** of $p_i$: actual phase response within the array | $p_i$의 **위상**: 배열 내 메타 원자의 실제 위상 응답
- **Isolated response**: $p_i^{\text{iso}} = \alpha_i \cdot E_{\text{inc},i}$ (no coupling) | **고립 응답**: $p_i^{\text{iso}} = \alpha_i \cdot E_{\text{inc},i}$ (커플링 무시)
- **Phase deviation**: $\Delta\varphi_i = \arg(p_i) - \arg(p_i^{\text{iso}})$ | **위상 편차**: $\Delta\varphi_i = \arg(p_i) - \arg(p_i^{\text{iso}})$

---

## Slide 7: Quantitative Metrics | 정량 지표

### 1. Phase Deviation | 위상 편차

$$\Delta\varphi_i = \arg(p_i^{\text{coupled}}) - \arg(p_i^{\text{isolated}})$$

Mean phase deviation across the array | 배열 전체의 평균 위상 편차:

$$\overline{\Delta\varphi} = \frac{1}{N}\sum_{i=1}^{N}|\Delta\varphi_i|$$

### 2. Maximum Phase Deviation | 위상 편차의 최댓값

$$\Delta\varphi_{\max} = \max_i |\Delta\varphi_i|$$

### 3. Amplitude Distortion Ratio (ADR) | 진폭 왜곡 비

$$\text{ADR}_i = \frac{|p_i^{\text{coupled}}|}{|p_i^{\text{isolated}}|}$$

Ideally ADR = 1 | 이상적이면 ADR = 1

### 4. Optical Theorem Check | 에너지 보존 검증

Verify that the extinction cross-section satisfies the optical theorem:
소광 단면적이 optical theorem과 일치하는지 확인:

$$\sigma_{\text{ext}} = \frac{4\pi k_0}{|E_0|^2} \sum_i \text{Im}\!\left(E_{\text{inc},i}^* \cdot p_i\right)$$

---

## Slide 8: Controlled Comparison | 비교 실험 설계

### Main comparison: Period (P) sweep | 메인 비교: 주기(P) 스윕

| Period | P/λ | Expected coupling | 주기 | 예상 커플링 강도 |
|--------|-----|-------------------|------|------------------|
| Dense | 0.5 | Strong coupling, large phase distortion | 밀집 | 강한 커플링, 큰 위상 왜곡 |
| Medium | 1.0 | Moderate | 중간 | 중간 수준 |
| Sparse | 1.5 | Weak coupling | 희박 | 약한 커플링 |
| Very sparse | 2.0 | Nearly isolated → baseline | 매우 희박 | 거의 고립 → 기준선 |

Fixed variables: identical meta-atoms (uniform array), same wavelength, same incidence
고정 변수: 동일한 메타 원자 (균일 배열), 동일 파장, 동일 입사 조건

### Additional comparison: Uniform vs Non-uniform array | 추가 비교: 균일 vs 비균일 배열

| Condition | Description | 조건 | 설명 |
|-----------|-------------|------|------|
| Uniform | All meta-atoms identical (same α) | 균일 배열 | 모든 메타 원자 동일 (같은 α) |
| Non-uniform | Each meta-atom has different α (phase gradient) | 비균일 배열 | 각 메타 원자 α가 다름 (위상 그래디언트) |

---

## Slide 9: Verification Plan | 검증 계획

### 1. Analytical comparison (Sanity Check) | 해석해 비교
- Single meta-atom (isolated): CDA result vs $p = \alpha \cdot E_{\text{inc}}$ direct calculation
- 메타 원자 1개 (고립): CDA 결과 vs $p = \alpha \cdot E_{\text{inc}}$ 직접 계산
- Two meta-atoms: compare with analytical 2-dipole coupling solution
- 메타 원자 2개: 해석적 2-dipole 커플링 해와 비교

### 2. Limiting case verification | 극한 검증
- Period P → ∞: coupled phase → isolated phase convergence
- 주기 P → ∞: 커플링된 위상 → 고립 위상으로 수렴 확인
- $\Delta\varphi \to 0$ as $P \to \infty$

### 3. Optical Theorem check (Conservation) | Optical Theorem 확인
- Verify extinction cross-section satisfies the optical theorem
- 소광 단면적이 optical theorem과 일치하는지 검증

### 4. Convergence check (Robustness) | 수렴성 검사
- Check if the central atom's phase deviation converges as array size N increases
- 배열 원자 수 N 변화 시 중심 원자의 위상 편차가 수렴하는지 확인

---

## Slide 10: Success Criteria | 성공 기준

### Minimum Viable Project | 최소 완성 기준
1. Build and solve the CDA linear system to compute dipole moments
   CDA 선형 시스템을 구축하고 풀어서 쌍극자 모멘트를 계산
2. Extract phase deviation between isolated and coupled responses
   고립 응답 vs 커플링 응답의 위상 차이를 추출
3. At least one $\overline{\Delta\varphi}(P)$ graph over a period sweep
   주기(P) 스윕에 따른 위상 편차 그래프 1개 이상
4. Verify analytical match for a single isolated dipole
   1개 고립 쌍극자에서 해석해와 일치 확인

### Full Project (Target) | 완전 프로젝트 (목표)
- All of the above | 위 항목 전부
- Uniform vs non-uniform array comparison | 균일 vs 비균일 배열 비교
- Optical theorem verification | Optical theorem 검증
- Array size convergence analysis | 배열 크기 수렴성 분석
- Quantitative threshold: at what period can coupling be safely ignored?
  "커플링을 무시해도 되는 주기 임계값" 정량적 제시
- Discussion of physical interpretation and limitations
  물리적 해석 및 한계점 논의

---

## Slide 11: Expected Results | 예상 결과

### Qualitative expectations | 정성적 예상
- **P < λ**: Strong coupling → phase deviation of tens of degrees or more
  강한 커플링 → 위상 편차 수십 도 이상
- **P ≈ λ**: Moderate → phase deviation of a few to ~10 degrees
  중간 수준 → 위상 편차 수 도 ~ 십수 도
- **P > 1.5λ**: Weak coupling → phase deviation within a few degrees
  커플링 약화 → 위상 편차 수 도 이내
- **P > 2λ**: Nearly identical to isolated case
  거의 고립과 동일

### Quantitative expectations (based on Green's function decay) | 정량적 예상
- 2D Green's function: $|G| \sim 1/\sqrt{r}$ (far field) → slow decay, distant atoms still contribute
  2D Green 함수: $|G| \sim 1/\sqrt{r}$ (원거리) → 완만한 감쇠, 먼 원자도 기여
- 3D Green's function: $|G| \sim 1/r$ → faster decay
  3D Green 함수: $|G| \sim 1/r$ → 더 빠른 감쇠

### Additional effects in non-uniform arrays | 비균일 배열에서의 추가 효과
- When adjacent atoms have different α, coupling pattern becomes asymmetric
  인접 원자의 α가 다르면 커플링 패턴이 비대칭적
- Regions with steep phase gradients are expected to have larger phase distortion
  위상 그래디언트가 급한 영역에서 위상 왜곡이 더 클 것으로 예상

---

## Slide 12: Timeline | 프로젝트 일정

| Week | Goal | Deliverable | 주차 | 목표 | 산출물 |
|------|------|-------------|------|------|--------|
| 1 | Project design, proposal presentation | This presentation | 1 | 프로젝트 설계, 제안 발표 | 본 발표 자료 |
| 2 | Implement CDA (Green's function + linear system), 1-dipole verification | Code + analytical comparison | 2 | CDA 구현, 1-dipole 검증 | 코드 + 해석해 비교 |
| 3 | Period sweep comparison, uniform vs non-uniform | Phase deviation graphs + interpretation | 3 | 주기 스윕 비교, 균일 vs 비균일 | 위상 편차 그래프 + 해석 |
| 4 | Optical theorem verification, convergence analysis, final presentation | Final presentation + code | 4 | 검증, 수렴성 분석, 최종 발표 | 최종 발표 + 코드 |

---

## Slide 13: Limitations and Assumptions | 한계점 및 가정

1. **Point dipole approximation | 점 쌍극자 근사**: Meta-atoms treated as points → valid only when atom size is small relative to the period
   메타 원자를 점으로 취급 → 원자 크기가 주기에 비해 작아야 유효
2. **Electric dipole only | 전기 쌍극자만 고려**: Real dielectric meta-atoms also support magnetic dipoles and higher-order multipoles
   실제 유전체 메타 원자는 자기 쌍극자 및 고차 다중극도 기여
3. **No substrate | 기판 효과 무시**: Free-space Green's function used → substrate reflection/transmission not included
   자유 공간 Green 함수 사용 → 기판 반사/투과 미포함
4. **Scalar model first | 스칼라 모델로 시작**: Vector polarization effects considered in extension phase
   벡터 편광 효과는 확장 단계에서 고려
5. **Finite array | 유한 배열**: Does not exactly match Bloch modes of infinite periodic structures (edge effect)
   무한 주기 구조의 Bloch 모드와 정확히 일치하지 않음

These limitations will be explicitly discussed in the final presentation.
이러한 한계점은 최종 발표에서 명시적으로 논의할 예정
