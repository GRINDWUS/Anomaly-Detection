# 🛡️ Software Requirements Specification (SRS)
## SecureMailScope: AI-Assisted Cryptographic Security Posture Assessment for Secure Email Communications

---

## 📄 Executive Summary (The Layman's Analogy)

Imagine a high-ranking intelligence officer at **NTRO (National Technical Research Organisation)** receiving an email that looks 100% like a confidential memo from the Prime Minister's Office. The sender name says *"PMO India"*, the signature looks official, and there are no spelling mistakes. 

However, hidden deep inside the digital envelope's invisible header stamps, an attacker has forged the origin IP, downgraded encryption, and used a lookalike domain (`pmо.gov.in` using a Cyrillic `'о'`).

**SecureMailScope** acts as an **Automated Digital Forensic Expert**. 
It inspects the invisible cryptographic seals (SPF, DKIM key lengths, DMARC, TLS certificates, ARC chains) and analyzes header routing geometry in real-time, giving NTRO analysts an immediate, mathematically proven **Trust & Risk Rating** before an officer ever opens an attachment or clicks a link.

---

## 1. 📌 System Overview & Objectives

### 1.1 Objective
To develop a real-time, zero-trust, AI-assisted cryptographic security posture assessment platform for **NTRO** that evaluates email headers, authentication records, domain reputations, and cryptographic transport layers without violating email content privacy.

### 1.2 Key Design Principles
- **100% Header & Metadata Centric:** Zero inspection of private email body text (Privacy-Preserving & Audit-Compliant).
- **Zero-Trust Offline Architecture:** All parsing, ML classification, and forensic report generation run **100% locally and offline** (Zero data leakage to external APIs like OpenAI/VirusTotal).
- **Interactive Live Validation:** Support for instant real-time drag-and-drop `.eml` analysis and live QR-forwarding.

---

## 2. ⚙️ System Architecture & Data Flow

