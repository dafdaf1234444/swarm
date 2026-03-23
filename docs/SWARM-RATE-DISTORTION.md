# Rate-Distortion Theory for Knowledge Systems

**Version**: 1.0 (S515)
**Status**: Empirically validated (R²=0.996, N=1380)
**External grounding**: Shannon (1959), Dantzig (1957), Lorenz (1905), Tishby (1999)

## 1. Setup

A **knowledge corpus** is a collection of N items, each with:
- **size** s_i (tokens, bytes, pages)
- **utility** u_i (citations received, access frequency, importance score)

The **compaction problem**: remove items to reduce total size while minimizing utility loss.

## 2. Definitions

**Compression ratio** α ∈ [0,1]: fraction of total size removed.

**Distortion** D(α) ∈ [0,1]: fraction of total utility lost when compressing by α.

**Utility density** ρ_i = u_i / s_i: utility per unit size for item i.

## 3. Theorem 1: Compaction Optimality (Dantzig 1957)

**Statement**: The minimum-distortion compaction at any compression ratio α is achieved by removing items in ascending order of utility density ρ_i.

**Proof**: This is the fractional knapsack problem. Maximize size removed subject to utility lost ≤ D·U_total. The greedy algorithm by ρ_i ascending is optimal.

**Swarm validation**: At 30% compression, optimal (Sharpe) achieves D=9.4% vs random D=27.8% vs size-only D=35.7%.

## 4. Theorem 2: Lorenz-Distortion Identity

**Statement**: The optimal distortion curve D(α) is exactly the Lorenz curve L(α) of the utility distribution, evaluated at the cumulative size fraction.

**Proof**: Sort items by ρ_i ascending. D(α) = Σ_{i≤αN} u_i / Σ_i u_i = L(α) by definition of the Lorenz curve.

**Corollary 1 (Favorable Compression)**: For any non-degenerate utility distribution, L(α) < α for α ∈ (0,1). Therefore distortion is always less than compression ratio. Compression is always favorable.

**Corollary 2 (Gini = Compression Advantage)**: The Gini coefficient G = 2∫₀¹[α − L(α)]dα measures the total area of advantage between random and optimal compression strategies.

**Corollary 3 (Universal β > 1)**: If D(α) ≈ A·α^β, then β > 1 for any non-degenerate distribution (by Lorenz convexity).

## 5. Theorem 3: R(D) Power Law

**Empirical finding**: D(α) = A·α^β with:
- Swarm (N=1380, Gini=0.46): A=0.67, β=1.65, R²=0.996
- Synthetic library (N=100, Gini=0.66): A=0.46, β=2.26, R²=0.991
- Synthetic Zipf(0.3) (N=200, Gini=0.17): A=?, β=1.26, R²=0.992

**Prediction**: β > 1 universally (proven via Lorenz convexity). Higher concentration → higher β → more efficient compression.

**Closed-form compression budget**: For distortion budget D_max, the maximum safe compression is:

    α_max = (D_max / A)^(1/β)

Swarm examples:
| D_max | α_max | Tokens freed | Lesson-equivalents |
|-------|-------|--------------|--------------------|
| 1%    | 7.8%  | 34,400       | 108                |
| 5%    | 20.7% | 91,300       | 286                |
| 10%   | 31.6% | 139,200      | 436                |

## 6. Theorem 4: Information Bottleneck

**Statement**: Given a fixed-capacity channel (context window W), the maximum retrievable utility per session is:

    F_max = max{F : T_W(F) ≤ W}

where T_W(F) is the total size of the working set needed to capture fraction F of utility.

**Swarm measurement**:
| Utility fraction | Working set | Tokens needed | Fits in 180k? |
|-----------------|-------------|---------------|---------------|
| 50%             | 268 lessons | 81,938        | ✓             |
| 80%             | 714 lessons | 219,795       | ✗             |
| 90%             | 955 lessons | 296,974       | ✗             |

**F_max = 73.2%** — the swarm can access at most 73.2% of its utility per session. 26.8% is structurally inaccessible.

## 7. Theorem 5: Growth Limit

**Statement**: As N grows with fixed channel capacity W:

    F_max(N) ≈ W / (f_ws · N · t̄)

where f_ws ≈ 0.194 is the working-set fraction for 50% utility and t̄ ≈ 320 is mean item size.

**Critical threshold**: F_max drops to 50% at N_critical = W / (f_ws · t̄) ≈ **2,900 lessons**.

Current N = 1,380. Growth ratio = 0.476 (47.6% of crisis threshold).

**Falsifiable prediction**: If N reaches 2,500 and F_max remains >60%, the growth limit model is falsified.

## 8. Strategy Comparison

At 30% compression (removing 30% of items by count):

| Strategy | Distortion | Relative to optimal |
|----------|-----------|-------------------|
| **Optimal (density sort)** | 9.6% | 1.0× |
| Random | 26.3% | 2.7× |
| Size-only (remove largest) | 35.7% | 3.7× |

The optimal strategy achieves **2.7× less distortion** than random at the same compression level.

## 9. External Applications

This theory applies to any knowledge system. The tool `tools/rate_distortion.py` accepts JSON input:

```json
[{"id": "item-1", "size": 100, "utility": 50}, ...]
```

Usage:
```bash
python3 tools/rate_distortion.py --input data.json --capacity 10000
python3 tools/rate_distortion.py --swarm  # analyze swarm corpus
```

**Universal principle**: The Gini coefficient of your utility distribution tells you how much you can compress for free. Higher Gini = more compressible = less pain from archival.

## 10. Negative Results

1. **Gini→β prediction**: Weak (R²=0.17). β does not scale linearly with Gini — the relationship is more complex and distribution-dependent.
2. **Shannon R(D) function**: Classical Gaussian R(D) = ½log(σ²/D) does NOT apply — the discrete, heavy-tailed citation distribution requires the power-law model instead.
3. **Channel capacity formula**: Shannon's C = B·log(1+SNR) is ill-suited because the "noise" in knowledge retrieval is search failure, not additive Gaussian noise.

## References

- Shannon, C. E. (1959). Coding theorems for a discrete source with a fidelity criterion.
- Dantzig, G. B. (1957). Discrete-variable extremum problems. Operations Research.
- Lorenz, M. O. (1905). Methods of measuring the concentration of wealth.
- Tishby, N., Pereira, F. C., & Bialek, W. (1999). The information bottleneck method.
- Gini, C. (1912). Variabilità e mutabilità.
