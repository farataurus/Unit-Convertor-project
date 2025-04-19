import streamlit as st
from streamlit_lottie import st_lottie
import requests

# ========== PAGE CONFIG ==========
st.set_page_config(
    page_title="Universal Converter | Farah Asghar",
    page_icon="📐",
    layout="centered",
    initial_sidebar_state="expanded"
)

# ========== LOTTIE ANIMATIONS ==========
def load_lottie_url(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

header_anim = load_lottie_url("https://assets1.lottiefiles.com/packages/lf20_5tkzkblw.json")
conversion_anim = load_lottie_url("https://assets1.lottiefiles.com/packages/lf20_1pxqjqps.json")

# ========== ENHANCED CSS FOR LIGHT/DARK THEME ==========
st.markdown("""
<style>
    [data-testid="stAppViewContainer"] > .main {
        background-color: transparent;
    }
    
    /* Card styling */
    .card {
        background-color: var(--secondary-background-color) !important;
        border-radius: 15px !important;
        padding: 25px !important;
        box-shadow: 0 8px 16px rgba(0,0,0,0.15) !important;
        margin-bottom: 25px !important;
        border: 2px solid var(--border-color) !important;
        transition: all 0.3s ease !important;
    }
    
    /* Input and result boxes */
    .input-box, .result-box {
        background-color: var(--box-background) !important;
        border-radius: 12px !important;
        padding: 15px !important;
        border: 2px solid var(--box-border-color) !important;
        margin: 10px 0 !important;
        transition: border-color 0.3s ease, transform 0.3s ease !important;
    }
    
    .input-box:hover, .result-box:hover {
        border-color: var(--primary-color) !important;
        transform: translateY(-2px) !important;
    }
    
    /* Animated result */
    .result {
        font-size: 1.6rem !important;
        color: var(--primary-color) !important;
        font-weight: bold !important;
        margin-top: 15px !important;
        animation: fadeInScale 0.5s ease-in-out !important;
    }
    
    @keyframes fadeInScale {
        0% {
            opacity: 0;
            transform: scale(0.8);
        }
        100% {
            opacity: 1;
            transform: scale(1);
        }
    }
    
    /* Input fields */
    .stNumberInput, .stSelectbox {
        background-color: var(--background-color) !important;
        border-radius: 10px !important;
        border: 1px solid var(--border-color) !important;
    }
    
    .stSelectbox label, .stNumberInput label {
        color: var(--text-color) !important;
        font-weight: 600 !important;
    }
    
    /* Button styling */
    .stButton>button {
        background-color: var(--primary-color) !important;
        color: white !important;
        border-radius: 10px !important;
        border: 2px solid var(--border-color) !important;
        padding: 10px 24px !important;
        transition: background-color 0.3s ease, transform 0.2s ease !important;
    }
    
    .stButton>button:hover {
        background-color: var(--primary-hover-color) !important;
        transform: scale(1.05) !important;
    }
    
    /* Footer */
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background: linear-gradient(45deg, #4b6cb7, #182848);
        color: white !important;
        text-align: center;
        padding: 15px;
        font-size: 14px;
        z-index: 100;
    }
    
    /* Theme variables */
    :root {
        --primary-color: #4b6cb7;
        --primary-hover-color: #3a5a9b;
        --secondary-background-color: rgba(255, 255, 255, 0.95);
        --box-background: rgba(240, 242, 246, 0.8);
        --text-color: #333;
        --border-color: #ddd;
        --box-border-color: #c0c7d3;
    }
    
    /* Dark theme overrides */
    @media (prefers-color-scheme: dark) {
        :root {
            --primary-color: #6c8bda;
            --primary-hover-color: #526cb7;
            --secondary-background-color: rgba(31, 41, 55, 0.95);
            --box-background: rgba(45, 55, 72, 0.8);
            --text-color: #f0f2f6;
            --border-color: #4a5568;
            --box-border-color: #6b7280;
        }
        .card {
            box-shadow: 0 8px 16px rgba(0,0,0,0.3) !important;
        }
    }
</style>
""", unsafe_allow_html=True)

# ========== CONVERSION FUNCTIONS ==========
def convert_units(value, from_unit, to_unit, category):
    conversions = {
        "length": {
            "mm": 0.001, "cm": 0.01, "m": 1, "km": 1000,
            "inch": 0.0254, "foot": 0.3048, "yard": 0.9144, "mile": 1609.34
        },
        "weight": {
            "mg": 0.001, "g": 1, "kg": 1000, "ton": 1000000,
            "ounce": 28.3495, "pound": 453.592
        },
        "temperature": {
            "celsius": lambda c: (c * 9/5) + 32,
            "fahrenheit": lambda f: (f - 32) * 5/9,
            "kelvin": lambda k: k - 273.15
        },
        "volume": {
            "ml": 0.001, "l": 1, "m3": 1000,
            "gallon": 3.78541, "quart": 0.946353, "pint": 0.473176, "cup": 0.24
        }
    }
    
    try:
        if category == "temperature":
            if from_unit == to_unit:
                return value
            return conversions[category][to_unit](value)
        else:
            if from_unit == to_unit:
                return value
            base_value = value * conversions[category][from_unit]
            return base_value / conversions[category][to_unit]
    except:
        return value

# ========== MAIN APP ==========
def main():
    # Initialize session state for unit selections
    if 'selected_from_unit' not in st.session_state:
        st.session_state.selected_from_unit = None
    if 'selected_to_unit' not in st.session_state:
        st.session_state.selected_to_unit = None

    # Header with animation
    col1, col2 = st.columns([1, 2])
    with col1:
        st_lottie(header_anim, height=120, key="header_anim")
    with col2:
        st.title("Universal Converter")
        st.markdown("**Convert between different units with ease**", unsafe_allow_html=True)
    
    # Category selection
    category = st.selectbox(
        "Select Conversion Type",
        ["length", "weight", "temperature", "volume"],
        key="category"
    )
    
    # Unit selection
    units = {
        "length": ["mm", "cm", "m", "km", "inch", "foot", "yard", "mile"],
        "weight": ["mg", "g", "kg", "ton", "ounce", "pound"],
        "temperature": ["celsius", "fahrenheit", "kelvin"],
        "volume": ["ml", "l", "m3", "gallon", "quart", "pint", "cup"]
    }
    
    # Conversion card
    with st.container():
        st.markdown("""<div class="card">""", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""<div class="input-box">""", unsafe_allow_html=True)
            value = st.number_input("Enter Value", min_value=0.0, format="%.4f", key="value")
            from_unit = st.selectbox(
                "From Unit",
                units[category],
                index=units[category].index(st.session_state.selected_from_unit) if st.session_state.selected_from_unit in units[category] else 0,
                key="from_unit"
            )
            st.session_state.selected_from_unit = from_unit
            st.markdown("""</div>""", unsafe_allow_html=True)
        
        with col2:
            st.markdown("""<div class="result-box">""", unsafe_allow_html=True)
            to_unit = st.selectbox(
                "To Unit",
                units[category],
                index=units[category].index(st.session_state.selected_to_unit) if st.session_state.selected_to_unit in units[category] else 1,
                key="to_unit"
            )
            st.session_state.selected_to_unit = to_unit
            result = convert_units(value, from_unit, to_unit, category)
            st.markdown(f"<div class='result'>{result:.4f} {to_unit}</div>", unsafe_allow_html=True)
            st.markdown("""</div>""", unsafe_allow_html=True)
        
        # Swap button
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("⇄ Swap Units", help="Click to swap units"):
                st.session_state.selected_from_unit, st.session_state.selected_to_unit = st.session_state.selected_to_unit, st.session_state.selected_from_unit
                st.rerun()
        
        st.markdown("""</div>""", unsafe_allow_html=True)
    
    # Conversion animation
    st_lottie(conversion_anim, height=200, key="conversion_anim")
    
    # Footer
    st.markdown("""
    <div class="footer">
        Developed with ❤️ by Farah Asghar | © 2025 Universal Converter | v1.2
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()