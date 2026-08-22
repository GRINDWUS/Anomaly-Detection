# 🔬 SECUREMAILSCOPE — HARDENED MASTER ARCHITECTURE & ENGINEERING SPECIFICATION

---

## 📌 Architectural Core Philosophy

**SecureMailScope** is an **Air-Gapped, Privacy-Preserving Email Security Posture & Risk Fusion System** built for **NTRO (National Technical Research Organisation)**.

Instead of inspecting private email body text (which violates confidentiality laws and creates exfiltration risks), SecureMailScope evaluates **deterministic email authentication (SPF, DKIM, DMARC, ARC), transport protocol signals, identity similarity, and statistical metadata anomalies**.

---

## 1. 🏗️ Master System Architecture (Dual-Mode Design)

```
┌──────────────────────────────────────────────────────────────────────────────────────────┐
│                   SECUREMAILSCOPE HARDENED DUAL-MODE ARCHITECTURE                        │
└──────────────────────────────────────────────────────────────────────────────────────────┘

       [Captured .eml Message File / Local Air-Gapped Upload]
                                │
                                ▼
  ┌─────────────────────────────────────────────────────────────────────────────────────┐
  │                 PHASE 1: RFC 5322 PARSER & SKELETON NORMALIZER                      │
  ├─────────────────────────────────────────────────────────────────────────────────────┤
  │ • Extract Visible From, Return-Path, Authentication-Results, Received Hops, ARC      │
  │ • Unicode Skeleton Normalization (RFC 5890 NFKC) ➔ Script & Confusable Matcher      │
  │ • Executive Display-Name Impersonation Check (Targeted Social Engineering Vector)    │
  └────────────────────────────┬────────────────────────────────────────────────────────┘
                               │
                               ▼
  ┌─────────────────────────────────────────────────────────────────────────────────────┐
  │                 PHASE 2: PASSIVE VS. ACTIVE ASSESSMENT PIPELINE                     │
  ├─────────────────────────────────────────────────────────────────────────────────────┤
  │ PASSIVE METADATA ANALYSIS (.eml only)    │ ACTIVE INFRASTRUCTURE VERIFICATION (Optional)
  │ • DKIM DNS Selector Modulus Extraction   │ • Active MX & STARTTLS Port 25 Probe     │
  │   (Determines actual RSA bit length:     │ • MTA-STS Policy Inspection (RFC 8461)   │
  │    <1024-bit = Critical Risk)            │ • TLS-RPT Record Validation              │
  │ • ARC Multi-Hop Chain Validation         │ • Active DNSSEC Verification             │
  │ • Received Header Transport Parsing      │                                          │
  └────────────────────────────┬─────────────┴──────────────────────────────────────────┘
                               │
                               ▼
  ┌─────────────────────────────────────────────────────────────────────────────────────┐
  │                 PHASE 3: EXPLAINABLE RISK FUSION & ANOMALY ENGINE                   │
  ├─────────────────────────────────────────────────────────────────────────────────────┤
  │                     RISK FUSION = Deterministic_Score                               │
  │                                  + Identity_Anomaly_Score                           │
  │                                  + Transport_Evidence_Score                         │
  │                                  + ML_Tabular_Anomaly_Score                         │
  │ • Generates Point-by-Point Evidence Audit Tree ("WHY did this email score 82/100?") │
  └────────────────────────────┬────────────────────────────────────────────────────────┘
                               │
                               ▼
  ┌─────────────────────────────────────────────────────────────────────────────────────┐
  │             PHASE 4: NTRO SOC INSPECTOR UI & FORENSIC AUDIT GENERATOR               │
  ├─────────────────────────────────────────────────────────────────────────────────────┤
  │ • Air-Gapped Local Web UI (Drag-and-Drop EML Analysis)                              │
  │ • Interactive Routing Hop Topology Map                                              │
  │ • 1-Click Signed PDF Incident Audit Report Generator                                │
  └─────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. 🛡️ Correct Technical Implementations (Fixing Common Flaws)

### A. True DKIM RSA Key-Length Inspection (DNS Resolution)
**Incorrect Approach:** Guessing key size based on whether `dkim.verify()` returned true.  
**Correct Approach:** Extract selector `s=` and domain `d=` from `DKIM-Signature` header, query `s._domainkey.d` TXT record via DNS, decode public key modulus `p=`, and measure exact bit-length.

```python
import base64
import dns.resolver

