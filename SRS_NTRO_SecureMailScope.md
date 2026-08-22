# 🛡️ Software Requirements Specification (SRS)
## SecureMailScope: AI-Assisted Cryptographic Security Posture Assessment for Secure Email Communications

---

## 📄 Executive Summary (The Layman's Analogy)

Imagine a high-ranking intelligence officer at **NTRO** receiving an email that looks 100% like a confidential memo from the Prime Minister's Office. The sender name says *"PMO India"*, the signature looks official, and there are no spelling mistakes. 

However, hidden deep inside the digital envelope's invisible header stamps, an attacker has forged the origin IP, bypassed encryption checks, and used a lookalike domain (`pmо.gov.in` with a Cyrillic `'о'`).

**SecureMailScope** acts as an **Automated Digital Forensic Expert**. 
It inspects the invisible cryptographic seals (SPF, DKIM, DMARC, TLS certificates, ARC chains) and analyzes header routing geometry in real-time, giving NTRO analysts an immediate, mathematically proven **Trust & Risk Rating** before an officer ever opens an attachment or clicks a link.

---

## 1. 📌 System Overview & Objectives

### 1.1 Objective
To develop a real-time, zero-trust, AI-assisted cryptographic security posture assessment platform for **NTRO (National Technical Research Organisation)** that evaluates email headers, authentication records, domain reputations, and cryptographic transport layers without violating email content privacy.

### 1.2 Key Design Principles
- **100% Header & Metadata Centric:** No reliance on reading private email body text (Privacy-Preserving).
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
  │                      MODULE 1: HEADER PARSER & CRYPTO EXTRACTOR                     │
  ├─────────────────────────────────────────────────────────────────────────────────────┤
  │ • Envelope Sender vs. Display Header From (Spoofing & Homograph Check)              │
  │ • Authentication-Results: SPF Alignment, DKIM RSA Key Size, DMARC Policy (p=reject)│
  │ • Hop Geometry: Extraction of all 'Received:' headers, TLS Cipher Suite, STARTTLS    │
  └────────────────────────────┬────────────────────────────────────────────────────────┘
                               │
                               ▼
  ┌─────────────────────────────────────────────────────────────────────────────────────┐
  │                      MODULE 2: CRYPTOGRAPHIC posture & ML ENGINE                    │
  ├─────────────────────────────────────────────────────────────────────────────────────┤
  │ • Cryptographic Rule Engine: Deterministic verification (dkimpy + DNSSEC check)    │
  │ • Homograph & Typosquatting Detector: Levenshtein Distance & Cyrillic Normalizer     │
  │ • Anomaly Classifier: XGBoost / Random Forest trained on header features           │
  └────────────────────────────┬────────────────────────────────────────────────────────┘
                               │
                               ▼
  ┌─────────────────────────────────────────────────────────────────────────────────────┐
  │                 MODULE 3: NTRO FORENSIC DASHBOARD & REPORT GENERATOR                │
  ├─────────────────────────────────────────────────────────────────────────────────────┤
  │ • Interactive Visual Hop Graph: D3.js physical server routing map                   │
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
  - **DKIM (DomainKeys Identified Mail):** Signature validity, Public Key Length (512-bit = Weak, 1024/2048-bit = Secure), Selector verification.
  - **DMARC (Domain-based Message Authentication):** Enforced policy (`none`, `quarantine`, `reject`), Percentage alignment.
  - **Transport Encryption (TLS):** Protocol Version (TLS 1.0/1.1 = Insecure, TLS 1.2/1.3 = Secure), Perfect Forward Secrecy (PFS) verification.
  - **ARC (Authenticated Received Chain):** Multi-hop trust preservation verification for forwarded messages.

### Module 2: Homograph, Typosquatting & Anomaly Detection Engine
* **Unicode Homograph Detection:** Converts incoming sender domain to Punycode and compares visual string distance using Levenshtein distance against known government domains (`gov.in`, `nic.in`, `ntro.gov.in`, `pmo.gov.in`).
* **Display-Name Impersonation Check:** Flag when `Header From` name contains executive keywords (e.g., *"Director General"*, *"Command Control"*) while actual `Envelope-From` address points to non-governmental email infrastructure.
* **Machine Learning Classifier:** XGBoost model trained on 18 header metadata features predicting probability of malicious security posture.

