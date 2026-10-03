import streamlit as st
import ollama
from elevenlabs.client import ElevenLabs

# ── Backend config — set your key here ───────────────────────────────────────
ELEVENLABS_API_KEY = "[ENCRYPTION_KEY]"

# ── Page Config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Dabba AI – Fridge to Feast",
    page_icon="🍱",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=Inter:wght@300;400;500;600&display=swap');

/* ── Root variables ── */
:root {
    --saffron:   #E8791A;
    --turmeric:  #D4A017;
    --clay:      #8B4513;
    --cream:     #FDF6EC;
    --bark:      #3D1F0D;
    --moss:      #556B2F;
    --spice:     #C0392B;
    --bg:        #1A0F05;
    --card:      rgba(255,255,255,0.05);
    --card-border: rgba(232,121,26,0.3);
    --glass:     rgba(253,246,236,0.07);
}

/* ── Global Reset ── */
html, body, [data-testid="stAppViewContainer"] {
    background: var(--bg) !important;
    font-family: 'Inter', sans-serif !important;
    color: var(--cream) !important;
}

/* ── Remove Streamlit branding ── */
#MainMenu, footer, header { visibility: hidden !important; }
[data-testid="stToolbar"] { display: none !important; }

/* ── Main container ── */
[data-testid="stAppViewContainer"] > .main {
    background: linear-gradient(160deg, #1A0F05 0%, #2D1505 40%, #1A0F05 100%) !important;
    min-height: 100vh;
}
.block-container {
    padding: 2rem 1.5rem 4rem !important;
    max-width: 760px !important;
}

/* ── Hero banner ── */
.hero-banner {
    background: linear-gradient(135deg, #2D1505 0%, #4A2010 50%, #2D1505 100%);
    border: 1px solid var(--card-border);
    border-radius: 24px;
    padding: 2.5rem 2rem;
    text-align: center;
    margin-bottom: 2.5rem;
    position: relative;
    overflow: hidden;
    box-shadow: 0 20px 60px rgba(232,121,26,0.15), inset 0 1px 0 rgba(255,255,255,0.1);
}
.hero-banner::before {
    content: '';
    position: absolute; inset: 0;
    background: radial-gradient(ellipse at 50% 0%, rgba(232,121,26,0.15) 0%, transparent 65%);
    pointer-events: none;
}
.hero-emoji {
    font-size: 4rem;
    display: block;
    margin-bottom: 0.5rem;
    filter: drop-shadow(0 4px 12px rgba(232,121,26,0.5));
}
.hero-title {
    font-family: 'Playfair Display', serif !important;
    font-size: 2.6rem !important;
    font-weight: 900 !important;
    background: linear-gradient(135deg, #F0A030, #E8791A, #D4A017);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin: 0 !important;
    line-height: 1.2 !important;
}
.hero-sub {
    color: rgba(253,246,236,0.65) !important;
    font-size: 0.95rem !important;
    margin-top: 0.5rem;
    letter-spacing: 0.5px;
}
.hero-chips {
    display: flex; gap: 8px; justify-content: center;
    flex-wrap: wrap; margin-top: 1.2rem;
}
.chip {
    background: rgba(232,121,26,0.15);
    border: 1px solid rgba(232,121,26,0.4);
    border-radius: 100px;
    padding: 4px 14px;
    font-size: 0.78rem;
    color: #F0A030;
    font-weight: 500;
    letter-spacing: 0.3px;
}

/* ── Section cards ── */
.section-card {
    background: var(--glass);
    border: 1px solid var(--card-border);
    border-radius: 18px;
    padding: 1.6rem 1.8rem;
    margin-bottom: 1.5rem;
    backdrop-filter: blur(8px);
    box-shadow: 0 8px 32px rgba(0,0,0,0.3);
    transition: border-color 0.3s;
}
.section-card:hover { border-color: rgba(232,121,26,0.55); }
.section-label {
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    color: var(--saffron);
    margin-bottom: 0.8rem;
    display: flex; align-items: center; gap: 6px;
}

/* ── Streamlit widgets ── */
[data-testid="stTextInput"] input,
[data-testid="stSelectbox"] select,
[data-testid="stSelectbox"] > div > div {
    background: rgba(255,255,255,0.06) !important;
    border: 1px solid rgba(232,121,26,0.35) !important;
    border-radius: 12px !important;
    color: var(--cream) !important;
    font-family: 'Inter', sans-serif !important;
}
[data-testid="stTextInput"] input:focus {
    border-color: var(--saffron) !important;
    box-shadow: 0 0 0 3px rgba(232,121,26,0.2) !important;
}

/* ── File uploader ── */
[data-testid="stFileUploader"] {
    background: rgba(255,255,255,0.04) !important;
    border: 2px dashed rgba(232,121,26,0.35) !important;
    border-radius: 16px !important;
    padding: 1rem !important;
    transition: border-color 0.3s, background 0.3s;
}
[data-testid="stFileUploader"]:hover {
    background: rgba(232,121,26,0.06) !important;
    border-color: var(--saffron) !important;
}
[data-testid="stFileUploaderDropzoneInput"] { cursor: pointer !important; }

/* ── Main button ── */
[data-testid="stButton"] button {
    background: linear-gradient(135deg, #E8791A, #D4501A) !important;
    color: white !important;
    border: none !important;
    border-radius: 14px !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 600 !important;
    font-size: 1rem !important;
    padding: 0.75rem 2rem !important;
    width: 100% !important;
    cursor: pointer !important;
    transition: all 0.25s ease !important;
    box-shadow: 0 4px 20px rgba(232,121,26,0.4) !important;
    letter-spacing: 0.3px !important;
}
[data-testid="stButton"] button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 28px rgba(232,121,26,0.55) !important;
    background: linear-gradient(135deg, #F08020, #E05518) !important;
}
[data-testid="stButton"] button:active { transform: translateY(0) !important; }

/* ── Step badges ── */
.step-badge {
    display: inline-flex;
    align-items: center;
    gap: 10px;
    background: linear-gradient(135deg, rgba(232,121,26,0.15), rgba(212,160,23,0.1));
    border: 1px solid rgba(232,121,26,0.4);
    border-radius: 100px;
    padding: 6px 18px;
    font-size: 0.8rem;
    font-weight: 600;
    color: #F0A030;
    margin-bottom: 1rem;
    letter-spacing: 0.5px;
}
.step-dot {
    width: 8px; height: 8px;
    background: var(--saffron);
    border-radius: 50%;
    animation: pulse 1.5s infinite;
}
@keyframes pulse {
    0%, 100% { opacity: 1; transform: scale(1); }
    50% { opacity: 0.5; transform: scale(0.8); }
}

/* ── Ingredients result ── */
.ingredients-box {
    background: linear-gradient(135deg, rgba(85,107,47,0.2), rgba(85,107,47,0.1));
    border: 1px solid rgba(85,107,47,0.5);
    border-radius: 14px;
    padding: 1rem 1.4rem;
    font-size: 0.9rem;
    color: #A8C87A;
    font-weight: 500;
    margin: 0.5rem 0 1.2rem;
}
.ingredients-box span { color: rgba(253,246,236,0.6); font-weight: 400; }

/* ── Recipe card ── */
.recipe-card {
    background: linear-gradient(135deg, rgba(44,17,5,0.9), rgba(58,25,8,0.9));
    border: 1px solid rgba(232,121,26,0.45);
    border-radius: 18px;
    padding: 1.8rem 2rem;
    line-height: 1.9;
    font-size: 0.97rem;
    color: var(--cream);
    margin-top: 0.5rem;
    box-shadow: 0 12px 40px rgba(0,0,0,0.4), inset 0 1px 0 rgba(255,255,255,0.05);
}
.recipe-title {
    font-family: 'Playfair Display', serif;
    font-size: 1.3rem;
    font-weight: 700;
    color: #F0A030;
    border-bottom: 1px solid rgba(232,121,26,0.3);
    padding-bottom: 0.8rem;
    margin-bottom: 1rem;
}

/* ── Audio player ── */
audio {
    width: 100% !important;
    border-radius: 12px !important;
    margin-top: 0.5rem;
    accent-color: var(--saffron) !important;
}

/* ── Info / success / error overrides ── */
[data-testid="stInfo"] {
    background: rgba(85,107,47,0.15) !important;
    border-left: 4px solid #556B2F !important;
    border-radius: 12px !important;
    color: #C5E08A !important;
}
[data-testid="stSuccess"] {
    background: rgba(232,121,26,0.12) !important;
    border-left: 4px solid var(--saffron) !important;
    border-radius: 12px !important;
    color: #F0A030 !important;
}
[data-testid="stError"] {
    background: rgba(192,57,43,0.15) !important;
    border-left: 4px solid var(--spice) !important;
    border-radius: 12px !important;
}

/* ── Divider ── */
.spice-divider {
    text-align: center;
    color: rgba(232,121,26,0.4);
    font-size: 1.2rem;
    letter-spacing: 8px;
    margin: 1.5rem 0;
    user-select: none;
}

/* ── Spinner ── */
[data-testid="stSpinner"] { color: var(--saffron) !important; }

/* ── Uploaded image ── */
[data-testid="stImage"] img {
    border-radius: 16px !important;
    border: 2px solid rgba(232,121,26,0.35) !important;
    box-shadow: 0 8px 32px rgba(0,0,0,0.4) !important;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: #200F03 !important;
    border-right: 1px solid rgba(232,121,26,0.2) !important;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(232,121,26,0.4); border-radius: 10px; }
::-webkit-scrollbar-thumb:hover { background: rgba(232,121,26,0.65); }

/* ── Footer ── */
.app-footer {
    text-align: center;
    font-size: 0.75rem;
    color: rgba(253,246,236,0.3);
    padding-top: 2rem;
    letter-spacing: 0.5px;
}
.app-footer a { color: rgba(232,121,26,0.6); text-decoration: none; }

/* ── Narrate toggle label ── */
.narrate-label {
    font-size: 0.85rem;
    color: rgba(253,246,236,0.7);
    margin-bottom: 0.3rem;
}
</style>
""", unsafe_allow_html=True)

# ── Hero Banner ───────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-banner">
    <span class="hero-emoji">🍱</span>
    <h1 class="hero-title">Dabba AI</h1>
    <p class="hero-sub">From fridge chaos to feast — powered by local AI</p>
    <div class="hero-chips">
        <span class="chip">🤖 Gemma 3 Vision</span>
        <span class="chip">🧠 Gemma 3 Recipe</span>
        <span class="chip">🔊 ElevenLabs Voice</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Settings Section ──────────────────────────────────────────────────────────
st.markdown('<div class="section-card">', unsafe_allow_html=True)
st.markdown('<div class="section-label">⚙️ Settings</div>', unsafe_allow_html=True)

dietary_need = st.selectbox(
    "Dietary Constraint",
    ["None", "Jain (No Onion/Garlic)", "High Protein", "Vegan", "Only 15 mins prep time"],
    help="We'll tailor the recipe to this constraint"
)

enable_narration = st.toggle(
    "🔊  Enable Voice Narration",
    value=True,
    help="Hear the recipe read aloud — great for hands-free cooking!"
)

st.markdown('</div>', unsafe_allow_html=True)

# ── Upload Section ────────────────────────────────────────────────────────────
st.markdown('<div class="section-card">', unsafe_allow_html=True)
st.markdown('<div class="section-label">📸 Snap Your Fridge</div>', unsafe_allow_html=True)

uploaded_file = st.file_uploader(
    "Drop a photo of your ingredients here",
    type=["jpg", "jpeg", "png", "webp"],
    label_visibility="collapsed",
    help="Works best with good lighting and a clear shot of your ingredients"
)
st.markdown("</div>", unsafe_allow_html=True)

# ── Image Preview ─────────────────────────────────────────────────────────────
if uploaded_file is not None:
    st.image(uploaded_file, caption="What we're working with today 👇", use_container_width=True)

    st.markdown('<div class="spice-divider">✦ ✦ ✦</div>', unsafe_allow_html=True)

    generate_clicked = st.button("🍳  Generate My Dabba Recipe", use_container_width=True)

    if generate_clicked:

        # ── STEP 1: Vision – Gemma 3 ─────────────────────────────────────────
        st.markdown("""
        <div class="step-badge">
            <span class="step-dot"></span>
            Step 1 of 3 — Gemma Vision
        </div>
        """, unsafe_allow_html=True)

        with st.spinner("Scanning your ingredients with Gemma…"):
            vision_prompt = (
                "Identify all the raw food ingredients visible in this image. "
                "List them concisely as comma-separated words only. No sentences, no explanations."
            )
            try:
                vision_response = ollama.chat(
                    model='gemma3',
                    messages=[{
                        'role': 'user',
                        'content': vision_prompt,
                        'images': [uploaded_file.getvalue()]
                    }]
                )
                ingredients = vision_response['message']['content'].strip()
            except Exception as e:
                st.error(f"Gemma vision error: {e}")
                st.stop()

        st.markdown(f"""
        <div class="ingredients-box">
            🥬 <span>Ingredients spotted:</span> &nbsp;{ingredients}
        </div>
        """, unsafe_allow_html=True)

        # ── STEP 2: Recipe – Gemma 3 ──────────────────────────────────────────
        st.markdown("""
        <div class="step-badge">
            <span class="step-dot"></span>
            Step 2 of 3 — Gemma 3 Recipe Generation
        </div>
        """, unsafe_allow_html=True)

        with st.spinner("Gemma 3 is crafting your dabba recipe…"):
            text_prompt = f"""You are a creative Indian home cook. I have these ingredients: {ingredients}.

Create a fast, practical dabba/tiffin recipe using ONLY these ingredients and standard Indian spices (salt, haldi, jeera, rai, hing, dhania powder, red chilli powder).
Dietary constraint: {dietary_need}.

Rules:
- Give the recipe a short, appetising name on the first line.
- Keep it to exactly 5 numbered steps or fewer.
- Keep each step under 2 sentences.
- Use simple conversational language.
- Do NOT add any intro or outro text."""

            try:
                recipe_response = ollama.chat(
                    model='gemma3',
                    messages=[{'role': 'user', 'content': text_prompt}]
                )
                recipe_text = recipe_response['message']['content'].strip()
            except Exception as e:
                st.error(f"Gemma 3 error: {e}")
                st.stop()

        # Extract the first line as title (if any)
        recipe_lines = recipe_text.split('\n')
        recipe_title = recipe_lines[0].strip().lstrip('*').strip() if recipe_lines else "Your Recipe"
        recipe_body  = '\n'.join(recipe_lines[1:]).strip()

        st.markdown(f"""
        <div class="recipe-card">
            <div class="recipe-title">🍽️ {recipe_title}</div>
            {recipe_body.replace(chr(10), '<br>')}
        </div>
        """, unsafe_allow_html=True)

        st.success("✅ Recipe ready! Time to cook.")

        # ── STEP 3: Narration – ElevenLabs ───────────────────────────────────
        if enable_narration:
            st.markdown("""
            <div class="step-badge">
                <span class="step-dot"></span>
                Step 3 of 3 — ElevenLabs Voice Narration
            </div>
            """, unsafe_allow_html=True)

            with st.spinner("Generating hands-free voice narration…"):
                try:
                    client = ElevenLabs(api_key=ELEVENLABS_API_KEY)
                    audio_generator = client.text_to_speech.convert(
                        text=recipe_text,
                        voice_id="JBFqnCBsd6RMkjVDRZzb",
                        model_id="eleven_multilingual_v2",
                        output_format="mp3_44100_128",
                    )
                    audio_bytes = b"".join(audio_generator)
                except Exception as e:
                    st.error(f"ElevenLabs narration error: {e}")
                    st.stop()

            st.markdown('<div class="section-card">', unsafe_allow_html=True)
            st.markdown('<div class="section-label">🔊 Voice Narration — Hands-Free Cooking</div>', unsafe_allow_html=True)
            st.audio(audio_bytes, format="audio/mp3")
            st.markdown("</div>", unsafe_allow_html=True)

        else:
            st.info("🔊 Voice narration is disabled. Enable it in Settings to hear your recipe aloud!")

# ── Empty state ───────────────────────────────────────────────────────────────
else:
    st.markdown("""
    <div style="text-align:center; padding: 2.5rem 1rem; opacity: 0.5;">
        <div style="font-size: 3rem; margin-bottom: 0.8rem;">📷</div>
        <p style="font-size: 0.9rem; letter-spacing: 0.5px;">Upload a photo of your ingredients above to get started</p>
    </div>
    """, unsafe_allow_html=True)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="app-footer">
    🍛 Dabba AI &nbsp;·&nbsp; Local AI, Zero Cloud &nbsp;·&nbsp;
    Built with <a href="https://streamlit.io" target="_blank">Streamlit</a>,
    <a href="https://ollama.com" target="_blank">Ollama</a> &amp;
    <a href="https://elevenlabs.io" target="_blank">ElevenLabs</a>
</div>
""", unsafe_allow_html=True)
