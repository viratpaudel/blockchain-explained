"""
Interactive Blockchain Demonstration.
Runs a live simulation showcasing Proof of Work mining, Merkle trees,
transaction validation, and tamper-detection mechanics.
"""

import time
from src.blockchain import Blockchain
from src.transaction import Transaction


def banner(title: str):
    print("\n" + "=" * 70)
    print(f"  {title.upper()}")
    print("=" * 70)


def main():
    banner("1. Initializing Blockchain & Genesis Block")
    setu_chain = Blockchain(difficulty=3, mining_reward=25.0)
    genesis = setu_chain.chain[0]
    print(f"[+] Genesis Block Created: #{genesis.index}")
    print(f"    Hash:         {genesis.hash}")
    print(f"    Merkle Root:  {genesis.merkle_root}")
    print(f"    Nonce:        {genesis.nonce}")
    print(f"    Transactions: {genesis.transactions}")

    banner("2. Mining Block #1: Alice Mines Initial Reward")
    start = time.time()
    block1 = setu_chain.mine_pending_transactions(miner_address="Alice")
    elapsed = time.time() - start
    print(f"[+] Block #1 successfully mined in {elapsed:.3f}s!")
    print(f"    Hash:         {block1.hash}")
    print(f"    Previous:     {block1.previous_hash}")
    print(f"    Nonce:        {block1.nonce}")
    print(f"    Alice Balance: {setu_chain.get_balance('Alice')} SETU")

    banner("3. Queuing Cryptographically Signed Transactions")
    tx1 = Transaction(sender="Alice", recipient="Bob", amount=10.0)
    tx1.sign("alice_private_key_secp256k1")
    setu_chain.add_transaction(tx1)

    tx2 = Transaction(sender="Alice", recipient="Charlie", amount=5.0)
    tx2.sign("alice_private_key_secp256k1")
    setu_chain.add_transaction(tx2)
    print(f"[+] Added 2 transactions to mempool. Pending: {len(setu_chain.pending_transactions)}")

    banner("4. Mining Block #2: Charlie Mines the Mempool")
    start = time.time()
    block2 = setu_chain.mine_pending_transactions(miner_address="Charlie")
    elapsed = time.time() - start
    print(f"[+] Block #2 successfully mined in {elapsed:.3f}s!")
    print(f"    Hash:        {block2.hash}")
    print(f"    Merkle Root: {block2.merkle_root}")
    print(f"    Balances:")
    print(f"      - Alice:   {setu_chain.get_balance('Alice')} SETU")
    print(f"      - Bob:     {setu_chain.get_balance('Bob')} SETU")
    print(f"      - Charlie: {setu_chain.get_balance('Charlie')} SETU")

    banner("5. Cryptographic Chain Audit")
    is_valid = setu_chain.is_chain_valid()
    print(f"[✓] Blockchain integrity check: {'VALID (ALL CRYPTOGRAPHIC PROOFS HOLD)' if is_valid else 'INVALID'}")

    banner("6. Attack Simulation: Tampering with Historical Transaction")
    print("[!] Malicious actor attempts to alter Block #2: changing Bob's received amount from 10.0 -> 1000.0 SETU...")
    # Attacker attempts to modify transaction data inside Block #2
    setu_chain.chain[2].transactions[1].amount = 1000.0

    print("[!] Re-auditing blockchain integrity after tampering...")
    tampered_valid = setu_chain.is_chain_valid()
    print(f"[✗] Post-Attack Blockchain validation: {'VALID' if tampered_valid else 'COMPROMISED / REJECTED'}")
    if not tampered_valid:
        print("    -> Tampering detected: Merkle Root mismatch and broken cryptographic hash pointer!")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()
