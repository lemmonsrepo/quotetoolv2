import streamlit as st
import platform

st.set_page_config(page_title="", layout="centered")

if "age_input" not in st.session_state:
    st.session_state.age_input = ""
if "selected_gender" not in st.session_state:
    st.session_state.selected_gender = None
if "submitted" not in st.session_state:
    st.session_state.submitted = False
if "copy_text" not in st.session_state:
    st.session_state.copy_text = ""

suffix = ""
if st.session_state.selected_gender == "Male":
    suffix = "M"
elif st.session_state.selected_gender == "Female":
    suffix = "F"

st.markdown(f'<div style="font-family: Myriad Pro; font-weight: bold; font-size: 32px; color: white; text-align: center; border: 1px solid #ccc; padding: 10px; width: 220px; margin: 20px auto;">{st.session_state.age_input + (" " + suffix if suffix else "")}</div>', unsafe_allow_html=True)

# RESET BUTTON
if st.button("RESET"):
    st.session_state.age_input = ""
    st.session_state.selected_gender = None
    st.session_state.submitted = False
    st.session_state.copy_text = ""

# Pricing data (same as before)
...  # omitted here for brevity but unchanged from your current version

# Results block
if st.session_state.submitted and st.session_state.age_input.isdigit():
    age = int(st.session_state.age_input)
    gender = st.session_state.selected_gender
    g_abbr = "M" if gender == "Male" else "F"

    st.markdown("""
        <style>
        .results { font-family: Myriad Pro; font-size: 22px; text-align: center; }
        .bold { font-weight: bold; }
        .copy-button-container { text-align: center; margin-top: 10px; }
        .copy-button { font-size: 16px; padding: 8px 20px; margin-top: 5px; border-radius: 6px; background-color: #444; color: white; border: none; cursor: pointer; }
        </style>
    """, unsafe_allow_html=True)

    st.markdown(f"<div class='results bold'>({age}{g_abbr})</div>", unsafe_allow_html=True)

    if age >= 65:
        fe = final_expense_prices[age][gender]
        out = f"FE ${fe}"
        st.session_state.copy_text = f"({age}{g_abbr})\n{out}"
        st.markdown(f"<div class='results bold'>{out}</div>", unsafe_allow_html=True)
    else:
        if age <= 45:
            plan = "IA"
            price = male_ia_prices[age] if gender == "Male" else female_ia_prices[age]
        else:
            plan = "TL"
            price = male_tl_prices[age] if gender == "Male" else female_tl_prices[age]
        sh = male_sh_prices[age] if gender == "Male" else female_sh_prices[age]
        bundle = price + sh
        line1 = f"<span class='bold'>{plan}${price}</span> | <span class='bold'>SH${sh}</span>"
        line2 = f"<span class='bold'>BUNDLE ${bundle}</span>"
        st.session_state.copy_text = f"({age}{g_abbr})\n{plan}${price} | SH${sh}\nBUNDLE ${bundle}"
        st.markdown(f"<div class='results'>{line1}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='results'>{line2}</div>", unsafe_allow_html=True)

    # Proper copy button using JS
    st.markdown(f"""
        <div class='copy-button-container'>
        <textarea id="copyText" style="opacity: 0; height: 1px;">{st.session_state.copy_text}</textarea>
        <button class='copy-button' onclick="navigator.clipboard.writeText(document.getElementById('copyText').value); let msg = document.createElement('div'); msg.innerText = 'Copied!'; msg.style.color = '#0f0'; document.body.appendChild(msg); setTimeout(()=>msg.remove(), 1500);">COPY</button>
        </div>
    """, unsafe_allow_html=True)

# Input flow (unchanged)
...  # remains the same
