"""Official GenLayer SDK Direct Mode checks (same runner/API as live Studionet)."""
import json


def _register(c, shipment="public-shipment-01", observed_high=7):
    c.register(
        shipment, "PUBLIC-LOT", 2, 8, 3, observed_high,
        "Cooling power was interrupted during the journey."
    )


def _mock(vm, verdict):
    vm.clear_mocks()
    vm.mock_llm(r"(?s).*Independently judge whether this self-reported refrigerated.*",
                json.dumps({"risk": verdict}))


def test_register_stores_exact_public_ranges(direct_deploy):
    c = direct_deploy("contracts/ColdChainProof.py")
    _register(c)
    r = json.loads(c.get_shipment("public-shipment-01"))
    assert r["status"] == "PENDING"
    assert r["allowed_high_c"] == 8
    assert r["observed_high_c"] == 7


def test_out_of_range_deterministically_overrides_note(direct_vm, direct_deploy):
    c = direct_deploy("contracts/ColdChainProof.py")
    _register(c, observed_high=12)
    c.review("public-shipment-01")
    assert json.loads(c.get_shipment("public-shipment-01"))["status"] == "OUT_OF_RANGE"
    with direct_vm.expect_revert("Already reviewed"):
        c.review("public-shipment-01")


def test_ai_review_consensus_disagreement(direct_vm, direct_deploy):
    c = direct_deploy("contracts/ColdChainProof.py")
    _register(c)
    _mock(direct_vm, "RISK")
    c.review("public-shipment-01")
    assert json.loads(c.get_shipment("public-shipment-01"))["status"] == "RISK"
    assert direct_vm.run_validator() is True
    _mock(direct_vm, "NO_RISK")
    assert direct_vm.run_validator() is False


def test_unauthorized_replay_and_invalid_ranges(direct_vm, direct_deploy, direct_bob):
    c = direct_deploy("contracts/ColdChainProof.py")
    _register(c)
    owner = direct_vm.sender
    direct_vm.sender = direct_bob
    with direct_vm.expect_revert("Only submitter can review"):
        c.review("public-shipment-01")
    direct_vm.sender = owner
    with direct_vm.expect_revert("Shipment already exists"):
        _register(c)
    with direct_vm.expect_revert("Invalid allowed temperatures"):
        c.register("public-shipment-02", "LOT", 9, 2, 3, 7, "The cooling power was stable.")
    with direct_vm.expect_revert("Shipment not found"):
        c.get_shipment("unknown")
