import html
import re
from typing import Dict, List

import streamlit as st

st.set_page_config(page_title="ScamEmotion", page_icon="🛡️", layout="wide")

st.markdown(
    """
<style>
:root {
    --bg: #F8F7F4;
    --card: #FFFFFF;
    --ink: #111827;
    --muted: #4B5563;
    --line: #E5E7EB;
    --red: #B91C1C;
    --red-dark: #7F1D1D;
    --red-soft: #FEE2E2;
    --yellow: #CA8A04;
    --yellow-soft: #FEF3C7;
    --green: #15803D;
    --green-soft: #DCFCE7;
    --blue-soft: #EFF6FF;
    --blue-line: #BFDBFE;
    --blue-text: #1D4ED8;
}
html, body, [class*="css"] { font-family: "Inter", sans-serif; }
.stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
    background-color: var(--bg) !important;
    background-image: none !important;
}
.block-container {
    max-width: 1080px;
    padding-top: 1.2rem;
    padding-bottom: 3rem;
    position: relative;
    z-index: 1;
}
h1, h2, h3, h4, p, label, div, span { color: var(--ink); }
.hero-card, .panel-card {
    background: transparent;
    border: none;
    border-top: 1px solid var(--line);
    border-radius: 0;
    padding: 1.25rem 0 1.1rem 0;
    box-shadow: none;
}
.hero-card { border-top: 3px solid var(--red); margin-bottom: 1.1rem; }
.title-main {
    font-size: 2.9rem;
    font-weight: 850;
    margin: 0 0 0.65rem 0;
    line-height: 1.08;
    color: var(--ink);
}
.subtitle-main {
    font-size: 1.12rem;
    line-height: 1.65;
    color: var(--muted);
    margin: 0;
}
.helper-text { color: var(--muted); font-size: 1rem; margin-top: -0.3rem; margin-bottom: 0.8rem; }
.result-card {
    background: #FFFFFF;
    border: 1px solid #EEF0F3;
    border-radius: 14px;
    padding: 1rem;
    height: 100%;
    box-shadow: none;
}
.module-card {
    background: #FFFFFF;
    border: 1px solid #EEF0F3;
    border-radius: 16px;
    padding: 1.05rem;
    height: 100%;
}
.module-title { font-size: 1.05rem; font-weight: 850; margin-bottom: 0.2rem; }
.module-caption { font-size: 0.9rem; color: var(--muted); line-height: 1.45; margin-bottom: 0.8rem; }
.result-label { font-size: 0.9rem; color: var(--muted); font-weight: 750; margin-bottom: 0.35rem; }
.result-value { font-size: 1.95rem; font-weight: 850; color: var(--ink); line-height: 1.15; }
.result-note { font-size: 0.92rem; color: var(--muted); margin-top: 0.45rem; line-height: 1.45; }
.badge {
    display: inline-block;
    padding: 0.38rem 0.78rem;
    border-radius: 999px;
    font-size: 0.92rem;
    font-weight: 750;
    border: 1px solid transparent;
    margin-top: 0.35rem;
}
.badge-low { background: var(--green-soft); color: var(--green); border-color: #BBF7D0; }
.badge-medium { background: var(--yellow-soft); color: var(--yellow); border-color: #FDE68A; }
.badge-high { background: var(--red-soft); color: var(--red); border-color: #FECACA; }
.badge-vhigh { background: #FDE8E8; color: var(--red-dark); border-color: #FCA5A5; }
.tag-wrap { display: flex; flex-wrap: wrap; gap: 10px; margin-top: 0.55rem; }
.tag {
    display: inline-block;
    padding: 0.5rem 0.8rem;
    border-radius: 12px;
    font-size: 0.95rem;
    font-weight: 650;
    border: 1px solid var(--line);
    color: var(--ink);
}
.tag-red { background: var(--red-soft); border-color: #FECACA; }
.tag-yellow { background: var(--yellow-soft); border-color: #FDE68A; }
.tag-green { background: var(--green-soft); border-color: #BBF7D0; }
.tag-blue { background: var(--blue-soft); border-color: var(--blue-line); color: var(--blue-text); }
.tag-neutral { background: #F3F4F6; border-color: #E5E7EB; }
.stTextArea textarea {
    background: #FFFFFF !important;
    color: var(--ink) !important;
    border: 1px solid #E5E7EB !important;
    border-radius: 12px !important;
    min-height: 180px !important;
    font-size: 1rem !important;
}
.stTextArea textarea::placeholder { color: #9CA3AF !important; }
.stTextArea textarea:focus {
    border: 1px solid var(--red) !important;
    box-shadow: 0 0 0 1px rgba(185, 28, 28, 0.08) !important;
    outline: none !important;
}
.stButton > button {
    background: var(--red) !important;
    color: white !important;
    border: none !important;
    border-radius: 14px !important;
    padding: 0.7rem 1.3rem !important;
    font-weight: 750 !important;
    font-size: 1rem !important;
}
.stButton > button:hover { background: #991B1B !important; color: white !important; }
.stButton > button * { color: #FFFFFF !important; }
.subtle-note {
    background: #FFFFFF;
    border: 1px solid #E5E7EB;
    border-radius: 14px;
    padding: 1rem 1.1rem;
    color: var(--muted);
    line-height: 1.6;
    box-shadow: none;
}
.meter-wrap { margin-top: 0.2rem; }
.meter-score {
    font-size: 1.85rem;
    font-weight: 850;
    color: var(--ink);
    line-height: 1.1;
    margin-bottom: 0.55rem;
}
.meter-zones {
    position: relative;
    width: 100%;
    height: 10px;
    border-radius: 999px;
    background: linear-gradient(90deg,
        #15803D 0%, #15803D 24%,
        #CA8A04 24%, #CA8A04 49%,
        #DC2626 49%, #DC2626 74%,
        #7F1D1D 74%, #7F1D1D 100%);
    opacity: 0.92;
}
.meter-pointer {
    position: absolute;
    top: -5px;
    width: 7px;
    height: 20px;
    border-radius: 999px;
    background: #111827;
    box-shadow: 0 0 0 2px #FFFFFF;
    transform: translateX(-50%);
}
.meter-scale {
    display: flex;
    justify-content: space-between;
    color: var(--muted);
    font-size: 0.72rem;
    margin-top: 0.35rem;
}
.pathway {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    gap: 8px;
    margin-top: 0.7rem;
}
.move-step {
    background: #FFFFFF;
    border: 1px solid #FECACA;
    color: var(--red-dark);
    border-radius: 14px;
    padding: 0.55rem 0.75rem;
    font-size: 0.92rem;
    font-weight: 750;
}
.move-arrow {
    color: var(--muted);
    font-weight: 900;
}
.move-box {
    border-left: 4px solid var(--red);
    background: #FFFFFF;
    border-radius: 12px;
    padding: 0.85rem 0.95rem;
    margin: 0.65rem 0;
    border-top: 1px solid #EEF0F3;
    border-right: 1px solid #EEF0F3;
    border-bottom: 1px solid #EEF0F3;
}
.move-name { font-weight: 850; margin-bottom: 0.25rem; }
.move-function { color: var(--muted); font-size: 0.93rem; line-height: 1.45; }
.small-muted { color: var(--muted); font-size: 0.9rem; line-height: 1.45; }
.evidence-text {
    background: #FFFFFF;
    border: 1px solid #EEF0F3;
    border-radius: 14px;
    padding: 1rem;
    line-height: 1.6;
}

/* Kotak muat naik gambar: putih dengan outline hitam */
[data-testid="stFileUploader"] {
    margin-top: 0.25rem !important;
    margin-bottom: 1rem !important;
}
[data-testid="stFileUploader"] section,
[data-testid="stFileUploaderDropzone"] {
    background: #FFFFFF !important;
    background-color: #FFFFFF !important;
    border: 1.5px solid #111827 !important;
    border-radius: 12px !important;
    padding: 1rem !important;
    box-shadow: none !important;
}
[data-testid="stFileUploaderDropzone"] > div,
[data-testid="stFileUploaderDropzone"] small,
[data-testid="stFileUploaderDropzone"] span,
[data-testid="stFileUploaderDropzone"] p {
    background: transparent !important;
    color: #111827 !important;
}
[data-testid="stFileUploaderDropzone"] button {
    min-width: 245px !important;
    height: 46px !important;
    background: #FFFFFF !important;
    background-color: #FFFFFF !important;
    border: 1px solid #111827 !important;
    border-radius: 10px !important;
    color: transparent !important;
    font-size: 0 !important;
    box-shadow: none !important;
    position: relative !important;
}
[data-testid="stFileUploaderDropzone"] button * {
    display: none !important;
}
[data-testid="stFileUploaderDropzone"] button::after {
    content: "Muat naik gambar di sini";
    color: #111827 !important;
    position: absolute;
    inset: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 400;
    font-size: 0.95rem;
}

</style>
""",
    unsafe_allow_html=True,
)

