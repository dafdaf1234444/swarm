# Real-World Distributed Systems Failures

## Yuan et al. 2014 — "Simple Testing Can Prevent Most Critical Failures"
198 randomly-selected failures across Cassandra, HBase, HDFS, MapReduce, Redis.

**Key findings**:
- 92% of catastrophic failures: incorrect handling of non-fatal errors
- 98% reproducible with ≤3 nodes
- 74% deterministic
- 58% preventable by simple pre-release testing

**Three error-handling anti-patterns**:
1. Swallowed errors: handlers that only log, no recovery
2. Placeholder handlers: TODO/FIXME in error paths
3. Overly broad catch-then-abort: catch(Exception) → System.exit()

**Implication**: the dominant failure mode is programmer error in error paths, not complex distributed algorithm bugs.

## Jepsen Results (Kingsbury, 2013-2025)
Tested 25+ systems. Common failure patterns:
1. **Premature acknowledgement**: fsync not before ack (NATS 2-min flush, Elasticsearch no default fsync)
2. **Split-brain during membership changes**: multiple leaders (RethinkDB, Elasticsearch)
3. **Inappropriate retry semantics**: auto-retry with new timestamps → duplicates (CockroachDB, TiDB)
4. **Weak default isolation**: claim strong, ship weak (MongoDB, RDS PostgreSQL)
5. **Infinite retry on failed connections**: prevents partition recovery (TiKV)
6. **Misleading claims**: Aerospike "100% uptime", RabbitMQ semaphore support

Notable recent findings:
- **Amazon RDS PostgreSQL 17.4** (2025): violates Snapshot Isolation in HEALTHY clusters — primary uses lock order, secondaries use WAL order → Long Fork anomaly
- **Kafka transactions** (2024): protocol assumes ordered delivery but uses multi-TCP → write loss, aborted reads, torn transactions. Unresolved.
- **TigerBeetle** (2025): meets Strong Serializability after fixes (0.16.30+)

## Network Partitions
Bailis & Kingsbury 2014: partitions happen on all real networks.
- WAN: 16-302 failures/link/year, 24-497 min downtime/link/year
- Median time between failures: ~50 minutes per link

Uptime Institute (2021-2024):
- Networking + software surpassed power as #1 outage cause (2021+)
- 45-62% of networking outages: configuration/change management
- 40% of orgs hit by human-error outage in prior 3 years

## Major Outages
| Outage | Year | Root Cause | Category |
|--------|------|-----------|----------|
| AWS S3 us-east-1 | 2017 | Operator removed too many servers | Human error |
| Cloudflare WAF | 2019 | Catastrophic regex backtracking, global deploy | Code quality + no canary |
| AWS us-east-1 | 2021 | Scaling event saturated internal network | Cascade from internal infra |
| Google Cloud | 2025 | Invalid config push without feature flag | Config management |
| Cloudflare Bot Mgmt | 2025 | DB schema change altered query semantics | Config + no integration test |

## Falsifiable Claims from Data
1. Systems without pre-ack fsync lose acknowledged data on node failure
2. Config/change management causes more outages than hardware
3. Incorrect error handling causes 90%+ of catastrophic failures
4. Most distributed bugs reproduce with ≤3 nodes
5. Global deploys without canary produce global outages from bad changes
6. Different visibility mechanisms on primary vs. secondary produce read anomalies

## Sources
- Yuan et al. OSDI 2014
- Jepsen analyses: jepsen.io/analyses
- Bailis & Kingsbury 2014: "The Network is Reliable"
- AWS postmortems: aws.amazon.com/message/41926/, aws.amazon.com/message/12721/
- Cloudflare blog postmortems (2019, 2025)
- Uptime Institute Annual Outage Analysis (2021-2024)
