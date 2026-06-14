import streamlit as st
import pandas as pd

from services.stock_data import get_stock_data
from services.forecast import (
    calculate_cagr,
    forecast_values
)
from services.risk import calculate_risk
from utils.ai_explainer import explain, explain_comparison

# 1. Page Configuration
st.set_page_config(
    page_title="AI Investment Simulator",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. Inject Premium Custom CSS (Minimalistic Light Theme)
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap');

    /* Background and Typography */
    .stApp {
        background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 50%, #e2e8f0 100%);
        color: #334155;
        font-family: 'Outfit', sans-serif;
    }
    
    /* Headers styling */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Outfit', sans-serif !important;
        font-weight: 700 !important;
        color: #0f172a !important;
    }

    .main-title {
        background: linear-gradient(135deg, #4f46e5 0%, #3b82f6 50%, #06b6d4 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        font-size: 2.8rem;
        margin-bottom: 0.3rem;
        text-align: left;
        letter-spacing: -0.03em;
    }

    .subtitle {
        color: #64748b;
        font-size: 1.1rem;
        margin-bottom: 2rem;
        font-weight: 400;
    }

    /* Glassmorphic Card Container */
    .glass-card {
        background: rgba(255, 255, 255, 0.7);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.6);
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 10px 30px -10px rgba(15, 23, 42, 0.05);
        margin-bottom: 24px;
    }

    /* Section Subheaders */
    .section-header {
        font-size: 1.25rem;
        font-weight: 600;
        color: #1e293b;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
        border-bottom: 1px solid rgba(0, 0, 0, 0.06);
        padding-bottom: 6px;
    }

    /* Side-by-Side Comparison Table */
    .glass-table {
        width: 100%;
        border-collapse: collapse;
        margin-top: 10px;
    }

    .glass-table th {
        font-family: 'Outfit', sans-serif;
        color: #475569;
        font-weight: 600;
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        padding: 14px 16px;
        text-align: right;
        border-bottom: 2px solid rgba(0, 0, 0, 0.06);
    }

    .glass-table th:first-child {
        text-align: left;
    }

    .glass-table td {
        padding: 16px;
        font-size: 0.95rem;
        color: #334155;
        border-bottom: 1px solid rgba(0, 0, 0, 0.04);
        font-variant-numeric: tabular-nums;
    }

    .glass-table tr:hover {
        background: rgba(255, 255, 255, 0.5);
    }

    .glass-lift {
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }

    .glass-lift:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(15, 23, 42, 0.03);
    }

    /* Risk Badges */
    .risk-badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 9999px;
        font-size: 0.8rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    .risk-low {
        background: rgba(16, 185, 129, 0.12);
        color: #059669;
        border: 1px solid rgba(16, 185, 129, 0.2);
    }
    
    .risk-medium {
        background: rgba(245, 158, 11, 0.12);
        color: #d97706;
        border: 1px solid rgba(245, 158, 11, 0.2);
    }
    
    .risk-high {
        background: rgba(239, 68, 68, 0.12);
        color: #dc2626;
        border: 1px solid rgba(239, 68, 68, 0.2);
        animation: pulse-badge 2s infinite ease-in-out;
    }

    .risk-unknown {
        background: rgba(100, 116, 139, 0.12);
        color: #475569;
        border: 1px solid rgba(100, 116, 139, 0.2);
    }

    @keyframes pulse-badge {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.7; }
    }

    /* AI Explainer Container */
    .ai-explainer {
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.05) 0%, rgba(168, 85, 247, 0.05) 100%);
        border: 1px solid rgba(99, 102, 241, 0.15);
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 4px 15px rgba(99, 102, 241, 0.02);
        margin-top: 15px;
    }

    .ai-header {
        font-size: 0.85rem;
        color: #4f46e5;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin-bottom: 12px;
        display: flex;
        align-items: center;
        gap: 6px;
    }

    /* Form Fields Styling override */
    div[data-baseweb="select"] > div, div[data-baseweb="input"] > div {
        background-color: rgba(255, 255, 255, 0.9) !important;
        border: 1px solid rgba(0, 0, 0, 0.08) !important;
        border-radius: 10px !important;
        color: #000000 !important;
    }

    /* Force text inside inputs and textareas to be true black for high legibility */
    input, textarea {
        color: #000000 !important;
        -webkit-text-fill-color: #000000 !important;
    }

    /* Primary Button Styling */
    .stButton>button {
        background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 10px 24px !important;
        font-weight: 600 !important;
        font-size: 16px !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 4px 12px rgba(99, 102, 241, 0.15) !important;
        width: 100% !important;
        margin-top: 15px;
    }

    .stButton>button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(99, 102, 241, 0.25) !important;
        border: none !important;
    }

    .stButton>button:active {
        transform: translateY(1px) !important;
    }
    
    .help-text {
        font-size: 0.8rem;
        color: #475569 !important;
        margin-top: -8px;
        margin-bottom: 12px;
    }

    /* Force dark text for all Streamlit widget labels, descriptions, and markdown text for high readability */
    div[data-testid="stWidgetLabel"] p,
    div[data-testid="stWidgetLabel"],
    label,
    .stSlider label,
    .stSlider p,
    div[data-testid="stMarkdownContainer"] p,
    div[data-testid="stMarkdownContainer"] span,
    div[data-testid="stMarkdownContainer"] li,
    div[data-baseweb="select"] div,
    .stMarkdown p,
    .help-text {
        color: #1e293b !important;
    }

    /* Customize Streamlit multiselect tag pills for clean minimalistic light theme (overriding red/white pills) */
    span[data-baseweb="tag"] {
        background-color: #f1f5f9 !important;
        color: #0f172a !important;
        border: 1px solid #cbd5e1 !important;
        border-radius: 6px !important;
    }
    span[data-baseweb="tag"] span {
        color: #0f172a !important;
    }
    span[data-baseweb="tag"] svg {
        fill: #475569 !important;
    }
    
    /* Dropdown options text color */
    div[role="listbox"] li {
        color: #0f172a !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# 3. App Title
st.markdown('<div class="main-title">Stock Comparison Terminal</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Evaluate and compare growth, risks, and forecasts of multiple stocks side-by-side (Minimalist Light Theme).</div>', unsafe_allow_html=True)

# 4. Popular Stocks Dictionary mapping friendly names to Yahoo Finance symbols
POPULAR_STOCKS = {
    "Tata Consultancy Services (TCS)": "TCS.NS",
    "Reliance Industries (RELIANCE)": "RELIANCE.NS",
    "Infosys Limited (INFY)": "INFY.NS",
    "HDFC Bank (HDFCBANK)": "HDFCBANK.NS",
    "ICICI Bank (ICICIBANK)": "ICICIBANK.NS",
    "Tata Steel (TATASTEEL)": "TATASTEEL.NS",
    "ITC Limited (ITC)": "ITC.NS",
    "State Bank of India (SBIN)": "SBIN.NS",
    "Apple Inc. (AAPL)": "AAPL",
    "Microsoft Corporation (MSFT)": "MSFT",
    "Alphabet Inc. (GOOGL)": "GOOGL",
    "Amazon.com Inc. (AMZN)": "AMZN",
    "Tesla Inc. (TSLA)": "TSLA",
    "NVIDIA Corporation (NVDA)": "NVDA",
    "Meta Platforms (META)": "META"
}

# Helper function to generate dynamic SVG sparkline for 30D trend
def generate_svg_sparkline(prices):
    if len(prices) == 0:
        return ""
    # Take the last 30 days
    prices = list(prices[-30:])
    min_p, max_p = min(prices), max(prices)
    range_p = max_p - min_p if max_p != min_p else 1
    
    # Green if last price is higher than start of the 30-day window, else red
    stroke_color = "#059669" if prices[-1] >= prices[0] else "#dc2626"
    
    points = []
    for idx, p in enumerate(prices):
        x = (idx / (len(prices) - 1)) * 100
        y = 28 - ((p - min_p) / range_p) * 26
        points.append(f"{x:.1f},{y:.1f}")
    
    path_data = "M " + " L ".join(points)
    return f"""
    <svg style="width: 100px; height: 30px; fill: none; stroke: {stroke_color}; stroke-width: 2; stroke-linecap: round; stroke-linejoin: round;" viewBox="0 0 100 30">
        <path d="{path_data}"></path>
    </svg>
    """

# 5. Two-column Layout: Inputs on left, Results on right
col_input, col_results = st.columns([1, 2], gap="large")

with col_input:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("Simulation Parameters")
    
    selected_stocks = st.multiselect(
        "Stock Selection",
        options=list(POPULAR_STOCKS.keys()),
        default=["Tata Consultancy Services (TCS)", "Apple Inc. (AAPL)"],
        help="Select one or more popular stocks to compare."
    )
    
    custom_symbols = st.text_input(
        "Custom Stock Symbol(s)",
        value="",
        help="Enter custom symbols separated by commas (e.g. MSFT, TSLA, RELIANCE.NS)"
    ).strip()
    
    # Process symbols
    symbols = []
    for name in selected_stocks:
        symbols.append(POPULAR_STOCKS[name])
        
    if custom_symbols:
        custom_list = [sym.strip().upper() for sym in custom_symbols.split(",") if sym.strip()]
        for sym in custom_list:
            if sym not in symbols:
                symbols.append(sym)
                
    # Limit to max 4 to avoid horizontal overflow
    if len(symbols) > 4:
        st.warning("Comparison layout supports up to 4 stocks. Showing the first 4.")
        symbols = symbols[:4]
        
    investment = st.number_input(
        "Investment Amount (₹)",
        value=10000,
        min_value=1,
        step=1000
    )
    
    years = st.slider(
        "Investment Horizon (Years)",
        min_value=1,
        max_value=10,
        value=5
    )
    
    analyze_btn = st.button("Run Simulation")
    st.markdown('</div>', unsafe_allow_html=True)

with col_results:
    if analyze_btn:
        if not symbols:
            st.error("Please select at least one stock or enter a custom symbol.")
        else:
            with st.spinner("Analyzing stock data and generating comparative AI insights..."):
                stocks_results = []
                fetch_errors = []
                
                for symbol in symbols:
                    try:
                        data = get_stock_data(symbol)
                        if data.empty or "Close" not in data.columns:
                            fetch_errors.append(f"No price data found for '{symbol}'")
                            continue
                            
                        # Clean data
                        data = data.dropna(subset=["Close"])
                        if len(data) < 2:
                            fetch_errors.append(f"Not enough price data for '{symbol}'")
                            continue
                            
                        start_price = data["Close"].iloc[0]
                        end_price = data["Close"].iloc[-1]
                        current_price = end_price
                        
                        actual_years = (data.index[-1] - data.index[0]).days / 365.25
                        if actual_years <= 0:
                            actual_years = 1.0
                            
                        cagr = calculate_cagr(start_price, end_price, actual_years)
                        forecasts = forecast_values(investment, cagr, years)
                        risk = calculate_risk(data)
                        
                        # Generate sparkline
                        sparkline_svg = generate_svg_sparkline(data["Close"])
                        
                        stocks_results.append({
                            "symbol": symbol,
                            "current_price": current_price,
                            "cagr": cagr,
                            "forecasts": forecasts,
                            "risk": risk,
                            "sparkline": sparkline_svg
                        })
                    except Exception as e:
                        fetch_errors.append(f"Error fetching '{symbol}': {e}")
                        
                for err in fetch_errors:
                    st.error(err)
                    
                if not stocks_results:
                    st.error("Unable to run simulation for any of the selected stocks.")
                else:
                    # Render side-by-side comparison table in a glass card
                    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                    st.markdown('<div class="section-header">Performance & Volatility Matrix</div>', unsafe_allow_html=True)
                    
                    # Create HTML table
                    table_html = '<table class="glass-table">'
                    
                    # Header row
                    table_html += '<tr><th>Metric</th>'
                    for res in stocks_results:
                        table_html += f'<th>{res["symbol"]}</th>'
                    table_html += '</tr>'
                    
                    # Current Price row
                    table_html += '<tr class="glass-lift"><td><b>Current Price</b></td>'
                    for res in stocks_results:
                        # Format currency based on whether it is US or Indian
                        currency_symbol = "$" if not res["symbol"].endswith(".NS") else "₹"
                        table_html += f'<td style="text-align: right; font-weight: 600;">{currency_symbol}{res["current_price"]:,.2f}</td>'
                    table_html += '</tr>'
                    
                    # 5-Year CAGR row
                    table_html += '<tr class="glass-lift"><td><b>5-Year CAGR</b></td>'
                    for res in stocks_results:
                        cagr_val = res["cagr"] * 100
                        cagr_color = "#059669" if cagr_val >= 0 else "#dc2626"
                        table_html += f'<td style="text-align: right; color: {cagr_color}; font-weight: 600;">{cagr_val:+.2f}%</td>'
                    table_html += '</tr>'
                    
                    # Conservative Forecast row
                    table_html += '<tr class="glass-lift"><td><b>Conservative Forecast</b></td>'
                    for res in stocks_results:
                        val = res["forecasts"]["conservative"]
                        table_html += f'<td style="text-align: right; color: #475569;">₹{val:,.0f}</td>'
                    table_html += '</tr>'
                    
                    # Expected Forecast row
                    table_html += '<tr class="glass-lift"><td><b>Expected Forecast</b></td>'
                    for res in stocks_results:
                        val = res["forecasts"]["expected"]
                        table_html += f'<td style="text-align: right; font-weight: 600; color: #4f46e5;">₹{val:,.0f}</td>'
                    table_html += '</tr>'
                    
                    # Optimistic Forecast row
                    table_html += '<tr class="glass-lift"><td><b>Optimistic Forecast</b></td>'
                    for res in stocks_results:
                        val = res["forecasts"]["optimistic"]
                        table_html += f'<td style="text-align: right;">₹{val:,.0f}</td>'
                    table_html += '</tr>'
                    
                    # Volatility Risk row
                    table_html += '<tr class="glass-lift"><td><b>Volatility Risk</b></td>'
                    for res in stocks_results:
                        risk_lower = res["risk"].lower()
                        if risk_lower not in ["low", "medium", "high"]:
                            risk_lower = "unknown"
                        table_html += f'<td style="text-align: right;"><span class="risk-badge risk-{risk_lower}">{res["risk"]}</span></td>'
                    table_html += '</tr>'
                    
                    # 30D Trend Sparkline row
                    table_html += '<tr class="glass-lift"><td><b>30-Day Price Trend</b></td>'
                    for res in stocks_results:
                        table_html += f'<td style="text-align: right; vertical-align: middle;">{res["sparkline"]}</td>'
                    table_html += '</tr>'
                    
                    table_html += '</table>'
                    
                    st.markdown(table_html, unsafe_allow_html=True)
                    
                    # Run AI Comparison Explainer
                    st.markdown('<div class="section-header" style="margin-top: 2.5rem;">AI Comparison & Insights</div>', unsafe_allow_html=True)
                    try:
                        # Prepare comparison details for Gemini
                        ai_data = [{"symbol": res["symbol"], "risk": res["risk"], "cagr": res["cagr"]} for res in stocks_results]
                        analysis_text = explain_comparison(ai_data)
                        
                        st.markdown(
                            f"""
                            <div class="ai-explainer">
                                <div class="ai-header">
                                    <span>✨</span> Gemini AI Multi-Stock Analyzer
                                </div>
                                <div style="font-size: 0.95rem; color: #334155; line-height: 1.6; font-weight: 400;">
                                    {analysis_text}
                                </div>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
                    except Exception as e:
                        st.error(f"Could not generate AI comparison insights: {e}")
                        
                    st.markdown('</div>', unsafe_allow_html=True)
    else:
        # Initial Landing Display when simulator hasn't run yet (Light Theme styled)
        st.markdown(
            """
            <div class="glass-card" style="text-align: center; padding: 60px 40px; border-style: dashed; border-color: rgba(0, 0, 0, 0.1); background: rgba(255,255,255,0.45);">
                <div style="font-size: 4rem; margin-bottom: 20px;">📊</div>
                <h3 style="color: #0f172a; font-weight: 600; margin-bottom: 10px;">Ready to Compare</h3>
                <p style="color: #475569; max-width: 500px; margin: 0 auto; line-height: 1.5;">
                    Select multiple stocks from the left panel (or enter custom symbols), specify your budget, and click <b>Run Simulation</b> to see side-by-side growth CAGR forecasts, risk analysis, and generative comparative AI insights.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )