import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

genai.configure(
    api_key=os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
)

model = genai.GenerativeModel(
    "gemini-3-flash-preview"
)

def explain(stock, risk, cagr):

    prompt = f"""
    Explain this stock in simple terms.

    Stock: {stock}
    Risk: {risk}
    CAGR: {round(cagr*100,2)}%

    Give 4 concise bullet points.
    """

    response = model.generate_content(
        prompt
    )

    return response.text


def explain_comparison(stocks_data):
    """
    Generate comparative analysis for multiple stocks.
    stocks_data: list of dicts like [{"symbol": "MSFT", "risk": "Low", "cagr": 0.18}, ...]
    """
    details = []
    for s in stocks_data:
        cagr_pct = f"{round(s['cagr'] * 100, 2)}%"
        details.append(f"Stock: {s['symbol']} | Risk Level: {s['risk']} | 5-Year CAGR: {cagr_pct}")
    
    stocks_str = "\n".join(details)
    
    prompt = f"""
    You are an expert financial analyst. Analyze and compare the following stocks side-by-side:

    {stocks_str}

    Provide a concise, professional comparison of these stocks. Highlight key differences in their risk-to-reward ratios and growth rates.
    Keep your response to exactly 3 sentences. Do not use markdown bullet points or bold text in the sentences, just write a continuous paragraph.
    """

    response = model.generate_content(
        prompt
    )

    return response.text.strip()


if __name__ == "__main__":
    # Test the API connection directly
    print("Testing Gemini API connection...")
    try:
        print("\n--- Testing Single Explainer ---")
        test_explanation = explain("TCS.NS", "Low", 0.15)
        print("Success! Response:")
        print(test_explanation)
        
        print("\n--- Testing Comparison Explainer ---")
        test_data = [
            {"symbol": "TCS.NS", "risk": "Low", "cagr": 0.15},
            {"symbol": "AAPL", "risk": "Medium", "cagr": 0.18},
            {"symbol": "TSLA", "risk": "High", "cagr": 0.28}
        ]
        test_comp = explain_comparison(test_data)
        print("Success! Response:")
        print(test_comp)
    except Exception as e:
        print(f"Error during API call: {e}")