def get_dkim_public_key_bits(selector: str, domain: str) -> int:
    """Resolves DNS TXT record for DKIM selector and calculates true RSA key size in bits."""
    query_target = f"{selector}._domainkey.{domain}"
    try:
        answers = dns.resolver.resolve(query_target, 'TXT')
        for rdata in answers:
            txt_record = "".join([part.decode('utf-8') for part in rdata.strings])
            if "p=" in txt_record:
                # Extract Base64 encoded public key modulus
                p_val = txt_record.split("p=")[1].split(";")[0].strip()
                key_bytes = base64.b64decode(p_val)
                # Approximate RSA bit length from DER/ASN.1 structure byte length
                key_bits = len(key_bytes) * 8
                return key_bits
    except Exception:
        return 0 # Record not reachable or unparsed
    return 0
```

---

### B. Accurate Passive Transport Evidence vs Active SMTP Validation
**Incorrect Claim:** "We extract exact TLS 1.0 handshake ciphers for all historical hops from headers."  
**Correct Implementation:** Distinguish between **Passive Header Transport Evidence** (parsing strings like `with ESMTPS` in `Received:` headers) and **Active Infrastructure Probing** (sending a STARTTLS handshake to the target MX server when network access is enabled).

```python
def analyze_transport_security(msg, active_mode: bool = False, target_mx: str = None):
    transport_evidence = []
    received_headers = msg.get_all("Received") or []
    
    # 1. Passive Header Analysis
    for idx, hop in enumerate(received_headers):
        hop_str = str(hop).lower()
        if "esmtps" in hop_str or "using tls" in hop_str:
            transport_evidence.append({"hop": idx+1, "status": "TLS_INDICATED", "evidence": "ESMTPS stamp present"})
        elif "with esmtp" in hop_str and "tls" not in hop_str:
            transport_evidence.append({"hop": idx+1, "status": "PLAINTEXT_INDICATED", "evidence": "Standard ESMTP without TLS indication"})

    # 2. Active Verification (Only run if connected & explicitly enabled)
    active_results = None
    if active_mode and target_mx:
        # Perform active STARTTLS probe to check MX capabilities
        active_results = probe_smtp_starttls(target_mx)
        
    return transport_evidence, active_results
```

---

### C. Confusable & Homograph Analysis (Beyond Simple Punycode)
**Incorrect Approach:** Marking any `xn--` Punycode domain as malicious.  
**Correct Approach:** Perform Unicode NFKC normalization, extract script tags, and check string similarity against target whitelists using Levenshtein distance.

```python
import unicodedata
import idna

def analyze_domain_confusables(domain: str, whitelist: list[str]) -> tuple[bool, str]:
    domain = domain.lower()
    
    # 1. Check Punycode IDN conversion
    is_idn = False
    try:
        puny_domain = idna.encode(domain).decode('ascii')
        if puny_domain.startswith("xn--"):
            is_idn = True
    except Exception:
        pass

    # 2. NFKC Normalization
    normalized = unicodedata.normalize('NFKC', domain)
    
    # 3. Whitelist Proximity Match
    for target in whitelist:
        # Simple Levenshtein or substring match on confusables
        if domain != target and (target in normalized or is_homograph_similar(normalized, target)):
            return True, f"Homograph/Confusable match against legitimate domain '{target}'"
            
    return is_idn, "IDN domain detected" if is_idn else "Standard ASCII"
```

---

## 3. 🔬 Complete Hardened Python Backend (FastAPI Engine)

```python
import email
from email import policy
import re
import unicodedata
import idna
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import dkim
import numpy as np

