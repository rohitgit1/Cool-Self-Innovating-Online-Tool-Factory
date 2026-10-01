import os
import random
import sys

# A collection of pre-made, high-quality, relevant single-file web tools.
TOOLS = [
    {
        "name": "json-formatter",
        "html": """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>JSON Formatter & Validator</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; padding: 2rem; max-width: 800px; margin: 0 auto; background: #f9fafb; color: #111827; }
        h1 { text-align: center; color: #2563eb; }
        textarea { width: 100%; height: 250px; padding: 1rem; border: 1px solid #d1d5db; border-radius: 0.5rem; font-family: monospace; font-size: 14px; margin-bottom: 1rem; box-sizing: border-box; }
        button { background: #2563eb; color: white; border: none; padding: 0.75rem 1.5rem; border-radius: 0.5rem; cursor: pointer; font-weight: bold; width: 100%; margin-bottom: 1rem; }
        button:hover { background: #1d4ed8; }
        .error { color: #dc2626; margin-top: 1rem; font-weight: bold; }
        pre { background: #1f2937; color: #f3f4f6; padding: 1rem; border-radius: 0.5rem; overflow-x: auto; display: none; }
    </style>
</head>
<body>
    <h1>JSON Formatter & Validator</h1>
    <textarea id="input" placeholder="Paste your JSON here..."></textarea>
    <button onclick="formatJSON()">Format & Validate JSON</button>
    <div id="error" class="error"></div>
    <pre id="output"></pre>
    <script>
        function formatJSON() {
            const input = document.getElementById('input').value;
            const errorDiv = document.getElementById('error');
            const outputPre = document.getElementById('output');

            errorDiv.textContent = '';
            outputPre.style.display = 'none';
            outputPre.textContent = '';

            if (!input.trim()) return;

            try {
                const parsed = JSON.parse(input);
                outputPre.textContent = JSON.stringify(parsed, null, 4);
                outputPre.style.display = 'block';
            } catch (e) {
                errorDiv.textContent = 'Invalid JSON: ' + e.message;
            }
        }
    </script>
</body>
</html>"""
    },
    {
        "name": "password-generator",
        "html": """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Secure Password Generator</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; padding: 2rem; max-width: 600px; margin: 0 auto; background: #f0fdf4; color: #064e3b; }
        h1 { text-align: center; }
        .container { background: white; padding: 2rem; border-radius: 1rem; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1); }
        .output { background: #f3f4f6; padding: 1rem; border-radius: 0.5rem; font-family: monospace; font-size: 1.5rem; text-align: center; margin-bottom: 1.5rem; word-break: break-all; }
        .controls { display: flex; flex-direction: column; gap: 1rem; }
        label { display: flex; justify-content: space-between; align-items: center; }
        input[type="range"] { width: 60%; }
        button { background: #16a34a; color: white; border: none; padding: 0.75rem; border-radius: 0.5rem; cursor: pointer; font-size: 1.1rem; font-weight: bold; margin-top: 1rem; }
        button:hover { background: #15803d; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Password Generator</h1>
        <div class="output" id="output">Click Generate</div>
        <div class="controls">
            <label>Length: <span id="lenDisplay">16</span> <input type="range" id="length" min="8" max="64" value="16" oninput="document.getElementById('lenDisplay').textContent = this.value"></label>
            <label><input type="checkbox" id="upper" checked> Uppercase (A-Z)</label>
            <label><input type="checkbox" id="lower" checked> Lowercase (a-z)</label>
            <label><input type="checkbox" id="numbers" checked> Numbers (0-9)</label>
            <label><input type="checkbox" id="symbols" checked> Symbols (!@#$%^&*)</label>
            <button onclick="generate()">Generate Password</button>
            <button onclick="copyToClipboard()" style="background: #4b5563;">Copy to Clipboard</button>
        </div>
    </div>
    <script>
        function generate() {
            const length = document.getElementById('length').value;
            const upper = document.getElementById('upper').checked;
            const lower = document.getElementById('lower').checked;
            const numbers = document.getElementById('numbers').checked;
            const symbols = document.getElementById('symbols').checked;

            const u = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
            const l = 'abcdefghijklmnopqrstuvwxyz';
            const n = '0123456789';
            const s = '!@#$%^&*()_+~`|}{[]:;?><,./-=';

            let charset = '';
            if (upper) charset += u;
            if (lower) charset += l;
            if (numbers) charset += n;
            if (symbols) charset += s;

            if (!charset) {
                document.getElementById('output').textContent = 'Select at least one option';
                return;
            }

            let password = '';
            for (let i = 0; i < length; i++) {
                password += charset[Math.floor(Math.random() * charset.length)];
            }
            document.getElementById('output').textContent = password;
        }

        function copyToClipboard() {
            const text = document.getElementById('output').textContent;
            navigator.clipboard.writeText(text).then(() => alert('Copied!'));
        }
        generate();
    </script>
</body>
</html>"""
    },
    {
        "name": "base64-encoder",
        "html": """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Base64 Encoder / Decoder</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; padding: 2rem; max-width: 800px; margin: 0 auto; background: #fffbeb; color: #78350f; }
        h1 { text-align: center; }
        textarea { width: 100%; height: 200px; padding: 1rem; border: 1px solid #d4d4d8; border-radius: 0.5rem; font-family: monospace; margin-bottom: 1rem; box-sizing: border-box; }
        .buttons { display: flex; gap: 1rem; margin-bottom: 1rem; }
        button { flex: 1; background: #d97706; color: white; border: none; padding: 0.75rem; border-radius: 0.5rem; cursor: pointer; font-weight: bold; }
        button:hover { background: #b45309; }
        .error { color: #ef4444; margin-bottom: 1rem; font-weight: bold; }
    </style>
</head>
<body>
    <h1>Base64 Encoder & Decoder</h1>
    <textarea id="input" placeholder="Enter text or Base64 here..."></textarea>
    <div id="error" class="error"></div>
    <div class="buttons">
        <button onclick="encode()">Encode to Base64</button>
        <button onclick="decode()">Decode from Base64</button>
    </div>
    <textarea id="output" placeholder="Result will appear here..." readonly></textarea>
    <script>
        function encode() {
            const input = document.getElementById('input').value;
            document.getElementById('error').textContent = '';
            try {
                document.getElementById('output').value = btoa(unescape(encodeURIComponent(input)));
            } catch (e) {
                document.getElementById('error').textContent = 'Error encoding string.';
            }
        }
        function decode() {
            const input = document.getElementById('input').value;
            document.getElementById('error').textContent = '';
            try {
                document.getElementById('output').value = decodeURIComponent(escape(atob(input)));
            } catch (e) {
                document.getElementById('error').textContent = 'Invalid Base64 string.';
            }
        }
    </script>
</body>
</html>"""
    },
    {
        "name": "word-counter",
        "html": r"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Word & Character Counter</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; padding: 2rem; max-width: 800px; margin: 0 auto; background: #faf5ff; color: #4c1d95; }
        h1 { text-align: center; }
        textarea { width: 100%; height: 300px; padding: 1rem; border: 1px solid #d8b4fe; border-radius: 0.5rem; font-size: 16px; margin-bottom: 1rem; box-sizing: border-box; }
        .stats { display: flex; justify-content: space-around; background: white; padding: 1rem; border-radius: 0.5rem; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        .stat { text-align: center; }
        .stat-value { font-size: 2rem; font-weight: bold; }
        .stat-label { font-size: 0.875rem; color: #6b7280; text-transform: uppercase; letter-spacing: 0.05em; }
    </style>
</head>
<body>
    <h1>Word & Character Counter</h1>
    <textarea id="input" placeholder="Type or paste your text here..." oninput="updateStats()"></textarea>
    <div class="stats">
        <div class="stat">
            <div class="stat-value" id="words">0</div>
            <div class="stat-label">Words</div>
        </div>
        <div class="stat">
            <div class="stat-value" id="chars">0</div>
            <div class="stat-label">Characters</div>
        </div>
        <div class="stat">
            <div class="stat-value" id="charsNoSpace">0</div>
            <div class="stat-label">Chars (No Spaces)</div>
        </div>
    </div>
    <script>
        function updateStats() {
            const text = document.getElementById('input').value;
            const words = text.trim() === '' ? 0 : text.trim().split(/\s+/).length;
            const chars = text.length;
            const charsNoSpace = text.replace(/\s/g, '').length;

            document.getElementById('words').textContent = words;
            document.getElementById('chars').textContent = chars;
            document.getElementById('charsNoSpace').textContent = charsNoSpace;
        }
    </script>
</body>
</html>"""
    }
]

def main():
    current_tool = ""
    try:
        if os.path.exists(".current_tool"):
            with open(".current_tool", "r") as f:
                current_tool = f.read().strip()
    except Exception:
        pass

    available_tools = [t for t in TOOLS if t["name"] != current_tool]
    if not available_tools:
        available_tools = TOOLS

    selected = random.choice(available_tools)

    with open("index.html", "w") as f:
        f.write(selected["html"])

    with open(".current_tool", "w") as f:
        f.write(selected["name"])

    print(f"Deployed tool: {selected['name']}")

if __name__ == "__main__":
    main()
