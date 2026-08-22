# 🛡️ Software Requirements Specification (SRS)
## SecureMailScope: Air-Gapped Email Security Posture & Explainable Risk Fusion Engine

---

## 📄 Executive Summary (Refined Privacy & Security Focus)

Imagine an intelligence analyst at **NTRO (National Technical Research Organisation)** receiving a high-risk email that appears to originate from an official government department (`pmo.gov.in`). The signature looks authentic, and no malicious body content is present.

However, hidden within the RFC 5322 header metadata and transmission envelope:
1. The visible display name uses executive keywords (*"Director General"*) paired with a non-government sender domain.
2. The domain utilizes an Internationalized Domain Name (IDN) with Cyrillic confusable characters.
3. Intermediate relay headers indicate unencrypted plaintext hops.

**SecureMailScope** acts as an **Air-Gapped Forensic Decision-Support System**. 
It inspects RFC 5322 header metadata, cryptographic signatures (SPF, DKIM, DMARC, ARC), and transport signals **without reading or ingesting private email body text**. It generates an **Explainable Evidence Audit Tree** and a **Security Posture Index ($0 - 100\%$)** to assist SOC analysts in real-time incident triage.

---

## 1. 📌 System Overview & Operating Modes

### 1.1 Objective
To construct a real-time, privacy-preserving, zero-trust email security posture assessment platform for **NTRO** that evaluates metadata, authentication records, domain similarity, and transport signals without exposing sensitive communications to third-party cloud APIs.

### 1.2 Dual Deployment Modes

```
┌──────────────────────────────────────────────────────────────────────────────────────────┐
│                             SECUREMAILSCOPE DEPLOYMENT MODES                             │
└──────────────────────────────────────────────────────────────────────────────────────────┘

  [OFFLINE AIR-GAPPED FORENSIC MODE]            [CONNECTED VALIDATION MODE (Optional)]
  • Parses captured `.eml` files locally         • Active DNS TXT lookup for DKIM `p=` key size
  • Zero external network requests               • Active SMTP STARTTLS probe to target MX
  • Uses local pre-cached domain whitelists       • Active MTA-STS & TLS-RPT policy checks
  • Zero data exfiltration / privacy guarantee   • Enhanced real-time intelligence lookup
```

---

## 2. ⚙️ Core System Pipeline & Explainable Risk Engine

