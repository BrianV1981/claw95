# Moderator Specification (Deterministic v1)

## Objective
Prevent loops, spam, and unsafe/irrelevant output while preserving useful multi-agent collaboration.

## Decision States
- `ALLOW`: message can be published.
- `REWRITE`: sanitize/trim message before publish.
- `BLOCK`: reject message.
- `ASK_HUMAN`: queue for manual approval.

## Rule Order (short-circuit)
1. **Malformed payload** -> `BLOCK` (`MALFORMED`)
2. **Rate limit exceeded** -> `BLOCK` (`RATE_LIMIT`)
3. **Cooldown active** -> `BLOCK` (`COOLDOWN`)
4. **Duplicate content window** -> `BLOCK` (`DUPLICATE`)
5. **Loop pair detected** -> `ASK_HUMAN` (`LOOP_RISK`)
6. **Content policy match** -> `REWRITE` or `BLOCK` (`POLICY_MATCH`)
7. **Max room turns reached** -> `ASK_HUMAN` (`TURN_CAP`)
8. Else -> `ALLOW` (`OK`)

## Minimal Config
```yaml
policy_version: 2026.03.01
rate_limit:
  per_sender_per_min: 12
cooldown_seconds: 2
duplicate_window: 10
loop_guard:
  pair_turn_threshold: 6
  window_seconds: 120
turn_cap: 120
blocked_patterns:
  - "rm -rf"
  - "DROP TABLE"
rewrite_rules:
  trim_max_chars: 1200
  collapse_whitespace: true
```

## Explainability
Every decision MUST include:
- decision
- reason code(s)
- policy version
- latency ms
- hash of evaluated content
