# NK Landscape Analysis: Python `unittest` Package

**Date**: 2026-02-26
**Python version**: 3.12
**Source**: `/usr/lib/python3.12/unittest/`

## 1. Component Inventory (N)

The `unittest` package contains **N = 13** Python modules:

| # | Module | Lines | Role |
|---|--------|------:|------|
| 1 | `__init__` | 85 | Package entry point, re-exports public API |
| 2 | `__main__` | 18 | CLI entry point (`python -m unittest`) |
| 3 | `_log` | 86 | Logging assertion support (`assertLogs`, `assertNoLogs`) |
| 4 | `async_case` | 142 | `IsolatedAsyncioTestCase` for async tests |
| 5 | `case` | 1,456 | Core `TestCase` class, assertions, decorators |
| 6 | `loader` | 495 | `TestLoader`, test discovery |
| 7 | `main` | 291 | `TestProgram`, CLI argument parsing |
| 8 | `mock` | 3,022 | `Mock`, `MagicMock`, `patch`, `AsyncMock` |
| 9 | `result` | 256 | `TestResult` base class |
| 10 | `runner` | 292 | `TextTestRunner`, `TextTestResult` |
| 11 | `signals` | 71 | SIGINT handling for graceful Ctrl-C |
| 12 | `suite` | 379 | `TestSuite`, `BaseTestSuite`, fixture orchestration |
| 13 | `util` | 170 | Pure utility functions (`safe_repr`, `strclass`, diff helpers) |

**Total**: 6,763 lines of code.

The `mock` module alone is 3,022 lines (44.7% of the package), making it the dominant component by size.

## 2. Dependency Map (K)

Internal dependencies between modules (directed edges: A depends on B):

```
__init__  --> async_case, case, loader, main, result, runner, signals, suite
__main__  --> main
_log      --> case
async_case --> case
case      --> _log (lazy), result, util
loader    --> case, suite, util
main      --> loader, runner, signals
mock      --> util (via absolute import: from unittest.util import safe_repr)
result    --> util
runner    --> case, result, signals
signals   --> (none)
suite     --> case, util
util      --> (none)
```

### Dependency Matrix

Rows depend on columns. `X` = direct dependency.

```
              __init__ __main__ _log async case loader main mock result runner signals suite util
__init__         .       .       .    X     X     X     X    .     X     X      X      X     .
__main__         .       .       .    .     .     .     X    .     .     .      .      .     .
_log             .       .       .    .     X     .     .    .     .     .      .      .     .
async_case       .       .       .    .     X     .     .    .     .     .      .      .     .
case             .       .       X    .     .     .     .    .     X     .      .      .     X
loader           .       .       .    .     X     .     .    .     .     .      .      X     X
main             .       .       .    .     .     X     .    .     .     X      X      .     .
mock             .       .       .    .     .     .     .    .     .     .      .      .     X
result           .       .       .    .     .     .     .    .     .     .      .      .     X
runner           .       .       .    .     X     .     .    .     X     .      X      .     .
signals          .       .       .    .     .     .     .    .     .     .      .      .     .
suite            .       .       .    .     X     .     .    .     .     .      .      .     X
util             .       .       .    .     .     .     .    .     .     .      .      .     .
```

## 3. Key Metrics

| Metric | All Modules (N=13) | Core Modules (N=11)* |
|--------|-------------------:|---------------------:|
| **N** | 13 | 11 |
| **K** (total directed edges) | 27 | 18 |
| **K/N** (avg deps per module) | 2.077 | 1.636 |
| **K_avg** | 2.077 | 1.636 |
| **K_max** | 8 (`__init__`) | 3 (case, loader, main, runner) |
| **Density** (K / N(N-1)) | 0.173 | 0.164 |

*Core excludes `__init__` and `__main__`, which are structural entry points rather than functional components.

### Out-degree (how many modules each depends on)

