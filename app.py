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

# ==============================
# Button Input Grid Logic (Fixed)
# ==============================
def add_digit(d):
    if len(st.session_state.age_input) < 2:
        if d == "9" and st.session_state.age_input == "":
            return
        st.session_state.age_input += d

def submit_gender(gender):
    st.session_state.selected_gender = gender
    st.session_state.submitted = True

if not st.session_state.submitted:
    layout = [["1", "2", "3"], ["4", "5", "6"], ["7", "8", "9"], ["MALE", "0", "FEMALE"]]
    for row in layout:
        cols = st.columns(3)
        for i, label in enumerate(row):
            if label == "MALE":
                cols[i].button(label, on_click=submit_gender, args=("Male",), disabled=len(st.session_state.age_input) != 2, key="male")
            elif label == "FEMALE":
                cols[i].button(label, on_click=submit_gender, args=("Female",), disabled=len(st.session_state.age_input) != 2, key="female")
            else:
                disable = False
                if st.session_state.age_input == "1" and label not in ["8", "9"]:
                    disable = True
                if st.session_state.age_input == "8" and label != "0":
                    disable = True
                if st.session_state.age_input and len(st.session_state.age_input) == 1 and int(st.session_state.age_input + label) > 80:
                    disable = True
                if st.session_state.age_input == "" and label == "9":
                    disable = True
                cols[i].button(label, on_click=add_digit, args=(label,), disabled=disable, key=f"btn_{label}")

# ==============================
# Pricing + Results + Copyable Block
# ==============================
male_ia_prices = {**{a: 21 for a in range(18, 41)}, **{a: 25 for a in range(41, 46)}}
female_ia_prices = {**{a: 20 for a in range(18, 41)}, **{a: 22 for a in range(41, 46)}}
male_tl_prices = {46: 25, 47: 27, 48: 28, 49: 30, 50: 31, 51: 33, 52: 35, 53: 37, 54: 39, 55: 41, 56: 45, 57: 49, 58: 53, 59: 58, 60: 62, 61: 70, 62: 77, 63: 84, 64: 93}
female_tl_prices = {46: 25, 47: 25, 48: 26, 49: 27, 50: 27, 51: 29, 52: 30, 53: 32, 54: 34, 55: 35, 56: 38, 57: 40, 58: 43, 59: 46, 60: 49, 61: 54, 62: 58, 63: 62, 64: 67}
male_sh_prices = {**{a: 9 for a in range(18, 41)}, **{41: 14, 42: 14, 43: 15, 44: 15, 45: 16}, 46: 17, 47: 18, 48: 19, 49: 20, 50: 21, 51: 26, 52: 26, 53: 28, 54: 29, 55: 30, 56: 32, 57: 33, 58: 35, 59: 37, 60: 38, 61: 50, 62: 53, 63: 58, 64: 67}
female_sh_prices = {18: 14, 19: 14, 20: 14, 21: 14, 22: 15, 23: 15, 24: 15, 25: 16, 26: 16, 27: 17, 28: 17, 29: 18, 30: 19, 31: 19, 32: 20, 33: 20, 34: 21, 35: 21, 36: 21, 37: 22, 38: 22, 39: 23, 40: 23, 41: 23, 42: 24, 43: 24, 44: 25, 45: 25, 46: 27, 47: 28, 48: 29, 49: 32, 50: 37, 51: 39, 52: 41, 53: 42, 54: 44, 55: 44, 56: 45, 57: 46, 58: 47, 59: 49, 60: 50, 61: 53, 62: 56, 63: 59, 64: 62}
final_expense_prices = {age: {"Male": m, "Female": f} for age, m, f in [(65, 80, 64), (66, 85, 68), (67, 89, 72), (68, 94, 76), (69, 99, 80), (70, 103, 84), (71, 110, 89), (72, 116, 95), (73, 123, 101), (74, 129, 107), (75, 136, 112), (76, 144, 120), (77, 152, 128), (78, 160, 137), (79, 168, 145), (80, 176, 153)]}

if st.session_state.submitted and st.session_state.age_input.isdigit():
    age = int(st.session_state.age_input)
    gender = st.session_state.selected_gender
    g_abbr = "M" if gender == "Male" else "F"

    if age >= 65:
        fe = final_expense_prices[age][gender]
        st.session_state.copy_text = f"({age}{g_abbr})\nFE ${fe}"
    else:
        plan = "IA" if age <= 45 else "TL"
        price = male_ia_prices[age] if gender == "Male" else female_ia_prices[age] if plan == "IA" else male_tl_prices[age] if gender == "Male" else female_tl_prices[age]
        sh = male_sh_prices[age] if gender == "Male" else female_sh_prices[age]
        bundle = price + sh
        st.session_state.copy_text = f"({age}{g_abbr})\n{plan}${price} | SH${sh}\nBUNDLE ${bundle}"

    st.markdown(f"""
        <style>
        .copy-box {{
            cursor: pointer;
            font-family: Myriad Pro;
            font-weight: bold;
            font-size: 22px;
            text-align: center;
            color: white;
            padding: 15px;
            border: 1px solid #555;
            border-radius: 8px;
            background-color: #222;
            margin-top: 20px;
        }}
        .copied-popup {{
            position: fixed;
            top: 20px;
            left: 50%;
            transform: translateX(-50%);
            background-color: #1f1;
            color: black;
            font-weight: bold;
            padding: 8px 16px;
            border-radius: 8px;
            z-index: 1000;
            animation: fadeout 2s ease-out forwards;
        }}
        @keyframes fadeout {{ from {{ opacity: 1; }} to {{ opacity: 0; }} }}
        </style>
        <div class="copy-box" onclick="navigator.clipboard.writeText(`{st.session_state.copy_text}`); let popup=document.createElement('div'); popup.className='copied-popup'; popup.innerText='Copied!'; document.body.appendChild(popup); setTimeout(() => popup.remove(), 2000);">
            {st.session_state.copy_text.replace('\n', '<br>')}
        </div>
    """, unsafe_allow_html=True)
