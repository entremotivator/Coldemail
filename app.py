import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json

# -------------------- CONFIGURATION --------------------
st.set_page_config(
    page_title="Advanced Cold Sales CRM", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .status-new { color: #ff6b6b; }
    .status-contacted { color: #4ecdc4; }
    .status-qualified { color: #45b7d1; }
    .status-proposal { color: #96ceb4; }
    .status-won { color: #77dd77; }
    .priority-high { background-color: #ffebee; }
    .priority-medium { background-color: #fff3e0; }
    .priority-low { background-color: #e8f5e8; }
</style>
""", unsafe_allow_html=True)

# -------------------- DEMO DATA --------------------
@st.cache_data
def load_demo_data():
    now = datetime.now()
    
    demo_data = [
        {
            "Prospect ID": 1,
            "Name": "Jane Smith",
            "Title / Role": "CTO",
            "Company": "TechNova",
            "Industry": "Technology",
            "Company Size": "Mid",
            "Location": "San Francisco, CA",
            "Email": "jane@technova.com",
            "Phone": "555-123-4567",
            "LinkedIn URL": "https://linkedin.com/in/janesmith",
            "Source": "LinkedIn",
            "Date Added": (now - timedelta(days=10)).strftime("%Y-%m-%d"),
            "Lead Status": "New",
            "Owner": "Rep A",
            "Pain Point(s)": "Wants to automate reporting processes and reduce manual data entry",
            "Solution Interest": "AI Analytics",
            "Priority": "High",
            "Email 1 Date": "",
            "Email 1 Status": "",
            "Email 2 Date": "",
            "Email 2 Status": "",
            "Email 3 Date": "",
            "Email 3 Status": "",
            "Call / Demo Date": "",
            "Deal Stage": "Prospecting",
            "Deal Value": "",
            "Notes": "High potential lead - expanding team, budget approved for Q4",
            "Opened Emails": 0,
            "Replies": 0,
            "Last Contact": "",
            "Next Follow Up": (now + timedelta(days=2)).strftime("%Y-%m-%d"),
            "Lead Score": 85,
            "Website": "https://technova.com",
            "Employee Count": "250",
            "Revenue": "$50M",
            "Budget": "$100K-$500K"
        },
        {
            "Prospect ID": 2,
            "Name": "Mark Taylor",
            "Title / Role": "Head of Marketing",
            "Company": "RetailPro",
            "Industry": "Retail",
            "Company Size": "Enterprise",
            "Location": "New York, NY",
            "Email": "mark@retailpro.com",
            "Phone": "555-987-6543",
            "LinkedIn URL": "https://linkedin.com/in/marktaylor",
            "Source": "Trade Show",
            "Date Added": (now - timedelta(days=20)).strftime("%Y-%m-%d"),
            "Lead Status": "Contacted",
            "Owner": "Rep B",
            "Pain Point(s)": "Needs AI for personalized customer engagement and inventory optimization",
            "Solution Interest": "AI Chatbots + Predictive Analytics",
            "Priority": "High",
            "Email 1 Date": (now - timedelta(days=18)).strftime("%Y-%m-%d"),
            "Email 1 Status": "Sent",
            "Email 2 Date": (now - timedelta(days=14)).strftime("%Y-%m-%d"),
            "Email 2 Status": "Opened",
            "Email 3 Date": "",
            "Email 3 Status": "",
            "Call / Demo Date": (now + timedelta(days=2)).strftime("%Y-%m-%d"),
            "Deal Stage": "Meeting Scheduled",
            "Deal Value": "$75,000",
            "Notes": "Very interested in demo, mentioned budget constraints but willing to explore ROI",
            "Opened Emails": 2,
            "Replies": 0,
            "Last Contact": (now - timedelta(days=14)).strftime("%Y-%m-%d"),
            "Next Follow Up": (now + timedelta(days=2)).strftime("%Y-%m-%d"),
            "Lead Score": 92,
            "Website": "https://retailpro.com",
            "Employee Count": "1200",
            "Revenue": "$500M",
            "Budget": "$50K-$200K"
        },
        {
            "Prospect ID": 3,
            "Name": "Sofia Martinez",
            "Title / Role": "Operations Manager",
            "Company": "HealthWorks",
            "Industry": "Healthcare",
            "Company Size": "Small",
            "Location": "Austin, TX",
            "Email": "sofia@healthworks.com",
            "Phone": "555-222-3333",
            "LinkedIn URL": "https://linkedin.com/in/sofiam",
            "Source": "Outbound List",
            "Date Added": (now - timedelta(days=35)).strftime("%Y-%m-%d"),
            "Lead Status": "Qualified",
            "Owner": "Rep A",
            "Pain Point(s)": "Reduce administrative overhead and improve patient data management",
            "Solution Interest": "RPA + AI Document Processing",
            "Priority": "Medium",
            "Email 1 Date": (now - timedelta(days=30)).strftime("%Y-%m-%d"),
            "Email 1 Status": "Opened",
            "Email 2 Date": (now - timedelta(days=27)).strftime("%Y-%m-%d"),
            "Email 2 Status": "Opened",
            "Email 3 Date": (now - timedelta(days=22)).strftime("%Y-%m-%d"),
            "Email 3 Status": "Replied",
            "Call / Demo Date": (now - timedelta(days=20)).strftime("%Y-%m-%d"),
            "Deal Stage": "Proposal Sent",
            "Deal Value": "$25,000",
            "Notes": "Positive response, evaluating budget. Decision maker identified as Dr. Wilson (CEO)",
            "Opened Emails": 3,
            "Replies": 1,
            "Last Contact": (now - timedelta(days=20)).strftime("%Y-%m-%d"),
            "Next Follow Up": (now + timedelta(days=3)).strftime("%Y-%m-%d"),
            "Lead Score": 78,
            "Website": "https://healthworks.com",
            "Employee Count": "45",
            "Revenue": "$8M",
            "Budget": "$10K-$50K"
        },
        {
            "Prospect ID": 4,
            "Name": "David Chen",
            "Title / Role": "VP of Engineering",
            "Company": "DataFlow Systems",
            "Industry": "Software",
            "Company Size": "Mid",
            "Location": "Seattle, WA",
            "Email": "dchen@dataflow.com",
            "Phone": "555-444-5555",
            "LinkedIn URL": "https://linkedin.com/in/davidchen",
            "Source": "Referral",
            "Date Added": (now - timedelta(days=5)).strftime("%Y-%m-%d"),
            "Lead Status": "New",
            "Owner": "Rep C",
            "Pain Point(s)": "Scaling data processing and reducing infrastructure costs",
            "Solution Interest": "AI-Powered Data Pipeline",
            "Priority": "High",
            "Email 1 Date": "",
            "Email 1 Status": "",
            "Email 2 Date": "",
            "Email 2 Status": "",
            "Email 3 Date": "",
            "Email 3 Status": "",
            "Call / Demo Date": "",
            "Deal Stage": "Prospecting",
            "Deal Value": "",
            "Notes": "Warm referral from existing client. Very technical background",
            "Opened Emails": 0,
            "Replies": 0,
            "Last Contact": "",
            "Next Follow Up": (now + timedelta(days=1)).strftime("%Y-%m-%d"),
            "Lead Score": 90,
            "Website": "https://dataflow.com",
            "Employee Count": "180",
            "Revenue": "$25M",
            "Budget": "$200K+"
        },
        {
            "Prospect ID": 5,
            "Name": "Emma Johnson",
            "Title / Role": "Chief Innovation Officer",
            "Company": "GreenTech Solutions",
            "Industry": "Clean Energy",
            "Company Size": "Enterprise",
            "Location": "Denver, CO",
            "Email": "emma@greentech.com",
            "Phone": "555-777-8888",
            "LinkedIn URL": "https://linkedin.com/in/emmajohnson",
            "Source": "Webinar",
            "Date Added": (now - timedelta(days=15)).strftime("%Y-%m-%d"),
            "Lead Status": "Contacted",
            "Owner": "Rep B",
            "Pain Point(s)": "Optimize energy distribution and predict maintenance needs",
            "Solution Interest": "Predictive AI + IoT Integration",
            "Priority": "Medium",
            "Email 1 Date": (now - timedelta(days=12)).strftime("%Y-%m-%d"),
            "Email 1 Status": "Opened",
            "Email 2 Date": (now - timedelta(days=8)).strftime("%Y-%m-%d"),
            "Email 2 Status": "Clicked",
            "Email 3 Date": "",
            "Email 3 Status": "",
            "Call / Demo Date": "",
            "Deal Stage": "Prospecting",
            "Deal Value": "$150,000",
            "Notes": "Attended our webinar, downloaded whitepaper. Engaged but cautious about timeline",
            "Opened Emails": 2,
            "Replies": 0,
            "Last Contact": (now - timedelta(days=8)).strftime("%Y-%m-%d"),
            "Next Follow Up": (now + timedelta(days=1)).strftime("%Y-%m-%d"),
            "Lead Score": 72,
            "Website": "https://greentech.com",
            "Employee Count": "800",
            "Revenue": "$200M",
            "Budget": "$100K-$300K"
        },
        {
            "Prospect ID": 6,
            "Name": "Michael Brown",
            "Title / Role": "Director of Operations",
            "Company": "LogiCorp",
            "Industry": "Logistics",
            "Company Size": "Enterprise",
            "Location": "Chicago, IL",
            "Email": "mbrown@logicorp.com",
            "Phone": "555-333-2222",
            "LinkedIn URL": "https://linkedin.com/in/michaelbrown",
            "Source": "Cold Email",
            "Date Added": (now - timedelta(days=45)).strftime("%Y-%m-%d"),
            "Lead Status": "Qualified",
            "Owner": "Rep A",
            "Pain Point(s)": "Route optimization and warehouse automation challenges",
            "Solution Interest": "AI Route Optimization",
            "Priority": "High",
            "Email 1 Date": (now - timedelta(days=42)).strftime("%Y-%m-%d"),
            "Email 1 Status": "Opened",
            "Email 2 Date": (now - timedelta(days=38)).strftime("%Y-%m-%d"),
            "Email 2 Status": "Replied",
            "Email 3 Date": (now - timedelta(days=32)).strftime("%Y-%m-%d"),
            "Email 3 Status": "Opened",
            "Call / Demo Date": (now - timedelta(days=28)).strftime("%Y-%m-%d"),
            "Deal Stage": "Negotiation",
            "Deal Value": "$200,000",
            "Notes": "In final negotiations. Comparing with competitors. Price sensitive but sees value",
            "Opened Emails": 3,
            "Replies": 2,
            "Last Contact": (now - timedelta(days=5)).strftime("%Y-%m-%d"),
            "Next Follow Up": (now + timedelta(days=2)).strftime("%Y-%m-%d"),
            "Lead Score": 88,
            "Website": "https://logicorp.com",
            "Employee Count": "2500",
            "Revenue": "$1.2B",
            "Budget": "$500K+"
        }
    ]
    
    return pd.DataFrame(demo_data)

# Initialize session state
if 'df' not in st.session_state:
    st.session_state.df = load_demo_data()

df = st.session_state.df

# -------------------- HELPER FUNCTIONS --------------------

def compute_advanced_metrics(df):
    total = len(df)
    contacted = len(df[df["Lead Status"] != "New"])
    meetings = len(df[df["Deal Stage"] == "Meeting Scheduled"])
    proposals = len(df[df["Deal Stage"] == "Proposal Sent"])
    negotiations = len(df[df["Deal Stage"] == "Negotiation"])
    closed_won = len(df[df["Deal Stage"] == "Closed Won"])
    closed_lost = len(df[df["Deal Stage"] == "Closed Lost"])

    # Email metrics
    total_emails_sent = df[["Email 1 Status", "Email 2 Status", "Email 3 Status"]].apply(
        lambda col: col.isin(["Sent", "Opened", "Clicked", "Replied"]).sum()
    ).sum()
    total_opened = df["Opened Emails"].sum()
    total_replies = df["Replies"].sum()
    
    open_rate = (total_opened / total_emails_sent) * 100 if total_emails_sent > 0 else 0
    reply_rate = (total_replies / total_emails_sent) * 100 if total_emails_sent > 0 else 0

    # Conversion rates
    contact_to_meeting = (meetings / contacted) * 100 if contacted > 0 else 0
    meeting_to_proposal = (proposals / meetings) * 100 if meetings > 0 else 0
    proposal_to_close = (closed_won / proposals) * 100 if proposals > 0 else 0

    # Deal value calculations
    def parse_value(x):
        try:
            return float(str(x).replace("$", "").replace(",", "").replace("K", "000").replace("M", "000000"))
        except:
            return np.nan

    deal_values = df["Deal Value"].apply(parse_value)
    avg_deal = deal_values.mean()
    total_pipeline = deal_values.sum()
    
    # Lead scoring
    avg_lead_score = df["Lead Score"].mean()

    return {
        "total": total,
        "contacted": contacted,
        "meetings": meetings,
        "proposals": proposals,
        "negotiations": negotiations,
        "closed_won": closed_won,
        "closed_lost": closed_lost,
        "total_emails_sent": int(total_emails_sent),
        "total_opened": int(total_opened),
        "total_replies": int(total_replies),
        "open_rate": round(open_rate, 1),
        "reply_rate": round(reply_rate, 1),
        "contact_to_meeting": round(contact_to_meeting, 1),
        "meeting_to_proposal": round(meeting_to_proposal, 1),
        "proposal_to_close": round(proposal_to_close, 1),
        "avg_deal": round(avg_deal, 2) if not np.isnan(avg_deal) else 0,
        "total_pipeline": round(total_pipeline, 2) if not np.isnan(total_pipeline) else 0,
        "avg_lead_score": round(avg_lead_score, 1)
    }

def get_color_for_status(status):
    colors = {
        "New": "#ff6b6b",
        "Contacted": "#4ecdc4", 
        "Opened": "#45b7d1",
        "Replied": "#96ceb4",
        "Qualified": "#77dd77",
        "Not Interested": "#ff9999"
    }
    return colors.get(status, "#cccccc")

def create_pipeline_funnel(df):
    stages = ["Prospecting", "Meeting Scheduled", "Proposal Sent", "Negotiation", "Closed Won"]
    counts = []
    
    for stage in stages:
        count = len(df[df["Deal Stage"] == stage])
        counts.append(count)
    
    fig = go.Figure(go.Funnel(
        y=stages,
        x=counts,
        textinfo="value+percent initial",
        marker=dict(color=["#ff6b6b", "#ffa726", "#42a5f5", "#66bb6a", "#4caf50"])
    ))
    
    fig.update_layout(
        title="Sales Pipeline Funnel",
        height=400,
        font=dict(size=12)
    )
    
    return fig

def create_lead_score_distribution(df):
    fig = px.histogram(
        df, 
        x="Lead Score", 
        nbins=20,
        title="Lead Score Distribution",
        color_discrete_sequence=["#1f77b4"]
    )
    fig.update_layout(height=400)
    return fig

def create_revenue_by_industry(df):
    def parse_value(x):
        try:
            return float(str(x).replace("$", "").replace(",", "").replace("K", "000").replace("M", "000000"))
        except:
            return 0
    
    df_temp = df.copy()
    df_temp["Deal Value Numeric"] = df_temp["Deal Value"].apply(parse_value)
    
    industry_revenue = df_temp.groupby("Industry")["Deal Value Numeric"].sum().reset_index()
    
    fig = px.bar(
        industry_revenue,
        x="Industry",
        y="Deal Value Numeric",
        title="Pipeline Value by Industry",
        color_discrete_sequence=["#2E86AB"]
    )
    fig.update_layout(height=400)
    return fig

# -------------------- SIDEBAR --------------------
st.sidebar.title("🎯 Sales CRM")
st.sidebar.markdown("---")

pages = [
    "🏠 Dashboard", 
    "👥 Prospects", 
    "✉️ Email Campaigns", 
    "📅 Calendar & Tasks", 
    "📊 Analytics", 
    "⚙️ Settings"
]
choice = st.sidebar.selectbox("Navigation", pages)

# Quick stats in sidebar
metrics = compute_advanced_metrics(df)
st.sidebar.markdown("### Quick Stats")
st.sidebar.metric("Total Prospects", metrics["total"])
st.sidebar.metric("Active Deals", metrics["proposals"] + metrics["negotiations"])
st.sidebar.metric("Pipeline Value", f"${metrics['total_pipeline']:,.0f}")

# -------------------- DASHBOARD --------------------
if choice == "🏠 Dashboard":
    st.title("📊 Sales Dashboard")
    st.markdown("*Real-time overview of your sales pipeline and performance*")

    # Key Metrics Row
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric(
            "Total Prospects", 
            metrics["total"],
            delta=f"+{metrics['total'] - 5}" if metrics['total'] > 5 else None
        )
    
    with col2:
        st.metric(
            "Contacted", 
            metrics["contacted"],
            delta=f"{round((metrics['contacted']/metrics['total'])*100, 1)}%" if metrics['total'] > 0 else "0%"
        )
    
    with col3:
        st.metric(
            "Email Open Rate", 
            f"{metrics['open_rate']}%",
            delta="2.3%" if metrics['open_rate'] > 50 else "-1.2%"
        )
    
    with col4:
        st.metric(
            "Reply Rate", 
            f"{metrics['reply_rate']}%",
            delta="0.8%" if metrics['reply_rate'] > 10 else "-0.5%"
        )
    
    with col5:
        st.metric(
            "Avg Lead Score", 
            f"{metrics['avg_lead_score']}/100",
            delta="3.2" if metrics['avg_lead_score'] > 80 else "-1.1"
        )

    st.markdown("---")

    # Charts Row
    col1, col2 = st.columns(2)
    
    with col1:
        st.plotly_chart(create_pipeline_funnel(df), use_container_width=True)
    
    with col2:
        st.plotly_chart(create_lead_score_distribution(df), use_container_width=True)

    # Performance Overview
    st.markdown("---")
    st.subheader("📈 Performance Overview")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Contact → Meeting", f"{metrics['contact_to_meeting']}%")
        st.metric("Total Pipeline", f"${metrics['total_pipeline']:,.0f}")
    
    with col2:
        st.metric("Meeting → Proposal", f"{metrics['meeting_to_proposal']}%")
        st.metric("Avg Deal Size", f"${metrics['avg_deal']:,.0f}")
    
    with col3:
        st.metric("Proposal → Close", f"{metrics['proposal_to_close']}%")
        st.metric("Active Negotiations", metrics['negotiations'])

    # Recent Activity
    st.markdown("---")
    st.subheader("🔥 Hot Prospects (Score > 85)")
    hot_prospects = df[df["Lead Score"] > 85].sort_values("Lead Score", ascending=False)
    
    if not hot_prospects.empty:
        for _, prospect in hot_prospects.iterrows():
            with st.container():
                col1, col2, col3, col4 = st.columns([3, 2, 2, 2])
                col1.write(f"**{prospect['Name']}** - {prospect['Company']}")
                col2.write(f"Score: {prospect['Lead Score']}")
                col3.write(f"Stage: {prospect['Deal Stage']}")
                col4.write(f"Value: {prospect['Deal Value'] or 'TBD'}")
    else:
        st.info("No high-scoring prospects yet. Focus on lead qualification!")

    # Upcoming Tasks
    st.markdown("---")
    st.subheader("📋 Upcoming Follow-ups")
    
    today = datetime.now().date()
    upcoming = df[df["Next Follow Up"] != ""]
    upcoming["Next Follow Up Date"] = pd.to_datetime(upcoming["Next Follow Up"]).dt.date
    upcoming = upcoming[upcoming["Next Follow Up Date"] >= today].sort_values("Next Follow Up Date")
    
    if not upcoming.empty:
        for _, task in upcoming.head(5).iterrows():
            days_until = (task["Next Follow Up Date"] - today).days
            urgency = "🔴" if days_until <= 1 else "🟡" if days_until <= 3 else "🟢"
            st.write(f"{urgency} **{task['Name']}** ({task['Company']}) - {task['Next Follow Up Date']} ({days_until} days)")
    else:
        st.info("No upcoming follow-ups scheduled.")

# -------------------- PROSPECTS --------------------
elif choice == "👥 Prospects":
    st.title("👥 Prospect Management")
    
    tab1, tab2, tab3 = st.tabs(["🔍 Browse & Filter", "➕ Add New", "✏️ Bulk Edit"])
    
    with tab1:
        st.subheader("Filter & Search Prospects")
        
        # Filters
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            status_filter = st.multiselect(
                "Lead Status", 
                df["Lead Status"].unique(),
                default=df["Lead Status"].unique()
            )
        
        with col2:
            industry_filter = st.multiselect(
                "Industry",
                df["Industry"].unique(),
                default=df["Industry"].unique()
            )
        
        with col3:
            owner_filter = st.multiselect(
                "Owner",
                df["Owner"].unique(),
                default=df["Owner"].unique()
            )
        
        with col4:
            priority_filter = st.multiselect(
                "Priority",
                df["Priority"].unique(),
                default=df["Priority"].unique()
            )

        # Apply filters
        filtered_df = df[
            (df["Lead Status"].isin(status_filter)) &
            (df["Industry"].isin(industry_filter)) &
            (df["Owner"].isin(owner_filter)) &
            (df["Priority"].isin(priority_filter))
        ]

        # Search functionality
        search_term = st.text_input("🔍 Search by name, company, or email:")
        if search_term:
            mask = (
                filtered_df["Name"].str.contains(search_term, case=False, na=False) |
                filtered_df["Company"].str.contains(search_term, case=False, na=False) |
                filtered_df["Email"].str.contains(search_term, case=False, na=False)
            )
            filtered_df = filtered_df[mask]

        st.write(f"Showing {len(filtered_df)} of {len(df)} prospects")

        # Display prospects with enhanced formatting
        display_cols = [
            "Prospect ID", "Name", "Company", "Title / Role", "Industry", 
            "Lead Status", "Deal Stage", "Lead Score", "Deal Value", "Next Follow Up"
        ]
        
        # Color coding for status
        styled_df = filtered_df[display_cols].copy()
        st.dataframe(
            styled_df,
            use_container_width=True,
            height=400
        )

        # Quick actions
        if not filtered_df.empty:
            st.markdown("### Quick Actions")
            col1, col2 = st.columns(2)
            
            with col1:
                selected_id = st.selectbox("Select Prospect", filtered_df["Prospect ID"].tolist())
                action = st.selectbox("Action", ["Update Status", "Schedule Follow-up", "Add Note"])
                
                if action == "Update Status":
                    new_status = st.selectbox("New Status", ["New", "Contacted", "Opened", "Replied", "Qualified", "Not Interested"])
                    if st.button("Update Status"):
                        idx = df[df["Prospect ID"] == selected_id].index[0]
                        st.session_state.df.at[idx, "Lead Status"] = new_status
                        st.success("Status updated!")
                        st.experimental_rerun()

            with col2:
                if action == "Schedule Follow-up":
                    follow_up_date = st.date_input("Follow-up Date", datetime.now() + timedelta(days=3))
                    if st.button("Schedule"):
                        idx = df[df["Prospect ID"] == selected_id].index[0]
                        st.session_state.df.at[idx, "Next Follow Up"] = follow_up_date.strftime("%Y-%m-%d")
                        st.success("Follow-up scheduled!")
                        st.experimental_rerun()
                
                elif action == "Add Note":
                    new_note = st.text_area("Add Note")
                    if st.button("Add Note") and new_note:
                        idx = df[df["Prospect ID"] == selected_id].index[0]
                        current_notes = st.session_state.df.at[idx, "Notes"]
                        updated_notes = f"{current_notes}\n[{datetime.now().strftime('%Y-%m-%d')}] {new_note}" if current_notes else f"[{datetime.now().strftime('%Y-%m-%d')}] {new_note}"
                        st.session_state.df.at[idx, "Notes"] = updated_notes
                        st.success("Note added!")
                        st.experimental_rerun()

    with tab2:
        st.subheader("Add New Prospect")
        
        with st.form("comprehensive_add_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Basic Information**")
                new_name = st.text_input("Full Name *", placeholder="John Doe")
                new_title = st.text_input("Title / Role *", placeholder="VP of Sales")
                new_company = st.text_input("Company *", placeholder="ABC Corp")
                new_industry = st.selectbox("Industry", ["Technology", "Healthcare", "Retail", "Manufacturing", "Finance", "Education", "Other"])
                new_size = st.selectbox("Company Size", ["Small (1-50)", "Mid (51-500)", "Enterprise (500+)"])
                new_location = st.text_input("Location", placeholder="City, State")
                
                st.markdown("**Contact Details**")
                new_email = st.text_input("Email *", placeholder="john@company.com")
                new_phone = st.text_input("Phone", placeholder="555-123-4567")
                new_linkedin = st.text_input("LinkedIn URL", placeholder="https://linkedin.com/in/johndoe")
                new_website = st.text_input("Company Website", placeholder="https://company.com")
            
            with col2:
                st.markdown("**Sales Information**")
                new_source = st.selectbox("Lead Source", ["LinkedIn", "Cold Email", "Referral", "Trade Show", "Webinar", "Website", "Other"])
                new_owner = st.selectbox("Owner", ["Rep A", "Rep B", "Rep C", "Rep D"])
                new_priority = st.selectbox("Priority", ["High", "Medium", "Low"])
                new_lead_score = st.slider("Lead Score", 0, 100, 50)
                
                st.markdown("**Business Context**")
                new_pain_points = st.text_area("Pain Points", placeholder="What challenges are they facing?")
                new_solution_interest = st.text_input("Solution Interest", placeholder="Which solutions interest them?")
                new_budget = st.selectbox("Budget Range", ["$10K-$50K", "$50K-$100K", "$100K-$300K", "$300K-$500K", "$500K+", "Unknown"])
                new_employee_count = st.text_input("Employee Count", placeholder="150")
                new_revenue = st.text_input("Company Revenue", placeholder="$50M")
                
                st.markdown("**Additional Notes**")
                new_notes = st.text_area("Notes", placeholder="Any additional context or observations")
            
            submitted = st.form_submit_button("Add Prospect", type="primary")
            
            if submitted:
                if new_name and new_company and new_email:
                    new_prospect = {
                        "Prospect ID": int(df["Prospect ID"].max() + 1) if not df.empty else 1,
                        "Name": new_name,
                        "Title / Role": new_title,
                        "Company": new_company,
                        "Industry": new_industry,
                        "Company Size": new_size.split(" ")[0],
                        "Location": new_location,
                        "Email": new_email,
                        "Phone": new_phone,
                        "LinkedIn URL": new_linkedin,
                        "Source": new_source,
                        "Date Added": datetime.now().strftime("%Y-%m-%d"),
                        "Lead Status": "New",
                        "Owner": new_owner,
                        "Pain Point(s)": new_pain_points,
                        "Solution Interest": new_solution_interest,
                        "Priority": new_priority,
                        "Email 1 Date": "",
                        "Email 1 Status": "",
                        "Email 2 Date": "",
                        "Email 2 Status": "",
                        "Email 3 Date": "",
                        "Email 3 Status": "",
                        "Call / Demo Date": "",
                        "Deal Stage": "Prospecting",
                        "Deal Value": "",
                        "Notes": new_notes,
                        "Opened Emails": 0,
                        "Replies": 0,
                        "Last Contact": "",
                        "Next Follow Up": (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d"),
                        "Lead Score": new_lead_score,
                        "Website": new_website,
                        "Employee Count": new_employee_count,
                        "Revenue": new_revenue,
                        "Budget": new_budget
                    }
                    
                    st.session_state.df = pd.concat([st.session_state.df, pd.DataFrame([new_prospect])], ignore_index=True)
                    st.success(f"✅ Added {new_name} from {new_company}!")
                    st.experimental_rerun()
                else:
                    st.error("Please fill in required fields: Name, Company, and Email")

    with tab3:
        st.subheader("Bulk Operations")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Bulk Status Update**")
            selected_prospects = st.multiselect(
                "Select Prospects", 
                df["Prospect ID"].tolist(),
                format_func=lambda x: f"{x} - {df[df['Prospect ID']==x]['Name'].iloc[0]} ({df[df['Prospect ID']==x]['Company'].iloc[0]})"
            )
            bulk_status = st.selectbox("New Status", ["New", "Contacted", "Opened", "Replied", "Qualified", "Not Interested"])
            
            if st.button("Update Selected") and selected_prospects:
                for prospect_id in selected_prospects:
                    idx = df[df["Prospect ID"] == prospect_id].index[0]
                    st.session_state.df.at[idx, "Lead Status"] = bulk_status
                st.success(f"Updated {len(selected_prospects)} prospects!")
                st.experimental_rerun()
        
        with col2:
            st.markdown("**Import from CSV**")
            uploaded_file = st.file_uploader("Upload CSV file", type=['csv'])
            if uploaded_file is not None:
                try:
                    new_df = pd.read_csv(uploaded_file)
                    st.write("Preview:")
                    st.dataframe(new_df.head())
                    
                    if st.button("Import Data"):
                        # Add IDs and merge
                        max_id = st.session_state.df["Prospect ID"].max()
                        new_df["Prospect ID"] = range(max_id + 1, max_id + 1 + len(new_df))
                        st.session_state.df = pd.concat([st.session_state.df, new_df], ignore_index=True)
                        st.success(f"Imported {len(new_df)} prospects!")
                        st.experimental_rerun()
                except Exception as e:
                    st.error(f"Error importing file: {e}")

# -------------------- EMAIL CAMPAIGNS --------------------
elif choice == "✉️ Email Campaigns":
    st.title("✉️ Email Campaign Management")
    
    tab1, tab2, tab3, tab4 = st.tabs(["📝 Templates", "📤 Send Campaigns", "📊 Performance", "🔄 Sequences"])
    
    with tab1:
        st.subheader("Email Templates")
        
        # Email template library
        templates = {
            "Initial Outreach": {
                "subject": "Quick question about [Company Name]'s [pain point]",
                "body": """Hi [First Name],

I noticed [Company Name] is [relevant observation about their business]. 

Many companies in [industry] are facing similar challenges with [specific pain point]. We've helped businesses like yours [specific benefit/result].

Would you be open to a brief conversation about how we could help [Company Name] achieve similar results?

Best regards,
[Your Name]
[Your Title]
[Company]"""
            },
            "Follow-up": {
                "subject": "Following up on [Company Name] + [Your Company]",
                "body": """Hi [First Name],

I wanted to follow up on my previous email about helping [Company Name] with [pain point].

I came across this case study of how [similar company] achieved [specific result] using our solution: [link or brief description]

Would you like to see how this could apply to [Company Name]?

Best,
[Your Name]"""
            },
            "Value Proposition": {
                "subject": "How [Competitor/Similar Company] reduced costs by 30%",
                "body": """Hi [First Name],

I thought you'd find this interesting:

[Similar Company] recently implemented our AI solution and saw:
• 30% reduction in operational costs
• 50% faster processing times  
• 90% accuracy improvement

Given [Company Name]'s focus on [relevant area], I believe we could deliver similar results for you.

Would you like a 15-minute call to explore this?

Best regards,
[Your Name]"""
            },
            "Final Attempt": {
                "subject": "Should I close your file?",
                "body": """Hi [First Name],

I've reached out a few times about helping [Company Name] with [pain point], but haven't heard back.

Should I assume this isn't a priority right now and close your file?

If the timing isn't right, just let me know when might be better to reconnect.

Best,
[Your Name]"""
            }
        }
        
        selected_template = st.selectbox("Choose Template", list(templates.keys()))
        template = templates[selected_template]
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.text_input("Subject Line", value=template["subject"], key="subject_edit")
        
        with col2:
            st.selectbox("Template Category", ["Outreach", "Follow-up", "Nurture", "Re-engagement"])
        
        edited_body = st.text_area("Email Body", value=template["body"], height=300)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("Save Template"):
                st.success("Template saved!")
        with col2:
            if st.button("Preview"):
                st.info("Preview functionality would show personalized version")
        with col3:
            if st.button("Test Send"):
                st.info("Test email would be sent to your email")

    with tab2:
        st.subheader("Send Email Campaigns")
        
        # Campaign setup
        campaign_name = st.text_input("Campaign Name", placeholder="Q4 Outreach - Technology Prospects")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Target selection
            st.markdown("**Target Audience**")
            target_status = st.multiselect("Target Lead Status", df["Lead Status"].unique(), default=["New"])
            target_industry = st.multiselect("Target Industry", df["Industry"].unique())
            target_priority = st.multiselect("Target Priority", df["Priority"].unique())
            
            # Filter targets
            targets = df[
                (df["Lead Status"].isin(target_status)) &
                (df["Industry"].isin(target_industry) if target_industry else df["Industry"].notna()) &
                (df["Priority"].isin(target_priority) if target_priority else df["Priority"].notna())
            ]
            
            st.write(f"**Targets: {len(targets)} prospects**")
            if not targets.empty:
                st.dataframe(targets[["Name", "Company", "Industry", "Lead Status"]], height=200)
        
        with col2:
            st.markdown("**Campaign Settings**")
            email_template = st.selectbox("Email Template", list(templates.keys()))
            send_date = st.date_input("Send Date", datetime.now())
            send_time = st.time_input("Send Time", datetime.now().time())
            
            # Personalization options
            st.checkbox("Auto-personalize company name", value=True)
            st.checkbox("Auto-personalize industry", value=True)
            st.checkbox("Include pain points", value=True)
            
            if st.button("Launch Campaign", type="primary"):
                if not targets.empty:
                    # Simulate sending emails
                    for idx, prospect in targets.iterrows():
                        # Update first available email slot
                        df_idx = df[df["Prospect ID"] == prospect["Prospect ID"]].index[0]
                        if not st.session_state.df.at[df_idx, "Email 1 Date"]:
                            st.session_state.df.at[df_idx, "Email 1 Date"] = send_date.strftime("%Y-%m-%d")
                            st.session_state.df.at[df_idx, "Email 1 Status"] = "Sent"
                        elif not st.session_state.df.at[df_idx, "Email 2 Date"]:
                            st.session_state.df.at[df_idx, "Email 2 Date"] = send_date.strftime("%Y-%m-%d")
                            st.session_state.df.at[df_idx, "Email 2 Status"] = "Sent"
                        elif not st.session_state.df.at[df_idx, "Email 3 Date"]:
                            st.session_state.df.at[df_idx, "Email 3 Date"] = send_date.strftime("%Y-%m-%d")
                            st.session_state.df.at[df_idx, "Email 3 Status"] = "Sent"
                        
                        # Update lead status
                        if st.session_state.df.at[df_idx, "Lead Status"] == "New":
                            st.session_state.df.at[df_idx, "Lead Status"] = "Contacted"
                    
                    st.success(f"🚀 Campaign '{campaign_name}' launched to {len(targets)} prospects!")
                    st.experimental_rerun()
                else:
                    st.warning("No targets selected for campaign")

    with tab3:
        st.subheader("Email Performance Analytics")
        
        # Performance by template/campaign
        email_performance = []
        for _, row in df.iterrows():
            for i in range(1, 4):
                email_date = row.get(f"Email {i} Date", "")
                email_status = row.get(f"Email {i} Status", "")
                if email_date and email_status:
                    email_performance.append({
                        "Email": f"Email {i}",
                        "Date": email_date,
                        "Status": email_status,
                        "Prospect": row["Name"],
                        "Industry": row["Industry"]
                    })
        
        if email_performance:
            perf_df = pd.DataFrame(email_performance)
            
            # Email performance charts
            col1, col2 = st.columns(2)
            
            with col1:
                status_counts = perf_df["Status"].value_counts()
                fig = px.pie(values=status_counts.values, names=status_counts.index, title="Email Status Distribution")
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                industry_performance = perf_df.groupby("Industry")["Status"].apply(lambda x: (x == "Opened").sum()).reset_index()
                industry_performance.columns = ["Industry", "Opens"]
                fig = px.bar(industry_performance, x="Industry", y="Opens", title="Opens by Industry")
                st.plotly_chart(fig, use_container_width=True)
            
            # Detailed performance table
            st.markdown("**Email Performance Details**")
            st.dataframe(perf_df, use_container_width=True)
        else:
            st.info("No email activity to analyze yet. Send some campaigns first!")

    with tab4:
        st.subheader("Automated Email Sequences")
        
        st.markdown("""
        **Current Sequence Configuration:**
        - Email 1: Sent immediately upon prospect addition
        - Email 2: Sent 3 days after Email 1 (if no reply)
        - Email 3: Sent 7 days after Email 2 (if no reply)
        """)
        
        # Sequence management
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Active Sequences**")
            active_sequences = df[
                (df["Email 1 Status"].isin(["Sent", "Opened"])) & 
                (df["Email 3 Status"] == "")
            ]
            
            if not active_sequences.empty:
                for _, seq in active_sequences.iterrows():
                    with st.container():
                        st.write(f"**{seq['Name']}** ({seq['Company']})")
                        st.write(f"Status: {seq['Lead Status']} | Next: Email {2 if not seq['Email 2 Date'] else 3}")
                        if st.button(f"Pause Sequence", key=f"pause_{seq['Prospect ID']}"):
                            st.info(f"Sequence paused for {seq['Name']}")
            else:
                st.info("No active sequences")
        
        with col2:
            st.markdown("**Sequence Settings**")
            seq_delay_1_2 = st.number_input("Days between Email 1 → 2", value=3, min_value=1, max_value=14)
            seq_delay_2_3 = st.number_input("Days between Email 2 → 3", value=7, min_value=1, max_value=21)
            
            auto_pause_on_reply = st.checkbox("Auto-pause on reply", value=True)
            auto_pause_on_meeting = st.checkbox("Auto-pause when meeting scheduled", value=True)
            
            if st.button("Save Sequence Settings"):
                st.success("Sequence settings updated!")

# -------------------- CALENDAR & TASKS --------------------
elif choice == "📅 Calendar & Tasks":
    st.title("📅 Calendar & Task Management")
    
    tab1, tab2, tab3 = st.tabs(["📅 Calendar View", "✅ Tasks", "🔔 Reminders"])
    
    with tab1:
        st.subheader("Sales Calendar")
        
        # Date range selector
        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input("Start Date", datetime.now() - timedelta(days=30))
        with col2:
            end_date = st.date_input("End Date", datetime.now() + timedelta(days=30))
        
        # Build comprehensive calendar events
        events = []
        for _, row in df.iterrows():
            # Email events
            for i, (col_label, event_type) in enumerate([
                ("Email 1 Date", "Email 1"), 
                ("Email 2 Date", "Email 2"), 
                ("Email 3 Date", "Email 3")
            ], 1):
                date_val = row.get(col_label, "")
                status = row.get(f"Email {i} Status", "")
                if date_val:
                    try:
                        date_parsed = pd.to_datetime(date_val).date()
                        if start_date <= date_parsed <= end_date:
                            events.append({
                                "Date": date_parsed,
                                "Type": event_type,
                                "Prospect": row["Name"],
                                "Company": row["Company"],
                                "Status": status,
                                "Priority": row["Priority"],
                                "Owner": row["Owner"]
                            })
                    except:
                        pass
            
            # Call/Demo events
            call_date = row.get("Call / Demo Date", "")
            if call_date:
                try:
                    date_parsed = pd.to_datetime(call_date).date()
                    if start_date <= date_parsed <= end_date:
                        events.append({
                            "Date": date_parsed,
                            "Type": "Call/Demo",
                            "Prospect": row["Name"],
                            "Company": row["Company"],
                            "Status": "Scheduled",
                            "Priority": row["Priority"],
                            "Owner": row["Owner"]
                        })
                except:
                    pass
            
            # Follow-up events
            followup_date = row.get("Next Follow Up", "")
            if followup_date:
                try:
                    date_parsed = pd.to_datetime(followup_date).date()
                    if start_date <= date_parsed <= end_date:
                        events.append({
                            "Date": date_parsed,
                            "Type": "Follow-up",
                            "Prospect": row["Name"],
                            "Company": row["Company"],
                            "Status": "Scheduled",
                            "Priority": row["Priority"],
                            "Owner": row["Owner"]
                        })
                except:
                    pass

        if events:
            events_df = pd.DataFrame(events).sort_values("Date")
            
            # Filter by owner
            owner_filter = st.multiselect("Filter by Owner", events_df["Owner"].unique(), default=events_df["Owner"].unique())
            filtered_events = events_df[events_df["Owner"].isin(owner_filter)]
            
            # Calendar view
            st.dataframe(
                filtered_events.style.apply(
                    lambda x: ['background-color: #ffebee' if x.Priority == 'High' 
                             else 'background-color: #fff3e0' if x.Priority == 'Medium'
                             else 'background-color: #e8f5e8' for i in x], 
                    axis=1
                ),
                use_container_width=True
            )
            
            # Today's events
            today_events = filtered_events[filtered_events["Date"] == datetime.now().date()]
            if not today_events.empty:
                st.markdown("### 🎯 Today's Activities")
                for _, event in today_events.iterrows():
                    priority_icon = "🔴" if event["Priority"] == "High" else "🟡" if event["Priority"] == "Medium" else "🟢"
                    st.write(f"{priority_icon} **{event['Type']}** with {event['Prospect']} ({event['Company']}) - {event['Owner']}")
        else:
            st.info("No events in selected date range.")

    with tab2:
        st.subheader("Task Management")
        
        # Create tasks from prospect data
        tasks = []
        today = datetime.now().date()
        
        for _, row in df.iterrows():
            # Overdue follow-ups
            next_followup = row.get("Next Follow Up", "")
            if next_followup:
                try:
                    followup_date = pd.to_datetime(next_followup).date()
                    if followup_date <= today:
                        tasks.append({
                            "Task": f"Follow up with {row['Name']}",
                            "Prospect": row["Name"],
                            "Company": row["Company"],
                            "Due Date": followup_date,
                            "Priority": row["Priority"],
                            "Type": "Follow-up",
                            "Status": "Overdue" if followup_date < today else "Due Today"
                        })
                except:
                    pass
            
            # Proposals requiring follow-up
            if row["Deal Stage"] == "Proposal Sent":
                last_contact = row.get("Last Contact", "")
                if last_contact:
                    try:
                        last_date = pd.to_datetime(last_contact).date()
                        days_since = (today - last_date).days
                        if days_since >= 7:
                            tasks.append({
                                "Task": f"Follow up on proposal with {row['Name']}",
                                "Prospect": row["Name"],
                                "Company": row["Company"],
                                "Due Date": today,
                                "Priority": "High",
                                "Type": "Proposal Follow-up",
                                "Status": "Overdue"
                            })
                    except:
                        pass
            
            # New prospects requiring initial contact
            if row["Lead Status"] == "New":
                date_added = pd.to_datetime(row["Date Added"]).date()
                days_since_added = (today - date_added).days
                if days_since_added >= 1:
                    tasks.append({
                        "Task": f"Initial outreach to {row['Name']}",
                        "Prospect": row["Name"],
                        "Company": row["Company"],
                        "Due Date": today,
                        "Priority": row["Priority"],
                        "Type": "Initial Contact",
                        "Status": "Pending"
                    })

        if tasks:
            tasks_df = pd.DataFrame(tasks)
            
            # Sort by priority and due date
            priority_order = {"High": 3, "Medium": 2, "Low": 1}
            tasks_df["Priority Score"] = tasks_df["Priority"].map(priority_order)
            tasks_df = tasks_df.sort_values(["Priority Score", "Due Date"], ascending=[False, True])
            
            # Display tasks with status colors
            st.markdown("### 📋 Your Tasks")
            for _, task in tasks_df.iterrows():
                priority_icon = "🔴" if task["Priority"] == "High" else "🟡" if task["Priority"] == "Medium" else "🟢"
                status_icon = "⚠️" if task["Status"] == "Overdue" else "🕐" if task["Status"] == "Due Today" else "📝"
                
                col1, col2, col3 = st.columns([6, 2, 2])
                with col1:
                    st.write(f"{priority_icon} {status_icon} {task['Task']}")
                with col2:
                    st.write(f"Due: {task['Due Date']}")
                with col3:
                    if st.button("Complete", key=f"complete_{task['Prospect']}_{task['Type']}"):
                        st.success("Task completed!")
        else:
            st.success("🎉 No pending tasks! Great job staying on top of everything.")

    with tab3:
        st.subheader("Automated Reminders")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Reminder Settings**")
            remind_followup = st.number_input("Remind me X days before follow-up", value=1, min_value=0, max_value=7)
            remind_proposal = st.number_input("Remind about proposals after X days", value=7, min_value=1, max_value=30)
            remind_no_activity = st.number_input("Remind about inactive leads after X days", value=14, min_value=7, max_value=60)
            
            email_reminders = st.checkbox("Email reminders", value=True)
            browser_notifications = st.checkbox("Browser notifications", value=False)
            
            if st.button("Save Reminder Settings"):
                st.success("Reminder settings saved!")
        
        with col2:
            st.markdown("**Upcoming Reminders**")
            
            # Generate reminders
            reminders = []
            for _, row in df.iterrows():
                # Follow-up reminders
                next_followup = row.get("Next Follow Up", "")
                if next_followup:
                    try:
                        followup_date = pd.to_datetime(next_followup).date()
                        remind_date = followup_date - timedelta(days=remind_followup)
                        if remind_date >= datetime.now().date():
                            reminders.append({
                                "Date": remind_date,
                                "Type": "Follow-up Reminder",
                                "Message": f"Follow up with {row['Name']} tomorrow",
                                "Priority": row["Priority"]
                            })
                    except:
                        pass
            
            if reminders:
                reminders_df = pd.DataFrame(reminders).sort_values("Date")
                st.dataframe(reminders_df, use_container_width=True)
            else:
                st.info("No upcoming reminders")

# -------------------- ANALYTICS --------------------
elif choice == "📊 Analytics":
    st.title("📊 Advanced Analytics")
    
    tab1, tab2, tab3, tab4 = st.tabs(["🔄 Conversion Funnel", "📈 Trends", "🎯 Lead Scoring", "💰 Revenue Analytics"])
    
    with tab1:
        st.subheader("Sales Conversion Funnel")
        
        # Enhanced funnel with conversion rates
        metrics = compute_advanced_metrics(df)
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.plotly_chart(create_pipeline_funnel(df), use_container_width=True)
        
        with col2:
            st.markdown("**Conversion Rates**")
            st.metric("Contact → Meeting", f"{metrics['contact_to_meeting']}%")
            st.metric("Meeting → Proposal", f"{metrics['meeting_to_proposal']}%")
            st.metric("Proposal → Close", f"{metrics['proposal_to_close']}%")
            
            # Benchmark comparisons
            st.markdown("**Industry Benchmarks**")
            st.write("📊 Contact → Meeting: 15-25%")
            st.write("📊 Meeting → Proposal: 40-60%")
            st.write("📊 Proposal → Close: 20-30%")

        # Funnel analysis by various dimensions
        st.markdown("---")
        st.subheader("Funnel Analysis by Segments")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # By Industry
            industry_funnel = df.groupby("Industry").agg({
                "Lead Status": lambda x: (x != "New").sum(),
                "Deal Stage": lambda x: (x == "Meeting Scheduled").sum()
            }).reset_index()
            industry_funnel.columns = ["Industry", "Contacted", "Meetings"]
            
            fig = px.bar(
                industry_funnel, 
                x="Industry", 
                y=["Contacted", "Meetings"],
                title="Funnel Performance by Industry",
                barmode="group"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # By Lead Source
            source_funnel = df.groupby("Source").agg({
                "Lead Status": lambda x: (x != "New").sum(),
                "Deal Stage": lambda x: (x.isin(["Meeting Scheduled", "Proposal Sent"])).sum()
            }).reset_index()
            source_funnel.columns = ["Source", "Contacted", "Advanced"]
            
            fig = px.bar(
                source_funnel,
                x="Source",
                y=["Contacted", "Advanced"],
                title="Performance by Lead Source",
                barmode="group"
            )
            st.plotly_chart(fig, use_container_width=True)

    with tab2:
        st.subheader("Sales Trends & Forecasting")
        
        # Time-based analysis
        df_temp = df.copy()
        df_temp["Date Added"] = pd.to_datetime(df_temp["Date Added"])
        df_temp["Week"] = df_temp["Date Added"].dt.to_period("W")
        
        weekly_adds = df_temp.groupby("Week").size().reset_index()
        weekly_adds.columns = ["Week", "New Prospects"]
        weekly_adds["Week"] = weekly_adds["Week"].astype(str)
        
        fig = px.line(
            weekly_adds,
            x="Week",
            y="New Prospects",
            title="Weekly Prospect Addition Trend",
            markers=True
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Activity trends
        st.markdown("---")
        col1, col2 = st.columns(2)
        
        with col1:
            # Email activity over time
            email_dates = []
            for _, row in df.iterrows():
                for col in ["Email 1 Date", "Email 2 Date", "Email 3 Date"]:
                    date_val = row.get(col, "")
                    if date_val:
                        try:
                            email_dates.append(pd.to_datetime(date_val).date())
                        except:
                            pass
            
            if email_dates:
                email_series = pd.Series(email_dates).value_counts().sort_index()
                fig = px.line(
                    x=email_series.index,
                    y=email_series.values,
                    title="Email Activity Timeline",
                    markers=True
                )
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Lead score trends
            fig = px.box(
                df,
                x="Lead Status",
                y="Lead Score",
                title="Lead Score Distribution by Status"
            )
            st.plotly_chart(fig, use_container_width=True)

    with tab3:
        st.subheader("Lead Scoring Analysis")
        
        # Lead scoring breakdown
        col1, col2 = st.columns(2)
        
        with col1:
            # Score distribution
            st.plotly_chart(create_lead_score_distribution(df), use_container_width=True)
            
            # Score statistics
            st.markdown("**Lead Score Statistics**")
            st.metric("Average Score", f"{df['Lead Score'].mean():.1f}")
            st.metric("Highest Score", f"{df['Lead Score'].max()}")
            st.metric("Lowest Score", f"{df['Lead Score'].min()}")
        
        with col2:
            # Scoring factors analysis
            st.markdown("**Top Scoring Prospects**")
            top_prospects = df.nlargest(5, "Lead Score")
            
            for _, prospect in top_prospects.iterrows():
                with st.container():
                    col_a, col_b, col_c = st.columns([3, 1, 1])
                    col_a.write(f"**{prospect['Name']}** - {prospect['Company']}")
                    col_b.write(f"Score: {prospect['Lead Score']}")
                    col_c.write(f"{prospect['Deal Stage']}")
            
            # Score correlation analysis
            st.markdown("**Score vs Engagement**")
            correlation_data = []
            for _, row in df.iterrows():
                correlation_data.append({
                    "Lead Score": row["Lead Score"],
                    "Email Engagement": row["Opened Emails"] + (row["Replies"] * 2),
                    "Company": row["Company"]
                })
            
            if correlation_data:
                corr_df = pd.DataFrame(correlation_data)
                fig = px.scatter(
                    corr_df,
                    x="Lead Score",
                    y="Email Engagement",
                    hover_data=["Company"],
                    title="Lead Score vs Email Engagement",
                    trendline="ols"
                )
                st.plotly_chart(fig, use_container_width=True)

    with tab4:
        st.subheader("Revenue Analytics")
        
        # Pipeline value analysis
        col1, col2 = st.columns(2)
        
        with col1:
            st.plotly_chart(create_revenue_by_industry(df), use_container_width=True)
        
        with col2:
            # Deal size by company size
            def parse_deal_value(x):
                try:
                    val = str(x).replace("$", "").replace(",", "")
                    if "K" in val:
                        return float(val.replace("K", "")) * 1000
                    elif "M" in val:
                        return float(val.replace("M", "")) * 1000000
                    else:
                        return float(val) if val else 0
                except:
                    return 0
            
            df_temp = df.copy()
            df_temp["Deal Value Numeric"] = df_temp["Deal Value"].apply(parse_deal_value)
            
            size_revenue = df_temp.groupby("Company Size")["Deal Value Numeric"].mean().reset_index()
            
            fig = px.bar(
                size_revenue,
                x="Company Size",
                y="Deal Value Numeric",
                title="Average Deal Size by Company Size",
                color_discrete_sequence=["#FF6B35"]
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Revenue forecasting
        st.markdown("---")
        st.subheader("Revenue Forecast")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            # Conservative estimate (high probability deals)
            high_prob_deals = df[df["Deal Stage"].isin(["Negotiation", "Proposal Sent"])]
            conservative_forecast = high_prob_deals["Deal Value"].apply(parse_deal_value).sum() * 0.7
            st.metric("Conservative (70%)", f"${conservative_forecast:,.0f}")
        
        with col2:
            # Optimistic estimate (all active deals)
            active_deals = df[df["Deal Stage"] != "Prospecting"]
            optimistic_forecast = active_deals["Deal Value"].apply(parse_deal_value).sum()
            st.metric("Optimistic (100%)", f"${optimistic_forecast:,.0f}")
        
        with col3:
            # Weighted forecast based on stage
            stage_weights = {
                "Prospecting": 0.1,
                "Meeting Scheduled": 0.2,
                "Proposal Sent": 0.5,
                "Negotiation": 0.8,
                "Closed Won": 1.0
            }
            
            weighted_forecast = 0
            for _, row in df.iterrows():
                deal_value = parse_deal_value(row["Deal Value"])
                weight = stage_weights.get(row["Deal Stage"], 0)
                weighted_forecast += deal_value * weight
            
            st.metric("Weighted Forecast", f"${weighted_forecast:,.0f}")

# -------------------- SETTINGS --------------------
elif choice == "⚙️ Settings":
    st.title("⚙️ CRM Settings & Configuration")
    
    tab1, tab2, tab3, tab4 = st.tabs(["👤 User Management", "🎨 Customization", "📤 Import/Export", "🔧 System"])
    
    with tab1:
        st.subheader("User Management")
        
        # Sales rep management
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Sales Representatives**")
            current_reps = df["Owner"].unique()
            
            for rep in current_reps:
                rep_prospects = len(df[df["Owner"] == rep])
                rep_meetings = len(df[(df["Owner"] == rep) & (df["Deal Stage"] == "Meeting Scheduled")])
                
                with st.container():
                    st.write(f"**{rep}**")
                    st.write(f"Prospects: {rep_prospects} | Meetings: {rep_meetings}")
        
        with col2:
            st.markdown("**Add New Rep**")
            new_rep_name = st.text_input("Rep Name")
            new_rep_email = st.text_input("Email")
            new_rep_territory = st.selectbox("Territory", ["West Coast", "East Coast", "Central", "International"])
            
            if st.button("Add Rep"):
                st.success(f"Added {new_rep_name} to the system!")

    with tab2:
        st.subheader("CRM Customization")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Pipeline Stages**")
            default_stages = ["Prospecting", "Meeting Scheduled", "Proposal Sent", "Negotiation", "Closed Won", "Closed Lost"]
            
            for i, stage in enumerate(default_stages):
                new_stage = st.text_input(f"Stage {i+1}", value=stage, key=f"stage_{i}")
            
            if st.button("Save Pipeline Stages"):
                st.success("Pipeline stages updated!")
        
        with col2:
            st.markdown("**Lead Scoring Weights**")
            
            st.slider("Company Size Weight", 0, 100, 25)
            st.slider("Industry Relevance", 0, 100, 20)
            st.slider("Engagement Level", 0, 100, 30)
            st.slider("Budget Fit", 0, 100, 25)
            
            if st.button("Recalculate All Scores"):
                st.info("Lead scores would be recalculated with new weights")

    with tab3:
        st.subheader("Data Import & Export")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Export Options**")
            
            export_format = st.selectbox("Export Format", ["CSV", "Excel", "JSON"])
            export_filter = st.selectbox("Export Filter", ["All Prospects", "Active Deals Only", "High Priority Only"])
            
            # Filter data based on selection
            if export_filter == "Active Deals Only":
                export_df = df[df["Deal Stage"] != "Prospecting"]
            elif export_filter == "High Priority Only":
                export_df = df[df["Priority"] == "High"]
            else:
                export_df = df
            
            if export_format == "CSV":
                csv_data = export_df.to_csv(index=False).encode("utf-8")
                st.download_button(
                    "📥 Download CSV",
                    csv_data,
                    f"prospects_export_{datetime.now().strftime('%Y%m%d')}.csv",
                    "text/csv"
                )
            elif export_format == "JSON":
                json_data = export_df.to_json(orient="records", indent=2)
                st.download_button(
                    "📥 Download JSON",
                    json_data,
                    f"prospects_export_{datetime.now().strftime('%Y%m%d')}.json",
                    "application/json"
                )
        
        with col2:
            st.markdown("**Import Data**")
            
            uploaded_file = st.file_uploader("Choose file", type=['csv', 'xlsx', 'json'])
            
            if uploaded_file is not None:
                try:
                    if uploaded_file.name.endswith('.csv'):
                        new_data = pd.read_csv(uploaded_file)
                    elif uploaded_file.name.endswith('.xlsx'):
                        new_data = pd.read_excel(uploaded_file)
                    elif uploaded_file.name.endswith('.json'):
                        new_data = pd.read_json(uploaded_file)
                    
                    st.write("Preview imported data:")
                    st.dataframe(new_data.head())
                    
                    if st.button("Import Data"):
                        # Add prospect IDs if missing
                        if "Prospect ID" not in new_data.columns:
                            max_id = st.session_state.df["Prospect ID"].max()
                            new_data["Prospect ID"] = range(max_id + 1, max_id + 1 + len(new_data))
                        
                        st.session_state.df = pd.concat([st.session_state.df, new_data], ignore_index=True)
                        st.success(f"Successfully imported {len(new_data)} prospects!")
                        st.experimental_rerun()
                        
                except Exception as e:
                    st.error(f"Error importing file: {e}")

    with tab4:
        st.subheader("System Configuration")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Database Management**")
            
            if st.button("🗑️ Clear All Data", type="secondary"):
                if st.checkbox("I understand this will delete all data"):
                    st.session_state.df = load_demo_data()
                    st.success("Data reset to demo state!")
                    st.experimental_rerun()
            
            st.markdown("**Backup & Restore**")
            if st.button("💾 Create Backup"):
                backup_data = st.session_state.df.to_json(orient="records", indent=2)
                st.download_button(
                    "Download Backup",
                    backup_data,
                    f"crm_backup_{datetime.now().strftime('%Y%m%d_%H%M')}.json",
                    "application/json"
                )
        
        with col2:
            st.markdown("**Integration Settings**")
            
            st.checkbox("Enable LinkedIn Integration", value=False)
            st.checkbox("Enable Calendar Sync", value=False)
            st.checkbox("Enable Email Provider Sync", value=False)
            
            st.selectbox("Time Zone", ["UTC", "EST", "PST", "CST", "MST"])
            st.selectbox("Date Format", ["YYYY-MM-DD", "MM/DD/YYYY", "DD/MM/YYYY"])
            
            if st.button("Save Integration Settings"):
                st.success("Settings saved!")

# -------------------- ADVANCED PROSPECT VIEW --------------------
else:
    st.title("🔍 All Prospects - Advanced View")
    
    # Advanced filtering and search
    st.subheader("Advanced Filters")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        status_filter = st.multiselect("Lead Status", df["Lead Status"].unique(), default=df["Lead Status"].unique())
        industry_filter = st.multiselect("Industry", df["Industry"].unique(), default=df["Industry"].unique())
    
    with col2:
        stage_filter = st.multiselect("Deal Stage", df["Deal Stage"].unique(), default=df["Deal Stage"].unique())
        priority_filter = st.multiselect("Priority", df["Priority"].unique(), default=df["Priority"].unique())
    
    with col3:
        score_range = st.slider("Lead Score Range", 0, 100, (0, 100))
        owner_filter = st.multiselect("Owner", df["Owner"].unique(), default=df["Owner"].unique())
    
    with col4:
        # Date filters
        date_from = st.date_input("Added After", datetime.now() - timedelta(days=90))
        date_to = st.date_input("Added Before", datetime.now())

    # Apply all filters
    filtered_df = df[
        (df["Lead Status"].isin(status_filter)) &
        (df["Industry"].isin(industry_filter)) &
        (df["Deal Stage"].isin(stage_filter)) &
        (df["Priority"].isin(priority_filter)) &
        (df["Lead Score"] >= score_range[0]) &
        (df["Lead Score"] <= score_range[1]) &
        (df["Owner"].isin(owner_filter)) &
        (pd.to_datetime(df["Date Added"]).dt.date >= date_from) &
        (pd.to_datetime(df["Date Added"]).dt.date <= date_to)
    ]

    # Search functionality
    search_col1, search_col2 = st.columns([3, 1])
    with search_col1:
        search_term = st.text_input("🔍 Search prospects...", placeholder="Search by name, company, email, or notes")
    with search_col2:
        sort_by = st.selectbox("Sort by", ["Lead Score", "Date Added", "Name", "Company", "Deal Value"])

    if search_term:
        search_mask = (
            filtered_df["Name"].str.contains(search_term, case=False, na=False) |
            filtered_df["Company"].str.contains(search_term, case=False, na=False) |
            filtered_df["Email"].str.contains(search_term, case=False, na=False) |
            filtered_df["Notes"].str.contains(search_term, case=False, na=False)
        )
        filtered_df = filtered_df[search_mask]

    # Sort results
    if sort_by == "Lead Score":
        filtered_df = filtered_df.sort_values("Lead Score", ascending=False)
    elif sort_by == "Date Added":
        filtered_df = filtered_df.sort_values("Date Added", ascending=False)
    else:
        filtered_df = filtered_df.sort_values(sort_by)

    st.write(f"**Showing {len(filtered_df)} of {len(df)} prospects**")

    # Column selector
    all_columns = df.columns.tolist()
    default_columns = [
        "Prospect ID", "Name", "Company", "Title / Role", "Industry", 
        "Lead Status", "Deal Stage", "Lead Score", "Priority", "Owner", 
        "Deal Value", "Next Follow Up"
    ]
    
    selected_columns = st.multiselect(
        "Select Columns to Display",
        all_columns,
        default=[col for col in default_columns if col in all_columns]
    )

    if selected_columns:
        # Enhanced dataframe display
        display_df = filtered_df[selected_columns].copy()
        
        # Add styling based on priority and status
        def highlight_priority(row):
            if 'Priority' in row:
                if row['Priority'] == 'High':
                    return ['background-color: #ffebee'] * len(row)
                elif row['Priority'] == 'Medium':
                    return ['background-color: #fff3e0'] * len(row)
                else:
                    return ['background-color: #e8f5e8'] * len(row)
            return [''] * len(row)
        
        st.dataframe(
            display_df.style.apply(highlight_priority, axis=1),
            use_container_width=True,
            height=600
        )

        # Prospect detail view
        if not filtered_df.empty:
            st.markdown("---")
            st.subheader("Prospect Details")
            
            selected_prospect_id = st.selectbox(
                "View Detailed Profile",
                filtered_df["Prospect ID"].tolist(),
                format_func=lambda x: f"{x} - {filtered_df[filtered_df['Prospect ID']==x]['Name'].iloc[0]} ({filtered_df[filtered_df['Prospect ID']==x]['Company'].iloc[0]})"
            )
            
            if selected_prospect_id:
                prospect = filtered_df[filtered_df["Prospect ID"] == selected_prospect_id].iloc[0]
                
                # Detailed prospect view
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.markdown("**Contact Information**")
                    st.write(f"**Name:** {prospect['Name']}")
                    st.write(f"**Title:** {prospect['Title / Role']}")
                    st.write(f"**Company:** {prospect['Company']}")
                    st.write(f"**Industry:** {prospect['Industry']}")
                    st.write(f"**Location:** {prospect['Location']}")
                    st.write(f"**Email:** {prospect['Email']}")
                    st.write(f"**Phone:** {prospect['Phone']}")
                    if prospect.get("LinkedIn URL"):
                        st.markdown(f"**LinkedIn:** [Profile]({prospect['LinkedIn URL']})")
                    if prospect.get("Website"):
                        st.markdown(f"**Website:** [Visit]({prospect['Website']})")
                
                with col2:
                    st.markdown("**Sales Information**")
                    st.write(f"**Lead Status:** {prospect['Lead Status']}")
                    st.write(f"**Deal Stage:** {prospect['Deal Stage']}")
                    st.write(f"**Lead Score:** {prospect['Lead Score']}/100")
                    st.write(f"**Priority:** {prospect['Priority']}")
                    st.write(f"**Owner:** {prospect['Owner']}")
                    st.write(f"**Source:** {prospect['Source']}")
                    st.write(f"**Date Added:** {prospect['Date Added']}")
                    st.write(f"**Deal Value:** {prospect['Deal Value'] or 'TBD'}")
                    st.write(f"**Budget:** {prospect.get('Budget', 'Unknown')}")
                
                with col3:
                    st.markdown("**Company Details**")
                    st.write(f"**Size:** {prospect['Company Size']}")
                    st.write(f"**Employees:** {prospect.get('Employee Count', 'Unknown')}")
                    st.write(f"**Revenue:** {prospect.get('Revenue', 'Unknown')}")
                    
                    st.markdown("**Engagement**")
                    st.write(f"**Emails Opened:** {prospect['Opened Emails']}")
                    st.write(f"**Replies:** {prospect['Replies']}")
                    st.write(f"**Last Contact:** {prospect.get('Last Contact', 'Never')}")
                    st.write(f"**Next Follow Up:** {prospect.get('Next Follow Up', 'Not scheduled')}")

                # Pain points and solution interest
                st.markdown("---")
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("**Pain Points**")
                    st.write(prospect.get('Pain Point(s)', 'Not specified'))
                
                with col2:
                    st.markdown("**Solution Interest**")
                    st.write(prospect.get('Solution Interest', 'Not specified'))

                # Notes section
                st.markdown("**Notes & Activity History**")
                notes = prospect.get('Notes', 'No notes yet')
                st.text_area("Notes", value=notes, height=100, disabled=True)
                
                # Quick actions for this prospect
                st.markdown("---")
                st.markdown("**Quick Actions**")
                
                action_col1, action_col2, action_col3, action_col4 = st.columns(4)
                
                with action_col1:
                    if st.button("📧 Send Email"):
                        st.info("Email composer would open")
                
                with action_col2:
                    if st.button("📞 Schedule Call"):
                        st.info("Calendar would open for scheduling")
                
                with action_col3:
                    if st.button("📝 Add Note"):
                        st.info("Note editor would open")
                
                with action_col4:
                    if st.button("🔄 Update Status"):
                        st.info("Status update form would appear")

        # Bulk operations
        st.markdown("---")
        st.subheader("Bulk Operations")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📧 Bulk Email Campaign"):
                st.info("Bulk email composer would open for selected prospects")
        
        with col2:
            if st.button("📊 Export Selected"):
                csv_data = filtered_df.to_csv(index=False).encode("utf-8")
                st.download_button(
                    "Download Filtered Data",
                    csv_data,
                    f"filtered_prospects_{datetime.now().strftime('%Y%m%d')}.csv",
                    "text/csv"
                )
        
        with col3:
            if st.button("🏷️ Bulk Tag"):
                st.info("Tag management interface would open")

# -------------------- FOOTER --------------------
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 20px;'>
    <p>Advanced Cold Sales CRM | Built with Streamlit | Last updated: {}</p>
    <p>💡 <strong>Tips:</strong> Use lead scoring to prioritize efforts | Set up automated sequences | Review analytics weekly</p>
</div>
""".format(datetime.now().strftime("%Y-%m-%d %H:%M")), unsafe_allow_html=True)
