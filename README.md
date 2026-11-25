# CYBERTRIAGE-AI
Bilingual (Arabic—MSA &amp; Saudi dialect—and English) NLP system for PII masking, security alert triage, NER, and semantic SOC playbook retrieval by Faisal Al-Khater under the supervision of Ms. Latifa Abdulmohsen.
# CyberTriage AI — Bilingual Cybersecurity Incident Triage & SOC Response Radar

**CyberTriage AI** is a bilingual (Arabic—Modern Standard & Saudi dialect—and English) Natural Language Processing system designed to sanitize cybersecurity incident reports, mask sensitive Personally Identifiable Information (`PII Masking`), classify alert severity/type (`phishing`, `malware`, `account_takeover`, `safe`), extract security entities (`NER`), and retrieve relevant `SOC Playbooks` via semantic search and re-ranking.

## Project & Team Details
* **Presenter / Student:** Faisal Al-Khater
* **Instructor:** Ms. Latifa Abdulmohsen
* **Challenge Team Roles:**
  * **Project Lead & Reviewer:** All Team Leaders ("كلنا قادة")
  * **NLP Engineer:** Azzam Abdullah
  * **Quality & Evaluation Lead:** Nasser Al-Otaibi
  * **Innovation & Presentation Lead:** Bassam Al-Mutairi

## End-to-End Pipeline
1. **Preprocessing & PII Masking:** Whitespace normalization, Arabic character normalization, and masking sensitive fields (`[EMAIL]`, `[PHONE]`, `[IP_ADDRESS]`).
2. **Tokenization & Transformer Classification:** Fine-tuning Arabic-capable Transformer models such as **CAMeLBERT** (`camelbert-mix` and `camelbert-da`) for alert classification, confidence scoring, and entity extraction.
3. **Semantic Search & Re-ranking:** Indexing `SOC Playbooks` with `FAISS` using multilingual sentence embeddings (`paraphrase-multilingual-MiniLM-L12-v2`) for Stage-1 retrieval, followed by `CrossEncoder` (`mmarco-mMiniLMv2-L12-H384-v1`) for Stage-2 re-ranking.
4. **Evaluation & Error Analysis:** Sliced evaluation across language, dialect, and text length, 95% Bootstrap confidence intervals (`95% CI`), and structured error taxonomy analysis.

## Quick Start
```bash
pip install -r requirements.txt
python src/cybertriage_pipeline.py
