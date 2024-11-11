from flask import Flask, request, jsonify, render_template
from gpt4all import GPT4All

# Initialize Flask app
app = Flask(__name__)

# Define the model path and type
model_path = "D:/Github/AI_chatbot_LLAMA-2.0/chatbot/model/"
model_type = "llama"

# Load the GPT4All model
print("Loading the model, please wait...")
try:
    # Here we pass a dummy model name ('local_model') since GPT4All expects it
    model = GPT4All(model_name="local_model", model_path=model_path, model_type=model_type, allow_download=False)
    print("Model loaded successfully!")
except Exception as e:
    print(f"Failed to load the model: {e}")
    exit(1)

# Function to generate a response from the chatbot
def chatbot_response(prompt):
    try:
        response = model.generate(prompt, max_tokens=150, temp=0.7, top_p=0.9)
        return response.strip()
    except Exception as e:
        return f"Error generating response: {str(e)}"

# API endpoint for chatbot interaction
@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message")
    if not user_input:
        return jsonify({"error": "No input provided"}), 400

    response = chatbot_response(user_input)
    return jsonify({"response": response})

# Serve the main HTML page
@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