```
┌──────────────────────────────────────────────────────────────────────────────────────────┐
│                            SECUREMAILSCOPE MASTER PIPELINE                               │
└──────────────────────────────────────────────────────────────────────────────────────────┘

  [Raw .eml File / Live Forwarded Email Stream]
                       │
                       ▼
  ┌─────────────────────────────────────────────────────────────────────────────────────┐
  │                 MODULE 1: RFC 5322 PARSER & SKELETON NORMALIZER                      │
  ├─────────────────────────────────────────────────────────────────────────────────────┤
  │ • Envelope Sender vs. Display Header From (Spoofing & Homograph Check)              │
  │ • Authentication-Results: SPF Alignment, DKIM RSA Key Size, DMARC Policy (p=reject)│
  │ • Hop Geometry: Extraction of all 'Received:' headers, TLS Cipher Suite, STARTTLS    │
  └────────────────────────────┬────────────────────────────────────────────────────────┘
                               │
                               ▼
  ┌─────────────────────────────────────────────────────────────────────────────────────┐
  │              MODULE 2: CRYPTOGRAPHIC POSTURE & ML ENGINE                            │
  ├─────────────────────────────────────────────────────────────────────────────────────┤
  │ • Cryptographic Rule Engine: Deterministic verification (dkimpy + DNSSEC check)    │
  │ • Homograph & Typosquatting Detector: Levenshtein Distance & Cyrillic Normalizer     │
  │ • Failure Kinetic Classifier: Handles ARC forwarding (RFC 8617) & weak RSA keys     │
  │ • Anomaly Classifier: XGBoost / Random Forest trained on 18 header features         │
  └────────────────────────────┬────────────────────────────────────────────────────────┘
                               │
                               ▼
  ┌─────────────────────────────────────────────────────────────────────────────────────┐
  │                 MODULE 3: NTRO FORENSIC DASHBOARD & REPORT GENERATOR                │
  ├─────────────────────────────────────────────────────────────────────────────────────┤
  │ • Interactive Visual Hop Graph: D3.js physical server routing map (TLS Downgrades)  │
  │ • Trust Score Card: Overall Risk (0-100%) + Cryptographic Breakdowns                │
  │ • 1-Click Forensic Export: Automated NTRO PDF Incident Report Generation            │
  └─────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 3. 🔬 Core Modules Deep-Dive

### Module 1: Cryptographic Header & Authentication Parser
* **Input:** Raw `.eml` file or raw RFC 5322 header string.
* **Extracted Features:**
  - **SPF (Sender Policy Framework):** Pass, Fail, SoftFail, Neutral, Alignment check.
  - **DKIM (DomainKeys Identified Mail):** Signature validity AND Public Key Length inspection ($<1024$-bit = Vulnerable, $\ge 2048$-bit / Ed25519 = Secure).
  - **DMARC (Domain-based Message Authentication):** Enforced policy (`none`, `quarantine`, `reject`), Percentage alignment.
  - **Transport Encryption (TLS):** Protocol Version (TLS 1.0/1.1 = Insecure, TLS 1.2/1.3 = Secure), Perfect Forward Secrecy (PFS) verification.
  - **ARC (Authenticated Received Chain):** Multi-hop trust preservation verification for forwarded messages (RFC 8617).

### Module 2: Homograph, Typosquatting & Anomaly Detection Engine
* **Unicode Homograph Detection:** Converts incoming sender domain to Punycode (RFC 5890) and compares visual string distance using Levenshtein distance against known government domains (`gov.in`, `nic.in`, `ntro.gov.in`, `pmo.gov.in`).
* **Display-Name Impersonation Check:** Flags when `Header From` name contains executive keywords (*Director General, Command Control, Admin*) while actual `Envelope-From` address points to consumer/non-governmental infrastructure.
* **Machine Learning Classifier:** XGBoost model trained on 18 non-content header metadata features predicting probability of malicious security posture.

### Module 3: Visual Hop Graph & 1-Click Forensic Auditor
* **Routing Hop Graph:** Reconstructs the full sequence of intermediate mail transfer agents (MTAs) from `Received:` headers. Highlights TLS downgrade points in bright red.
* **Automated PDF Generator:** Produces a standardized, formal 2-page NTRO Forensic Audit Report with evidence hashes and recommended firewall block actions.

---

## ⚠️ 4. Real-World Limitations, Failures & Research Counter-Measures

Below are the **7 major technical challenges** in email security posture assessment and how SecureMailScope solves them:

| Challenge / Vulnerability | Research / Industry Basis | SecureMailScope Solution |
|---------------------------|---------------------------|--------------------------|
| **1. Forwarded Emails Failing SPF** | RFC 8617 (Authenticated Received Chain - ARC) | Implement **ARC Chain Validation**. If SPF fails but valid ARC seals exist from trusted intermediate hops (e.g., Google/Microsoft), downgrade the SPF penalty score by 80%. |
| **2. Weak 512-bit / 1024-bit DKIM Keys** | RFC 8301 (Deprecating 512-bit RSA keys) | Extract public key modulus `p=` from DNS. If key size is $<1024$-bit, flag **CRITICAL RISK** even if `DKIM: PASS`. |
| **3. STARTTLS Stripping / Downgrade Attacks** | RFC 8461 (MTA-STS) & ACM CoNEXT | Parse all `Received:` headers in reverse order. Flag any unencrypted or TLS 1.0/1.1 hop in **bright red** on the visual hop graph. |
| **4. Unicode Homograph Spoofing** | RFC 5890 Punycode & Unicode Security | Apply **Skeleton Normalization**. Convert domains to Punycode (`xn--`) and match against official government domain whitelists. |
| **5. Display-Name Executive Impersonation** | Social Engineering Tactics | Extract `display_name` & `addr_spec`. Trigger warning if executive titles match non-government sender domains. |
| **6. Slow Hackathon Wi-Fi / DNS Timeouts** | Demo Reliability Engineering | **Multi-Tiered Local Cache Strategy:** SQLite database with cached DNS/SPF/DMARC records for Top 10,000 domains + 300ms DNS query timeout. |
| **7. Privacy & Classification Laws** | Government Intelligence Standards | **100% Header & Metadata Analysis.** System operates with zero content inspection, ensuring complete privacy compliance. |

---

## 📊 5. Non-Functional Requirements & Performance Benchmarks

| Metric | Target Goal | Justification |
|--------|-------------|---------------|
| **Analysis Latency** | $< 350 \text{ ms}$ per email | Instant feedback for email security gateways |
| **Model Precision (Phishing/Spoof)**| $> 96.5\%$ | Minimizes false security alarms |
| **False Negative Rate (Missed Attacks)**| $< 0.1\%$ | Critical for national security communications |
| **Offline Functionality** | $100\%$ | Zero data leakage to public internet |
| **Header Parsing Speed** | $> 1,000 \text{ headers/sec}$ | High-throughput enterprise gateway processing |

---

## 📅 6. 36-Hour Hackathon Sprint Plan

```
HOUR 00 - 06: CORE PARSER & CRYPTO ENGINE
├── Implement Python `email` & `dkimpy` header extraction pipeline
├── Build SPF, DKIM Key-Length, DMARC, and TLS feature extractor
└── Test on Enron & Nazario Phishing sample .eml files

HOUR 06 - 14: ML MODEL & HOMOGRAPH DETECTOR
├── Train XGBoost classifier on 18 header metadata features
├── Implement Punycode Unicode Homograph & Levenshtein distance matcher
└── Output: Evaluated model with >95% precision/recall

HOUR 14 - 24: DASHBOARD & VISUAL HOP GRAPH
├── Build React / Streamlit NTRO Audit Dashboard
├── Create D3.js / NetworkX Server Hop Graph (mapping IP locations & TLS downgrades)
└── Implement 1-Click Forensic PDF Audit Generator (ReportLab)

HOUR 24 - 30: LIVE DEMO QR FORWARDING & TESTING
├── Setup FastAPI endpoint with WebSocket real-time updates
├── Build Live QR Code / Drag-and-Drop .eml scanner for judges
└── Test live email forwarding end-to-end

HOUR 30 - 36: PRESENTATION POLISH & JUDGE Q&A PREP
├── Finalize pitch deck focusing on NTRO deployment scenario
└── Practice live judge demonstration (Judges forward their own emails)
```

---

<div align="center">

**Prepared for Smart India Hackathon 2026 | NTRO (National Technical Research Organisation)**

</div>
