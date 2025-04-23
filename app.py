import streamlit as st
import streamlit.components.v1 as components
import platform

st.set_page_config(page_title="", layout="centered")

# Reset state on initial page load
if st.button("RESET"):
    st.session_state.clear()
    st.experimental_rerun()

if "age_input" not in st.session_state:
    st.session_state.age_input = ""
if "selected_gender" not in st.session_state:
    st.session_state.selected_gender = None
if "submitted" not in st.session_state:
    st.session_state.submitted = False

# Input display
suffix = ""
if st.session_state.selected_gender == "Male":
    suffix = " M"
elif st.session_state.selected_gender == "Female":
    suffix = " F"
st.markdown(f'<div style="font-family: Myriad Pro; font-weight: bold; font-size: 32px; text-align: center; border: 1px solid #ccc; padding: 10px; width: 220px; margin: 20px auto;">{st.session_state.age_input}{suffix}</div>', unsafe_allow_html=True)

if not st.session_state.submitted:
    components.html("""
    <div style="display: grid; grid-template-columns: repeat(3, 80px); gap: 12px; justify-content: center;">
      <button class="key" onclick="send(1)">1</button>
      <button class="key" onclick="send(2)">2</button>
      <button class="key" onclick="send(3)">3</button>
      <button class="key" onclick="send(4)">4</button>
      <button class="key" onclick="send(5)">5</button>
      <button class="key" onclick="send(6)">6</button>
      <button class="key" onclick="send(7)">7</button>
      <button class="key" onclick="send(8)">8</button>
      <button class="key" onclick="send(9)">9</button>
      <button class="key" style="background-color: #007bff; color: white;" onclick="send('M')">M</button>
      <button class="key" onclick="send(0)">0</button>
      <button class="key" style="background-color: #e91e63; color: white;" onclick="send('F')">F</button>
    </div>
    <script>
      const streamlitSend = (v) => {
        const el = window.parent.document.querySelector('iframe');
        el.contentWindow.postMessage({ isStreamlitMessage: true, type: 'streamlit:setComponentValue', value: v }, '*');
      }
      function send(val) {
        streamlitSend(val);
      }
    </script>
    <style>
      .key {
        width: 80px;
        height: 80px;
        font-size: 24px;
        font-weight: bold;
        font-family: 'Myriad Pro', sans-serif;
        border: none;
        background-color: #333;
        color: #fff;
        border-radius: 6px;
        transition: background-color 0.2s;
      }
      .key:hover {
        background-color: #555;
      }
      .key:active {
        background-color: #888;
      }
    </style>
    """, height=400)

# Pricing logic
male_ia_prices = {**{a: 21 for a in range(18, 41)}, **{a: 25 for a in range(41, 46)}}
female_ia_prices = {**{a: 20 for a in range(18, 41)}, **{a: 22 for a in range(41, 46)}}
male_tl_prices = {46: 25, 47: 27, 48: 28, 49: 30, 50: 31, 51: 33, 52: 35, 53: 37, 54: 39, 55: 41, 56: 45, 57: 49, 58: 53, 59: 58, 60: 62, 61: 70, 62: 77, 63: 84, 64: 93}
female_tl_prices = {46: 25, 47: 25, 48: 26, 49: 27, 50: 27, 51: 29, 52: 30, 53: 32, 54: 34, 55: 35, 56: 38, 57: 40, 58: 43, 59: 46, 60: 49, 61: 54, 62: 58, 63: 62, 64: 67}
male_sh_prices = {**{a: 9 for a in range(18, 41)}, **{41: 14, 42: 14, 43: 15, 44: 15, 45: 16}, 46: 17, 47: 18, 48: 19, 49: 20, 50: 21, 51: 26, 52: 26, 53: 28, 54: 29, 55: 30, 56: 32, 57: 33, 58: 35, 59: 37, 60: 38, 61: 50, 62: 53, 63: 58, 64: 67}
female_sh_prices = {18: 14, 19: 14, 20: 14, 21: 14, 22: 15, 23: 15, 24: 15, 25: 16, 26: 16, 27: 17, 28: 17, 29: 18, 30: 19, 31: 19, 32: 20, 33: 20, 34: 21, 35: 21, 36: 21, 37: 22, 38: 22, 39: 23, 40: 23, 41: 23, 42: 24, 43: 24, 44: 25, 45: 25, 46: 27, 47: 28, 48: 29, 49: 32, 50: 37, 51: 39, 52: 41, 53: 42, 54: 44, 55: 44, 56: 45, 57: 46, 58: 47, 59: 49, 60: 50, 61: 53, 62: 56, 63: 59, 64: 62}
final_expense_prices = {age: {"Male": m, "Female": f} for age, m, f in [(65, 80, 64), (66, 85, 68), (67, 89, 72), (68, 94, 76), (69, 99, 80), (70, 103, 84), (71, 110, 89), (72, 116, 95), (73, 123, 101), (74, 129, 107), (75, 136, 112), (76, 144, 120), (77, 152, 128), (78, 160, 137), (79, 168, 145), (80, 176, 153)]}

# Output after submission
if st.session_state.submitted and st.session_state.age_input.isdigit():
    age = int(st.session_state.age_input)
    gender = st.session_state.selected_gender
    if age >= 65:
        fe_price = final_expense_prices[age][gender]
        st.markdown(f"<div class='results'>FE${fe_price}</div>", unsafe_allow_html=True)
    else:
        if age <= 45:
            plan = "IA"
            price = male_ia_prices[age] if gender == "Male" else female_ia_prices[age]
        else:
            plan = "TL"
            price = male_tl_prices[age] if gender == "Male" else female_tl_prices[age]
        sh = male_sh_prices[age] if gender == "Male" else female_sh_prices[age]
        bundle = price + sh
        st.markdown(f"<div class='results'>{plan}${price}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='results'>SH${sh}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='results'>BUNDLE${bundle}</div>", unsafe_allow_html=True)
