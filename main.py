import random
import streamlit as st

# Set up the web page configuration
st.set_page_config(page_title="Web Taxi Tycoon", page_icon="🚕", layout="centered")

# --- GAME DATA ---
CAR_DEALER = [
    {"name": "Rusty Sedan", "speed_multiplier": 1.0, "price": 0, "icon": "🚗"},
    {
        "name": "Yellow Cab Pro",
        "speed_multiplier": 1.5,
        "price": 150,
        "icon": "🚕",
    },
    {"name": "Electric Taxi", "speed_multiplier": 2.2, "price": 500, "icon": "🚙"},
    {"name": "Supercar Taxi", "speed_multiplier": 3.5, "price": 1500, "icon": "🏎️"},
]

HOUSE_MARKET = [
    {"name": "None / Taxi Backseat", "price": 0, "icon": "💤"},
    {"name": "Suburban Apartment", "price": 300, "icon": "🏢"},
    {"name": "Downtown Condo", "price": 1000, "icon": "🌆"},
    {"name": "Luxury Mansion", "price": 3000, "icon": "🏰"},
]

PASSENGERS = [
    {"name": "Business Exec", "base_fare": 50, "dialogue": "To the financial district, quickly!"},
    {"name": "Tourist", "base_fare": 30, "dialogue": "Can you take me to the big monument?"},
    {"name": "Chef", "base_fare": 40, "dialogue": "I'm late for my dinner rush opening!"},
    {"name": "Student", "base_fare": 25, "dialogue": "Just dropping me off at the library campus, please."},
]

# --- SESSION STATE INITIALIZATION ---
if "money" not in st.session_state:
    st.session_state.money = 0
    st.session_state.car_idx = 0
    st.session_state.house_idx = 0
    st.session_state.current_passenger = None
    st.session_state.game_log = []

# --- HELPER FUNCTIONS ---
def log_message(msg):
    st.session_state.game_log.insert(0, msg)
    if len(st.session_state.game_log) > 5:
        st.session_state.game_log.pop()


# --- UI HEADER ---
st.title("🚕 Taxi Tycoon: Web Edition")
st.write("Pick up passengers, earn fares, and build your luxury lifestyle right from your browser!")
st.markdown("---")

# --- DASHBOARD METRICS ---
col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="Wallet Balance", value=f"${st.session_state.money}")
with col2:
    current_car = CAR_DEALER[st.session_state.car_idx]
    st.metric(label="Current Vehicle", value=f"{current_car['icon']} {current_car['name']}")
with col3:
    current_house = HOUSE_MARKET[st.session_state.house_idx]
    st.metric(label="Real Estate", value=f"{current_house['icon']} {current_house['name']}")

st.markdown("---")

# --- GAMEPLAY CORE ---
left_side, right_side = st.columns([2, 1])

with left_side:
    st.subheader("🚏 Dispatch Center")

    # Scenario 1: Waiting for a passenger
    if st.session_state.current_passenger is None:
        st.info("Your taxi is idling at the curb. Scan the city streets for a passenger fare!")
        if st.button("🔍 Search for Passenger", type="primary", use_container_width=True):
            passenger = random.choice(PASSENGERS)
            # Fare formula based on vehicle speed multiplier
            multiplier = CAR_DEALER[st.session_state.car_idx]["speed_multiplier"]
            passenger["actual_fare"] = int(passenger["base_fare"] * multiplier)
            st.session_state.current_passenger = passenger
            log_message(f"Found a passenger: {passenger['name']}.")
            st.rerun()

    # Scenario 2: Passenger is in the car
    else:
        p = st.session_state.current_passenger
        st.success(f"**Passenger On Board:** {p['name']}")
        st.chat_message("user").write(f'"{p["dialogue"]}"')
        st.write(f"💵 **Estimated Payout:** `${p['actual_fare']}`")
        
        if st.button("🏁 Drive to Destination", type="primary", use_container_width=True):
            fare_earned = p['actual_fare']
            st.session_state.money += fare_earned
            log_message(f"Successfully dropped off {p['name']}! Earned ${fare_earned}.")
            st.session_state.current_passenger = None
            st.rerun()

    # Activity Feed / Log
    if st.session_state.game_log:
        st.caption("Recent Shift Activity:")
        for log in st.session_state.game_log:
            st.write(log)

# --- UPGRADE SHOP ---
with right_side:
    st.subheader("🛍️ Tycoon Shop")
    
    # Car Upgrades
    st.write("**Dealership**")
    if st.session_state.car_idx < len(CAR_DEALER) - 1:
        next_car = CAR_DEALER[st.session_state.car_idx + 1]
        st.caption(f"Next: {next_car['icon']} {next_car['name']} (Gives higher multipliers)")
        if st.button(f"Buy for ${next_car['price']}", key="buy_car", use_container_width=True):
            if st.session_state.money >= next_car["price"]:
                st.session_state.money -= next_car["price"]
                st.session_state.car_idx += 1
                log_message(f"Purchased a brand new {next_car['name']}!")
                st.rerun()
            else:
                st.error("Not enough cash!")
    else:
        st.write("🥇 *Max vehicle tier achieved!*")

    st.markdown("---")
    
    # House Upgrades
    st.write("**Real Estate Market**")
    if st.session_state.house_idx < len(HOUSE_MARKET) - 1:
        next_house = HOUSE_MARKET[st.session_state.house_idx + 1]
        st.caption(f"Next: {next_house['icon']} {next_house['name']}")
        if st.button(f"Buy for ${next_house['price']}", key="buy_house", use_container_width=True):
            if st.session_state.money >= next_house["price"]:
                st.session_state.money -= next_house["price"]
                st.session_state.house_idx += 1
                log_message(f"Moved into a gorgeous {next_house['name']}!")
                st.rerun()
            else:
                st.error("Not enough cash!")
    else:
        st.write("🏆 *You own the finest mansion in town!*")
