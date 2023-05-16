from flask import Flask, render_template_string, request
from dotenv import load_dotenv
import openai
import os


load_dotenv()  # Load environment variables from .env file

openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)

@app.route("/")
def home():
    return render_template_string('''
        
<!DOCTYPE html>
<html>
    <head>
        <title>Osana Chat Friend</title>
        <style>
            body {
                background: linear-gradient(to right, #bdaaff, #eaa6ff);
                font-family: Arial, sans-serif;
                font-size: 14px;
                
                margin: 0;
            }

            h1 {
                background: linear-gradient(to left, #3d1abc, #b424e0);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                font-size: 100px;
                text-align: center;
              
               
            }
                 
            form {
                margin: 0;
                padding: 20px;
                display: flex;
                align-items: center;
                justify-content: center;
                flex-direction: column;
                
            }

            label {
                display: block;
                margin-bottom: 10px;
            }

            input[type="text"] {
                border: none;
                outline: none;
                padding: 10px;
                font-size: 16px;
                border-radius: 30px;
                background-color: #f3d8fc;
                box-shadow: 0 3px 10px rgba(0, 0, 0, 0.2);
                transition: all 0.5s ease-in-out;
                width: 80%;
                margin-bottom: 20px;
                flex-grow: 5;
                width: calc(100% - 80px);
                margin-right: 10px;
                position: fixed;
                bottom: 0;
                
            }

            input[type="text"]:focus {
                outline: none;
                box-shadow: 0 0 5px 2px #5f067a;
            }

            button[type="submit"] {
                background-color: #57047e;
                border: none;
                border-radius: 30px;
                color: white;
                cursor: pointer;
                font-size: 18px;
                padding: 10px 20px;
                transition: all 0.3s ease-in-out;
                position: fixed;
                bottom: 20px;
                right: 30px;
                height: 40px;
            }
            button[type="submit"] :hover {
                background-color: #ca06ca;
            }
        
            #response {
                margin: 0;
                padding: 20px;
                border-radius: 30px;
            }

            #response p {
                margin: 10px 0;
            }

            #response p:nth-child(odd) {
                border-radius: 20px 20px 20px 0;
                padding: 10px 20px;
                color: #fff;
                border: 1px solid transparent;
                background-image: linear-gradient(to right, #3d1abc, #b424e0);
            }

            #response p:nth-child(even) {
                background-color: #b424e0;
                border-radius: 20px 20px 0 20px;
                color: #fff;
                margin-left: 100px;
                padding: 10px 20px;
                border: 1px solid transparent;
                background-image: linear-gradient(to left, #3d1abc, #b424e0);
            }

            #response p:last-child {
                border-radius: 0 0 20px 20px;
            }
        </style>
    </head>
    <body>
        <h1>Osana Chat Friend</h1>
        <div id="response"></div>
        <form action="/chat" method="POST">
            <input type="text" id="user_input" name="user_input" placeholder="Type your message...">
            <button type="submit">Send</button>
            
        </form>
        <script>
            const form = document.querySelector("form");
            const responseDiv = document.querySelector("#response");
            form.addEventListener("submit", function(event)
 {
                event.preventDefault();
                const user_input = document.querySelector("#user_input").value;
                fetch("/chat", {
                    method: "POST",
                    body: new URLSearchParams({"user_input": user_input})
                })
                .then(response => response.json())
                .then(data => {
                    responseDiv.innerHTML += `<p>You: ${user_input}</p>`;
                    responseDiv.innerHTML += `<p>Osana: ${data.ai_response} ${data.emoji}</p>`;
                    document.querySelector("#user_input").value = "";
                });
            });
        </script>
    </body>
</html>
    ''')

@app.route("/chat", methods=["POST"])
def chat():
    
    user_input = request.form["user_input"]

    def generate_emoji(text):
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=f"Convert this text into emoji.\n happy: 😁😂🤣😃😄😆 \n {text}",
            temperature=0.8,
            max_tokens=60,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0,
            stop=["\n"]
        )
        return response.choices[0].text.strip()

    def generate_response(prompt):
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0.7,
        )
        return response.choices[0].text.strip()

    prompt = f"User: {user_input} Osana:"
    ai_response = generate_response(prompt)
    emoji = generate_emoji(ai_response)


    return {"ai_response": ai_response, "emoji": emoji}

if __name__ == "__main__":
    app.run(debug=True)