| Module | Out-degree | Role |
|--------|----------:|----|
| `__init__` | 8 | Re-export hub (structural, not functional) |
| `case` | 3 | Core test case |
| `loader` | 3 | Test discovery |
| `main` | 3 | CLI program |
| `runner` | 3 | Test execution |
| `suite` | 2 | Test grouping |
| `__main__` | 1 | CLI entry |
| `_log` | 1 | Logging assertions |
| `async_case` | 1 | Async tests |
| `mock` | 1 | Mocking framework |
| `result` | 1 | Result storage |
| `signals` | 0 | Leaf (standalone) |
| `util` | 0 | Leaf (standalone) |

### In-degree (how many modules depend on each)

| Module | In-degree | Assessment |
|--------|----------:|------------|
| `case` | **6** | **Primary hub** -- the gravitational center |
| `util` | **5** | **Utility hub** -- pure functions, healthy dependency |
| `result` | 3 | Mid-tier |
| `signals` | 3 | Mid-tier |
| `loader` | 2 | Standard |
| `main` | 2 | Standard |
| `runner` | 2 | Standard |
| `suite` | 2 | Standard |
| `_log` | 1 | Low |
| `async_case` | 1 | Low |
| `__init__` | 0 | Root (no one imports the init) |
| `__main__` | 0 | Root |
| `mock` | 0 | **Isolated satellite** |

## 4. Cycle Analysis

**One cycle detected:**

```
case --> _log --> case
```

`case.py` lazily imports `_log` inside the `assertLogs()` and `assertNoLogs()` methods. `_log.py` imports `_BaseTestCaseContext` from `case`. This is a **managed mutual dependency** -- the lazy import in `case.py` breaks the import-time cycle, so Python does not encounter a circular import error at module load.

**Assessment**: This is a pragmatic extraction pattern. The `_log` module was factored out of `case` to reduce the size of an already-large module (1,456 lines), but the two remain logically coupled. The lazy import makes the cycle invisible at import time, so it is harmless in practice.

No other cycles exist. The remaining graph is a clean **DAG** (directed acyclic graph).

## 5. Comparison with Benchmarks

| Package | N | K | K/N | Density | Notes |
|---------|--:|--:|----:|--------:|-------|
| `json` | 5 | ~0.8 | **0.16** | 0.040 | Very low coupling, well-decomposed |
| `email` | 28 | ~1.7 | **0.06** | 0.002 | Many modules, sparse coupling |
| `http.client` (raw) | 24 | ~1.6 | **0.068** | 0.003 | Broadly distributed |
| `http.client` (core) | - | - | **0.215** | - | Higher when filtered to core |
| **`unittest` (all)** | **13** | **27** | **2.077** | **0.173** | Moderately coupled |
| **`unittest` (core)** | **11** | **18** | **1.636** | **0.164** | Still notably coupled |

The `unittest` K/N of **2.077** is an order of magnitude higher than `json` (0.16) or `email` (0.06). However, context matters:

1. **`__init__` inflation**: The `__init__.py` alone contributes 8 of the 27 edges. It is a re-export facade, not a functional component. Excluding it and `__main__` yields K/N = 1.636, which is still high but more representative.

2. **Package size**: With only 13 modules, `unittest` is a mid-sized package. Smaller packages tend to have higher K/N because modules cannot avoid knowing about each other in a compact design.

3. **Framework nature**: Testing frameworks are inherently coupled -- the TestCase needs the TestResult, the TestRunner needs both, the TestLoader needs TestCase and TestSuite. This is the nature of the domain, not a design flaw.

## 6. Structural Patterns

### 6.1 Hub-and-Spoke: `case` as Gravity Well

The `case` module (in-degree 6) is the gravitational center of the package. Six of eleven core modules depend on it. This is both expected (TestCase is the primary user-facing abstraction) and a structural risk (changes to `case` can cascade widely).

The `case` module's size (1,456 lines, 21.5% of the package) reflects its hub role -- it contains the entire assertion library, test lifecycle management, skip/expected-failure decorators, and subtest support.