# -----------------------------------------------------------------------------
# Dataset prototaip ScamEmotion:
# Fokus analisis pada pencetus emosi dan manipulasi emosi dalam mesej digital.
# -----------------------------------------------------------------------------

EMOTION_PATTERNS: Dict[str, Dict[str, object]] = {
    "Ketakutan": {
        "weight": 22,
        "description": "Membangkitkan rasa takut terhadap kehilangan akses, tindakan undang-undang atau ancaman keselamatan.",
        "patterns": [
            r"akaun.*dibekukan", r"akaun.*disekat", r"akaun.*ditutup", r"disenarai hitam",
            r"aktiviti luar biasa", r"tindakan undang-undang", r"polis", r"pihak berkuasa",
            r"kehilangan akses", r"keselamatan akaun",
        ],
    },
    "Kecemasan": {
        "weight": 20,
        "description": "Mendesak pengguna bertindak segera tanpa semakan lanjut.",
        "patterns": [
            r"segera", r"sekarang", r"serta-merta", r"24 jam", r"15 minit", r"30 minit",
            r"hari ini", r"sebelum jam", r"malam ini", r"akhir hari ini",
        ],
    },
    "Harapan ganjaran": {
        "weight": 20,
        "description": "Membangkitkan harapan melalui janji keuntungan, bonus, hadiah atau wang yang akan dilepaskan.",
        "patterns": [
            r"untung", r"keuntungan", r"ganjaran", r"bonus", r"pulangan", r"diluluskan",
            r"hadiah", r"wang.*dilepaskan", r"modal.*jadi", r"pendapatan harian",
        ],
    },
    "Kepercayaan palsu": {
        "weight": 18,
        "description": "Membina rasa percaya melalui penyamaran autoriti, imej rasmi atau hubungan palsu.",
        "patterns": [
            r"bank", r"pegawai", r"wakil", r"rasmi", r"syarikat berdaftar", r"lesen",
            r"invois", r"suruhanjaya", r"testimoni", r"ramai pelanggan",
        ],
    },
    "Simpati": {
        "weight": 16,
        "description": "Mengeksploitasi rasa kasihan, bantuan kecemasan atau kesusahan orang lain.",
        "patterns": [
            r"bantu", r"sumbangan", r"anak sakit", r"kesusahan", r"derma",
            r"kecemasan keluarga", r"tolong", r"memerlukan bantuan",
        ],
    },
    "Rasa bersalah": {
        "weight": 16,
        "description": "Membuat pengguna berasa bersalah, bertanggungjawab atau terpaksa memenuhi permintaan.",
        "patterns": [
            r"jika anda tidak", r"anda punca", r"tolong saya", r"jangan kecewakan",
            r"harap kerjasama", r"tanggungjawab anda", r"demi keselamatan",
        ],
    },
}

