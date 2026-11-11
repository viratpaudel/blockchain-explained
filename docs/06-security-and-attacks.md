# Module 06: Blockchain Security & Attack Vectors

While blockchain guarantees cryptographic ledger immutability, vulnerabilities in consensus rules, peer-to-peer networking, and application-layer smart contracts have resulted in billions of dollars in historical exploits.

---

## 1. Network & Consensus Attacks

### 1. 51% Attack (Double Spending)
If an entity controls $> 50\%$ of the network's mining hashrate (PoW) or staked capital (PoS), they can:
- Mine private blocks in secret and release a longer chain to reorganize the public ledger (**Reorg**).
- Double-spend coins by reversing their own past payments.
- Censor transactions from specific addresses.
- *Limitation*: Even with 51% hashrate, an attacker **cannot** forge transactions or spend coins from wallets without private keys.

### 2. Sybil & Eclipse Attacks
- **Sybil Attack**: Spawning thousands of pseudonymous nodes to gain disproportionate voting influence. Solved by proof-of-work/stake requirements.
- **Eclipse Attack**: An attacker isolates a target victim node by surrounding all of its peer connections with attacker-controlled IP addresses, feeding it counterfeit chain state.

---

## 2. Smart Contract Vulnerabilities

### 1. Reentrancy Attacks (The DAO Hack, 2016)
Occurs when an external contract call transfers funds *before* updating the user's internal balance:

```solidity
// VULNERABLE CODE:
function withdraw(uint256 amount) external {
    require(balances[msg.sender] >= amount);
    (bool success, ) = msg.sender.call{value: amount}(""); // Handover execution!
    require(success);
    balances[msg.sender] -= amount; // State updated too late!
}
```

An attacker's contract implements a `fallback()` / `receive()` function that re-invokes `withdraw()` before the balance is deducted, draining the entire pool.

#### Prevention: Checks-Effects-Interactions Pattern
```solidity
// SECURE CODE:
function withdraw(uint256 amount) external {
    require(balances[msg.sender] >= amount); // 1. Check
    balances[msg.sender] -= amount;          // 2. Effect (Update State)
    (bool success, ) = msg.sender.call{value: amount}(""); // 3. Interaction
    require(success);
}
```

---

## 3. DeFi-Specific Attack Vectors

### 1. Flash Loan Price Oracle Manipulation
1. Attacker takes an uncollateralized Flash Loan of \$50M USDC from Aave.
2. Dumps the \$50M into a low-liquidity Uniswap pool to artificially crash the spot price.
3. Interacts with a lending protocol relying on the spot AMM price as its oracle, borrowing underpriced assets.
4. Repays the flash loan within the identical block, pocketing the arbitrage difference.
- **Defense**: Use Time-Weighted Average Price (TWAP) or decentralized off-chain oracles (e.g., Chainlink).

### 2. Signature Replay Attacks
Using a valid signed message from one chain on another chain (e.g., Ethereum Mainnet vs Arbitrum).
- **Defense**: EIP-712 structured data hashing with explicit `chainId` domain separators.

---

## 🛡️ Web3 Smart Contract Audit Checklist

- [x] **Checks-Effects-Interactions**: Update state before making external contract calls.
- [x] **ReentrancyGuard**: Use OpenZeppelin's `nonReentrant` modifier on state-altering external methods.
- [x] **Decentralized Oracles**: Never use instantaneous AMM spot reserves (`balanceOf`) for collateral valuation.
- [x] **Access Control**: Explicit `onlyOwner` or RBAC controls on administrative functions.
- [x] **Commit-Reveal Schemes**: Protect sensitive user actions against public mempool front-running.
