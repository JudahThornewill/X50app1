import streamlit as st
from openai import OpenAI

# 🌐 Load API key securely from Streamlit secrets
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# ⚙️ Streamlit page config
st.set_page_config(page_title="X50 LEW Estimator", layout="centered")
st.title("🌱 X50: Lifelong Wellbeing Estimator")
st.markdown("Use this tool to estimate your **LEW** (Life-Enhanced Wellbeing) and get guidance to improve it.")

# 🧮 User inputs
life_expectancy = st.slider("Estimated Remaining Life Expectancy (years)", 0.0, 120.0, 40.0)
wellby_score = st.slider("WELLBY Score (0–10)", 0.0, 10.0, 7.0)
risk_adjustment = st.slider("Risk Adjustment Factor (0.0–1.0)", 0.0, 1.0, 0.85)

# 📊 LEW calculation
lew = life_expectancy * wellby_score * risk_adjustment
st.subheader("📊 Your Estimated LEW")
st.metric(label="LEW (Life-Enhanced Wellbeing)", value=round(lew, 2))

# 🤖 Advice generator using GPT
def generate_advice(lew, wellby, risk):
    prompt = f"""
    You are X50 AI, a pragmatic, motivational wellbeing advisor.
    A user has a LEW score of {lew}, a WELLBY score of {wellby}, and a risk factor of {risk}.
    Offer 2–3 practical, uplifting insights about how they can improve their wellbeing—
    either through increasing life expectancy, boosting WELLBYs, or reducing risk.
    Be encouraging, concise, and grounded in science-based wisdom.
    """

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You're a motivational LEW advisor."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )

    return response.choices[0].message.content.strip()

# 🧭 Generate and display guidance
with st.spinner("Thinking deeply about your wellbeing..."):
    try:
        advice = generate_advice(lew, wellby_score, risk_adjustment)
        st.subheader("🧭 X50 AI Guidance")
        st.write(advice)
    except Exception as e:
        st.error("An error occurred while generating advice.")
        st.caption(f"Details: {e}")

# 🧠 Footer
st.markdown("---")
st.caption("🧠 This is an early prototype. X50 AI provides motivational insights—not medical advice.")