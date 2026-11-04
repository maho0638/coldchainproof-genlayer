# ColdChainProof — Refrigerated Shipment Risk Consensus

**Live-verified GenLayer Intelligent Contract on public Studionet.**

ColdChainProof distinguishes hard temperature-limit breaches from AI assessment of a self-reported handling note. It stores transparent on-chain receipts without claiming to validate physical sensors.

## Contract API

Source: `contracts/ColdChainProof.py` (SDK aligned with the previously accepted Sightline project).

- `register(shipment_id, batch, allowed_low_c, allowed_high_c, observed_low_c, observed_high_c, handling_note)` — stores a unique, public shipment claim.
- `review(shipment_id)` — caller-only, once. If readings exceed permitted limits, status is deterministically `OUT_OF_RANGE`. Otherwise, GenLayer validators independently assess note risk as `RISK`, `NO_RISK`, or `UNCLEAR`.
- `get_shipment(shipment_id)` — public JSON receipt, including the original claimed readings.

The range is deliberately restricted to whole-degree Celsius readings from 0 to 50 °C (not freezing temperatures or fractional measurements). Every public shipment ID must be unique. Invalid ranges, missing cases, unauthorized or repeated reviews and malformed model responses are rejected.

**Limitations:** Measurements and handling notes are supplied by the caller. The contract does not authenticate sensors, origin, freshness, standards compliance or delivery. AI consensus is not an independent audit of real-world temperature. Do not submit confidential shipment information.

## Verified live Studionet execution

- Contract: `0x4E45b3B82bDC5EA513DefAa75aE1E9d01e9E7fDb`
- [GenLayer Explorer](https://explorer-studio.genlayer.com/address/0x4E45b3B82bDC5EA513DefAa75aE1E9d01e9E7fDb)
- Out-of-range register: `0x7213489485174e311c760b2d8220590bf8bf7e6a2845dbc6506c282e62d26fcf`
- Out-of-range review: `0x2e79952fb2108b27344a65b566fe928c430ba9fc2a593e9e5861adda0c5929cb` → `OUT_OF_RANGE`
- AI-note register: `0x346bfe46808e6cee321c8a0076024490baa5a8dd60a80d0d12305f083d983819`
- AI-note review: `0xcb5954fc61ddd82d2ffbade3491541e9cf9bb5190fa77bfcfaaef126256f24b7` → `RISK`
- [Successful end-to-end network run](https://github.com/maho0638/coldchainproof-genlayer/actions/runs/41828777843)
- Local Direct Mode and GenVM lint: `.github/workflows/checks.yml`; hosted network proof: `.github/workflows/studionet.yml`

No production mainnet transaction is claimed.

## Portal submission

See [SUBMISSION.md](SUBMISSION.md) for the ready-to-paste title, English description and required repository + explorer evidence.
