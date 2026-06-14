import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

# Retrieve API Key
api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")

if api_key:
    genai.configure(api_key=api_key)

MODELS_TO_TRY = [
    "gemini-2.0-flash",
    "gemini-1.5-flash",
    "gemini-3-flash-preview"
]

def generate_content_with_fallback(prompt):
    if not api_key:
        raise ValueError("Gemini API key is not configured. Please add GOOGLE_API_KEY or GEMINI_API_KEY to your environment variables or Streamlit secrets.")
    
    last_error = None
    for model_name in MODELS_TO_TRY:
        try:
            model = genai.GenerativeModel(model_name)
            response = model.generate_content(
                prompt,
                request_options={"timeout": 10.0}
            )
            return response.text
        except Exception as e:
            last_error = e
            # Log or continue to the next model fallback
            continue
            
    # If all models failed, raise the last encountered exception
    raise last_error if last_error else RuntimeError("Failed to generate content using all available models.")


def explain(stock, risk, cagr):
    prompt = f"""
    Explain this stock in simple terms.

    Stock: {stock}
    Risk: {risk}
    CAGR: {round(cagr*100,2)}%

    Give 4 concise bullet points.
    """

    try:
        return generate_content_with_fallback(prompt)
    except Exception as e:
        return f"Error generating explanation: {e}"


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

    try:
        res = generate_content_with_fallback(prompt)
        return res.strip()
    except Exception as e:
        return f"Could not generate AI comparison insights: {e}"


if __name__ == "__main__":
    # Test the API connection directly
    print("Testing Gemini API connection...")
    try:
        print("\n--- Testing Single Explainer ---")
        test_explanation = explain("TCS.NS", "Low", 0.15)
        print("Response:")
        print(test_explanation)
        
        print("\n--- Testing Comparison Explainer ---")
        test_data = [
            {"symbol": "TCS.NS", "risk": "Low", "cagr": 0.15},
            {"symbol": "AAPL", "risk": "Medium", "cagr": 0.18},
            {"symbol": "TSLA", "risk": "High", "cagr": 0.28}
        ]
        test_comp = explain_comparison(test_data)
        print("Response:")
        print(test_comp)
    except Exception as e:
        print(f"Error during API call: {e}")