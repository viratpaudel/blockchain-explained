# Module 01: Cryptography & Block Anatomy

Cryptography forms the mathematical foundation of blockchain immutability, data integrity, and identity verification.

---

## 1. Cryptographic Hash Functions (SHA-256)

A cryptographic hash function maps input data of arbitrary size to a fixed-size bit string (digest).

```
"Alice pays Bob 5 BTC" ──► [ SHA-256 ] ──► 2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824
```

### Essential Properties:
1. **Deterministic**: The same input always produces the exact same hash output.
2. **Pre-image Resistance (One-Way)**: Given hash `H`, it is computationally infeasible to find `x` such that `Hash(x) = H`.
3. **Second Pre-image Resistance**: Given input `x`, it is infeasible to find a different `y` such that `Hash(x) = Hash(y)`.
4. **Collision Resistance**: It is computationally impossible to find any two arbitrary inputs `x` and `y` that share `Hash(x) = Hash(y)`.
5. **Avalanche Effect**: Flipping a single bit in the input radically scrambles the resulting output (typically ~50% of the bits change).

---

## 2. Asymmetric Cryptography & Digital Signatures

Blockchains use public-key cryptography (typically elliptic curve cryptography like `secp256k1` or `Ed25519`). The Python wallet in this repository is an educational simulator: its address is a hash of private-key text, and its transaction signature is a plain hash, not an elliptic-curve signature. It does not provide the verification or key protection required for real funds. Do not reuse real wallet keys with this code.

A production system derives a public key from the private key using a reviewed curve implementation and verifies signatures against the public key:

- **Private Key**: A randomly generated 256-bit number known strictly to the owner.
- **Public Key**: Derived mathematically from the private key via elliptic curve point multiplication ($K = k \cdot G$).
- **Public Address**: A hashed, encoded version of the public key (e.g., Keccak-256 in Ethereum, RIPEMD160 in Bitcoin).

### The Digital Signature Workflow:

```
[Transaction Data] + [Private Key] ──► [Sign Algorithm] ──► [Digital Signature]

[Transaction Data] + [Public Key] + [Digital Signature] ──► [Verify Algorithm] ──► True / False
```

- **Authentication**: Proves the sender authorized the transaction.
- **Non-repudiation**: The signer cannot deny originating the message.
- **Integrity**: Any tampering with the transaction payload breaks the signature.

---

## 3. Merkle Trees & Cryptographic Proofs

A **Merkle Tree** (binary hash tree) organizes all transactions inside a block into a single 32-byte hash called the **Merkle Root**.

```
                        [ Merkle Root (Hash0123) ]
                                /        \
                               /          \
                      [ Hash01 ]          [ Hash23 ]
                       /      \            /      \
                  [ Hash0 ] [ Hash1 ]  [ Hash2 ] [ Hash3 ]
                     |         |          |         |
                   Tx 0      Tx 1       Tx 2      Tx 3
```

### Why Merkle Trees are Revolutionary:
1. **SPV (Simplified Payment Verification)**: A lightweight mobile node doesn't need to download millions of transactions. It only downloads block headers.
2. **Logarithmic Proof Size**: To prove transaction `Tx 2` is included in a block with $N$ transactions requires only $\lceil\log_2 N\rceil$ intermediate hashes (a Merkle audit path), instead of scanning all $N$ transactions.

---

## 4. Inside a Block

Every block in a blockchain consists of two sections:

### 1. Block Header (~80 bytes in Bitcoin)
- **Version**: Protocol rule version.
- **Previous Block Hash**: 256-bit hash linking to parent block.
- **Merkle Root**: 256-bit summary hash of all transactions.
- **Timestamp**: Unix epoch timestamp.
- **Difficulty Target (Bits)**: The target threshold the block hash must satisfy.
- **Nonce**: 32-bit arbitrary number incremented during mining.

### 2. Block Body
- Transaction counter.
- Full array of serialized transactions (including the Coinbase / Miner reward transaction).

```
   Block #100                     Block #101
┌─────────────────────────┐    ┌─────────────────────────┐
│ Previous: 0000abc...    │◄───│ Previous: 0000def...    │
│ Merkle Root: 38f9...    │    │ Merkle Root: 82a1...    │
│ Nonce: 1,842,910        │    │ Nonce: 4,029,183        │
│ Hash: 0000def...        │    │ Hash: 000098a...        │
├─────────────────────────┤    ├─────────────────────────┤
│ [Tx0, Tx1, Tx2, ...]    │    │ [Tx0, Tx1, Tx2, ...]    │
└─────────────────────────┘    └─────────────────────────┘
```
