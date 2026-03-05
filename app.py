from flask import Flask, request, jsonify, render_template
import json
import os

app = Flask(__name__)


def load_rules(lang="en"):
    """Load the correct rules JSON based on selected language."""
    filename = "rules_ta.json" if lang == "ta" else "rules_en.json"
    rules_path = os.path.join(os.path.dirname(__file__), filename)
    with open(rules_path, "r", encoding="utf-8") as f:
        return json.load(f)


def match_rule(user_input, lang="en"):
    """Match user input against keywords in the appropriate language rules file."""
    rules = load_rules(lang)
    user_input_lower = user_input.lower()

    for rule in rules:
        keywords = rule.get("keywords", [])
        for keyword in keywords:
            if keyword.lower() in user_input_lower:
                return rule
    return None


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/process", methods=["POST"])
def process():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No input provided"}), 400

    user_input = data.get("message", "")
    lang = data.get("lang", "en")

    # Match against the correct language JSON
    matched_rule = match_rule(user_input, lang)

    if matched_rule:
        title = matched_rule.get("title", "")
        steps = matched_rule.get("steps", [])
        warning = matched_rule.get("warning", "")
        category = matched_rule.get("category", "")

        response = {
            "title": title,
            "steps": steps,
            "category": category,
        }

        if warning:
            response["warning"] = warning

        return jsonify(response)

    # Fallback message in the correct language
    return jsonify({
        "response": (
            "மன்னிக்கவும், புரியவில்லை. மீண்டும் முயற்சிக்கவும்."
            if lang == "ta"
            else "Sorry, I could not understand. Please try again."
        )
    })


if __name__ == "__main__":
    app.run(debug=True)
