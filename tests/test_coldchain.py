"""Offline logic tests with a mocked GenLayer host (not chain consensus)."""
import importlib.util
import json
import sys
import types
from pathlib import Path
import pytest


class UserError(Exception):
    pass


class Return:
    def __init__(self, calldata):
        self.calldata = calldata


class TreeMap(dict):
    def __class_getitem__(cls, args):
        return cls


def setup_contract():
    gl = types.ModuleType("genlayer")
    gl.contract = types.SimpleNamespace(Contract=type("Contract", (), {}))
    gl.storage = types.SimpleNamespace(TreeMap=TreeMap, inmem_allocate=lambda cls: cls())
    gl.public = types.SimpleNamespace(write=lambda fn: fn, view=lambda fn: fn)
    gl.message = types.SimpleNamespace(sender_address="alice")
    gl.vm = types.SimpleNamespace(Result=object, Return=Return, UserError=UserError)
    gl.nondet = types.SimpleNamespace(exec_prompt=lambda p, response_format: {"risk": "NO_RISK"})

    def consensus(produce, verify):
        value = produce()
        if not verify(Return(value)):
            raise UserError("Validator disagreed")
        return value

    gl.vm.run_nondet_default = consensus
    types_module = types.ModuleType("genlayer.types")
    types_module.Address, types_module.u32 = str, int
    previous = (sys.modules.get("genlayer"), sys.modules.get("genlayer.types"))
    sys.modules["genlayer"], sys.modules["genlayer.types"] = gl, types_module
    path = Path(__file__).resolve().parents[1] / "contracts" / "ColdChainProof.py"
    spec = importlib.util.spec_from_file_location("cold_chain_contract", path)
    module = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(module)
    finally:
        for name, old in zip(("genlayer", "genlayer.types"), previous):
            if old is None:
                sys.modules.pop(name, None)
            else:
                sys.modules[name] = old
    return module, gl


def test_normal_and_single_review():
    m, gl = setup_contract()
    c = m.ColdChainProof()
    i = c.register("LOT-17", 2, 8, 3, 6, "Refrigerator remained stable.")
    assert i == 1 and c.total_shipments() == 1
    assert c.review(i) == "NO_RISK"
    assert json.loads(c.get_shipment(i))["status"] == "NO_RISK"
    with pytest.raises(UserError):
        c.review(i)


def test_out_of_range_precedes_ai():
    m, gl = setup_contract()
    c = m.ColdChainProof()
    i = c.register("LOT-17", 2, 8, 2, 12, "Everything was perfect.")
    gl.nondet.exec_prompt = lambda p, response_format: (_ for _ in ()).throw(AssertionError("AI ran"))
    assert c.review(i) == "OUT_OF_RANGE"


def test_reject_bad_ranges_and_unauthorized_review():
    m, gl = setup_contract()
    c = m.ColdChainProof()
    with pytest.raises(UserError):
        c.register("LOT-17", 9, 2, 3, 5, "Inspection notes")
    i = c.register("LOT-17", 2, 8, 3, 5, "Inspection notes")
    gl.message.sender_address = "mallory"
    with pytest.raises(UserError):
        c.review(i)
    assert json.loads(c.get_shipment(i))["status"] == "PENDING"


def test_bad_ai_reply_and_validator_disagreement_do_not_store():
    m, gl = setup_contract()
    c = m.ColdChainProof()
    i = c.register("LOT-17", 2, 8, 3, 5, "Inspection notes")
    gl.nondet.exec_prompt = lambda p, response_format: {"risk": "CERTIFIED"}
    with pytest.raises(UserError):
        c.review(i)
    votes = iter([{"risk": "RISK"}, {"risk": "NO_RISK"}])
    gl.nondet.exec_prompt = lambda p, response_format: next(votes)
    with pytest.raises(UserError):
        c.review(i)
    assert json.loads(c.get_shipment(i))["status"] == "PENDING"