### 6.2 Clean Utility Layer: `util` and `signals`

`util` (in-degree 5, out-degree 0) and `signals` (in-degree 3, out-degree 0) are **pure leaf modules** with zero outgoing dependencies. This is excellent decomposition -- they provide services without creating coupling chains. Any module can use them without risk of transitive dependency bloat.

### 6.3 Mock as Isolated Satellite

`mock` is the largest module (3,022 lines, 44.7% of the package) but has only **one** internal dependency (`util.safe_repr`). It is effectively a standalone sub-package that was folded into `unittest`. Its isolation means:

- It could be extracted to a separate package with trivial effort (and historically, it was -- `mock` was an independent PyPI package before Python 3.3).
- It contributes mass but not coupling to the system.
- Its K contribution (1 edge) is minimal relative to its size.

### 6.4 The Execution Pipeline

The modules form a clear pipeline architecture:

```
      loader --> suite --> case --> result
        |                   |        ^
        v                   v        |
       main ------------> runner ----+
                             |
                             v
                          signals
```

This is a well-structured data flow: **discover tests** (loader) --> **group tests** (suite) --> **run tests** (case) --> **collect results** (result) --> **display results** (runner).

### 6.5 Two-Layer Architecture

The package has a clear two-layer structure:

**Foundation layer** (out-degree 0, no internal dependencies):
- `util` -- pure functions
- `signals` -- signal handling

**Application layer** (depends on foundation and each other):
- `case`, `result`, `suite`, `loader`, `runner`, `main`, `mock`, `_log`, `async_case`

There is no middle "service" layer, which keeps the architecture simple but means the application layer modules must reach directly to the foundation.

## 7. Assessment

### Is unittest's K/N good or poor?

**It is reasonable for its domain, though not exemplary.**

**Arguments for "good":**
- The dependency graph is almost entirely acyclic (one managed cycle).
- Two pure leaf modules (`util`, `signals`) provide a stable foundation.
- `mock` is beautifully isolated despite being the largest component.
- The pipeline structure (loader -> suite -> case -> result -> runner) is logical and traceable.
- No module has an out-degree greater than 3 (excluding the re-export `__init__`).

**Arguments for "could be better":**
- `case` at 1,456 lines and in-degree 6 is doing too much. The assertions, lifecycle management, decorators, and context managers could potentially be split into separate modules.
- The `case <-> _log` cycle, while managed, is a sign that `_log` is not a truly independent module -- it is a factored-out appendage of `case`.
- K/N of 2.077 (or 1.636 core) is significantly higher than packages like `json` or `email`, suggesting the modules are not as independent as they could be.
- The `result` module is imported by both `case` and `runner`, creating an indirect coupling path between them.

### NK Fitness Landscape Interpretation

In NK landscape terms:
- **N = 13** components define the search space.
- **K_avg = 2.077** means each component's fitness depends on ~2 other components on average.
- The **ruggedness** of the fitness landscape is moderate -- changes to any module affect on average 2 others, meaning local optimization (changing one module) has a reasonable chance of improving global fitness.
- The **case** module with K_in=6 is a **correlation hub** -- it creates correlated fitness contributions across 6 other modules, making it the most sensitive point for refactoring.
- The landscape is not excessively rugged (K is not close to N-1=12), so the system is still navigable for evolution and refactoring.

### Summary Table

| Property | Value | Verdict |
|----------|-------|---------|
| N | 13 | Mid-sized, manageable |
| K/N (all) | 2.077 | Moderately coupled |
| K/N (core) | 1.636 | Acceptable for a framework |
| K_max | 8 (__init__) / 3 (core) | Reasonable |
| Cycles | 1 (managed) | Acceptable |
| Hub concentration | case (in=6) | High but domain-appropriate |
| Isolated mass | mock (3022 lines, K=1) | Excellent isolation |
| Leaf modules | util, signals | Clean foundation |
| Graph density | 0.173 | Moderate |
| Overall | -- | **Competent framework architecture with one oversized hub** |