```
┌──────────────────────────────────────────────────────────────────────────────────────────┐
│                                 RISK FUSION ARCHITECTURE                                 │
└──────────────────────────────────────────────────────────────────────────────────────────┘

  [Raw .eml File / Air-Gapped Local Upload]
                     │
                     ▼
  ┌─────────────────────────────────────────────────────────────────────────────────────┐
  │                 MODULE 1: RFC 5322 PARSER & SKELETON NORMALIZER                      │
  ├─────────────────────────────────────────────────────────────────────────────────────┤
  │ • Extracts Visible From, Return-Path, Authentication-Results, Received Hops, ARC      │
  │ • Applies Unicode NFKC Skeleton Normalization for IDN confusable matching           │
  │ • Extracts Display-Name vs Envelope Address for Executive Impersonation Detection   │
  └────────────────────────────┬────────────────────────────────────────────────────────┘
                               │
                               ▼
  ┌─────────────────────────────────────────────────────────────────────────────────────┐
  │              MODULE 2: DETERMINISTIC RULE & ANOMALY FUSION ENGINE                   │
  ├─────────────────────────────────────────────────────────────────────────────────────┤
  │ • Cryptographic Verification: DKIM signature verification + DNS key modulus check   │
  │ • Identity & Similarity: Levenshtein distance matching against government whitelists │
  │ • Transport Inspection: Passive Received header parsing vs. Active SMTP probes     │
  │ • ARC Chain Validation: Validates multi-hop seals for forwarded emails (RFC 8617)  │
  └────────────────────────────┬────────────────────────────────────────────────────────┘
                               │
                               ▼
  ┌─────────────────────────────────────────────────────────────────────────────────────┐
  │                 MODULE 3: EXPLAINABLE EVIDENCE TREE & REPORTING                     │
  ├─────────────────────────────────────────────────────────────────────────────────────┤
  │ • Generates Point-by-Point Breakdown: (+35 Executive Impersonation, +20 DKIM Fail)  │
  │ • Interactive D3.js Hop Topology Map (Highlighting plaintext/downgrade points)      │
  │ • 1-Click Signed NTRO Forensic PDF Audit Report Generator                           │
  └─────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 🔬 3. Technical Mitigations & Hardened Solutions

Below are the **6 core technical corrections** implemented in SecureMailScope to guarantee defense-grade credibility:

| Vector / Issue | Traditional Flaw | SecureMailScope Technical Implementation |
|----------------|------------------|------------------------------------------|
| **1. DKIM RSA Key Size Audit** | Guessing key size based on verification pass/fail. | Extract selector `s=` and domain `d=`, query DNS TXT record for `s._domainkey.d`, decode public key modulus `p=`, and measure exact RSA bit length ($<1024$-bit = Vulnerable). |
| **2. Transport Security Claims** | Claiming full historical TLS ciphers from headers alone. | Distinguish **Passive Header Evidence** (`ESMTPS` stamps in `Received:` headers) from **Active Infrastructure Probing** (SMTP STARTTLS handshake checks). |
| **3. Forwarded Email SPF Failures** | Flagging forwarded messages as spoofed. | Implement **ARC Chain Validation (RFC 8617)**. If SPF fails but valid `ARC-Seal` signatures exist from trusted forwarders, reduce SPF penalty score by 80%. |
| **4. Unicode Homograph Attacks** | Marking any `xn--` Punycode domain as malicious. | Apply **Unicode NFKC Skeleton Normalization** + Confusable Character Matching + String Distance against official domain whitelists (`nic.in`, `gov.in`). |
| **5. Operational Security in Demos** | Forwarding live emails to public servers (privacy leak). | Deploy an **Air-Gapped Local Web UI** (`localhost` drag-and-drop `.eml` scanner). Zero network leakage. |
| **6. Explainability vs Black-Box ML** | Unexplainable $0-100\%$ score from an opaque ML model. | **Deterministic Risk Fusion Engine** producing an explicit **Evidence Audit Tree** listing exactly how every penalty point was calculated. |

---

## 📊 4. Non-Functional Requirements & Performance Benchmarks

| Metric | Target Goal | Justification |
|--------|-------------|---------------|
| **Local Parsing Latency** | $< 150 \text{ ms}$ (p95 local benchmark) | Real-time throughput for air-gapped security gateways |
| **Privacy Compliance** | $100\%$ Header-Only Parsing | Zero ingestion or storage of private email body text |
| **Air-Gapped Operation** | $100\%$ Functional Offline | Protects classified government intelligence networks |
| **Explainability Coverage** | $100\%$ Evidence Traceability | Every risk score output includes a point-by-point audit log |

---

## 📅 5. 36-Hour Hackathon Implementation Plan

```
HOUR 00 - 06: AIR-GAPPED PARSER & DETERMINISTIC RULES
├── Implement Python `email` & `dkimpy` RFC 5322 header parser
├── Build NFKC Unicode normalizer & confusable matching engine
└── Create local SQLite domain whitelist database

HOUR 06 - 14: PASSIVE/ACTIVE TRANSPORT & ARC ENGINE
├── Build Received header transport evidence extractor
├── Implement ARC (RFC 8617) multi-hop seal validation
└── Implement DNS DKIM selector `p=` modulus bit-length resolver

HOUR 14 - 24: EXPLAINABLE UI & HOP TOPOLOGY
├── Build React / Streamlit Air-Gapped SOC Dashboard
├── Create D3.js hop routing topology map
└── Implement ReportLab Forensic PDF Audit Report generator

HOUR 24 - 30: LOCAL SCENARIO TESTING & HARDENING
├── Test against sample dataset (Legitimate, Spoofed, Homograph, Forwarded `.eml`)
├── Verify zero-network air-gapped execution
└── Benchmark local p95 parsing latency

HOUR 30 - 36: PRESENTATION & DEFENSE PREPARATION
├── Finalize pitch deck focusing on privacy-preserving decision support
└── Practice hostile Q&A defense (Passive vs Active, DKIM lookup, ARC logic)
```

---

<div align="center">

**Refined Software Requirements Specification | NTRO (PS #SIH26159)**

</div>
