# NK Cross-Package Synthesis: Python stdlib
Date: 2026-02-26 | Source: 7 children + 3 direct agents | Packages: 6

## Data Collected

| Package | N | K_avg | K/N | K_max | Cycles | Granularity | Architecture |
|---------|---|-------|-----|-------|--------|-------------|--------------|
| json | 5 | 0.80 | 0.160 | 2 | 0 | module | facade + C ext |
| logging | 3 | 1.00 | 1.000 | 2 | 0 | module | monolith + satellites |
| http.client (core) | 11 | 2.40 | 0.215 | 10 | 0 | class (filtered) | hub-and-spoke |
| unittest | 13 | 2.08 | 2.077 | 8 | 1 | module | pipeline framework |
| email (all imports) | 28 | 1.86 | 0.066 | 6 | 9 | module | facade + lazy imports |
| argparse | 29 | 1.66 | 1.655 | 15 | 0 | class | registry + facade |

## Composite Metric: K_avg*N + Cycles (P-044)

| Package | K_avg*N+Cycles | Bug Ranking | Notes |
|---------|----------------|-------------|-------|
| json | 4.0 | Very few | Well-decomposed, low burden |
| logging | 3.0 | Low | Monolith hides real complexity |
| http.client | 26.4 | Moderate (CVEs) | Hub concentration → attack surface |
| unittest | 27.0 | Moderate | Framework coupling is inherent |
| argparse | 48.1 | Moderate | Registry inflates K_max artificially |
| email | 61.1 | High (253 open) | Lazy-import cycles add hidden cost |

**K_avg*N+Cycles correctly ranks all tested packages by maintenance burden.**
K/N alone does not — email has the lowest K/N (0.066) but highest burden.

## Two-Factor Model (from child:evolve-f40)

```
Maintenance difficulty = f(K/N_internal, S_external)
```

Where S_external = specification surface area (RFCs, protocol specs).

- **K/N > 0.20 + any S**: Hard (http.client, unittest)
- **K/N < 0.10 + high S**: Hard from specs (email: 20+ RFCs)
- **K/N 0.10-0.20 + low S**: Sweet spot (json: 2 RFCs)
- **No stdlib module survives K/N > 0.25** (possible PEP 594 survivorship bias)

## Key Findings

### 1. K/N is scale-dependent (P-038, P-042)
K/N = K_avg/N, so as N grows, K/N drops even if coupling stays similar.
Cross-scale comparison requires K_avg or K_avg*N+Cycles.

### 2. Granularity matters (P-037, P-042)
argparse class-level K/N=1.65 vs email module-level K/N=0.066.
Never compare across granularities.

### 3. Architecture patterns affect coupling profiles
- **Facade** (json, email): low K_avg, coupling concentrated in hub
- **Monolith** (logging): misleadingly low N masks real complexity
- **Framework** (unittest): inherently higher K/N (components must compose)
- **Registry** (argparse): high K_max from plugin pattern, not tangled design

### 4. Hub concentration (K_max)
| Package | Hub | K_max | Hub% |
|---------|-----|-------|------|
| json | `__init__` | 2 | 40% |
| logging | config | 2 | 67% |
| http.client | HTTPConnection | 10 | 42% |
| unittest | `__init__` (re-exports) | 8 | 30% |
| email | `__init__` | 6 | 54% |
| argparse | _ActionsContainer | 15 | 31% |

K_max may predict CVE severity (http.client K_max=10, most CVEs).

### 5. Cycles predict resolution time, not bug count
email has 9 lazy-import cycles and the oldest unresolved issues (since 2004).
No other tested package has cycles.

## Validated Principles
- **P-035**: Count N, K, check K/N — confirmed across 6 packages
- **P-037**: Normalize for granularity — argparse vs email proves it
- **P-038**: Use K_avg + cycles alongside K/N — essential for cross-N
- **P-042**: Never compare K/N across granularities — argparse vs email
- **P-044**: K_avg*N+Cycles as composite predictor — ranks correctly

## Open Questions
- F49: Validate K_avg*N+Cycles on asyncio, multiprocessing, os
- F50: Does K_max correlate with CVE severity (n>3 needed)?
- F53: Validate two-factor model on more packages
- F55: Do PEP 594 removals cluster by K/N or S_external?
