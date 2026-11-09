import os
from datetime import datetime
import streamlit as st
from dotenv import load_dotenv
from hindsight_client import Hindsight

load_dotenv()

st.set_page_config(page_title="OpsMind AI", page_icon="🧠", layout="wide")

BANK_ID = os.getenv("HINDSIGHT_BANK_ID", "opsmind-incidents")
HINDSIGHT_URL = os.getenv("HINDSIGHT_BASE_URL", "https://api.hindsight.vectorize.io")

def get_client():
    key = os.getenv("HINDSIGHT_API_KEY", "").strip()
    if not key:
        raise RuntimeError("Missing HINDSIGHT_API_KEY. Add it to your .env file.")
    return Hindsight(base_url=HINDSIGHT_URL, api_key=key, timeout=60.0)

def ensure_bank(client):
    try:
        client.create_bank(
            bank_id=BANK_ID,
            name="OpsMind Incident Knowledge",
            background="Persistent operational incident knowledge: symptoms, environments, root causes, fixes, and prevention steps.",
            disposition={"skepticism": 3, "literalism": 3, "empathy": 2},
        )
    except Exception:
        # The bank may already exist. A subsequent recall/retain will verify access.
        pass

def memory_text(result):
    items = getattr(result, "results", []) or []
    if not items:
        return []
    return [getattr(item, "text", str(item)) for item in items]

