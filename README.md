# CyberTriage AI — Bilingual Cybersecurity Incident Triage & SOC Response Radar

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![NLP](https://img.shields.io/badge/NLP-Transformers%20%7C%20CAMeLBERT-0EA5E9?style=for-the-badge)](#architecture--pipeline)
[![Search](https://img.shields.io/badge/Semantic%20Search-FAISS%20%7C%20CrossEncoder-10B981?style=for-the-badge)](#architecture--pipeline)
[![Evaluation](https://img.shields.io/badge/Evaluation-Sliced%20%7C%2095%25%20Bootstrap%20CI-F59E0B?style=for-the-badge)](#evaluation--error-analysis)

> **Bilingual (Arabic — MSA & Saudi Dialect — and English) NLP pipeline** for privacy-preserving incident sanitization (`PII Masking`), alert triage (`phishing`, `malware`, `account_takeover`, `safe`), entity extraction (`NER`), and semantic `SOC Playbook` retrieval.

---

## Project Governance & Team

| Role | Name | Focus Area |
| :--- | :--- | :--- |
| **Presenter / Student** | **Faisal Al-Khater** | End-to-end project showcase & integration |
| **Instructor** | **Ms. Latifa Abdulmohsen** | Course supervision & technical review |
| **Project Lead & Reviewer** | **Faisal al khater** | Discussion moderation, challenge question & final decision |
| **NLP Engineer** | **Azzam Abdullah** | Preprocessing, tokenization, CAMeLBERT fine-tuning & workflow |
| **Quality & Evaluation Lead** | **Nasser Al-Otaibi** | Metrics, data leakage prevention, sliced eval & error analysis |
| **Innovation & Presentation Lead** | **Bassam Al-Mutairi** | Pitch deck, product differentiation & real-world adoption |

---

## Architecture & Pipeline

```text
+-----------------------------------------------------------------------+
|                        Incoming Security Alert                        |
|               (Arabic [MSA / Saudi Dialect] & English)                |
+-----------------------------------+-----------------------------------+
                                    |
                                    v
+-----------------------------------------------------------------------+
| 1. Preprocessing & PII Masking                                        |
|    • Whitespace & Arabic character normalization                      |
|    • Masking [EMAIL], [PHONE], [IP_ADDRESS] before downstream models  |
+-----------------------------------+-----------------------------------+
                                    |
                                    v
+-----------------------------------------------------------------------+
| 2. Tokenization & Transformer Triage                                  |
|    • Subword tokenization & clitic/word-id alignment                  |
|    • Fine-tuned CAMeLBERT (mix / DA) -> Category, Confidence & NER    |
|    • Confidence threshold check -> Auto-triage or Human-in-the-Loop   |
+-----------------------------------+-----------------------------------+
                                    |
                                    v
+-----------------------------------------------------------------------+
| 3. Two-Stage Bilingual Semantic Search                                |
|    • Stage-1: Multilingual embeddings + FAISS index (fast recall)     |
|    • Stage-2: Cross-Encoder re-ranking -> Top SOC Playbooks           |
+-----------------------------------+-----------------------------------+
                                    |
                                    v
+-----------------------------------------------------------------------+
| 4. Evaluation & Error Taxonomy                                        |
|    • Sliced evaluation (Language, Dialect, Length)                    |
|    • 1,000-iteration Bootstrap 95% CI                                 |
|    • Root-cause taxonomy (Class Overlap, Dialect Shift, Out-of-Scope) |
+-----------------------------------------------------------------------+
## Live Demo
* **Interactive Web App:** [CyberTriage AI Demo](https://bilingual-incident-compass.lovable.app)
@SDAIAAcademy
