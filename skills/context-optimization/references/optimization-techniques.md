# Optimization Techniques Reference

## Technique Comparison

| Technique | Token Savings | Implementation Cost | Risk |
|-----------|--------------|-------------------|------|
| Observation masking | 30-60% per turn | Low | Info loss if premature |
| Prefix caching | 0% (compute savings) | Medium | Cache invalidation |
| Context partitioning | 10-30% | Medium | Partition imbalance |
| Budget allocation | Prevents overflow | Low | Budget rigidity |
| Format optimization | 15-40% | Low | Readability tradeoff |
| Just-in-time retrieval | 40-70% | Medium | Retrieval latency |

## Budget Allocation Templates

### Chat Agent (128K context)
| Partition | Allocation | Tokens |
|-----------|-----------|--------|
| System | 8% | 10,240 |
| Tools | 4% | 5,120 |
| Knowledge | 15% | 19,200 |
| History | 40% | 51,200 |
| Task | 10% | 12,800 |
| Headroom | 23% | 29,440 |

### Research Agent (200K context)
| Partition | Allocation | Tokens |
|-----------|-----------|--------|
| System | 5% | 10,000 |
| Tools | 3% | 6,000 |
| Knowledge | 30% | 60,000 |
| History | 25% | 50,000 |
| Task | 12% | 24,000 |
| Headroom | 25% | 50,000 |
