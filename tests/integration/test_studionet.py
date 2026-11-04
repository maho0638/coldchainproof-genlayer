"""Hosted Studionet proof for the supported legacy GenLayer contract runner."""
import json
from gltest import get_contract_factory
from gltest.assertions import tx_execution_succeeded


def write(call, tag):
    tx = call.transact(consensus_max_rotations=4, wait_interval=10000, wait_retries=50)
    assert tx_execution_succeeded(tx), f"{tag} failed; tx={tx.get('hash', '')}"
    print(f"{tag}_TX={tx.get('hash', '')}", flush=True)


def test_public_studionet_contract(default_account):
    c = get_contract_factory("ColdChainProof").deploy(
        account=default_account, consensus_max_rotations=4)
    address = str(c.address)
    assert address.startswith("0x") and len(address) == 42
    print(f"COLDCHAINPROOF_CONTRACT_ADDRESS={address}", flush=True)
    print(f"COLDCHAINPROOF_EXPLORER=https://explorer-studio.genlayer.com/address/{address}", flush=True)

    write(c.register(args=[
        "public-shipment-001", "PUBLIC-LOT-01", 2, 8, 1, 10,
        "The logger recorded a temperature excursion during delivery."
    ]), "COLDCHAINPROOF_REGISTER_OUT_OF_RANGE")
    write(c.review(args=["public-shipment-001"]), "COLDCHAINPROOF_REVIEW_OUT_OF_RANGE")
    first = json.loads(c.get_shipment(args=["public-shipment-001"]).call())
    assert first["status"] == "OUT_OF_RANGE"

    write(c.register(args=[
        "public-shipment-002", "PUBLIC-LOT-02", 2, 8, 3, 7,
        "Cooling power was interrupted for two hours during delivery."
    ]), "COLDCHAINPROOF_REGISTER_AI")
    write(c.review(args=["public-shipment-002"]), "COLDCHAINPROOF_REVIEW_AI")
    result = json.loads(c.get_shipment(args=["public-shipment-002"]).call())
    assert result["status"] in ("RISK", "NO_RISK", "UNCLEAR")
    print(f"COLDCHAINPROOF_FINAL_AI_VERDICT={result['status']}", flush=True)