CONTROL_PATTERNS: Dict[str, str] = {
    r"jangan kongsi otp|tidak berkongsi otp|jangan berkongsi otp": "Peringatan keselamatan OTP",
    r"jangan kongsi kata laluan|jangan berkongsi kata laluan|jangan kongsi pin": "Peringatan keselamatan kata laluan/PIN",
    r"saluran rasmi|laman rasmi|portal rasmi|aplikasi rasmi|kaunter rasmi": "Semakan melalui saluran rasmi",
    r"terma dan syarat|invois rasmi|resit rasmi|emel rasmi": "Bukti transaksi sah",
    r"semak dahulu|membuat semakan|semakan melalui": "Semakan rasmi",
}


def risk_level(score: int) -> str:
    if score <= 24:
        return "Rendah"
    if score <= 49:
        return "Sederhana"
    if score <= 74:
        return "Tinggi"
    return "Sangat Tinggi"


def badge_class(level: str) -> str:
    return {
        "Rendah": "badge-low",
        "Sederhana": "badge-medium",
        "Tinggi": "badge-high",
        "Sangat Tinggi": "badge-vhigh",
    }.get(level, "badge-medium")


def risk_meter(score: int) -> str:
    score = max(0, min(100, int(score)))
    return f"""
    <div class="meter-wrap">
        <div class="meter-score">{score}/100</div>
        <div class="meter-zones"><span class="meter-pointer" style="left:{score}%;"></span></div>
        <div class="meter-scale"><span>0</span><span>25</span><span>50</span><span>75</span><span>100</span></div>
    </div>
    """


def unique(items: List[str]) -> List[str]:
    return list(dict.fromkeys(items))


