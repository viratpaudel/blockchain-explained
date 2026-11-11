# Module 03: Smart Contracts & The Ethereum Virtual Machine (EVM)

While Bitcoin was designed as decentralized programmable money, Ethereum generalized the blockchain into a **decentralized, Turing-complete world computer**.

---

## 1. What is a Smart Contract?

First conceptualized by Nick Szabo in 1994, a **smart contract** is self-executing code deployed to an immutable address on the blockchain.
- Operates under the premise: **"Code is Law"**.
- Does not require a lawyer, escrow agent, or bank to enforce execution.
- If predefined conditions are satisfied, state transitions execute automatically.

---

## 2. EVM Architecture

The **Ethereum Virtual Machine (EVM)** is a stack-based runtime environment embedded in every full node.

```
┌──────────────────────────────────────────────────────────┐
│                     EVM State Machine                    │
│                                                          │
│  [ Stack ]       [ Memory ]         [ Storage ]          │
│  1024 depth      Volatile byte      Persistent 256-bit   │
│  256-bit words   array              key-value trie (Gas) │
│                                                          │
│  ┌────────────────────────────────────────────────────┐  │
│  │ EVM Bytecode: PUSH1 0x60 PUSH1 0x40 MSTORE CALL ...│  │
│  └────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────┘
```

### Key Memory Spaces:
1. **Stack**: LIFO stack holding up to 1024 256-bit elements. All arithmetic operations occur here.
2. **Memory**: Temporary byte array allocated during contract execution; discarded after call completion.
3. **Storage**: Permanent, expensive key-value mapping ($2^{256} \to 2^{256}$) stored directly in the global Merkle Patricia Trie.
4. **Calldata**: Read-only, immutable byte array containing the transaction payload and function arguments.

---

## 3. Gas Mechanics & Halting Problem

Because the EVM is Turing-complete (supporting loops), a malicious actor could write an infinite loop (`while(true){}`) to freeze all nodes across the world.

### The Solution: Gas
- Every EVM opcode consumes a designated amount of **Gas** (computational units).
  - e.g., `ADD`: 3 gas, `SSTORE` (writing to storage): up to 20,000 gas.
- The sender specifies:
  - **Gas Limit**: Maximum gas they are willing to burn.
  - **Gas Price / Base Fee + Priority Tip** (EIP-1559): Cost per unit of gas in Gwei ($10^{-9}$ ETH).
- If gas runs out mid-execution: state changes **revert**, but the burned gas is forfeited to the block builder.

---

## 4. Token Standards

Standardized interfaces allow smart contracts and decentralized exchanges (DEXs) to interact seamlessly:

### 1. ERC-20 (Fungible Tokens)
Every unit is identical (e.g., USDC, UNI, DAI).
```solidity
interface IERC20 {
    function totalSupply() external view returns (uint256);
    function balanceOf(address account) external view returns (uint256);
    function transfer(address to, uint256 value) external returns (bool);
    function approve(address spender, uint256 value) external returns (bool);
    function transferFrom(address from, address to, uint256 value) external returns (bool);
}
```

### 2. ERC-721 (Non-Fungible Tokens - NFTs)
Each token has a unique `tokenId` representing discrete ownership of digital or real-world assets.

### 3. ERC-1155 (Multi-Token Standard)
Combines fungible and non-fungible tokens into a single smart contract for gas-efficient batch operations.
