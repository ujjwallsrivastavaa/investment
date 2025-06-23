import pytest
from market_sim.pow.proof_of_work import ProofOfWork

def test_pow_mining_and_validation():
    pow = ProofOfWork(difficulty_bits=18)
    data = "test_trade"
    nonce, hash_val, elapsed = pow.mine(data)
    assert isinstance(nonce, int)
    assert pow.validate(data, nonce)
    print(f"Nonce: {nonce}, Hash: {hash_val}, Time: {elapsed:.2f}s")

def test_pow_invalid_nonce():
    pow = ProofOfWork(difficulty_bits=18)
    data = "test_trade"
    bad_nonce = 0
    assert not pow.validate(data, bad_nonce)
    print("Invalid nonce correctly rejected.")