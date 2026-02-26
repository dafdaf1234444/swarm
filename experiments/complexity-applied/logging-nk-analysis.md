# NK Landscape Analysis: Python `logging` Package

**Date**: 2026-02-26
**Python version**: 3.12
**Package**: `logging` (stdlib)

## 1. Module Inventory (N)

The `logging` package consists of exactly **3 modules**:

| Module | File | Lines | Classes | Top-level Functions |
|--------|------|------:|--------:|--------------------:|
| `logging` (core) | `__init__.py` | 2,345 | 18 | 31 |
| `logging.handlers` | `handlers.py` | 1,605 | 14 | 0 |
| `logging.config` | `config.py` | 1,050 | 6 | 12 |
| **Total** | | **5,000** | **38** | **43** |

**N = 3**

## 2. Dependency Map (K)

### 2.1 Internal Dependency Edges

| From | To | Edge Type | Distinct Attributes Used |
|------|----|-----------|------------------------:|
| `handlers` | `__init__` | `import logging` | 7 |
| `config` | `__init__` | `import logging` | 13 |
| `config` | `handlers` | `import logging.handlers` | 5 |

**Total directed edges: K = 3**

The dependency graph is a **DAG** (directed acyclic graph) with no cycles:

```
__init__  <----  handlers
   ^
   |
 config  ---->  handlers
```

### 2.2 Detailed Attribute Coupling

**handlers.py -> logging (7 attributes)**:
- `logging.FileHandler` (base class for 3 handler classes)
- `logging.Handler` (base class for 9 handler classes)
- `logging.CRITICAL`, `logging.DEBUG`, `logging.ERROR`, `logging.INFO`, `logging.WARNING` (level constants)

**config.py -> logging (13 attributes)**:
- Public API: `logging.Filter`, `logging.Formatter`, `logging.Handler`, `logging.NOTSET`, `logging.PlaceHolder`, `logging.getLogger`, `logging.root`, `logging.shutdown`
- Private internals: `logging._acquireLock`, `logging._releaseLock`, `logging._checkLevel`, `logging._handlers`, `logging._handlerList`

**config.py -> logging.handlers (5 attributes)**:
- `logging.handlers.MemoryHandler`
- `logging.handlers.QueueHandler`
- `logging.handlers.QueueListener`
- `logging.handlers.SMTPHandler`
- `logging.handlers.SysLogHandler`

### 2.3 Dependency Direction Summary

| Module | In-degree | Out-degree | Total degree |
|--------|----------:|----------:|-----------:|
| `__init__` | 2 | 0 | 2 |
| `handlers` | 1 | 1 | 2 |
| `config` | 0 | 2 | 2 |

## 3. NK Metrics

| Metric | Value | Notes |
|--------|------:|-------|
| **N** | 3 | Number of modules |
| **K** (total edges) | 3 | Directed dependency edges between modules |
| **K/N** | 1.00 | Dependency density ratio |
| **K_avg** | 1.00 | Average dependencies per module (K/N) |
| **K_max** | 2 | Maximum out-degree (config.py) |
| **K_max_in** | 2 | Maximum in-degree (__init__.py) |
| **Max possible K** | 6 | N * (N-1) for a directed graph |
| **K/K_max_possible** | 0.50 | Graph density (50% of possible edges used) |

## 4. Comparison with Known Benchmarks

| Package | N | K | K/N | K_avg | Assessment |
|---------|--:|--:|----:|------:|------------|
| `json` | 5 | ~0.8 | 0.16 | 0.16 | Excellent: minimal coupling |
| `email` | 28 | ~1.7 | 0.06 | 0.06 | Excellent: very loose coupling |
| `http.client` (core) | 24 | ~5.2 | 0.215 | 0.215 | Good: moderate coupling |
| **`logging`** | **3** | **3** | **1.00** | **1.00** | **See analysis below** |

The raw K/N = 1.00 for logging is dramatically higher than the benchmarks. However, this demands careful interpretation.

## 5. Analysis and Interpretation

### 5.1 The Small-N Distortion

The K/N ratio is misleading for very small N. With only 3 modules:
- The minimum non-trivial K/N is 0.33 (one edge)
- The maximum K/N is 2.00 (fully connected directed graph)
- Any meaningful package with 3 modules will have K/N >= 0.33

For comparison, if `json` (N=5) had the same *graph density* as logging (50%), it would have K=10 and K/N=2.0. Logging's 50% graph density is actually moderate.

### 5.2 The Monolith Problem

The real finding is not high coupling -- it is **extreme concentration**. The `__init__.py` module contains:
- **2,345 of 5,000 lines** (47% of code)
- **18 of 38 classes** (47%)
- **31 of 43 top-level functions** (72%)
- All core abstractions: `LogRecord`, `Logger`, `Handler`, `Formatter`, `Filter`, `Manager`, etc.

