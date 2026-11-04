"""Hosted GenLayer Studionet proof: deploy, record bounds, AI review, read."""
import json
from gltest import get_contract_factory
from gltest.assertions import tx_execution_succeeded
from gltest.types import TransactionStatus


def _confirmed_write(call, label):
    receipt = call.transact(
        consensus_max_rotations=4,
        wait_transaction_status=TransactionStatus.FINALIZED,
        wait_interval=10000,
        wait_retries=55,
    )
    print(f"{label}_RECEIPT={json.dumps(receipt, default=str)}", flush=True)
    assert tx_execution_succeeded(receipt), f"{label} failed: {receipt}"
    print(f"{label}_TX={receipt.get('hash', '')}", flush=True)
    return receipt


def test_coldchainproof_real_studionet_lifecycle(default_account):
    contract = get_contract_factory("ColdChainProof").deploy(
        account=default_account,
        consensus_max_rotations=4,
    )
    address = str(contract.address)
    assert address.startswith("0x") and len(address) == 42
    print(f"COLDCHAINPROOF_DEPLOYED_ADDRESS={address}", flush=True)
    print(f"COLDCHAINPROOF_EXPLORER=https://explorer-studio.genlayer.com/address/{address}", flush=True)

    _confirmed_write(
        contract.register(args=[
            "PUBLIC-LOT-01", 2, 8, 1, 10, "The logger recorded a temperature excursion.",
        ]),
        "COLDCHAINPROOF_REGISTER_OUT_OF_RANGE",
    )
    assert int(contract.total_shipments().call()) == 1
    _confirmed_write(contract.review(args=[1]), "COLDCHAINPROOF_REVIEW_OUT_OF_RANGE")
    assert json.loads(contract.get_shipment(args=[1]).call())["status"] == "OUT_OF_RANGE"

    _confirmed_write(
        contract.register(args=[
            "PUBLIC-LOT-02", 2, 8, 3, 7,
            "Cooling power was interrupted during the journey; check any possible cargo impact.",
        ]),
        "COLDCHAINPROOF_REGISTER_AI",
    )
    _confirmed_write(contract.review(args=[2]), "COLDCHAINPROOF_REVIEW_AI")
    second = json.loads(contract.get_shipment(args=[2]).call())
    assert second["status"] in {"RISK", "NO_RISK", "UNCLEAR"}
    assert int(contract.total_shipments().call()) == 2
    print(f"COLDCHAINPROOF_FINAL_AI_VERDICT={second['status']}", flush=True)