def tag_html(items: List[str], cls: str) -> str:
    safe_items = [html.escape(x) for x in (items or ["Tiada petanda yang ketara"])]
    return '<div class="tag-wrap">' + ''.join([f'<span class="tag {cls}">{t}</span>' for t in safe_items]) + '</div>'


def find_control_matches(text: str):
    labels, score = [], 0
    for pattern, label in CONTROL_PATTERNS.items():
        if re.search(pattern, text, flags=re.I):
            labels.append(label)
            score += 8
    return score, unique(labels)


def analyse_emotions(message: str):
    text = message.strip().lower()
    detected = []
    total_score = 0

    for emotion, info in EMOTION_PATTERNS.items():
        matched = [p for p in info["patterns"] if re.search(p, text, flags=re.I)]
        if matched:
            detected.append({
                "name": emotion,
                "score": int(info["weight"]),
                "description": str(info["description"]),
            })
            total_score += int(info["weight"])

    emotion_names = [item["name"] for item in detected]
    control_score, control_labels = find_control_matches(text)

    # Kenaikan risiko apabila beberapa emosi digunakan serentak.
    if "Ketakutan" in emotion_names and "Kecemasan" in emotion_names:
        total_score += 14
    if "Harapan ganjaran" in emotion_names and "Kepercayaan palsu" in emotion_names:
        total_score += 10
    if len(detected) >= 4:
        total_score += 12

    total_score = max(0, min(100, total_score - control_score))

    if detected:
        dominant = max(detected, key=lambda item: item["score"])
        dominant_emotion = dominant["name"]
        dominant_description = dominant["description"]
    else:
        dominant_emotion = "Tiada pencetus emosi dominan"
        dominant_description = "Sistem tidak mengesan manipulasi emosi yang ketara dalam mesej."

    return {
        "overall_score": total_score,
        "overall_level": risk_level(total_score),
        "emotions": emotion_names,
        "dominant_emotion": dominant_emotion,
        "dominant_description": dominant_description,
        "control_phrases": control_labels,
        "threat_category": classify_threat(text, emotion_names, total_score),
    }


def classify_threat(text: str, emotions: List[str], score: int) -> str:
    if re.search(r"otp|kata laluan|password|pin|akaun.*dibekukan|akaun.*disekat", text, flags=re.I):
        return "Eksploitasi ketakutan / pengambilalihan akaun"
    if re.search(r"pelaburan|pulangan|untung|modal.*jadi|keuntungan|bonus", text, flags=re.I):
        return "Eksploitasi harapan keuntungan"
    if re.search(r"pinjaman|bantuan|dana|diluluskan|caj proses|caj pengesahan", text, flags=re.I):
        return "Eksploitasi harapan bantuan atau pinjaman"
    if re.search(r"derma|sumbangan|anak sakit|kesusahan|tolong", text, flags=re.I):
        return "Eksploitasi simpati"
    if score >= 60:
        return "Mesej berisiko tinggi dengan manipulasi emosi"
    return "Tiada kategori ancaman yang jelas"


def control_message(category: str) -> str:
    if "ketakutan" in category.lower() or "akaun" in category.lower():
        return "Amaran keselamatan yang sah lazimnya mengingatkan pengguna supaya tidak berkongsi OTP, kata laluan atau PIN dengan sesiapa."
    if "keuntungan" in category.lower():
        return "Mesej pelaburan yang sah biasanya menyatakan risiko, dokumen rasmi dan saluran semakan tanpa menjanjikan keuntungan segera."
    if "pinjaman" in category.lower() or "bantuan" in category.lower():
        return "Mesej bantuan atau pinjaman yang sah tidak mendesak bayaran caj proses sebelum wang dilepaskan dan biasanya merujuk portal rasmi."
    if "simpati" in category.lower():
        return "Kempen bantuan yang sah biasanya menyatakan penganjur, saluran rasmi, rekod transaksi dan kaedah semakan yang jelas."
    return "Mesej yang sah biasanya memberi ruang semakan, menyatakan saluran rasmi dan tidak memaksa tindakan segera."


st.markdown(
    """
<div class="hero-card">
  <div class="title-main">ScamEmotion</div>
  <p class="subtitle-main">ScamEmotion ialah aplikasi amaran awal penipuan siber berasaskan Kecerdasan Buatan (AI) yang menganalisis pencetus emosi dan manipulasi emosi dalam mesej digital, termasuk ketakutan, kecemasan, harapan ganjaran, kepercayaan palsu, simpati dan rasa bersalah.</p>
</div>
""",
    unsafe_allow_html=True,
)

