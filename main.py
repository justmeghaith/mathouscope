import random
import streamlit as st

# Set up the web page configuration
st.set_page_config(page_title="Grand Theft Loney V: Web Edition", page_icon="🗽", layout="wide")

# --- GAME DATA ---
CAR_DEALER = [
    "Lamborghini Aventador (BEST CAR)", "Ferrari 488", "Porsche 911", 
    "Bugatti Chiron", "McLaren P1", "Aston Martin DB11", "Nissan GT-R",
    "Toyota Supra", "Ford Mustang", "Chevrolet Camaro", "Dodge Charger",
    "BMW M4", "Audi R8", "Mercedes AMG GT", "Tesla Model S", 
    "Honda Civic Type R", "Volkswagen Golf GTI", "Jeep Wrangler",
    "Range Rover", "Subaru WRX STI", "Mazda RX-7"
]

COUNTRIES_CITIES = {
    "United States": ["Los Santos", "Liberty City", "Vice City"],
    "Japan": ["Tokyo", "Kyoto", "Osaka"],
    "United Kingdom": ["London", "Manchester", "Edinburgh"],
    "France": ["Paris", "Marseille", "Lyon"]
}

CLOTHES_SHOP = {
    "Leather Jacket": 150,
    "Designer Hoodie": 300,
    "Suit & Tie": 500,
    "Gold Chain Outfit": 1200
}

SHOES_SHOP = {
    "Old Sneakers": 0,
    "Running Kicks": 80,
    "Luxury Skate Shoes": 250,
    "Hype Beast Boots": 600
}

# --- SESSION STATE INITIALIZATION ---
if "game_started" not in st.session_state:
    st.session_state.game_started = False
    st.session_state.loney = 500  # Currency named Loney
    st.session_state.current_outfit = "Default Rags"
    st.session_state.current_shoes = "Old Sneakers"
    st.session_state.country = "United States"
    st.session_state.city = "Los Santos"
    st.session_state.is_married = False
    st.session_state.kids_count = 0
    st.session_state.current_car = "None (On Foot)"
    st.session_state.garage = []
    st.session_state.is_flying = False
    st.session_state.logs = ["Welcome to Grand Theft Loney V! Customize your character to begin."]

def add_log(msg):
    st.session_state.logs.insert(0, msg)

# --- MAIN MENU & CUSTOMIZER ---
if not st.session_state.game_started:
    st.title("🗽 GRAND THEFT LONEY V")
    st.subheader("Main Menu & Character Customization")
    
    # Mode Selector
    mode = st.radio("Select Game Mode:", ["Offline Story Mode", "Online Multiplayer (Server Live)"], horizontal=True)
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🎛️ Game Controls Guide")
        st.info(
            "**Steal Car:** Click the 'Hijack Vehicle' button\n\n"
            "**Buy Items/Food:** Use the Tycoon Shopping tabs\n\n"
            "**Admin Panel:** Use the sidebar menu to toggle cheats\n\n"
            "**Family System:** Meet NPCs to marry and spawn children"
        )
        
        st.markdown("### 🛫 Select Your Drop Destination")
        chosen_country = st.selectbox("Select Country:", list(COUNTRIES_CITIES.keys()))
        chosen_city = st.selectbox("Select City/Dropzone:", COUNTRIES_CITIES[chosen_country])
        
    with col2:
        st.markdown(f"### 🛍️ Character Customizer (Wallet: ${st.session_state.loney} Loney)")
        
        # Clothes buy
        selected_clothes = st.selectbox("Choose Clothes:", list(CLOTHES_SHOP.keys()))
        if st.button(f"Purchase Top for ${CLOTHES_SHOP[selected_clothes]} Loney"):
            price = CLOTHES_SHOP
