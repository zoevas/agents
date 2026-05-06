import streamlit as st
from langgraph_flow.graph import build_graph

st.title("AI Travel Planner with LangGraph ✈️")

origin = st.text_input("Origin", "Athens")
destination = st.text_input("Destination", "Rome")

departure_date = st.date_input("Departure Date")
return_date = st.date_input("Return Date")

budget = st.selectbox("Hotel Budget", ["low", "mid", "high"])
duration = st.slider("Days", 1, 14, 5)

preferences = f"{budget} budget hotel, city center, comfortable stay"

if st.button("Generate Plan"):
    graph = build_graph()

    result = graph.invoke({
        "origin": origin,
        "destination": destination,
        "location": (41.9028, 12.4964),
        "preferences": preferences,
        "duration": duration,
        "departure_date": str(departure_date),
        "return_date": str(return_date),
        "flight_budget": 300,
    })

    st.subheader("📅 Best Travel Month")
    st.write(result.get("best_months"))

    st.subheader("✈️ Flight")
    st.write(result.get("selected_flight"))

    st.subheader("🏨 Hotel")
    st.write(result.get("selected_hotel"))

    st.subheader("🗺️ Itinerary")
    st.write(result.get("itinerary"))

    st.subheader("🧠 Debug Logs")

    for log in result.get("debug_logs", []):
        st.write(log)