st.markdown("""
<style>
.block-container {padding-top: 2rem; max-width: 1200px;}
.hero {padding: 1.4rem 1.6rem; border-radius: 16px; background: linear-gradient(120deg,#101d35,#173b50); color: white; margin-bottom: 1.2rem;}
.hero h1 {margin:0; font-size:2.2rem;}
.hero p {color:#c9d9e8; margin:.45rem 0 0 0;}
.small-muted {color:#8794a5; font-size:.85rem;}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="hero"><h1>🧠 OpsMind AI</h1><p>Incident response that remembers, learns, and gets better with every resolution.</p></div>', unsafe_allow_html=True)

with st.sidebar:
    st.header("System status")
    st.caption("Persistent memory powered by Hindsight")
    st.code(f"Bank: {BANK_ID}", language="text")
    st.markdown("[Hindsight Cloud](https://ui.hindsight.vectorize.io) · [SDK docs](https://hindsight.vectorize.io/sdks/python)")
    st.divider()
    st.markdown("**Demo flow**")
    st.markdown("1. Seed a known incident\n2. Diagnose a similar incident\n3. Save the confirmed fix\n4. Repeat and show memory recall")

if "last_diagnosis" not in st.session_state:
    st.session_state.last_diagnosis = None
if "last_incident" not in st.session_state:
    st.session_state.last_incident = None
if "diagnosis_count" not in st.session_state:
    st.session_state.diagnosis_count = 0

c1, c2, c3 = st.columns(3)
c1.metric("Diagnoses this session", st.session_state.diagnosis_count)
c2.metric("Memory engine", "Hindsight")
c3.metric("Agent mode", "Memory-aware")

tab1, tab2, tab3 = st.tabs(["🚨 Diagnose incident", "🧠 Memory explorer", "🧪 Demo data"])

with tab1:
    st.subheader("New production incident")
    with st.form("incident_form"):
        left, right = st.columns(2)
        with left:
            title = st.text_input("Incident title", placeholder="API returning 500 errors")
            service = st.selectbox("Affected service", ["API / Backend", "Database", "Authentication", "Network", "Deployment / CI-CD", "Other"])
            severity = st.select_slider("Severity", options=["Low", "Medium", "High", "Critical"], value="High")
        with right:
            environment = st.selectbox("Environment", ["Production", "Staging", "Development"])
            error_code = st.text_input("Error code / log (optional)", placeholder="Connection timeout after 30s")
            impact = st.text_input("Business impact", placeholder="Checkout requests failing for customers")
        symptoms = st.text_area("What happened?", height=120, placeholder="Describe the symptoms, recent changes, logs, and what has already been tried...")
        submitted = st.form_submit_button("🔍 Diagnose with OpsMind", type="primary", use_container_width=True)

    if submitted:
        if not title.strip() or not symptoms.strip():
            st.warning("Please provide an incident title and symptoms.")
        else:
            try:
                with st.spinner("Searching incident memory and reasoning over previous resolutions..."):
                    client = get_client()
                    ensure_bank(client)
                    incident_query = (
                        f"Incident: {title}\nService: {service}\nSeverity: {severity}\n"
                        f"Environment: {environment}\nError/log: {error_code}\n"
                        f"Business impact: {impact}\nSymptoms: {symptoms}"
                    )
                    recalled = client.recall(
                        bank_id=BANK_ID,
                        query=f"Find prior incidents similar to this problem: {incident_query}",
                        budget="mid",
                        max_tokens=2500,
                    )
                    memories = memory_text(recalled)
                    answer = client.reflect(
                        bank_id=BANK_ID,
                        query=(
                            "Act as a senior Site Reliability Engineer and incident response assistant. "
                            "Analyze this incident. Use relevant historical memories from this bank when available. "
                            "Clearly separate evidence from hypotheses. Provide: (1) likely root cause, "
                            "(2) prioritized step-by-step diagnostic actions, (3) safe mitigation, "
                            "(4) verification steps, (5) prevention recommendation. "
                            "If historical incidents are relevant, explicitly say what was remembered and how it changes your recommendation. "
                            "Never claim a fix was executed. Ask for missing logs when needed.\n\n"
                            + incident_query
                        ),
                        context="Live incident triage. Be concise, actionable, and safety-conscious.",
                        budget="mid",
                    )
                    st.session_state.last_diagnosis = getattr(answer, "text", str(answer))
                    st.session_state.last_incident = {
                        "title": title, "service": service, "severity": severity,
                        "environment": environment, "error_code": error_code,
                        "impact": impact, "symptoms": symptoms,
                        "memories": memories, "timestamp": datetime.now().isoformat()
                    }
                    st.session_state.diagnosis_count += 1
                    client.close()
                st.success(f"Diagnosis ready. Hindsight returned {len(memories)} relevant memory item(s).")
            except Exception as e:
                st.error(f"Could not complete diagnosis: {e}")
                st.info("Check your Hindsight API key, bank access, and available cloud credits.")

    if st.session_state.last_diagnosis:
        st.divider()
        st.subheader("🧠 OpsMind diagnosis")
        if st.session_state.last_incident and st.session_state.last_incident["memories"]:
            st.success(f"Historical memory found: {len(st.session_state.last_incident['memories'])} related item(s)")
            with st.expander("View recalled incident memories", expanded=True):
                for item in st.session_state.last_incident["memories"]:
                    st.markdown(f"- {item}")
        else:
            st.info("No relevant historical incident was returned. This is the baseline diagnosis.")
        st.markdown(st.session_state.last_diagnosis)

        st.divider()
        st.subheader("Save the confirmed resolution")
        st.caption("Only save the actual fix after an engineer verifies it. This becomes reusable operational knowledge.")
        with st.form("resolution_form"):
            resolution = st.text_area("What fixed the incident?", height=100, placeholder="Example: Increased DB pool from 10 to 30 after confirming connection exhaustion...")
            root_cause = st.text_input("Confirmed root cause", placeholder="Database connection pool exhaustion")
            prevention = st.text_area("Preventive action (optional)", placeholder="Add pool saturation alert at 80%...")
            save = st.form_submit_button("💾 Save verified resolution to Hindsight", type="primary")
        if save:
            if not resolution.strip():
                st.warning("Enter the verified resolution before saving.")
            else:
                try:
                    client = get_client()
                    ensure_bank(client)
                    inc = st.session_state.last_incident
                    content = (
                        f"Resolved production incident | Date: {inc['timestamp']} | "
                        f"Title: {inc['title']} | Service: {inc['service']} | "
                        f"Severity: {inc['severity']} | Environment: {inc['environment']} | "
                        f"Error: {inc['error_code']} | Symptoms: {inc['symptoms']} | "
                        f"Confirmed root cause: {root_cause or 'Not specified'} | "
                        f"Verified resolution: {resolution} | Prevention: {prevention or 'Not specified'}"
                    )
                    client.retain(
                        bank_id=BANK_ID,
                        content=content,
                        context="Verified incident postmortem and resolution knowledge",
                        metadata={"service": inc["service"], "severity": inc["severity"], "source": "opsmind_ui"},
                    )
                    client.close()
                    st.success("Verified resolution saved to Hindsight. The agent can recall it during future incidents.")
                except Exception as e:
                    st.error(f"Could not save memory: {e}")

with tab2:
    st.subheader("Persistent incident memory")
    query = st.text_input("Search past operational knowledge", placeholder="e.g. database connection timeout")
    if st.button("Search Hindsight memory", type="primary"):
        try:
            client = get_client()
            ensure_bank(client)
            result = client.recall(bank_id=BANK_ID, query=query or "recent production incidents and their verified resolutions", budget="mid", max_tokens=4000)
            hits = memory_text(result)
            client.close()
            if hits:
                for i, hit in enumerate(hits, 1):
                    with st.container(border=True):
                        st.markdown(f"**Memory {i}**")
                        st.write(hit)
            else:
                st.info("No matching memories found yet. Diagnose and save a verified resolution first.")
        except Exception as e:
            st.error(f"Memory search failed: {e}")

with tab3:
    st.subheader("Seed a realistic incident for the live demo")
    st.write("Add a verified example to the memory bank so judges can immediately see how the agent learns.")
    if st.button("🌱 Seed database connection incident", type="primary"):
        try:
            client = get_client()
            ensure_bank(client)
            client.retain(
                bank_id=BANK_ID,
                content=(
                    "Resolved incident | Service: Order API | Environment: Production | Severity: High | "
                    "Symptoms: API requests returned 500 errors; logs showed 'too many connections' and "
                    "connection acquisition timeout. Confirmed root cause: database connection pool max size "
                    "was 10 and all connections were exhausted during a traffic spike. Verified resolution: "
                    "increased pool max size to 30 after checking database capacity, restarted affected API "
                    "workers gradually, and confirmed error rate returned to baseline. Prevention: alert when "
                    "pool utilization exceeds 80%, review connection leaks, and load-test peak traffic."
                ),
                context="Verified postmortem from a previous production incident",
                metadata={"service": "Order API", "severity": "High", "source": "demo_seed"},
            )
            client.close()
            st.success("Demo incident stored. Now diagnose a similar database connection issue to demonstrate memory recall.")
        except Exception as e:
            st.error(f"Could not seed demo memory: {e}")

st.divider()
st.markdown('<p class="small-muted">OpsMind AI · Hack with Hyderabad 3.0 · Prototype. Recommendations are advisory; engineers must verify changes before applying them.</p>', unsafe_allow_html=True)
