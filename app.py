import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="", layout="centered")

if "quote_input" not in st.session_state:
    st.session_state.quote_input = ""
if "submitted" not in st.session_state:
    st.session_state.submitted = False
if "copy_text" not in st.session_state:
    st.session_state.copy_text = ""
if "copied" not in st.session_state:
    st.session_state.copied = False


def reset_state():
    st.session_state.quote_input = ""
    st.session_state.submitted = False
    st.session_state.copy_text = ""
    st.session_state.copied = False

# This will force results to update immediately when the input changes
input_value = st.text_input("Enter Age + Gender (e.g. 26F)", max_chars=3)
if input_value != st.session_state.quote_input:
    st.session_state.quote_input = input_value.upper()
    st.experimental_rerun()

if st.button("RESET"):
    reset_state()

if st.session_state.quote_input and len(st.session_state.quote_input) == 3 and st.session_state.quote_input[:2].isdigit() and st.session_state.quote_input[-1].upper() in ["M", "F"] and st.session_state.quote_input[0] in ["1", "2", "3", "4", "5", "6", "7", "8"]:
    st.session_state.submitted = True
    age = int(st.session_state.quote_input[:2])
    gender = "Male" if st.session_state.quote_input[-1].upper() == "M" else "Female"

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

    plan, price, sh = get_prices(age, gender)
    g_abbr = "M" if gender == "Male" else "F"

    if plan == "FE":
        copy_block = f"({age}{g_abbr})\nFE ${price}"
        html_block = f"""
        <div onclick="navigator.clipboard.writeText(`{copy_block}`); window.parent.postMessage('copied', '*');" 
             style='cursor: pointer; font-family: Myriad Pro; color: white; font-size: 22px; text-align: center; line-height: 1.6; background-color: #2c2c2c; padding: 10px; border-radius: 8px;'>
            ({age}{g_abbr})<br>
            <b>FE ${price}</b>
        </div>
        """
    else:
        bundle = price + sh
        copy_block = f"({age}{g_abbr})\n{plan}${price} | SH${sh}\nBUNDLE ${bundle}"
        html_block = f"""
        <div onclick="navigator.clipboard.writeText(`{copy_block}`); window.parent.postMessage('copied', '*');" 
             style='cursor: pointer; font-family: Myriad Pro; color: white; font-size: 22px; text-align: center; line-height: 1.6; background-color: #2c2c2c; padding: 10px; border-radius: 8px;'>
            ({age}{g_abbr})<br>
            <b>{plan}${price}</b> | <b>SH${sh}</b><br>
            <b>BUNDLE ${bundle}</b>
        </div>
        """

    st.session_state.copy_text = copy_block
    st.markdown(html_block, unsafe_allow_html=True)

    components.html("""
    <script>
    window.addEventListener('message', (event) => {
        if (event.data === 'copied') {
            const copiedBox = window.parent.document.querySelector("[data-testid='stMarkdownContainer']");
            if (copiedBox && !document.getElementById('copied-msg')) {
                const msg = document.createElement('div');
                msg.id = 'copied-msg';
                msg.innerText = '✔ Copied!';
                msg.style.color = '#00ffcc';
                msg.style.fontSize = '16px';
                msg.style.marginTop = '6px';
                msg.style.textAlign = 'center';
                copiedBox.appendChild(msg);
            }
        }
    });
    </script>
    """, height=0)
