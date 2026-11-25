# CyberTriage AI — Review & Challenge Q&A Documentation

**Project:** CyberTriage AI (Bilingual Cybersecurity Incident Triage & SOC Response Radar)  
**Presenter / Student:** Faisal Al-Khater  
**Instructor:** Ms. Latifa Abdulmohsen  
**Live Demo:** [CyberTriage AI Interactive App](https://bilingual-incident-compass.lovable.app)

---

## Team Roles & Governance

| Role | Name | Responsibility |
| :--- | :--- | :--- |
| **Project Lead & Reviewer** | **كلنا قادة (All Team Leaders)** | Moderates the session, questions team members, poses the challenge question, and issues the final decision |
| **NLP Engineer** | **Azzam Abdullah** | Answers questions on data preprocessing, tokenization, Transformer selection, fine-tuning, and end-to-end workflow |
| **Quality & Evaluation Lead** | **Nasser Al-Otaibi** | Answers questions on evaluation metrics, data leakage prevention, dialect reliability, and error analysis |
| **Innovation & Presentation Lead** | **Bassam Al-Mutairi** | Presents the project overview, problem statement, competitive advantages, and real-world deployment |

---

## 1. Project Lead Questions to Innovation & Presentation Lead (Bassam Al-Mutairi)

* **Q1: What is the project name and core idea?**  
  **A:** **CyberTriage AI** is a bilingual (Arabic—MSA and Saudi dialect—and English) NLP system that sanitizes incoming cybersecurity alerts (`PII Masking`), classifies incident types (`phishing`, `malware`, `account_takeover`, `safe`), extracts key security entities (`NER`), and retrieves matching `SOC Playbooks` via semantic search.

* **Q2: What problem does it solve, and who is the target user?**  
  **A:** Security Operations Centers (`SOC`) and IT support teams receive high volumes of unstructured alerts written in mixed Arabic, Saudi dialect, and English, often containing exposed sensitive user data. Manual triage is slow and error-prone; CyberTriage AI accelerates first-line triage for SOC analysts and incident responders.

* **Q3: What differentiates CyberTriage AI from traditional triage solutions?**  
  **A:**
  1. **Dialect & Bilingual Understanding:** Uses Arabic-specialized Transformers (`CAMeLBERT-mix` and `CAMeLBERT-DA`) rather than rigid English-only keyword rules.
  2. **Built-in Privacy Protection (`PII Masking`):** Automatically redacts emails, Saudi phone numbers, and IP addresses before downstream processing.
  3. **Semantic Playbook Retrieval:** Combines `FAISS` dense retrieval with `CrossEncoder` re-ranking to recommend actionable response steps across language shifts.
  4. **Transparent Evaluation:** Relies on sliced evaluation, `95%` bootstrap confidence intervals, and confidence thresholds for human-in-the-loop escalation.

---

## 2. Project Lead Questions to NLP Engineer (Azzam Abdullah)

* **Q1: How did you prepare text using Preprocessing and Tokenization?**  
  **A:** We normalize whitespace, redact sensitive PII (`[EMAIL]`, `[PHONE]`, `[IP_ADDRESS]`), and normalize Arabic character variants (`إ/أ/آ -> ا`, `ى -> ي`, `ة -> ه`). Then we apply the model's subword `Tokenizer` with token-to-word alignment (`word_ids` / clitic awareness) to preserve word boundaries and handle Arabic prefixes/suffixes cleanly.

* **Q2: Which Transformer models did you use and why?**  
  **A:** We use **CAMeLBERT** (`camelbert-mix` and `camelbert-da`) for Arabic and dialectal classification/NER because of its strong morphological and contextual representation of Arabic, alongside multilingual `SentenceTransformer` (`paraphrase-multilingual-MiniLM-L12-v2`) and `CrossEncoder` (`mmarco-mMiniLMv2-L12-H384-v1`) for cross-lingual playbook retrieval.

* **Q3: How did you use Fine-tuning to improve performance?**  
  **A:** We fine-tuned the pre-trained Transformer weights on labeled cybersecurity incident reports (`phishing`, `malware`, `account_takeover`, `safe`), adapting general language representations to domain-specific threat terminology and SOC context.

* **Q4: How did you handle Arabic, English, and regional dialects?**  
  **A:** We built a unified bilingual pipeline supporting both Arabic and English inputs, applied Arabic orthographic normalization and clitic-aware tokenization, included Saudi dialect, MSA, and English samples in training/evaluation, and leveraged `CAMeLBERT-DA` for dialect-heavy inputs.

* **Q5: How does the project work step-by-step (Workflow)?**  
  **A:**
  1. **Ingest & Sanitize:** Clean text and mask PII (`[EMAIL]`, `[PHONE]`, `[IP_ADDRESS]`).
  2. **Tokenize & Classify:** Run subword tokenization and fine-tuned Transformer inference to predict category and confidence score.
  3. **Extract Entities (`NER`):** Identify threats, assets, indicators, and locations.
  4. **Retrieve Playbooks:** Query `FAISS` (`Stage-1`) and re-rank top candidates with `CrossEncoder` (`Stage-2`) to present actionable SOC steps.

---

## 3. Project Lead Questions to Quality & Evaluation Lead (Nasser Al-Otaibi)

* **Q1: How did you measure model performance?**  
  **A:** We evaluate classification using `Macro-F1`, `Precision`, `Recall`, and `Accuracy` with `95%` bootstrap confidence intervals (`1,000` resamples), and evaluate playbook retrieval using `Recall@10` and `MRR@10`.

* **Q2: How did you prevent Data Leakage?**  
  **A:** All preprocessing parameters, label encoders, and `FAISS` indexes are fitted strictly on the training split, and grouped/stratified splitting (`GroupShuffleSplit`) ensures near-duplicate or template-based alerts never appear across both training and test sets.

* **Q3: How did you verify result quality across languages and dialects?**  
  **A:** Through **Sliced Evaluation**, breaking down metrics separately across `Language` (Arabic vs. English), `Dialect` (Saudi, MSA, Other), and `Alert Length` (Short vs. Long) rather than relying on a single aggregate score.

* **Q4: How did you analyze errors and ensure real-world readiness?**  
  **A:** We built a structured **Error Taxonomy** categorizing misclassifications (such as `Class Overlap: Phishing vs. Account Takeover`, `Dialect Shift`, and `Out-of-Scope Queries`) and implemented a confidence threshold (`< 0.75`) that routes uncertain alerts to human SOC analysts (`Human-in-the-Loop`).

---

## 4. Cross-Team Peer Questions

* **NLP Engineer → Quality & Evaluation Lead:**
  * *How do we know the model is learning properly?*  
    By monitoring steady convergence of both `Training Loss` and `Validation Loss` across epochs while checking validation `Macro-F1` to ensure no overfitting occurs.
  * *How do we compare performance before and after Fine-tuning?*  
    By benchmarking the base pre-trained checkpoint against the fine-tuned model on the exact same held-out test split using identical metrics (`Macro-F1`, `Precision`, `Recall`).
  * *If a model achieves 90% Accuracy, does that automatically mean it is excellent?*  
    No—in imbalanced security datasets, a model can reach 90% accuracy by over-predicting `safe` alerts while missing critical `account_takeover` or `malware` incidents. Per-class `Recall`, `Macro-F1`, and slice-level metrics are essential.

* **NLP Engineer → Innovation & Presentation Lead:**
  * *How can an NLP model be turned into a practical service for end users?*  
    By wrapping the inference pipeline behind a fast REST API (e.g., FastAPI) connected to an interactive SOC dashboard or ticketing system, complete with PII redaction, confidence thresholds, and analyst feedback logging.

* **Quality & Evaluation Lead → NLP Engineer:**
  * *Which metrics fit our project best?*  
    `Macro-F1` to balance all four incident classes equally, high `Recall` to avoid missing real attacks, `Precision` to minimize alert fatigue, and `Recall@10` / `MRR@10` for playbook retrieval.
  * *How does Semantic Search work in the project?*  
    Alerts and SOC playbooks are encoded into dense multilingual vectors indexed in `FAISS` for fast Stage-1 candidate retrieval, then scored as `(query, playbook)` pairs by a `CrossEncoder` in Stage-2 for high-precision re-ranking.
  * *How do we optimize inference speed without sacrificing quality?*  
    By capping sequence length (`max_length`) at the empirical `p95` token length, running `CrossEncoder` re-ranking only on top-`k` `FAISS` candidates, using quantized weights, and caching frequent queries.

* **Quality & Evaluation Lead → Innovation & Presentation Lead:**
  * *How can the project be expanded in the future?*  
    Direct integration with `SIEM/SOAR` platforms and email gateways, expanded technical IOC entity extraction (domains, hashes, CVEs), and continuous active learning from analyst corrections.

* **Innovation & Presentation Lead → NLP Engineer:**
  * *What is the most critical technology that makes our project viable in production?*  
    Combining domain-adapted Arabic Transformers (`CAMeLBERT`) with automated `PII Masking` and two-stage semantic retrieval (`FAISS` + `CrossEncoder`), delivering privacy compliance, dialect comprehension, and actionable response guidance in a lightweight pipeline.

---

## 5. Challenge Question & Team Response

> **Challenge Scenario:** If deployed in a real organization and the model performs well on Modern Standard Arabic (MSA) but struggles with Saudi dialect alerts, how will you detect, resolve, and verify the fix?

1. **Detection:** Isolate the performance drop using **Sliced Evaluation** (`Dialect = Saudi` vs. `MSA`) and inspect misclassified Saudi alerts via **Error Analysis** to identify dialectal vocabulary, phrasing, and clitic patterns causing errors.
2. **Resolution:** Refine Arabic text normalization and subword handling, augment the training set with authentic Saudi-dialect security reports across all categories, and fine-tune a dialect-capable checkpoint such as **`CAMeLBERT-DA`**.
3. **Verification:** Re-evaluate on a leakage-free Saudi-dialect test set (`GroupShuffleSplit`), verifying statistically meaningful gains in `Macro-F1`, `Recall`, and `95%` bootstrap confidence intervals before redeployment.

---

## 6. Project Lead Final Decision

* **Strongest Project Highlight:** Seamless integration of privacy-preserving `PII Masking`, bilingual/dialect-aware Transformer triage, and two-stage semantic `SOC Playbook` retrieval backed by slice-level evaluation.
* **Final Reviewer Verdict:** **Successful ✔**
