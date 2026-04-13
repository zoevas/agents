import streamlit as st
from supervisor import SupervisorAgent

st.title("AI Travel Planner ✈️")

destination = st.text_input("Destination", "Rome")
preferences = st.text_area("Hotel preferences")
duration = st.slider("Days", 1, 14, 5)

if st.button("Generate"):
    supervisor = SupervisorAgent()

    result = supervisor.execute({
        "destination": destination,
        "location": (41.9028, 12.4964),
        "preferences": preferences,
        "duration": duration
    })

    st.write(result)