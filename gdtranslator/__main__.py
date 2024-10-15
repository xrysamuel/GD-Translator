import sys
import io
from subprocess import Popen, DEVNULL, PIPE
import argparse

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

from .url_base64 import url_safe_base64_encode

parser = argparse.ArgumentParser()
parser.add_argument("source_text", help="the text you want to translate", type=str)
parser.add_argument("--config", help="path to config.yaml", type=str)
args = parser.parse_args()
source_text = args.source_text
config_path = args.config

encoded_source_text = url_safe_base64_encode(source_text)
command = f'{sys.executable} -m gdtranslator.server --config "{config_path}"'
Popen(command, stdout=DEVNULL, stderr=DEVNULL, shell=True)

css = f"""
<style>
.translator-box {{
    flex: 1;
    padding: 10px;
    border: 1px solid #d0dde2;
    border-radius: 8px;
    margin: 10px;
    padding: 20px;
    position: relative;
}}
.translator-container {{
    display: flex;
}}
.translator-title {{
    position: absolute;
    top: -15px;
    left: 20px;
    background-color: #e0e8f0;
    padding: 5px;
    border-radius: 5px;
    color: #4480f8
}}
</style>
"""

html = f"""
<div class="translator-container">
    <div class="translator-box">
        <div class="translator-title">EN</div>
        <div id="translator-intput">{source_text}</div>
    </div>
    <div class="translator-box">
        <div class="translator-title">ZH</div>
        <div id="translator-output"></div>
    </div>
</div>
"""

js = f"""
<script>
    const outputDiv = document.getElementById('translator-output');
    const source = new EventSource('http://localhost:5000/translate?q={encoded_source_text}');
    source.addEventListener("end", (event) => {{
        source.close();
    }})
    source.onmessage = function (event) {{
        outputDiv.innerHTML += event.data;
    }};
</script>
"""

print(css)
print(html)
print(js)