This is a **monolith with satellites** pattern, not a decomposed package. The real N -- the number of meaningful architectural components -- is arguably much higher than 3. The `__init__.py` alone contains what would be 5-8 modules in a well-decomposed package:
1. Level management (`CRITICAL`, `DEBUG`, etc. + `addLevelName`, `getLevelName`)
2. `LogRecord` and factories
3. Formatting (`Formatter`, `PercentStyle`, `StrFormatStyle`, `StringTemplateStyle`, `BufferingFormatter`)
4. Filtering (`Filter`, `Filterer`)
5. Core handler infrastructure (`Handler`, `StreamHandler`, `FileHandler`)
6. Logger hierarchy (`Logger`, `RootLogger`, `Manager`, `PlaceHolder`)
7. `LoggerAdapter`
8. Module-level convenience API (`getLogger`, `basicConfig`, `debug`, `info`, etc.)

### 5.3 Config Module: Deep Coupling to Internals

The `config` module accesses **5 private attributes** of `__init__`:
- `logging._acquireLock`
- `logging._releaseLock`
- `logging._checkLevel`
- `logging._handlers`
- `logging._handlerList`

This is a strong code smell. These underscore-prefixed names represent internal implementation details. The config module cannot function without intimate knowledge of the core module's internals, making it fragile to refactoring. This is **coupling through private API** -- the worst kind in terms of maintenance burden.

### 5.4 Handlers Module: Clean Coupling

By contrast, `handlers.py` couples only to **public API** (base classes and level constants). This is clean, intentional extension-point coupling. All 14 handler classes inherit from either `logging.Handler` or `logging.FileHandler` -- exactly the pattern the architecture intended.

### 5.5 Cycle Analysis

**No cycles exist.** The dependency graph is a clean DAG:
- `__init__` depends on nothing within the package
- `handlers` depends only on `__init__`
- `config` depends on both `__init__` and `handlers`

This is structurally sound. The layering is:
```
Layer 0 (foundation):  __init__
Layer 1 (extensions):  handlers
Layer 2 (configuration): config
```

### 5.6 Coupling Hubs

**Hub by in-degree**: `__init__` (in-degree = 2) -- both other modules depend on it.
This is expected for a core module and is not problematic.

**Hub by out-degree**: `config` (out-degree = 2) -- it depends on both other modules.
Also expected: configuration must know about what it configures.

**Hub by attribute surface area**: `config` -> `__init__` uses 13 distinct attributes (including 5 private ones), making this the highest-coupling edge by far.

### 5.7 Isolated Modules

None. All 3 modules participate in the dependency graph. There are no dead or orphan modules.

## 6. External Dependencies (stdlib)

For completeness, each module's external stdlib imports:

| Module | Unconditional Imports | Conditional (lazy) Imports |
|--------|----------------------|---------------------------|
| `__init__` | `sys`, `os`, `time`, `io`, `re`, `traceback`, `warnings`, `weakref`, `collections.abc`, `types`, `string`, `threading`, `atexit` (13) | `pickle` (1) |
| `handlers` | `io`, `socket`, `os`, `pickle`, `struct`, `time`, `re`, `stat`, `queue`, `threading`, `copy` (11) | `smtplib`, `email.message`, `email.utils`, `win32evtlogutil`, `win32evtlog`, `http.client`, `urllib.parse`, `base64` (8) |
| `config` | `errno`, `functools`, `io`, `os`, `queue`, `re`, `struct`, `threading`, `traceback`, `socketserver` (10) | `configparser`, `multiprocessing.queues`, `json`, `select` (4) |

The `handlers` module makes heavy use of **lazy imports** for protocol-specific dependencies (SMTP, HTTP, Windows Event Log), which is good practice -- it avoids loading expensive modules until the specific handler type is actually used.

## 7. Summary Assessment

| Dimension | Finding | Verdict |
|-----------|---------|---------|
| K/N ratio | 1.00 | Misleadingly high due to small N; actual graph density (50%) is moderate |
| Cycle freedom | No cycles | Good: clean layered DAG |
| Decomposition quality | Monolith `__init__` (47% of code, 72% of functions) | Poor: under-decomposed core |
| Coupling quality | `config` uses 5 private attributes of `__init__` | Poor: fragile internal coupling |
| Extension pattern | `handlers` uses only public base classes | Good: clean extension points |
| Effective N | ~8-10 logical components crammed into 3 files | Package would benefit from further decomposition |

### Overall Verdict

The `logging` package's NK profile reveals a **monolith-with-satellites** anti-pattern. The low module count (N=3) masks significant internal complexity within `__init__.py`. The K/N = 1.00 is not inherently problematic for a 3-module package, but the **coupling quality** is mixed:

- **Good**: `handlers` -> `__init__` is clean public-API coupling through inheritance
- **Bad**: `config` -> `__init__` reaches into private internals, creating hidden fragility
- **Structural**: The package would score much better on NK metrics if `__init__.py` were decomposed into 5-8 focused modules (records, formatting, filtering, handlers-base, logger-hierarchy, convenience-api)

Compared to the benchmarks, `logging` achieves its low apparent coupling not through good decomposition but through **under-modularization** -- stuffing most logic into one giant file. This is a common pattern in older Python stdlib packages that predate modern packaging conventions.

**If `__init__.py` were split into its ~8 logical components**, the resulting package would likely have N~10, K~12-15, and K/N~1.2-1.5, which would more honestly reflect the actual internal complexity while still being a reasonable ratio for a tightly-integrated framework package.