st.markdown('<div class="panel-card">', unsafe_allow_html=True)
st.markdown("## Semak Mesej Mencurigakan")
st.markdown('<p class="helper-text">Masukkan mesej di bawah:</p>', unsafe_allow_html=True)
message = st.text_area("Mesej", label_visibility="collapsed", placeholder="Masukkan mesej di sini", key="message_input")
st.markdown('<p class="helper-text">atau muat naik gambar di bawah:</p>', unsafe_allow_html=True)
uploaded_image = st.file_uploader("Muat naik gambar di sini", type=["png", "jpg", "jpeg"], label_visibility="collapsed")
if uploaded_image is not None:
    st.image(uploaded_image, caption="Tangkapan layar yang dimuat naik", use_container_width=True)
check = st.button("Semak Mesej")
st.markdown('</div>', unsafe_allow_html=True)

if check and message.strip():
    result = analyse_emotions(message)

    st.markdown('<div class="panel-card">', unsafe_allow_html=True)
    st.markdown("## Keputusan Keseluruhan")
    c1, c2, c3 = st.columns([1.1, 0.9, 1.2])
    with c1:
        st.markdown(
            f'<div class="result-card"><div class="result-label">Skor Risiko Keseluruhan</div>{risk_meter(result["overall_score"])}'
            '</div>',
            unsafe_allow_html=True,
        )
    with c2:
        level = result["overall_level"]
        st.markdown(
            f'<div class="result-card"><div class="result-label">Tahap Risiko</div><div class="badge {badge_class(level)}">{level}</div>'
            '</div>',
            unsafe_allow_html=True,
        )
    with c3:
        st.markdown(
            f'<div class="result-card"><div class="result-label">Kategori Ancaman</div><div class="result-note" style="color:#111827;font-weight:750;">{html.escape(result["threat_category"])}</div>'
            '</div>',
            unsafe_allow_html=True,
        )
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="panel-card">', unsafe_allow_html=True)
    st.markdown("## Analisis Pencetus Emosi")
    dominant_card = (
        '<div class="module-card">'
        f'<div class="module-title">{html.escape(result["dominant_emotion"])}</div>'
        f'<div class="module-caption">{html.escape(result["dominant_description"])}</div>'
        '</div>'
    )
    st.markdown(dominant_card, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="panel-card">', unsafe_allow_html=True)
    st.markdown("## Frasa dan Petanda Dikesan")
    sections = [
        ("Pencetus Emosi", result["emotions"], "tag-blue"),
        ("Padanan Kawalan Sah", result["control_phrases"], "tag-green"),
    ]
    for title, tags, cls in sections:
        st.markdown(f"#### {title}")
        st.markdown(tag_html(tags, cls), unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="panel-card">', unsafe_allow_html=True)
    st.markdown("## Padanan Data Kawalan Sepadan")
    st.markdown(f'<div class="subtle-note">{html.escape(control_message(result["threat_category"]))}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    guidance = {
        "Rendah": "Risiko rendah dikesan. Namun begitu, pengguna masih digalakkan menyemak kesahihan mesej melalui saluran rasmi.",
        "Sederhana": "Terdapat beberapa pencetus emosi yang mencurigakan. Semak sumber mesej dan elakkan membuat bayaran, menekan pautan atau berkongsi maklumat peribadi sebelum pengesahan lanjut.",
        "Tinggi": "Mesej menunjukkan manipulasi emosi yang kuat. Jangan berkongsi maklumat peribadi, jangan membuat bayaran dan semak melalui saluran rasmi.",
        "Sangat Tinggi": "Mesej ini menunjukkan risiko yang sangat tinggi. Jangan kongsi OTP, kata laluan atau PIN, jangan tekan pautan, jangan buat bayaran dan segera semak dengan pihak rasmi.",
    }
    st.markdown('<div class="panel-card">', unsafe_allow_html=True)
    st.markdown("## Cadangan Tindakan Selamat")
    st.markdown(f'<div class="subtle-note">{html.escape(guidance[result["overall_level"]])}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="panel-card">', unsafe_allow_html=True)
    st.markdown("## Penafian")
    st.markdown('<div class="subtle-note">ScamEmotion ialah prototaip amaran awal dan tidak menggantikan semakan rasmi. Pengguna digalakkan menyemak kesahihan mesej melalui saluran rasmi sebelum berkongsi maklumat peribadi, menekan pautan atau membuat sebarang transaksi kewangan.</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

elif check and not message.strip():
    st.warning("Sila masukkan mesej terlebih dahulu.")
