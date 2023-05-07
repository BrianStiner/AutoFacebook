from flask import Flask, render_template, request, jsonify
from threading import Lock
import conversation_script

app = Flask(__name__)
lock = Lock()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_conversation', methods=['POST'])
def get_conversation():
    with lock:
        conversation_script.main()
        with open("chat_output.txt", "r") as file:
            conversation = file.read()
    return jsonify(conversation=conversation)

if __name__ == "__main__":
    app.run(debug=True)
