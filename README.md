# ColdChainProof

A small GenLayer Intelligent Contract for **self-reported refrigerated shipment checks**. It records a claimed allowed temperature range, the observed range, and a brief handling note.

- If the reported readings exceed the permitted range, the result is deterministically `OUT_OF_RANGE`.
- Otherwise, an AI reviewer judges whether the handling note suggests a cold-chain risk: `RISK`, `NO_RISK`, or `UNCLEAR`. GenLayer validators independently compare that exact risk label using `run_nondet_default`.
- The original submitter can review a shipment only once; anyone can read the public receipt.

## Contract

`contracts/ColdChainProof.py` — `ColdChainProof`

1. `register(batch, allowed_low_c, allowed_high_c, observed_low_c, observed_high_c, handling_note)` returns a shipment ID.
2. `review(shipment_id)` returns a result.
3. `get_shipment(shipment_id)` retrieves the public JSON record.
4. `total_shipments()` returns the total count.

All temperature readings are whole-number **Celsius 0–50°C**. This scope covers nonfreezing refrigerated shipments, **not** frozen cargo or negative temperatures.

## Limitations

**This does not authenticate sensors, certificates, delivery logs or actual storage conditions.** It cannot establish that the submitter's readings or note are truthful. AI agreement on a narrative is not proof of compliance. All submitted information is public on-chain. Do not submit sensitive shipment details or personal information. There is no escrow, financial settlement, or automated payment.

## Verification

```bash
python -m pip install pytest
python -m compileall -q contracts tests
pytest -q tests
```

Offline unit tests use a mocked GenLayer host, **not** live validator consensus. Real GenVM deployment and finalized consensus are separate checks and must not be claimed without receipts.

## Origin

An independent GenLayer project; purpose and contract behavior are different from ClauseMirror, ConsensusGuard, and Sightline.
