from flask import Flask, request, jsonify, send_from_directory
import pandas as pd
import re
import requests
import json
from datetime import datetime

app = Flask(__name__)

# === Load dataset ===
try:
    df = pd.read_excel('aka_studio_designs.xlsx')
    print("✅ Excel file loaded successfully.")
except Exception as e:
    print(f"❌ Error loading Excel file: {e}")
    df = pd.DataFrame()

# === Local LLM URL ===
LOCAL_LLM_URL = "http://127.0.0.1:8000/generate"

# === Power Automate Flow URL ===
POWER_AUTOMATE_URL = "https://prod-17.australiasoutheast.logic.azure.com:443/workflows/6d87bbd2a85e41ba94b1e47f1cc85e20/triggers/manual/paths/invoke?api-version=2016-06-01&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=rWQeysCtuYyR0flTB8T1y0BOPifTVmSHPRzceXKMfck"

# === History file ===
HISTORY_FILE = "chat_history.jsonl"

# === Helpers ===

def log(msg):
    print(f"[{datetime.now()}] {msg}")

def clean_budget_text(budget_text):
    digits = re.findall(r'\d+', str(budget_text))
    return int(digits[0]) if digits else 0

def clean_timeline_text(timeline_text):
    digits = re.findall(r'\d+', str(timeline_text))
    return int(digits[0]) if digits else 0

def local_llm_generate(prompt):
    try:
        res = requests.post(LOCAL_LLM_URL, json={"text": prompt})
        res.raise_for_status()
        return res.json()["reply"]
    except Exception as e:
        log(f"❌ Local LLM failed: {e}")
        return "Couldn’t generate summary — please try again."

def guess_logo_idea(company_name, business_type):
    name = company_name.lower()
    btype = business_type.lower()
    if "burger" in name or "burger" in btype:
        return "🍔 Burger icon with playful style"
    elif "juice" in name or "fruit" in name or "juice" in btype:
        return "🍍 Fruit splash icon"
    elif "tech" in name or "computer" in name or "technology" in btype:
        return "💻 Circuit or pixel icon"
    elif "gaming" in name or "game" in btype:
        return "🎮 Game controller"
    elif "coffee" in name or "cafe" in name or "coffee" in btype:
        return "☕ Coffee cup"
    elif "music" in name or "music" in btype:
        return "🎵 Music note"
    else:
        return f"🔆 Symbol for {business_type}"

# === Serve static ===

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/<path:path>')
def static_files(path):
    return send_from_directory('.', path)

# === Health check ===

@app.route('/api/ping')
def ping():
    return jsonify({"status": "✅ Server is running."})

# === Chat API ===

@app.route('/api/chat', methods=['POST'])
def chat():
    if df.empty:
        return jsonify({"reply": "❌ No design data available. Please check your Excel file."})

    data = request.json

    company_name = data.get('company_name', '').strip()
    business_type = data.get('business_type', '').strip()
    brand_theme = data.get('brand_theme', '').strip()
    logo_idea = data.get('logo_idea', '').strip()
    interior_theme = data.get('interior_theme', '').strip()
    colours = data.get('colours', '').strip()
    signage = data.get('signage', '').strip()
    materials = data.get('materials', '').strip()
    budget_raw = str(data.get('budget', '')).strip()
    timeline_raw = str(data.get('timeline', '')).strip()

    # === Basic input check ===
    if not company_name or not business_type:
        return jsonify({"reply": "❌ Please provide both company name and business type."})

    budget = clean_budget_text(budget_raw)
    timeline = clean_timeline_text(timeline_raw)
    timeline_label = f"{timeline} week{'s' if timeline != 1 else ''}"

    # === Improved dataset fallback ===
    theme_words = [w for w in brand_theme.lower().split() if w]
    type_words = [w for w in business_type.lower().split() if w]

    theme_mask = df['Brand Theme'].str.lower().apply(
        lambda theme: any(word in theme for word in theme_words)
    )

    type_mask = df['Business Type'].str.lower().apply(
        lambda btype: any(word in btype for word in type_words)
    )

    match = df[type_mask & theme_mask]
    row = match.iloc[0] if not match.empty else None

    if row is not None:
        if not interior_theme: interior_theme = row['Interior Theme']
        if not colours: colours = row['Typical Colours']
        if not signage: signage = row['Recommended Signage']
        if not materials: materials = row['Materials']
        if not budget: budget = clean_budget_text(row['Budget Range'])
        if not timeline: timeline = clean_timeline_text(row['Timeline'])
    else:
        log("⚠️ No dataset match — using user inputs only.")

    if not logo_idea:
        logo_idea = guess_logo_idea(company_name, business_type)

    # === Build suggestion ===
    raw_suggestion = f"""
📌 **Logo Idea:** {logo_idea}
🎨 **Colors:** {colours or 'N/A'}
🪑 **Interior Theme:** {interior_theme or 'N/A'}
🖼️ **Signage:** {signage or 'N/A'}
🧱 **Materials:** {materials or 'N/A'}
💰 **Budget:** ${budget}
⏳ **Timeline:** {timeline_label}
"""

    # === Build prompt ===
    prompt = f"""
The project is for a {business_type} called "{company_name}" with a budget of ${budget} and timeline of {timeline_label}.

Rewrite this suggestion clearly in proper english language:
{raw_suggestion}

Guidelines:
- Speak directly: use 'your', not 'client'.
- Do not use greetings or sign off.
- Write 4–6 short paragraphs.
- Naturally use at least 2 emojis per idea.
- End with a practical, cheerful final tip with a fun emoji.
"""

    log("✨ Sending design brief to TinyLlama...")
    ai_summary = local_llm_generate(prompt)
    final_reply = ai_summary.strip()

    # Save history
    record = {
        "timestamp": datetime.now().isoformat(),
        "company": company_name,
        "business_type": business_type,
        "budget": budget,
        "timeline": timeline,
        "summary": final_reply
    }
    with open(HISTORY_FILE, "a") as f:
        f.write(json.dumps(record) + "\n")

    return jsonify({
        "reply": final_reply,
        "company": company_name,
        "budget": budget,
        "timeline": timeline
    })

# === History route ===

@app.route('/api/history', methods=['GET'])
def get_history():
    try:
        with open(HISTORY_FILE, "r") as f:
            lines = f.readlines()
        return jsonify([json.loads(line) for line in lines])
    except Exception as e:
        log(f"❌ Error reading history: {e}")
        return jsonify([])

# === Power Automate save route ===
@app.route('/api/save', methods=['POST'])
def save_to_sharepoint():
    data = request.json

    try:
        budget_clean = clean_budget_text(data.get('budget'))
        timeline_clean = clean_timeline_text(data.get('timeline'))

        payload = {
            "FullName": data.get('full_name'),
            "CompanyName": data.get('company_name'),
            "BusinessType": data.get('business_type'),
            "BrandTheme": data.get('brand_theme'),
            "Budget": budget_clean,     
            "Timeline": timeline_clean,  
            "Summary": data.get('summary')
        }

        log(f"➡️ Sending payload to Power Automate: {payload}")

        res = requests.post(POWER_AUTOMATE_URL, json=payload)
        res.raise_for_status()
        return jsonify({"status": "✅ Data sent to SharePoint!"}), 200

    except Exception as e:
        log(f"❌ Error sending to Power Automate: {e}")
        return jsonify({"status": "❌ Failed to send to SharePoint"}), 500

# === Error handler ===

@app.errorhandler(500)
def internal_error(e):
    return jsonify({"error": "💥 Internal server error occurred."}), 500

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
