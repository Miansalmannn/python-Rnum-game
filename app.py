from flask import Flask, render_template_string, request, session, redirect, url_for
import random

app = Flask(__name__)
app.secret_key = 'any_secret_key_here'  # needed for sessions
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>🎯 Number Guessing Game</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-900 text-gray-100 min-h-screen flex items-center justify-center">
    <div class="bg-gray-800 p-8 rounded-2xl shadow-lg w-full max-w-md text-center">
        <h1 class="text-3xl font-bold mb-4">🎯 Number Guessing Game</h1>
        <p class="mb-4">{{ message }}</p>

        {% if attempts_left > 0 and not guessed %}
        <form method="post" class="space-y-4">
            <input type="text" name="guess" placeholder="Enter your guess"
                   class="w-full px-4 py-2 rounded-md border border-gray-600 bg-gray-700 focus:outline-none focus:ring-2 focus:ring-blue-500"
                   autofocus required>
            <button type="submit"
                    class="w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 rounded-md transition duration-200">
                Guess
            </button>
        </form>
        <p class="mt-4">Attempts left: <span class="px-3 py-1 bg-yellow-500 text-black rounded-full">{{ attempts_left }}</span></p>
        {% endif %}

        {% if guessed or attempts_left == 0 %}
        <a href="{{ url_for('reset') }}"
           class="inline-block mt-6 bg-green-600 hover:bg-green-700 text-white font-semibold px-6 py-2 rounded-md transition duration-200">
            Play again
        </a>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    # Initialize game if not started
    if "number_to_guess" not in session:
        session["number_to_guess"] = random.randint(1, 100)
        session["attempts"] = 0
        session["max_attempts"] = 3
        session["guessed"] = False

    message = "I'm thinking of a number between 1 and 100."
    guessed = session.get("guessed", False)

    if request.method == "POST":
        guess_input = request.form.get("guess", "")
        if not guess_input.isdigit():
            message = "Please enter a valid number."
        else:
            guess = int(guess_input)
            session["attempts"] += 1
            if guess < session["number_to_guess"]:
                message = f"Too low! Try again."
            elif guess > session["number_to_guess"]:
                message = f"Too high! Try again."
            else:
                message = f"🎉 Congratulations! You guessed it in {session['attempts']} attempts."
                session["guessed"] = True

    attempts_left = session["max_attempts"] - session["attempts"]

    if attempts_left == 0 and not session.get("guessed"):
        message = f"😢 Oops! You're out of attempts. The number was {session['number_to_guess']}."

    return render_template_string(HTML_TEMPLATE, message=message, attempts_left=attempts_left, guessed=session.get("guessed"))

@app.route("/reset")
def reset():
    session.pop("number_to_guess", None)
    session.pop("attempts", None)
    session.pop("max_attempts", None)
    session.pop("guessed", None)
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)
