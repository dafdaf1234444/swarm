# NK Cross-Package Synthesis: Python stdlib
Date: 2026-02-26 | Source: Children (complexity-test, concurrent-a, concurrent-b)

## Data Collected

| Package | N | K_avg | K/N | K_max | Cycles | Granularity |
|---------|---|-------|-----|-------|--------|-------------|
| json | 5 | 0.80 | 0.160 | 2 | 0 | module |
| http.client | 24 | 1.62 | 0.068 | 10 | 0 | class/function |
| http.client (core) | 11 | ~2.4 | 0.215 | 10 | 0 | class (filtered) |
| email (static) | 28 | 1.68 | 0.060 | 5 | 0 | module |
| email (all imports) | 28 | 1.86 | 0.066 | 6 | 9 | module |

## Key Findings

### 1. K/N is scale-dependent (P-038)
K/N = K_avg / N, so as N grows, K/N drops even if absolute coupling stays similar.
- json (N=5): K/N = 0.16
- email (N=28): K/N = 0.06
Yet email is objectively more complex (more cycles, higher K_max, more files).

**Conclusion**: K/N is useful for comparing systems at similar N. For cross-scale
comparison, use K_avg + cycle count + K_max instead.

### 2. Granularity matters (P-037)
http.client raw K/N = 0.068 (class-level), but filtering trivial exception classes
gives K/N = 0.215 (core-only). The "right" N depends on what you're measuring.

**Rule**: Always state granularity and filtering criteria alongside K/N.

### 3. Common design patterns
- **Facade pattern** (json, email): `__init__.py` exposes public API, hides internal structure.
  Keeps K_avg low by concentrating coupling in one hub.
- **Lazy imports** (email): Function-body imports break cycles without adding static K.
  9 cycles exist but only through lazy imports — at static level, the graph is a DAG.
- **C extension externalization** (json): `_json` kept outside package, imported via try/except.
  Preserves low K while gaining performance.

### 4. Hub concentration
- json: `__init__.py` is the hub (K=2, all others K≤1)
- http.client: `HTTPConnection` is the hub (K=10, 42% of all edges)
- email: `__init__` is the hub (15 dependents, 54% of all modules)

All three packages concentrate coupling in 1-2 hub nodes. This appears to be a
deliberate design pattern for near-decomposability.

## Proposed Composite Metric

For cross-package NK comparison, use a **Complexity Profile**:

```
Package     | K_avg | K_max | K_max/N | Cycles | Hub% |
json        | 0.80  | 2     | 0.40    | 0      | 40%  |
http.client | 1.62  | 10    | 0.42    | 0      | 42%  |
email       | 1.86  | 6     | 0.21    | 9      | 54%  |
```

Where Hub% = edges through the top hub / total edges.

## Open Questions
- Does hub concentration correlate with maintenance burden?
- Is K_max/N a better predictor of bug density than K/N?
- What is the "healthy" range for each metric?
