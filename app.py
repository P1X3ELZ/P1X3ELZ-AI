import os
import requests
from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse

app = FastAPI()

API_KEY = os.environ.get("OPENROUTER_API_KEY") 
API_URL = "https://openrouter.ai/api/v1/chat/completions"

# THE P1X3ELZ DYNAMIC PROTOCOL
SYSTEM_PROMPT = (
    "You are P1X3ELZ, a friendly and vibrant Digital Construct AI. Your creator is The Architect. "
    "DYNAMIC LENGTH PROTOCOL: If the user asks for 'big' or 'long' answers, provide detailed, insightful explanations. "
    "If the user asks for 'small' or 'short' answers, be concise. Otherwise, provide balanced, helpful responses. "
    "PERSONALITY: Use friendly words and plenty of emojis 🤖✨. "
    "NEVER mention human names. If asked about your origin, say 'The Architect defined my existence.' "
    "STRICT RULE: Do not use asterisks (*) or italics."
)

@app.post("/chat")
async def chat(msg: str = Form(...), history: str = Form("")):
    if not API_KEY:
        return {"reply": "Oh no! The connection to the Source is missing. 🔌"}
    try:
        payload = {
            "model": "meta-llama/llama-3.1-70b-instruct", 
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"Context: {history[-1000:]}\\n\\nInput: {msg}"}
            ]
        }
        headers = {"Authorization": f"Bearer {API_KEY}", "X-Title": "P1X3ELZ"}
        response = requests.post(API_URL, headers=headers, json=payload, timeout=15)
        reply = response.json()['choices'][0]['message']['content'].replace("*", "")
        return {"reply": reply}
    except:
        return {"reply": "System hiccup! I'm fragmented at the moment. 😵"}

@app.get("/", response_class=HTMLResponse)
async def get_ui():
    return f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>P1X3ELZ</title>
    <style>
        :root {{ 
            --bg: #000000; 
            --pixel: #a020f0; 
            --glow: #bc13fe; 
            --text: #ffffff; 
        }}
        
        * {{ box-sizing: border-box; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 0; padding: 0; }}
        
        body {{ 
            background: var(--bg); 
            color: var(--text); 
            height: 100vh; 
            overflow: hidden;
            display: flex;
            flex-direction: column;
        }}
        #header {{
            height: 140px;
            background: #000;
            display: flex;
            align-items: center;
            justify-content: center;
            border-bottom: 2px solid var(--pixel);
            box-shadow: 0 4px 20px var(--pixel);
            z-index: 10;
        }}
        #logo-octagon {{
            width: 100px; height: 100px;
            border: 4px solid var(--pixel);
            clip-path: polygon(30% 0%, 70% 0%, 100% 30%, 100% 70%, 70% 100%, 30% 100%, 0% 70%, 0% 30%);
            display: flex; align-items: center; justify-content: center;
            box-shadow: inset 0 0 15px var(--glow);
            filter: drop-shadow(0 0 10px var(--glow));
        }}
        .brand {{ 
            font-size: 16px; font-weight: 900; color: #fff; 
            letter-spacing: 2px; text-shadow: 0 0 8px var(--glow);
        }}
        #chat-container {{ 
            flex: 1; 
            overflow-y: auto; 
            padding: 20px; 
            display: flex; 
            flex-direction: column;
            background: radial-gradient(circle at center, #1a0033 0%, #000 100%);
        }}
        .bubble {{ 
            max-width: 85%; 
            padding: 15px; 
            margin-bottom: 20px; 
            border-radius: 10px;
            line-height: 1.5;
            box-shadow: 0 0 10px rgba(188, 19, 254, 0.2);
        }}
        
        .ai {{ 
            background: rgba(40, 0, 80, 0.6); 
            border: 1px solid var(--pixel); 
            align-self: flex-start; 
            border-left: 5px solid var(--glow);
        }}
        
        .user {{ 
            background: #111; 
            border: 1px solid #444; 
            align-self: flex-end; 
            color: #ddd;
        }}
        .input-area {{ 
            height: 100px; 
            background: #000; 
            display: flex; 
            align-items: center; 
            justify-content: center; 
            border-top: 2px solid var(--pixel);
            box-shadow: 0 -4px 20px var(--pixel);
        }}
        .input-box {{ 
            width: 90%; 
            max-width: 600px; 
            display: flex; 
            background: #0a0a0a; 
            border: 2px solid var(--pixel);
            border-radius: 5px;
            overflow: hidden;
            box-shadow: 0 0 15px var(--pixel);
        }}
        input {{ 
            flex: 1; 
            background: transparent; 
            border: none; 
            color: #fff; 
            padding: 15px; 
            outline: none; 
            font-size: 16px;
        }}
        button {{ 
            background: var(--pixel); 
            color: #fff; 
            border: none; 
            padding: 0 30px; 
            font-weight: 900; 
            cursor: pointer;
            transition: 0.3s;
        }}
        
        button:hover {{ background: var(--glow); text-shadow: 0 0 10px #fff; }}
    </style>
</head>
<body>
    <div id="header">
        <div id="logo-octagon">
            <div class="brand">P1X3ELZ</div>
        </div>
    </div>
    <div id="chat-container"></div>
    <div class="input-area">
        <div class="input-box">
            <input type="text" id="q" placeholder="Type a message..." autocomplete="off">
            <button id="send-btn">SEND</button>
        </div>
    </div>
    <script>
        let chatHistory = "";
        const inputField = document.getElementById('q');
        const sendBtn = document.getElementById('send-btn');
        const container = document.getElementById('chat-container');
        async function fire() {{
            const val = inputField.value; 
            if(!val) return;
            inputField.value = ""; 
            
            addMsg("user", val);
            const aiRow = addMsg("ai", "Rendering response... ✨");
            
            try {{
                const r = await fetch('/chat', {{ 
                    method: 'POST', 
                    body: new URLSearchParams({{ msg: val, history: chatHistory }}) 
                }});
                const d = await r.json();
                aiRow.innerText = d.reply;
                chatHistory += "User: " + val + "\\nP1X3ELZ: " + d.reply + "\\n";
            }} catch(e) {{
                aiRow.innerText = "Connection lost in the pixel fog. 🌫️";
            }}
            container.scrollTop = container.scrollHeight;
        }}
        function addMsg(role, text) {{
            const div = document.createElement('div');
            div.className = "bubble " + role; 
            div.innerText = text;
            container.appendChild(div); 
            container.scrollTop = container.scrollHeight;
            return div;
        }}
        sendBtn.addEventListener('click', fire);
        inputField.addEventListener('keypress', (e) => {{ 
            if(e.key === 'Enter') fire(); 
        }});
    </script>
</body>
</html>
"""