### Module 3: Visual Hop Graph & 1-Click Forensic Auditor
* **Routing Hop Graph:** Reconstructs the full sequence of intermediate mail transfer agents (MTAs) from `Received:` headers. Highlights TLS downgrade points in red.
* **Automated PDF Generator:** Produces a standardized, formal 2-page NTRO Forensic Audit Report with cryptographic evidence hashes and recommended firewall block actions.

---

## ⚠️ 4. Real-World Limitations, Failures & Research Counter-Measures

Below are the **5 major technical challenges** in email security posture assessment and how SecureMailScope solves them:

---

### 🔴 Limitation #1: "Legitimate Emails Failing SPF Due to Forwarding"
* **The Challenge:** When an email is legitimate but forwarded through an intermediary server, SPF checks naturally fail (because the forwarding server IP is not listed in the original sender's SPF record). Naive models flag these as attacks.
* **Research Basis:** RFC 8617 (Authenticated Received Chain - ARC protocol).
* **Our Solution:** Implement **ARC Header Chain Validation**. If SPF fails but valid ARC headers exist with signed DKIM stamps from trusted intermediate hops, the system recalculates risk to avoid false positives.

---

### 🔴 Limitation #2: "Weak 512-bit / 1024-bit DKIM RSA Key Attacks"
* **The Challenge:** Attackers can sign malicious emails using real DKIM keys if the target domain uses legacy, short 512-bit RSA keys that are vulnerable to prime factorization attacks.
* **Research Basis:** IEEE Security & Privacy (Semiconductor & Cryptography standards).
* **Our Solution:** SecureMailScope doesn't just check `DKIM: PASS`. It extracts the **public key size** from DNS. Keys $< 1024\text{ bits}$ are flagged with a **HIGH CRYPTOGRAPHIC RISK** rating regardless of signature validity.

---

### 🔴 Limitation #3: "Unicode Homograph / IDN Visual Spoofing"
* **The Challenge:** Attackers register domains like `pmo-gov.in` or use Cyrillic characters (e.g., `pmo.gоv.in`) where the `'о'` is U+043E (Cyrillic Small Letter O) instead of U+006F (Latin O).
* **Our Solution:** Implement **Skeleton Normalization (RFC 5890 Punycode)** + **Confusable Character Mapping** using the Unicode Consortium Security standard. All input domains are normalized to ASCII before matching against whitelist databases.

---

### 🔴 Limitation #4: "Offline DNS Lookup Delays During Live Demo"
* **The Challenge:** Querying live public DNS for SPF/DKIM/DMARC records during a hackathon demo can fail due to slow venue Wi-Fi or DNS rate-limiting.
* **Our Solution:** **Multi-Tiered DNS Cache Engine.**
  1. Pre-cached local SQLite database containing DNS/SPF/DMARC records for Top 5,000 domains.
  2. Asynchronous parallel DNS resolver (`dnspython` + `asyncio`) with a 500ms fallback timeout.

---

### 🔴 Limitation #5: "Privacy Violations (Reading Email Content)"
* **The Challenge:** Intelligence agencies like NTRO cannot deploy tools that parse private body text due to confidentiality laws.
* **Our Solution:** **Strict Header-Only Metadata Analysis.** The system operates 100% on headers and cryptographic envelopes, guaranteeing **zero content inspection**.

---

## 📊 5. Non-Functional Requirements & Performance Benchmarks

| Metric | Target Goal | Justification |
|--------|-------------|---------------|
| **Analysis Latency** | $< 350 \text{ ms}$ per email | Instant feedback for email gateways |
| **Model Precision (Phishing/Spoof)**| $> 96.5\%$ | Minimizes false security alarms |
| **False Negative Rate (Missed Attacks)**| $< 0.1\%$ | Critical for defense & national security |
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
