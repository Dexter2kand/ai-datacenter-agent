
import streamlit as st
import pandas as pd
from ai_agent import analyze_incident
from database import (
    init_database,
    add_equipment,
    get_equipment,
    add_incident,
    get_incidents
)

st.set_page_config(
    page_title="AI Data Center Agent",
    page_icon="🏢",
    layout="wide"
)

init_database()

st.title("🏢 AI Data Center Troubleshooting")
st.caption("Equipment & Incident Knowledge Management")

page = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Equipment Registry",
        "Incident Management",
"AI Troubleshooting"
    ]
)

equipment = get_equipment()
incidents = get_incidents()

if page == "Dashboard":

    st.header("📊 Data Center Dashboard")

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Equipment", len(equipment))
    col2.metric("Total Incidents", len(incidents))

    verified = sum(
        1 for i in incidents
        if i["verification_status"] == "Verified"
    )
    col3.metric("Verified Repairs", verified)

    if equipment:
        df = pd.DataFrame(equipment)
        st.subheader("Equipment by Category")
        st.bar_chart(df["category"].value_counts())

    if incidents:
        st.subheader("Recent Incidents")
        st.dataframe(
            pd.DataFrame(incidents),
            use_container_width=True
        )

elif page == "Equipment Registry":

    st.header("⚙️ Equipment Registry")

    with st.form("equipment_form"):

        name = st.text_input("Equipment Name")

        category = st.selectbox(
            "Category",
            [
                "UPS", "Battery", "PDU", "Generator",
                "CRAC", "CRAH", "Chiller",
                "Server", "Network", "BMS", "Other"
            ]
        )

        manufacturer = st.text_input("Manufacturer")
        model = st.text_input("Model")
        location = st.text_input("Location")

        submitted = st.form_submit_button(
            "Add Equipment"
        )

        if submitted:
            if not name.strip():
                st.error("Equipment name is required.")
            else:
                add_equipment(
                    name, category, manufacturer,
                    model, location
                )
                st.success("Equipment added successfully!")
                st.rerun()

    st.subheader("Registered Equipment")

    if equipment:
        st.dataframe(
            pd.DataFrame(equipment),
            use_container_width=True
        )
    else:
        st.info("No equipment registered yet.")

elif page == "Incident Management":

    st.header("🚨 Incident Management")

    if not equipment:
        st.warning(
            "Register equipment before adding incidents."
        )
    else:
        equipment_options = {
            f"{e['id']} - {e['name']}": e["id"]
            for e in equipment
        }

        with st.form("incident_form"):

            selected = st.selectbox(
                "Equipment",
                list(equipment_options.keys())
            )

            alarm_code = st.text_input("Alarm Code")

            symptoms = st.text_area(
                "Symptoms / Fault Description"
            )

            root_cause = st.text_area(
                "Confirmed Root Cause"
            )

            corrective_action = st.text_area(
                "Corrective Action"
            )

            contractor = st.text_input(
                "Contractor / Technician"
            )

            verification = st.selectbox(
                "Verification Status",
                ["Unverified", "Verified"]
            )

            submitted = st.form_submit_button(
                "Save Incident"
            )

            if submitted:
                if not symptoms.strip():
                    st.error("Fault description is required.")
                else:
                    add_incident(
                        equipment_options[selected],
                        alarm_code,
                        symptoms,
                        root_cause,
                        corrective_action,
                        contractor,
                        verification
                    )

                    st.success("Incident saved!")
                    st.rerun()

    st.subheader("Incident History")

    if incidents:
        st.dataframe(
            pd.DataFrame(incidents),
            use_container_width=True
        )
    else:
        st.info("No incidents recorded yet.")


elif page == "AI Troubleshooting":

    st.header("🤖 AI Troubleshooting Assistant")

    question = st.text_area(
        "Describe the equipment fault",
        placeholder="UPS-02 reports FAN_FAILURE and high temperature"
    )

    if st.button("Analyze Incident"):

        if not question.strip():
            st.warning("Please describe the incident.")
        else:
            with st.spinner("AI is analyzing..."):
                try:
                    answer = analyze_incident(question)
                    st.markdown(answer)
                except Exception as error:
                    st.error(f"Analysis failed: {error}")

