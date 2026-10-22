import streamlit as st
import pickle
import re
import string
import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

# ---------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------
st.set_page_config(
    page_title="SMS Shield | Spam Detector",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------------------------------------------------------
# NLTK SETUP
# ---------------------------------------------------------
@st.cache_resource
def setup_nltk():
    resources = [
        ("corpora/stopwords", "stopwords"),
        ("tokenizers/punkt", "punkt"),
        ("tokenizers/punkt_tab", "punkt_tab"),
    ]
    for path, package in resources:
        try:
            nltk.data.find(path)
        except LookupError:
            try:
                nltk.download(package, quiet=True)
            except Exception:
                pass

    return PorterStemmer(), set(stopwords.words("english"))

ps, STOP_WORDS = setup_nltk()

# ---------------------------------------------------------
# LOAD MODEL + VECTORIZER
# ---------------------------------------------------------
@st.cache_resource
def load_artifacts():
    with open("model.pkl", "rb") as f:
        model = pickle.load(f)
    with open("vectorizer.pkl", "rb") as f:
        vectorizer = pickle.load(f)
    return model, vectorizer

model, vectorizer = load_artifacts()

# ---------------------------------------------------------
# SAME PREPROCESSING PIPELINE USED IN THE NOTEBOOK
# ---------------------------------------------------------
def transform_text(text):
    text = str(text).lower()

    try:
        tokens = nltk.word_tokenize(text)
    except Exception:
        # Fallback keeps the app usable if NLTK tokenizer data is unavailable.
        tokens = re.findall(r"\b\w+\b", text)

    tokens = [token for token in tokens if token.isalnum()]

    final_tokens = []
    for token in tokens:
        if token not in STOP_WORDS and token not in string.punctuation:
            final_tokens.append(ps.stem(token))

    return " ".join(final_tokens)


def classify_message(message):
    transformed = transform_text(message)
    features = vectorizer.transform([transformed])

    prediction = int(model.predict(features)[0])
    probabilities = model.predict_proba(features)[0]

    ham_probability = float(probabilities[0])
    spam_probability = float(probabilities[1])

    return prediction, ham_probability, spam_probability, transformed


# ---------------------------------------------------------
# CUSTOM DARK UI
# ---------------------------------------------------------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    .stApp {
        background:
            radial-gradient(circle at 10% 10%, rgba(99,102,241,.16), transparent 28%),
            radial-gradient(circle at 90% 15%, rgba(14,165,233,.12), transparent 25%),
            radial-gradient(circle at 50% 100%, rgba(168,85,247,.10), transparent 30%),
            #080b12;
        color: #f8fafc;
    }

    .block-container {
        max-width: 1180px;
        padding-top: 2rem;
        padding-bottom: 4rem;
    }

    .hero {
        padding: 2.5rem 1rem 1.5rem;
        text-align: center;
    }

    .badge {
        display: inline-block;
        padding: .45rem .9rem;
        border: 1px solid rgba(129,140,248,.35);
        background: rgba(99,102,241,.10);
        border-radius: 999px;
        color: #c7d2fe;
        font-size: .82rem;
        font-weight: 700;
        letter-spacing: .08em;
        text-transform: uppercase;
    }

    .hero h1 {
        margin: 1rem 0 .5rem;
        font-size: clamp(2.4rem, 6vw, 4.8rem);
        line-height: 1;
        font-weight: 800;
        background: linear-gradient(90deg, #f8fafc, #a5b4fc, #67e8f9, #f8fafc);
        background-size: 250% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: gradientMove 5s linear infinite;
    }

    @keyframes gradientMove {
        0% { background-position: 0% center; }
        100% { background-position: 250% center; }
    }

    .hero p {
        color: #94a3b8;
        font-size: 1.05rem;
        max-width: 720px;
        margin: 0 auto;
    }

    .glass-card {
        background: linear-gradient(145deg, rgba(17,24,39,.88), rgba(15,23,42,.65));
        border: 1px solid rgba(148,163,184,.13);
        border-radius: 24px;
        padding: 1.35rem;
        box-shadow: 0 25px 70px rgba(0,0,0,.28);
        backdrop-filter: blur(16px);
    }

    .section-title {
        font-size: 1.15rem;
        font-weight: 800;
        color: #e2e8f0;
        margin-bottom: .35rem;
    }

    .section-subtitle {
        color: #64748b;
        font-size: .88rem;
        margin-bottom: 1rem;
    }

    textarea {
        background: #0b1120 !important;
        color: #f8fafc !important;
        border: 1px solid #263247 !important;
        border-radius: 16px !important;
    }

    textarea:focus {
        border-color: #818cf8 !important;
        box-shadow: 0 0 0 2px rgba(129,140,248,.15) !important;
    }

    div.stButton > button {
        width: 100%;
        min-height: 3.2rem;
        border: 0;
        border-radius: 14px;
        color: white;
        font-weight: 800;
        font-size: 1rem;
        background: linear-gradient(135deg, #6366f1, #8b5cf6);
        box-shadow: 0 12px 30px rgba(99,102,241,.25);
        transition: all .2s ease;
    }

    div.stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 18px 35px rgba(99,102,241,.35);
    }

    .metric-card {
        background: #0b1120;
        border: 1px solid #1e293b;
        border-radius: 18px;
        padding: 1rem;
        text-align: center;
    }

    .metric-label {
        color: #64748b;
        font-size: .78rem;
        text-transform: uppercase;
        letter-spacing: .08em;
    }

    .metric-value {
        color: #f8fafc;
        font-size: 1.45rem;
        font-weight: 800;
        margin-top: .25rem;
    }

    .result {
        border-radius: 22px;
        padding: 1.6rem;
        text-align: center;
        margin-top: 1rem;
        animation: pop .45s ease-out;
    }

    .spam-result {
        background: linear-gradient(145deg, rgba(127,29,29,.35), rgba(69,10,10,.22));
        border: 1px solid rgba(248,113,113,.30);
    }

    .ham-result {
        background: linear-gradient(145deg, rgba(6,78,59,.35), rgba(2,44,34,.22));
        border: 1px solid rgba(52,211,153,.30);
    }

    @keyframes pop {
        0% { opacity: 0; transform: scale(.94) translateY(10px); }
        100% { opacity: 1; transform: scale(1) translateY(0); }
    }

    .result-icon {
        font-size: 3.3rem;
        margin-bottom: .4rem;
        animation: float 2.2s ease-in-out infinite;
    }

    @keyframes float {
        0%,100% { transform: translateY(0); }
        50% { transform: translateY(-7px); }
    }

    .result h2 {
        margin: 0;
        color: #f8fafc;
    }

    .result p {
        color: #cbd5e1;
        margin: .5rem 0 0;
    }

    .footer {
        text-align: center;
        color: #475569;
        font-size: .78rem;
        margin-top: 3rem;
    }

    .tip {
        color: #94a3b8;
        font-size: .84rem;
        line-height: 1.55;
        padding: .9rem 1rem;
        background: rgba(15,23,42,.55);
        border: 1px solid rgba(148,163,184,.10);
        border-radius: 14px;
    }

    .stProgress > div > div > div > div {
        border-radius: 999px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ---------------------------------------------------------
# HERO
# ---------------------------------------------------------
st.markdown(
    """
    <div class="hero">
        <div class="badge">AI • NLP • Naive Bayes</div>
        <h1>SMS Shield</h1>
        <p>Paste a message and let the machine-learning model decide whether it looks like <b>SPAM</b> or a normal <b>HAM</b> message.</p>
    </div>
    """,
    unsafe_allow_html=True
)

# ---------------------------------------------------------
# INPUT
# ---------------------------------------------------------
left, right = st.columns([1.35, .65], gap="large")

with left:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">📩 Message Scanner</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-subtitle">Enter the SMS you want to analyse.</div>',
        unsafe_allow_html=True
    )

    examples = {
        "🎁 Prize message": "Congratulations! You have won a free prize. Click now to claim your reward!",
        "💳 Bank alert": "Your account has been credited with Rs 5000. Call customer support if this was not you.",
        "👋 Normal chat": "Hey, are we meeting at 6 pm today? Let me know.",
    }

    selected = st.selectbox("Try an example", ["Custom message"] + list(examples.keys()))

    default_text = "" if selected == "Custom message" else examples[selected]
    message = st.text_area(
        "SMS",
        value=default_text,
        height=190,
        placeholder="e.g. Congratulations! You won a free voucher...",
        label_visibility="collapsed"
    )

    char_count = len(message)
    word_count = len(message.split()) if message.strip() else 0

    m1, m2, m3 = st.columns(3)
    with m1:
        st.markdown(
            f'<div class="metric-card"><div class="metric-label">Characters</div><div class="metric-value">{char_count}</div></div>',
            unsafe_allow_html=True
        )
    with m2:
        st.markdown(
            f'<div class="metric-card"><div class="metric-label">Words</div><div class="metric-value">{word_count}</div></div>',
            unsafe_allow_html=True
        )
    with m3:
        st.markdown(
            f'<div class="metric-card"><div class="metric-label">Model</div><div class="metric-value">MNB</div></div>',
            unsafe_allow_html=True
        )

    st.write("")
    scan = st.button("🔍  Analyse Message", use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with right:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">🧠 How it works</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subtitle">Same core preprocessing used during model training.</div>', unsafe_allow_html=True)

    st.markdown(
        """
        <div class="tip">
        <b>1. Clean</b><br>Lowercase + remove non-alphanumeric tokens.
        </div><br>
        <div class="tip">
        <b>2. NLP preprocessing</b><br>Remove English stopwords and apply Porter stemming.
        </div><br>
        <div class="tip">
        <b>3. TF-IDF</b><br>Convert the processed message into numerical features.
        </div><br>
        <div class="tip">
        <b>4. Prediction</b><br>Multinomial Naive Bayes returns the final class.
        </div>
        """,
        unsafe_allow_html=True
    )
    st.markdown("</div>", unsafe_allow_html=True)

# ---------------------------------------------------------
# RESULT
# ---------------------------------------------------------
if scan:
    if not message.strip():
        st.warning("Please enter an SMS before analysing.")
    else:
        with st.spinner("Scanning message..."):
            prediction, ham_prob, spam_prob, transformed = classify_message(message)

        if prediction == 1:
            st.markdown(
                f"""
                <div class="result spam-result">
                    <div class="result-icon">🚨</div>
                    <h2>SPAM DETECTED</h2>
                    <p>This message was classified as spam by the trained model.</p>
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                f"""
                <div class="result ham-result">
                    <div class="result-icon">🛡️</div>
                    <h2>SAFE / HAM</h2>
                    <p>This message was classified as a normal message by the trained model.</p>
                </div>
                """,
                unsafe_allow_html=True
            )

        st.write("")
        st.markdown("### 📊 Model Confidence")

        c1, c2 = st.columns(2)
        with c1:
            st.metric("HAM probability", f"{ham_prob * 100:.2f}%")
            st.progress(ham_prob)
        with c2:
            st.metric("SPAM probability", f"{spam_prob * 100:.2f}%")
            st.progress(spam_prob)

        with st.expander("🔎 View NLP preprocessing"):
            st.code(transformed if transformed else "[empty after preprocessing]")

        # Final success animation.
        if prediction == 1:
            st.toast("🚨 Spam detected!", icon="🚨")
        else:
            st.toast("🛡️ Message looks safe!", icon="🛡️")

        st.balloons()

# ---------------------------------------------------------
# FOOTER
# ---------------------------------------------------------
st.markdown(
    """
    <div class="footer">
        Built with Streamlit • TF-IDF • Multinomial Naive Bayes
    </div>
    """,
    unsafe_allow_html=True
)