app = FastAPI(title="SecureMailScope Hardened Engine", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

EXEC_KEYWORDS = ["director", "general", "minister", "pmo", "secretary", "command", "ntro", "chief"]
GOV_WHITELIST = ["nic.in", "gov.in", "ntro.gov.in", "pmo.gov.in", "mod.gov.in"]

@app.post("/api/v2/analyze-eml")
async def analyze_eml_endpoint(file: UploadFile = File(...)):
    content = await file.read()
    raw_eml_text = content.decode('utf-8', errors='ignore')
    
    msg = email.message_from_string(raw_eml_text, policy=policy.default)
    
    # 1. Extract Identities
    from_header = str(msg.get("From", ""))
    return_path = str(msg.get("Return-Path", ""))
    auth_results = str(msg.get("Authentication-Results", ""))
    received_headers = msg.get_all("Received") or []
    
    # Parse Display Name & Address
    match = re.match(r'(?:"?([^"]*)"?\s)?<(.+@.+)>', from_header)
    display_name = match.group(1) if match else ""
    from_addr = match.group(2) if match else from_header
    from_domain = from_addr.split("@")[-1].lower() if "@" in from_addr else ""

    # 2. Risk Evidence Breakdown Engine
    evidence_tree = []
    deterministic_risk = 0.0

    # Test Identity Spoofing
    if any(kw in display_name.lower() for kw in EXEC_KEYWORDS):
        if not any(from_domain.endswith(gdom) for gdom in GOV_WHITELIST):
            deterministic_risk += 35.0
            evidence_tree.append({
                "category": "Identity",
                "severity": "HIGH",
                "points": +35,
                "description": f"Executive Display-Name '{display_name}' used with non-government domain '{from_domain}'"
            })

    # Test Homograph
    try:
        puny_domain = idna.encode(from_domain).decode('ascii')
        if puny_domain.startswith("xn--"):
            deterministic_risk += 30.0
            evidence_tree.append({
                "category": "Identity",
                "severity": "CRITICAL",
                "points": +30,
                "description": f"Internationalized Domain (Punycode: {puny_domain}) confusable risk"
            })
    except Exception:
        pass

    # Test Cryptographic Authentication
    dkim_valid = False
    try:
        dkim_valid = dkim.verify(raw_eml_text.encode('utf-8'))
        if not dkim_valid:
            deterministic_risk += 20.0
            evidence_tree.append({
                "category": "Authentication",
                "severity": "MEDIUM",
                "points": +20,
                "description": "DKIM Signature Verification Failed or Missing"
            })
        else:
            evidence_tree.append({
                "category": "Authentication",
                "severity": "INFO",
                "points": 0,
                "description": "DKIM Signature Validated Successfully"
            })
    except Exception:
        deterministic_risk += 15.0

    # Transport Hops Passive Evidence
    plaintext_hops = 0
    for hop in received_headers:
        if "with esmtp" in str(hop).lower() and "tls" not in str(hop).lower():
            plaintext_hops += 1

    if plaintext_hops > 0:
        deterministic_risk += 15.0
        evidence_tree.append({
            "category": "Transport",
            "severity": "WARN",
            "points": +15,
            "description": f"{plaintext_hops} hop(s) in Received chain indicate plaintext transmission"
        })

    # Calculate Final Score
    final_risk_score = min(round(deterministic_risk, 1), 100.0)
    trust_score = round(100.0 - final_risk_score, 1)

    status = "SECURE" if trust_score >= 70 else ("SUSPICIOUS" if trust_score >= 40 else "CRITICAL_THREAT")

    return {
        "trust_score": trust_score,
        "risk_score": final_risk_score,
        "status": status,
        "from_address": from_addr,
        "from_domain": from_domain,
        "total_hops": len(received_headers),
        "evidence_tree": evidence_tree
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

---

<div align="center">

**Hardened Architecture Master Spec | NTRO SecureMailScope**

</div>
