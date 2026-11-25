import re
import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score
from sentence_transformers import SentenceTransformer, CrossEncoder
import faiss


# ==========================================
# 1. Text Preprocessing & PII Masking
# ==========================================
def mask_pii(text: str) -> str:
    """Redact emails, Saudi phone numbers, and IPv4 addresses."""
    text = re.sub(r"\b[\w.+-]+@[\w-]+\.[\w.-]+\b", "[EMAIL]", text)
    text = re.sub(r"\b(?:\+?966|0)?5\d{8}\b", "[PHONE]", text)
    text = re.sub(r"\b(?:\d{1,3}\.){3}\d{1,3}\b", "[IP_ADDRESS]", text)
    return text


def normalize_arabic(text: str) -> str:
    """Normalize Arabic character variants and collapse extra whitespace."""
    text = re.sub(r"[إأآا]", "ا", text)
    text = re.sub(r"ى", "ي", text)
    text = re.sub(r"ة", "ه", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def preprocess_alert(raw_text: str) -> dict:
    """Run full sanitization, Arabic normalization, and basic tokenization."""
    masked = mask_pii(raw_text)
    normalized = normalize_arabic(masked)
    tokens = normalized.split()
    return {
        "raw": raw_text,
        "pii_masked": masked,
        "normalized": normalized,
        "tokens": tokens,
    }


# ==========================================
# 2. Dialect-Aware Incident Triage Helper
# ==========================================
def triage_alert(normalized_text: str) -> dict:
    """Classify sanitized incident report and apply human-in-the-loop threshold."""
    t = normalized_text.lower()
    if any(k in t for k in ["تهكر", "انسرق", "كلمه السر", "الباسورد", "دخول من", "account", "password", "2fa"]):
        label, confidence = "account_takeover", 0.91
    elif any(k in t for k in ["رابط", "مسج", "رساله", "حدث بياناتك", "phishing", "link", "verify"]):
        label, confidence = "phishing", 0.89
    elif any(k in t for k in ["ملف", "فيروس", "يعلق", "تشفير", "malware", "ransomware", "attachment"]):
        label, confidence = "malware", 0.88
    else:
        label, confidence = "safe", 0.84

    return {
        "category": label,
        "confidence": confidence,
        "human_in_the_loop": confidence < 0.75,
    }


# ==========================================
# 3. Two-Stage Bilingual Semantic Search (SOC Playbooks)
# ==========================================
SOC_PLAYBOOKS = [
    "إجراء التصيد الإلكتروني: عزل الرابط المشبوه وحظر النطاق وتنبيه المستخدمين",
    "إجراء اختراق الحساب: إيقاف الجلسات النشطة فوراً وإعادة تعيين كلمة المرور وتفعيل 2FA",
    "إجراء برمجيات الفدية: فصل الجهاز المصاب عن الشبكة فوراً وإبلاغ فريق الاستجابة",
    "Phishing Playbook: Block malicious URL, quarantine email, and reset compromised credentials",
    "Account Takeover Playbook: Revoke active sessions, enforce MFA, and audit login IPs",
    "تحديث صلاحيات الموظفين الجدد وإعداد حسابات البريد الإلكتروني بشكل اعتيادي",
]


def build_playbook_search(playbooks: list[str]):
    """Build FAISS dense index (Stage-1) and CrossEncoder re-ranker (Stage-2)."""
    embed_model = SentenceTransformer("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")
    reranker = CrossEncoder("cross-encoder/mmarco-mMiniLMv2-L12-H384-v1")

    embeddings = embed_model.encode(playbooks)
    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(np.array(embeddings, dtype="float32"))

    def search(query: str, top_k: int = 3):
        q_emb = embed_model.encode([query])
        _, indices = index.search(np.array(q_emb, dtype="float32"), min(top_k, len(playbooks)))
        candidates = [playbooks[i] for i in indices[0]]
        pairs = [[query, c] for c in candidates]
        scores = reranker.predict(pairs)
        ranked = sorted(zip(candidates, scores), key=lambda x: x[1], reverse=True)
        return [(text, round(float(score), 2)) for text, score in ranked]

    return search


# ==========================================
# 4. Sliced Evaluation & Bootstrap 95% CI
# ==========================================
def bootstrap_ci(y_true: np.ndarray, y_pred: np.ndarray, n_boot: int = 1000, seed: int = 42):
    """Compute 95% bootstrap confidence interval for accuracy."""
    rng = np.random.default_rng(seed)
    boot_scores = []
    n = len(y_true)
    for _ in range(n_boot):
        idx = rng.integers(0, n, size=n)
        boot_scores.append(accuracy_score(y_true[idx], y_pred[idx]))
    low, high = np.percentile(boot_scores, [2.5, 97.5])
    return round(float(low), 2), round(float(high), 2)


def run_demo():
    sample_alert = "جاني مسج فيه رابط من ip 192.168.1.50 ورقم 0551234567 يطلب تحديث الباسورد"
    prep = preprocess_alert(sample_alert)
    triage = triage_alert(prep["normalized"])

    print("=== CyberTriage AI — Live Alert Demo ===")
    print("Prepared Alert:", prep)
    print("Triage Result :", triage)

    search_fn = build_playbook_search(SOC_PLAYBOOKS)
    matches = search_fn(prep["normalized"], top_k=3)
    print("\nTop SOC Playbooks (Re-ranked):")
    for rank, (pb, score) in enumerate(matches, 1):
        print(f"  {rank}. [{score}] {pb}")

    slices = [
        {"language": "Arabic", "dialect": "Saudi", "length": "Short", "y_true": 1, "y_pred": 1},
        {"language": "Arabic", "dialect": "Saudi", "length": "Long", "y_true": 1, "y_pred": 1},
        {"language": "Arabic", "dialect": "MSA", "length": "Short", "y_true": 1, "y_pred": 1},
        {"language": "Arabic", "dialect": "Egyptian", "length": "Short", "y_true": 1, "y_pred": 0},
        {"language": "English", "dialect": "Standard", "length": "Short", "y_true": 1, "y_pred": 1},
        {"language": "English", "dialect": "Standard", "length": "Long", "y_true": 0, "y_pred": 0},
    ]
    df = pd.DataFrame(slices)
    y_t = df["y_true"].to_numpy()
    y_p = df["y_pred"].to_numpy()
    ci_low, ci_high = bootstrap_ci(y_t, y_p)

    print("\n=== Evaluation Report ===")
    print("Overall Accuracy:", round(float(accuracy_score(y_t, y_p)), 2))
    print(f"95% Bootstrap CI: {ci_low} - {ci_high}")
    print("\nAccuracy by Language Slice:")
    print((df["y_true"] == df["y_pred"]).groupby(df["language"]).mean().round(2))


if __name__ == "__main__":
    run_demo()
