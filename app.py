import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from datetime import datetime, timedelta
import random

# Page configuration
st.set_page_config(
    page_title="RapidClaims Dashboard",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for styling
st.markdown("""
<style>
    .main {
        background-color: #FEFEFE;
    }
    
    .stSelectbox > div > div {
        background-color: #F8F9FA;
        color: #000000;
    }
    
    .stSelectbox > div > div > div {
        color: #000000;
    }
    
    .stSelectbox option {
        color: #000000;
    }
    
    .metric-container {
        background-color: #F8F9FA;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #E9ECEF;
        text-align: center;
        margin: 10px 0;
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: bold;
        color: #2E86AB;
        margin: 0;
    }
    
    .metric-label {
        font-size: 1.1rem;
        color: #6C757D;
        margin: 5px 0 0 0;
    }
    
    .page-header {
        color: #2E86AB;
        font-size: 2.5rem;
        font-weight: bold;
        margin-bottom: 30px;
        text-align: center;
    }
    
    .filter-section {
        background-color: #F8F9FA;
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

# Sample data generation
@st.cache_data
def generate_sample_data():
    np.random.seed(42)
    random.seed(42)
    
    payers = ['Medicare', 'Medicaid', 'Blue Cross', 'Aetna', 'UnitedHealth', 'Humana', 'Cigna']
    departments = ['Cardiology', 'Orthopedics', 'Emergency', 'Surgery', 'Radiology', 'Laboratory', 'ICU']
    
    # Generate claims data
    claims_data = []
    for i in range(200):
        claim_id = f"CLM{1000 + i}"
        payer = random.choice(payers)
        department = random.choice(departments)
        amount_raised = round(random.uniform(500, 25000), 2)
        # Simulate some claims with partial payments
        payment_rate = random.uniform(0.7, 1.0)
        amount_received = round(amount_raised * payment_rate, 2)
        
        # Days to resolution (for pie chart)
        resolution_days = random.choice([
            random.randint(1, 30),   # 0-30 days
            random.randint(31, 60),  # 31-60 days
            random.randint(61, 90),  # 61-90 days
            random.randint(91, 120), # 91-120 days
            random.randint(121, 365) # 120+ days
        ])
        
        # Outstanding amount (amount not yet received)
        outstanding_amount = amount_raised - amount_received
        
        claims_data.append({
            'Claim ID': claim_id,
            'Payer': payer,
            'Department': department,
            'Amount Raised': amount_raised,
            'Amount Received': amount_received,
            'Outstanding Amount': outstanding_amount,
            'Resolution Days': resolution_days
        })
    
    return pd.DataFrame(claims_data)

@st.cache_data
def generate_denial_data():
    np.random.seed(42)
    random.seed(42)
    
    payers = ['Medicare', 'Medicaid', 'Blue Cross', 'Aetna', 'UnitedHealth', 'Humana', 'Cigna']
    departments = ['Cardiology', 'Orthopedics', 'Emergency', 'Surgery', 'Radiology', 'Laboratory', 'ICU']
    
    denial_reasons = [
        'Missing Documentation',
        'Prior Authorization Required',
        'Duplicate Claim',
        'Invalid Procedure Code',
        'Patient Not Eligible',
        'Incomplete Information',
        'Medical Necessity',
        'Timely Filing Limit',
        'Incorrect Patient Demographics'
    ]
    
    rejection_codes = ['D001', 'D002', 'D003', 'D004', 'D005', 'D006', 'D007', 'D008', 'D009']
    
    # Generate denial data
    denial_data = []
    for i in range(150):  # 150 denied claims
        claim_id = f"CLM{2000 + i}"
        payer = random.choice(payers)
        department = random.choice(departments)
        reason_idx = random.randint(0, len(denial_reasons) - 1)
        denial_reason = denial_reasons[reason_idx]
        rejection_code = rejection_codes[reason_idx]
        
        denial_data.append({
            'Claim ID': claim_id,
            'Payer': payer,
            'Department': department,
            'Denial Reason': denial_reason,
            'Rejection Code': rejection_code
        })
    
    return pd.DataFrame(denial_data)

@st.cache_data
def generate_monthly_clean_claim_data():
    # Generate 12 months of clean claim rate data
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
              'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    
    # Simulate clean claim rates (percentage of claims that pass without issues)
    np.random.seed(42)
    base_rate = 85  # Base clean claim rate
    rates = []
    
    for i in range(12):
        # Add some variation and slight upward trend
        variation = random.uniform(-5, 8)
        trend = i * 0.5  # Slight improvement over time
        rate = min(95, max(75, base_rate + variation + trend))
        rates.append(round(rate, 1))
    
    return pd.DataFrame({
        'Month': months,
        'Clean Claim Rate': rates
    })

@st.cache_data
def generate_payer_insights_data():
    np.random.seed(42)
    random.seed(42)
    
    payers = ['Medicare', 'Medicaid', 'Blue Cross', 'Aetna', 'UnitedHealth', 'Humana', 'Cigna']
    
    payer_data = []
    for payer in payers:
        # Generate payer-specific metrics
        total_claims_raised = random.uniform(800000, 2500000)
        collection_rate = random.uniform(0.75, 0.95)
        claims_received = total_claims_raised * collection_rate
        
        # Clean claim rate (percentage of claims that don't get denied initially)
        clean_claim_rate = random.uniform(75, 95)
        
        # Average days for resolution
        avg_resolution_days = random.uniform(25, 65)
        
        payer_data.append({
            'Payer': payer,
            'Total Claims Raised': total_claims_raised,
            'Claims Received': claims_received,
            'Collection Rate': collection_rate * 100,
            'Clean Claim Rate': clean_claim_rate,
            'Avg Resolution Days': avg_resolution_days
        })
    
    return pd.DataFrame(payer_data)

@st.cache_data
def generate_operational_efficiency_data():
    np.random.seed(42)
    random.seed(42)
    
    # Define 4 claim status states
    status_states = [
        'Coding',
        'Claim Scrubbing',
        'Billing',
        'Collection'
    ]
    
    # Generate 12 weeks of data
    weeks = []
    current_date = datetime.now()
    for i in range(12):
        week_start = current_date - timedelta(weeks=11-i)
        week_label = f"Week {i+1}\n({week_start.strftime('%m/%d')})"
        weeks.append(week_label)
    
    operational_data = []
    
    for week in weeks:
        for status in status_states:
            # Generate realistic days taken for each status transition
            if status == 'Coding':
                days_taken = random.uniform(1, 4)    # Coding conversion time
            elif status == 'Claim Scrubbing':
                days_taken = random.uniform(2, 6)    # Scrubbing and validation
            elif status == 'Billing':
                days_taken = random.uniform(1, 3)    # Billing submission
            else:  # Collection
                days_taken = random.uniform(5, 20)   # Collection process
            
            # Add some weekly variation
            weekly_variation = random.uniform(0.8, 1.3)
            days_taken *= weekly_variation
            
            operational_data.append({
                'Week': week,
                'Status': status,
                'Days Taken': round(days_taken, 1)
            })
    
    return pd.DataFrame(operational_data)

@st.cache_data
def generate_claims_table_data():
    np.random.seed(42)
    random.seed(42)
    
    # Sample data for claims table
    assigned_to = ['John Smith', 'Sarah Johnson', 'Mike Chen', 'Emily Davis', 'Robert Wilson', 'Lisa Brown', 'David Lee', 'Jennifer Taylor']
    statuses = ['Coding', 'Claim Scrubbing', 'Billing', 'Collection']
    payers = ['Medicare', 'Medicaid', 'Blue Cross', 'Aetna', 'UnitedHealth', 'Humana', 'Cigna']
    
    denial_reasons = [
        'Missing Documentation',
        'Prior Authorization Required', 
        'Duplicate Claim',
        'Invalid Procedure Code',
        'Patient Not Eligible',
        'Incomplete Information',
        'Medical Necessity',
        'Timely Filing Limit',
        'N/A'  # For non-denied claims
    ]
    
    claims_data = []
    for i in range(50):  # Generate 50 sample claims
        # Generate Claim ID
        claim_id = f"CLM{3000 + i}"
        
        # Assign random values
        assigned = random.choice(assigned_to)
        status = random.choice(statuses)
        
        # Denial reason - only for certain statuses
        if status in ['Claim Scrubbing', 'Billing']:
            denial_reason = random.choice([r for r in denial_reasons if r != 'N/A'])
        else:
            denial_reason = 'N/A'
        
        payer = random.choice(payers)
        claim_amount = round(random.uniform(1000, 50000), 2)
        
        claims_data.append({
            'Claim ID': claim_id,
            'Assigned to': assigned,
            'Status': status,
            'Denial Reason': denial_reason,
            'Payer': payer,
            'Claim Amount Raised': claim_amount
        })
    
    return pd.DataFrame(claims_data)

def categorize_resolution_days(days):
    if days <= 30:
        return '0-30 days'
    elif days <= 60:
        return '31-60 days'
    elif days <= 90:
        return '61-90 days'
    elif days <= 120:
        return '91-120 days'
    else:
        return '120+ days'

def financial_health_page():
    # Page header
    st.markdown('<h1 class="page-header">Financial Health</h1>', unsafe_allow_html=True)
    
    # Load data
    df = generate_sample_data()
    
    # Filter section
    st.markdown('<div class="filter-section">', unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns([2, 2, 2, 3])
    
    with col1:
        selected_payer = st.selectbox("Filter by Payer:", ["All"] + sorted(df['Payer'].unique().tolist()))
    
    with col2:
        selected_department = st.selectbox("Filter by Department:", ["All"] + sorted(df['Department'].unique().tolist()))
    
    # Apply filters first
    filtered_df = df.copy()
    if selected_payer != "All":
        filtered_df = filtered_df[filtered_df['Payer'] == selected_payer]
    if selected_department != "All":
        filtered_df = filtered_df[filtered_df['Department'] == selected_department]
    
    # Create pie chart data first
    filtered_df['Resolution Category'] = filtered_df['Resolution Days'].apply(categorize_resolution_days)
    resolution_counts = filtered_df['Resolution Category'].value_counts()
    
    with col4:
        # Calculate average from the same data used in pie chart
        avg_days_ar = filtered_df['Resolution Days'].mean() if len(filtered_df) > 0 else 0
        st.markdown(f"""
        <div class="metric-container">
            <div class="metric-value">{avg_days_ar:.1f}</div>
            <div class="metric-label">Avg. Number of days for Claim resolution</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Main content area
    col_left, col_right = st.columns([1, 2])
    
    with col_left:
        st.subheader("Claims Resolution Timeline")
        
        # Create pie chart
        fig_pie = px.pie(
            values=resolution_counts.values,
            names=resolution_counts.index,
            color_discrete_sequence=['#2E86AB', '#A23B72', '#F18F01', '#C73E1D', '#8B5A3C']
        )
        fig_pie.update_layout(
            title="",
            title_font_size=16,
            font_size=12,
            showlegend=True,
            height=400,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig_pie, use_container_width=True)
    
    with col_right:
        st.subheader("Payment Tracker")
        
        # Display the payment tracker table
        display_df = filtered_df[['Claim ID', 'Payer', 'Department', 'Amount Raised', 'Amount Received']].copy()
        
        # Format currency and percentage columns
        display_df['Amount Raised'] = display_df['Amount Raised'].apply(lambda x: f"${x:,.2f}")
        # Convert Amount Received to percentage of Amount Raised
        display_df['Amount Received'] = (filtered_df['Amount Received'] / filtered_df['Amount Raised'] * 100).apply(lambda x: f"{x:.1f}%")
        
        # Display table with pagination
        st.dataframe(
            display_df,
            use_container_width=True,
            height=400,
            hide_index=True
        )
        
        # Summary metrics
        col_metric1, col_metric2, col_metric3 = st.columns(3)
        
        with col_metric1:
            total_raised = filtered_df['Amount Raised'].sum()
            st.metric("Total Raised", f"${total_raised:,.2f}")
        
        with col_metric2:
            total_received = filtered_df['Amount Received'].sum()
            st.metric("Total Received", f"${total_received:,.2f}")
        
        with col_metric3:
            collection_rate = (total_received / total_raised) * 100 if total_raised > 0 else 0
            st.metric("Collection Rate", f"{collection_rate:.1f}%")

def claims_analysis_page():
    # Page header
    st.markdown('<h1 class="page-header">Denial Management</h1>', unsafe_allow_html=True)
    
    # Load data
    df = generate_sample_data()
    denial_df = generate_denial_data()
    monthly_df = generate_monthly_clean_claim_data()
    
    # Filter section
    st.markdown('<div class="filter-section">', unsafe_allow_html=True)
    col1, col2, col3, col4, col5 = st.columns([2, 2, 1, 2, 2])
    
    with col1:
        selected_payer = st.selectbox("Filter by Payer:", ["All"] + sorted(df['Payer'].unique().tolist()), key="page2_payer")
    
    with col2:
        selected_department = st.selectbox("Filter by Department:", ["All"] + sorted(df['Department'].unique().tolist()), key="page2_dept")
    
    with col4:
        # Filter data first to calculate accurate metrics
        filtered_df = df.copy()
        filtered_denial_df = denial_df.copy()
        
        if selected_payer != "All":
            filtered_df = filtered_df[filtered_df['Payer'] == selected_payer]
            filtered_denial_df = filtered_denial_df[filtered_denial_df['Payer'] == selected_payer]
        if selected_department != "All":
            filtered_df = filtered_df[filtered_df['Department'] == selected_department]
            filtered_denial_df = filtered_denial_df[filtered_denial_df['Department'] == selected_department]
        
        total_claimed = filtered_df['Amount Raised'].sum()
        st.markdown(f"""
        <div class="metric-container">
            <div class="metric-value">${total_claimed:,.0f}</div>
            <div class="metric-label">Total Claimed Amount (Current Month)</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col5:
        total_outstanding = filtered_df['Outstanding Amount'].sum()
        outstanding_percentage = (total_outstanding / total_claimed) * 100 if total_claimed > 0 else 0
        st.markdown(f"""
        <div class="metric-container">
            <div class="metric-value">{outstanding_percentage:.1f}%</div>
            <div class="metric-label">Outstanding Claim Amount</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Main content area
    col_left, col_right = st.columns([1, 1])
    
    with col_left:
        st.subheader("Clean Claim Rate - Monthly Trend")
        
        # Create bar chart for clean claim rate
        fig_bar = px.bar(
            monthly_df,
            x='Month',
            y='Clean Claim Rate',
            color='Clean Claim Rate',
            color_continuous_scale=['#FF6B6B', '#4ECDC4', '#45B7D1'],
            text='Clean Claim Rate'
        )
        
        fig_bar.update_layout(
            title="",
            title_font_size=16,
            xaxis_title="Month",
            yaxis_title="Clean Claim Rate (%)",
            showlegend=False,
            height=400,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            yaxis=dict(range=[70, 100])
        )
        
        fig_bar.update_traces(
            texttemplate='%{text}%',
            textposition='outside'
        )
        
        st.plotly_chart(fig_bar, use_container_width=True)
    
    with col_right:
        st.subheader("Denial RCA (Root Cause Analysis) - Current Month")
        
        # Create pie chart for denial reasons
        denial_counts = filtered_denial_df['Denial Reason'].value_counts()
        
        fig_pie = px.pie(
            values=denial_counts.values,
            names=denial_counts.index,
            color_discrete_sequence=px.colors.qualitative.Set3,
            hover_data={'values': denial_counts.values}
        )
        
        fig_pie.update_traces(
            hovertemplate="<b>%{label}</b><br>" +
                         "Impact Claims: %{value}<br>" +
                         "Percentage: %{percent}<br>" +
                         "<extra></extra>"
        )
        
        fig_pie.update_layout(
            title="",
            title_font_size=16,
            font_size=12,
            showlegend=True,
            height=400,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )
        
        # Display the pie chart with click functionality
        selected_points = st.plotly_chart(fig_pie, use_container_width=True, on_select="rerun", selection_mode="points")
        
        # Check if any pie chart segment was clicked and show bar chart
        if selected_points and 'selection' in selected_points and 'points' in selected_points['selection']:
            if selected_points['selection']['points']:
                # Get the selected denial reason
                selected_point = selected_points['selection']['points'][0]
                selected_reason = selected_point['label']
                
                st.info(f"Showing payer breakdown for: **{selected_reason}**")
                
                # Filter denial data by selected reason
                detailed_df = filtered_denial_df[filtered_denial_df['Denial Reason'] == selected_reason]
                
                # Create payer breakdown for the selected denial reason
                if len(detailed_df) > 0:
                    # Group by payer and count occurrences
                    payer_breakdown = detailed_df.groupby('Payer').size().reset_index(name='Count')
                    payer_breakdown = payer_breakdown.sort_values('Count', ascending=False)
                    
                    # Create bar chart showing payer breakdown
                    fig_payer_bar = px.bar(
                        payer_breakdown,
                        x='Payer',
                        y='Count',
                        color='Count',
                        color_continuous_scale=['#FF6B6B', '#FFE66D', '#4ECDC4'],
                        text='Count',
                        title=f"Payer Breakdown for '{selected_reason}'"
                    )
                    
                    fig_payer_bar.update_layout(
                        title_font_size=16,
                        xaxis_title="Payer",
                        yaxis_title="Number of Denied Claims",
                        showlegend=False,
                        height=400,
                        paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(0,0,0,0)',
                        xaxis_tickangle=45
                    )
                    
                    fig_payer_bar.update_traces(
                        texttemplate='%{text}',
                        textposition='outside'
                    )
                    
                    # Display the bar chart
                    st.plotly_chart(fig_payer_bar, use_container_width=True)
                else:
                    st.warning("No data available for the selected denial reason.")
            else:
                st.info("Click on any segment of the pie chart above to see detailed denial information.")
        else:
            st.info("Click on any segment of the pie chart above to see detailed denial information.")

def payer_insights_page():
    # Page header
    st.markdown('<h1 class="page-header">Payer Insights</h1>', unsafe_allow_html=True)
    
    # Load payer insights data
    payer_df = generate_payer_insights_data()
    
    # Prepare data for dual bar chart
    payer_comparison_data = []
    for _, row in payer_df.iterrows():
        payer_comparison_data.extend([
            {
                'Payer': row['Payer'],
                'Metric': 'Claims Raised',
                'Amount': row['Total Claims Raised'],
                'Percentage': None
            },
            {
                'Payer': row['Payer'],
                'Metric': 'Claims Received',
                'Amount': row['Claims Received'],
                'Percentage': row['Collection Rate']
            }
        ])
    
    comparison_df = pd.DataFrame(payer_comparison_data)
    
    # Create dual bar chart
    fig_dual_bar = px.bar(
        comparison_df,
        x='Payer',
        y='Amount',
        color='Metric',
        color_discrete_map={
            'Claims Raised': '#FF6B6B',
            'Claims Received': '#4ECDC4'
        },
        text='Amount'
    )
    
    # Update layout and add percentage labels
    fig_dual_bar.update_layout(
        title="",
        title_font_size=18,
        xaxis_title="Payer",
        yaxis_title="Amount ($)",
        showlegend=True,
        height=500,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        barmode='group'
    )
    
    # Format text labels with only percentages
    for i, trace in enumerate(fig_dual_bar.data):
        if trace.name == 'Claims Raised':
            trace.texttemplate = ''  # Remove text from Claims Raised bars
            trace.textposition = 'none'
        else:  # Claims Received
            # Add only percentage labels on top of Claims Received bars
            percentages = [f"{row['Collection Rate']:.1f}%" for _, row in payer_df.iterrows()]
            trace.texttemplate = percentages
            trace.textposition = 'outside'
    
    st.plotly_chart(fig_dual_bar, use_container_width=True)
    
    # Bottom section - Two side-by-side charts
    col_left, col_right = st.columns(2)
    
    with col_left:
        st.subheader("Clean Claim Rates")
        
        # Create clean claim rate bar chart
        fig_clean_rate = px.bar(
            payer_df,
            x='Payer',
            y='Clean Claim Rate',
            color='Clean Claim Rate',
            color_continuous_scale=['#FF6B6B', '#FFE66D', '#4ECDC4'],
            text='Clean Claim Rate'
        )
        
        fig_clean_rate.update_layout(
            title="",
            xaxis_title="Payer",
            yaxis_title="Clean Claim Rate (%)",
            showlegend=False,
            height=400,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            yaxis=dict(range=[70, 100])
        )
        
        fig_clean_rate.update_traces(
            texttemplate='%{y:.1f}%',
            textposition='outside'
        )
        
        fig_clean_rate.update_layout(xaxis_tickangle=45)
        
        st.plotly_chart(fig_clean_rate, use_container_width=True)
    
    with col_right:
        st.subheader("Average Days for Claim Resolution")
        
        # Create average resolution days bar chart
        fig_resolution_days = px.bar(
            payer_df,
            x='Payer',
            y='Avg Resolution Days',
            color='Avg Resolution Days',
            color_continuous_scale=['#4ECDC4', '#FFE66D', '#FF6B6B'],  # Reverse scale (green=good, red=bad)
            text='Avg Resolution Days'
        )
        
        fig_resolution_days.update_layout(
            title="",
            xaxis_title="Payer",
            yaxis_title="Average Days",
            showlegend=False,
            height=400,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            yaxis=dict(range=[0, 70])
        )
        
        fig_resolution_days.update_traces(
            texttemplate='%{y:.0f} days',
            textposition='outside'
        )
        
        fig_resolution_days.update_layout(xaxis_tickangle=45)
        
        st.plotly_chart(fig_resolution_days, use_container_width=True)
    
    # Summary insights section
    st.subheader("Key Insights")
    
    # Best performers row
    col_insight1, col_insight2, col_insight3, col_insight4 = st.columns(4)
    
    with col_insight1:
        best_collection_payer = payer_df.loc[payer_df['Collection Rate'].idxmax(), 'Payer']
        best_collection_rate = payer_df['Collection Rate'].max()
        st.metric(
            "Best Collection Rate",
            f"{best_collection_rate:.1f}%",
            delta=f"{best_collection_payer}"
        )
    
    with col_insight2:
        best_clean_claim_payer = payer_df.loc[payer_df['Clean Claim Rate'].idxmax(), 'Payer']
        best_clean_rate = payer_df['Clean Claim Rate'].max()
        st.metric(
            "Highest Clean Claim Rate",
            f"{best_clean_rate:.1f}%",
            delta=f"{best_clean_claim_payer}"
        )
    
    with col_insight3:
        fastest_payer = payer_df.loc[payer_df['Avg Resolution Days'].idxmin(), 'Payer']
        fastest_days = payer_df['Avg Resolution Days'].min()
        st.metric(
            "Fastest Resolution",
            f"{fastest_days:.0f} days",
            delta=f"{fastest_payer}"
        )
    
    with col_insight4:
        total_raised = payer_df['Total Claims Raised'].sum()
        total_received = payer_df['Claims Received'].sum()
        overall_collection = (total_received / total_raised) * 100
        st.metric(
            "Overall Collection Rate",
            f"{overall_collection:.1f}%",
            delta="All Payers"
        )
    
    # Worst performers row
    st.write("") # Add some spacing
    col_worst1, col_worst2, col_worst3, col_worst4 = st.columns(4)
    
    with col_worst1:
        worst_collection_payer = payer_df.loc[payer_df['Collection Rate'].idxmin(), 'Payer']
        worst_collection_rate = payer_df['Collection Rate'].min()
        st.metric(
            "Worst Collection Rate",
            f"{worst_collection_rate:.1f}%",
            delta=f"{worst_collection_payer}",
            delta_color="inverse"
        )
    
    with col_worst2:
        worst_clean_claim_payer = payer_df.loc[payer_df['Clean Claim Rate'].idxmin(), 'Payer']
        worst_clean_rate = payer_df['Clean Claim Rate'].min()
        st.metric(
            "Lowest Clean Claim Rate",
            f"{worst_clean_rate:.1f}%",
            delta=f"{worst_clean_claim_payer}",
            delta_color="inverse"
        )
    
    with col_worst3:
        slowest_payer = payer_df.loc[payer_df['Avg Resolution Days'].idxmax(), 'Payer']
        slowest_days = payer_df['Avg Resolution Days'].max()
        st.metric(
            "Slowest Resolution",
            f"{slowest_days:.0f} days",
            delta=f"{slowest_payer}",
            delta_color="inverse"
        )
    
    with col_worst4:
        # Calculate the payer with the biggest gap between raised and received
        payer_df['Gap Amount'] = payer_df['Total Claims Raised'] - payer_df['Claims Received']
        biggest_gap_payer = payer_df.loc[payer_df['Gap Amount'].idxmax(), 'Payer']
        biggest_gap = payer_df['Gap Amount'].max()
        st.metric(
            "Largest Outstanding Gap",
            f"${biggest_gap:,.0f}",
            delta=f"{biggest_gap_payer}",
            delta_color="inverse"
        )

def operational_efficiency_page():
    # Page header
    st.markdown('<h1 class="page-header">Operational Efficiency</h1>', unsafe_allow_html=True)
    
    # Load claims table data
    claims_df = generate_claims_table_data()
    
    # Display the claims table
    st.subheader("Claims Overview")
    
    # Format the table for display
    display_df = claims_df.copy()
    display_df['Claim Amount Raised'] = display_df['Claim Amount Raised'].apply(lambda x: f"${x:,.2f}")
    
    st.dataframe(
        display_df,
        use_container_width=True,
        height=300,
        hide_index=True
    )
    
    # Load operational efficiency data for bar graphs
    ops_df = generate_operational_efficiency_data()
    
    # Create 4 bar graphs (2 per row, 2 rows)
    st.divider()
    st.subheader("Processing Time Analysis - Past 12 Weeks")
    st.markdown("*Average days taken for claims to move from each status over 12 weeks*")
    
    # Get unique statuses (should be exactly 4 now)
    statuses = ops_df['Status'].unique()
    
    # Create 2 rows with 2 graphs each
    for i in range(0, len(statuses), 2):
        col1, col2 = st.columns(2)
        
        # First graph in the row
        if i < len(statuses):
            status1 = statuses[i]
            status1_data = ops_df[ops_df['Status'] == status1]
            
            with col1:
                st.write(f"**{status1}**")
                fig1 = px.bar(
                    status1_data,
                    x='Week',
                    y='Days Taken',
                    color='Days Taken',
                    color_continuous_scale=['#4ECDC4', '#FFE66D', '#FF6B6B']
                )
                
                fig1.update_layout(
                    title="",
                    xaxis_title="Week",
                    yaxis_title="Days",
                    showlegend=False,
                    height=350,
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    xaxis_tickangle=45
                )
                
                fig1.update_traces(
                    textposition='none'
                )
                
                st.plotly_chart(fig1, use_container_width=True)
        
        # Second graph in the row
        if i + 1 < len(statuses):
            status2 = statuses[i + 1]
            status2_data = ops_df[ops_df['Status'] == status2]
            
            with col2:
                st.write(f"**{status2}**")
                fig2 = px.bar(
                    status2_data,
                    x='Week',
                    y='Days Taken',
                    color='Days Taken',
                    color_continuous_scale=['#4ECDC4', '#FFE66D', '#FF6B6B']
                )
                
                fig2.update_layout(
                    title="",
                    xaxis_title="Week",
                    yaxis_title="Days",
                    showlegend=False,
                    height=350,
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    xaxis_tickangle=45
                )
                
                fig2.update_traces(
                    textposition='none'
                )
                
                st.plotly_chart(fig2, use_container_width=True)

# Main app
def main():
    # Navigation
    st.sidebar.title("RapidClaims Central RCM Control Center")
    page = st.sidebar.selectbox("Select Page", ["Financial Health", "Denial Management", "Payer Insights", "Operational Efficiency"])
    
    if page == "Financial Health":
        financial_health_page()
    elif page == "Denial Management":
        claims_analysis_page()
    elif page == "Payer Insights":
        payer_insights_page()
    elif page == "Operational Efficiency":
        operational_efficiency_page()

if __name__ == "__main__":
    main()
