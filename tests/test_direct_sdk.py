"""Real GenLayer Direct SDK tests; no public chain transactions."""
import json


def mock_risk(vm, verdict):
    vm.mock_llm(r".*", json.dumps(json.dumps({"risk": verdict})))


def test_real_direct_deployment_storage_and_auth(direct_vm, direct_deploy, direct_bob):
    direct_vm.check_pickling = True
    c = direct_deploy("contracts/ColdChainProof.py")
    cid = c.register("LOT-2026", 2, 8, 3, 7, "Cooling stable during journey")
    assert cid == 1
    assert c.total_shipments() == 1
    assert json.loads(c.get_shipment(cid))["status"] == "PENDING"
    direct_vm.sender = direct_bob
    with direct_vm.expect_revert("Only author can review"):
        c.review(cid)


def test_real_direct_deterministic_threshold_precedes_ai(direct_vm, direct_deploy):
    c = direct_deploy("contracts/ColdChainProof.py")
    cid = c.register("LOT-2026", 2, 8, 0, 11, "All conditions reportedly stable")
    assert c.review(cid) == "OUT_OF_RANGE"
    assert json.loads(c.get_shipment(cid))["status"] == "OUT_OF_RANGE"
    with direct_vm.expect_revert("Already reviewed"):
        c.review(cid)


def test_real_direct_validator_agreement_and_disagreement(direct_vm, direct_deploy):
    direct_vm.check_pickling = True
    mock_risk(direct_vm, "RISK")
    c = direct_deploy("contracts/ColdChainProof.py")
    cid = c.register("LOT-2026", 2, 8, 3, 7, "Power failure during delivery")
    assert c.review(cid) == "RISK"
    assert direct_vm.run_validator() is True
    direct_vm.clear_mocks()
    mock_risk(direct_vm, "NO_RISK")
    assert direct_vm.run_validator() is False


def test_real_direct_rejects_bad_ranges_and_controls(direct_vm, direct_deploy):
    c = direct_deploy("contracts/ColdChainProof.py")
    with direct_vm.expect_revert("Invalid allowed range"):
        c.register("LOT-2026", 9, 2, 3, 7, "Stable cooling throughout")
    with direct_vm.expect_revert("Invalid observed range"):
        c.register("LOT-2026", 2, 8, 9, 2, "Stable cooling throughout")
    with direct_vm.expect_revert("Invalid control character"):
        c.register("LOT-2026", 2, 8, 3, 7, "Stable\u202e handling")
    assert c.total_shipments() == 0
