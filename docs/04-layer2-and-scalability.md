# Module 04: Layer 2 Scaling & Rollups

Decentralized Layer 1 blockchains process transactions serially (Bitcoin ~7 TPS, Ethereum L1 ~15-30 TPS). To support global throughput, computation must scale **off-chain** while maintaining Layer 1 decentralized security.

---

## 1. Rollup Mechanics: Off-Chain Execution, On-Chain Security

A **Rollup** executes hundreds of transactions off-chain, compresses their state changes, and posts minimal transaction batches and state roots back down to Layer 1.

```
[Users Send Transactions]
           │
           ▼
[ Layer 2 Sequencer / Execution Engine ]  (High TPS: 2,000 - 10,000 TPS)
           │
           ▼  (Compress & Batch)
[ State Root + Calldata / Blob Space ] ──► [ Layer 1 Consensus & Data Availability ]
```

---

## 2. Optimistic Rollups vs. Zero-Knowledge (ZK) Rollups

```
┌──────────────────────┬──────────────────────────────┬──────────────────────────────┐
│ Property             │ Optimistic Rollups           │ ZK-Rollups                   │
├──────────────────────┼──────────────────────────────┼──────────────────────────────┤
│ Core Mechanism       │ Assume valid; challenge window│ Cryptographic validity proof │
│ Settlement Time      │ 7-day challenge dispute delay│ Instant (minutes for proof)  │
│ Proof Math           │ Interactive Fraud Proofs     │ zk-SNARKs / zk-STARKs        │
│ Computational Cost   │ Low sequencer cost           │ High prover generation cost  │
│ Leading Projects     │ Arbitrum, Optimism, Base     │ zkSync, Starknet, Scroll     │
└──────────────────────┴──────────────────────────────┴──────────────────────────────┘
```

### Optimistic Rollups (Fraud Proofs)
- State transitions are assumed honest by default.
- Anyone can inspect the posted data and submit an on-chain **Fraud Proof** during a 7-day challenge window.
- If fraud is proven, the invalid state transition is rolled back, and the fraudulent sequencer's bond is slashed.

### ZK-Rollups (Validity Proofs)
- Sequencers generate a succinct mathematical zero-knowledge proof (zk-SNARK or zk-STARK) proving mathematical execution correctness.
- The L1 smart contract verifies this proof in milliseconds; invalid states are cryptographically impossible to commit.

---

## 3. Data Availability & EIP-4844 (Proto-Danksharding)

For fraud proofs or state reconstruction to work, the raw transaction data must be accessible to anyone:
- Historically, rollups stored data as expensive L1 `calldata`.
- **EIP-4844** introduced temporary ephemeral **Data Blobs** (~128 KB each) pruned after ~18 days.
- Slashed Layer 2 transaction fees by over 90%, paving the way for mass adoption.
