# GenLayer Portal contribution — ColdChainProof

**Category:** Developer → Intelligent Contracts
**Title:** ColdChainProof — Refrigerated Shipment Risk Consensus

## Notes / Description (below 1,000 characters)

ColdChainProof is a live-deployed GenLayer Intelligent Contract for transparent refrigerated-shipment risk receipts. A requester records allowed and observed temperature ranges and a handling note. The contract deterministically reports OUT_OF_RANGE when an observed reading breaches the permitted interval, regardless of narrative claims. Otherwise, GenLayer validators independently evaluate the note and agree on RISK, NO_RISK or UNCLEAR before recording the result. Duplicate shipment IDs, unauthorized reviews, repeated decisions, invalid ranges and malformed AI outputs are rejected. On public Studionet, two distinct cases passed deployment, transaction and read-back tests: an out-of-range case returned OUT_OF_RANGE, and an in-range case with interrupted cooling returned RISK. Sensor readings are self-reported; no independent sensor certification is claimed.

## Required evidence (enter as separate URLs)

**GitHub Repository**
https://github.com/maho0638/coldchainproof-genlayer

**GenLayer Explorer Contract**
https://explorer-studio.genlayer.com/address/0x4E45b3B82bDC5EA513DefAa75aE1E9d01e9E7fDb

## Additional evidence

- Live network CI: https://github.com/maho0638/coldchainproof-genlayer/actions/runs/41828777843
- Live source code: https://github.com/maho0638/coldchainproof-genlayer/blob/fix/studionet-compatible-20261104/contracts/ColdChainProof.py
- Out-of-range review tx: https://explorer-studio.genlayer.com/tx/0x2e79952fb2108b27344a65b566fe928c430ba9fc2a593e9e5861adda0c5929cb
- AI review tx: https://explorer-studio.genlayer.com/tx/0xcb5954fc61ddd82d2ffbade3491541e9cf9bb5190fa77bfcfaaef126256f24b7

## Limits

Live proof is on public **Studionet**, not Bradbury or mainnet. Sensor readings have not been authenticated. No Portal submission was made automatically.
