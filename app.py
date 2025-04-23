import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="", layout="centered")

if "age_input" not in st.session_state:
    st.session_state.age_input = ""
if "selected_gender" not in st.session_state:
    st.session_state.selected_gender = None
if "submitted" not in st.session_state:
    st.session_state.submitted = False
if "copy_text" not in st.session_state:
    st.session_state.copy_text = ""

def reset_state():
    st.session_state.age_input = ""
    st.session_state.selected_gender = None
    st.session_state.submitted = False
    st.session_state.copy_text = ""

suffix = ""
if st.session_state.selected_gender == "Male":
    suffix = "M"
elif st.session_state.selected_gender == "Female":
    suffix = "F"

st.markdown(f'<div style="font-family: Myriad Pro; font-weight: bold; font-size: 32px; color: white; text-align: center; border: 1px solid #ccc; padding: 10px; width: 220px; margin: 20px auto;">{st.session_state.age_input + (" " + suffix if suffix else "")}</div>', unsafe_allow_html=True)

if st.button("RESET"):
    reset_state()

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
                if st.session_state.age_input == "" and label == "9":
                    disable = True
                if st.session_state.age_input and len(st.session_state.age_input) == 1 and int(st.session_state.age_input + label) > 80:
                    disable = True
                cols[i].button(label, on_click=add_digit, args=(label,), disabled=disable, key=f"btn_{label}")

# Keyboard input handling
key_input = st.text_input("", value="", max_chars=2, key="keyboard_input", label_visibility="collapsed")
if key_input == "" and st.session_state.submitted is False:
    key_input = st.query_params.get("keyboard_input", [""])[0]
if key_input in ["\b", "\x7f"]:
    reset_state()
elif key_input.isdigit():
    for digit in key_input:
        if len(st.session_state.age_input) < 2:
            if digit == "9" and st.session_state.age_input == "":
                continue
            if st.session_state.age_input == "1" and digit not in ["8", "9"]:
                continue
            if st.session_state.age_input == "8" and digit != "0":
                continue
            if st.session_state.age_input == "" and digit == "9":
                continue
            if len(st.session_state.age_input) == 1 and int(st.session_state.age_input + digit) > 80:
                continue
            st.session_state.age_input += digit

def get_prices(age, gender):
    ia_prices = {
        "Male": {**{a: 21 for a in range(18, 41)}, **{a: 25 for a in range(41, 46)}},
        "Female": {**{a: 20 for a in range(18, 41)}, **{a: 22 for a in range(41, 46)}}
    }
    tl_prices = {
        "Male": {46: 25, 47: 27, 48: 28, 49: 30, 50: 31, 51: 33, 52: 35, 53: 37, 54: 39, 55: 41, 56: 45, 57: 49, 58: 53, 59: 58, 60: 62, 61: 70, 62: 77, 63: 84, 64: 93},
        "Female": {46: 25, 47: 25, 48: 26, 49: 27, 50: 27, 51: 29, 52: 30, 53: 32, 54: 34, 55: 35, 56: 38, 57: 40, 58: 43, 59: 46, 60: 49, 61: 54, 62: 58, 63: 62, 64: 67},
    }
    sh_prices = {
        "Male": {
            18: 9, 19: 9, 20: 9, 21: 9, 22: 9, 23: 9, 24: 9, 25: 9, 26: 9, 27: 9, 28: 9, 29: 9, 30: 9,
            31: 9, 32: 9, 33: 10, 34: 10, 35: 10, 36: 10, 37: 11, 38: 11, 39: 12, 40: 13, 41: 14, 42: 15, 43: 15, 44: 16, 45: 17,
            46: 18, 47: 19, 48: 20, 49: 21, 50: 23, 51: 26, 52: 28, 53: 30, 54: 32, 55: 35, 56: 37, 57: 39, 58: 42, 59: 44,
            60: 49, 61: 53, 62: 58, 63: 62, 64: 67
        },
        "Female": {18: 14, 19: 14, 20: 14, 21: 14, 22: 15, 23: 15, 24: 15, 25: 16, 26: 16, 27: 17, 28: 17, 29: 18, 30: 19, 31: 19, 32: 20, 33: 20, 34: 21, 35: 21, 36: 21, 37: 22, 38: 22, 39: 23, 40: 23, 41: 23, 42: 24, 43: 24, 44: 25, 45: 25, 46: 27, 47: 28, 48: 29, 49: 32, 50: 37, 51: 39, 52: 41, 53: 42, 54: 44, 55: 44, 56: 45, 57: 46, 58: 47, 59: 49, 60: 50, 61: 53, 62: 56, 63: 59, 64: 62},
    }
    fe_prices = {
        "Male": {65: 80, 66: 85, 67: 89, 68: 94, 69: 99, 70: 103, 71: 110, 72: 116, 73: 123, 74: 129, 75: 136, 76: 144, 77: 152, 78: 160, 79: 168, 80: 176},
        "Female": {65: 64, 66: 68, 67: 72, 68: 76, 69: 80, 70: 84, 71: 89, 72: 95, 73: 101, 74: 107, 75: 112, 76: 120, 77: 128, 78: 137, 79: 145, 80: 153},
    }

    if age >= 65:
        return "FE", fe_prices[gender][age], 0
    elif age <= 45:
        price = ia_prices[gender][age]
        return "IA", price, sh_prices[gender][age]
    else:
        return "TL", tl_prices[gender][age], sh_prices[gender][age]

if st.session_state.submitted and st.session_state.age_input.isdigit():
    age = int(st.session_state.age_input)
    gender = st.session_state.selected_gender
    g_abbr = "M" if gender == "Male" else "F"
    plan, price, sh = get_prices(age, gender)

    if plan == "FE":
        copy_block = f"({age}{g_abbr})\nFE ${price}"
        html_block = f"""
        <div style='font-family: Myriad Pro; color: white; font-size: 22px; text-align: center; line-height: 1.6;'>
            ({age}{g_abbr})<br>
            <b>FE ${price}</b>
        </div>
        """
    else:
        bundle = price + sh
        copy_block = f"({age}{g_abbr})\n{plan}${price} | SH${sh}\nBUNDLE ${bundle}"
        html_block = f"""
        <div style='font-family: Myriad Pro; color: white; font-size: 22px; text-align: center; line-height: 1.6;'>
            ({age}{g_abbr})<br>
            <b>{plan}${price}</b> | <b>SH${sh}</b><br>
            <b>BUNDLE ${bundle}</b>
        </div>
        """
    st.session_state.copy_text = copy_block
    st.markdown(html_block, unsafe_allow_html=True)
    st.text_input("", value=copy_block, label_visibility="collapsed")
