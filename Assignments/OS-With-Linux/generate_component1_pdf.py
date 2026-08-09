#!/usr/bin/env python3
import os
import subprocess
import weasyprint

WORKGROUND = "/home/elish4h/Rajagiri/Assignments/OS-With-Linux/Commands word files/command_pdfs/workground"
OUT_PDF_1 = "/home/elish4h/Rajagiri/Assignments/OS-With-Linux/Commands word files/command_pdfs/completed_pdf/Component_1_Commands.pdf"
OUT_PDF_2 = "/home/elish4h/Rajagiri/Assignments/OS-With-Linux/Component_1_Commands.pdf"

os.makedirs(WORKGROUND, exist_ok=True)

def escape_html(text):
    return (text.replace("&", "&amp;")
                .replace("<", "&lt;")
                .replace(">", "&gt;")
                .replace('"', "&quot;"))

questions = [
    {
        "num": "1",
        "question": "What command will you use to create a file called summary.txt and few lines of text in it?",
        "prompt_path": "~/. /../../workground",
        "cmd_input": "cat > summary.txt",
        "user_typing": "This is line 1 of summary.\nThis is line 2 of summary.\nThis is line 3 of summary.",
        "verify_cmd": "cat summary.txt",
        "verify_out": "This is line 1 of summary.\nThis is line 2 of summary.\nThis is line 3 of summary."
    },
    {
        "num": "2",
        "question": "Create a folder named backup, and copy summary.txt into it without changing the filename.",
        "prompt_path": "~/. /../../workground",
        "cmd_input": "mkdir backup && cp summary.txt backup/",
        "verify_cmd": "ls -l backup/",
        "verify_out": "total 4\n-rw-r--r--. 1 user user 81 Aug  9 10:33 summary.txt"
    },
    {
        "num": "3",
        "question": "Rename the file inside backup/ from summary.txt to summary_backup.txt.",
        "prompt_path": "~/. /../../workground",
        "cmd_input": "mv backup/summary.txt backup/summary_backup.txt",
        "verify_cmd": "ls -l backup/",
        "verify_out": "total 4\n-rw-r--r--. 1 user user 81 Aug  9 10:33 summary_backup.txt"
    },
    {
        "num": "4",
        "question": "Create three files — day1.txt, day2.txt, and day3.txt — with one command.",
        "prompt_path": "~/. /../../workground",
        "cmd_input": "touch day1.txt day2.txt day3.txt",
        "verify_cmd": "ls -l day1.txt day2.txt day3.txt",
        "verify_out": "-rw-r--r--. 1 user user 0 Aug  9 10:33 day1.txt\n-rw-r--r--. 1 user user 0 Aug  9 10:33 day2.txt\n-rw-r--r--. 1 user user 0 Aug  9 10:33 day3.txt"
    },
    {
        "num": "5",
        "question": "How many lines, words, and characters are in summary.txt?",
        "prompt_path": "~/. /../../workground",
        "cmd_input": "wc summary.txt",
        "verify_cmd": None,
        "verify_out": " 3 18 81 summary.txt"
    }
]

html_blocks = []

for q in questions:
    q_title = f"{q['num']}. {escape_html(q['question'])}"
    p_path = q['prompt_path']
    
    if q['num'] == "1":
        # Question 1 shows cat > summary.txt, text entry, and cat summary.txt
        terminal_content = f"""
<span class="prompt-path">{p_path}</span> <span class="prompt-git">git:❯main</span> <span class="prompt-cmd">cat &gt; summary.txt</span>
<span class="typing">This is line 1 of summary.
This is line 2 of summary.
This is line 3 of summary.
^C</span>
<span class="prompt-path">{p_path}</span> <span class="prompt-git">git:❯main</span> <span class="prompt-cmd">cat summary.txt</span>
<div class="output-text">This is line 1 of summary.
This is line 2 of summary.
This is line 3 of summary.</div>
<span class="prompt-path">{p_path}</span> <span class="prompt-git">git:❯main</span> |
"""
    elif q['verify_cmd']:
        terminal_content = f"""
<span class="prompt-path">{p_path}</span> <span class="prompt-git">git:❯main</span> <span class="prompt-cmd">{escape_html(q['cmd_input'])}</span>
<span class="prompt-path">{p_path}</span> <span class="prompt-git">git:❯main</span> <span class="prompt-cmd">{escape_html(q['verify_cmd'])}</span>
<div class="output-text">{escape_html(q['verify_out'])}</div>
<span class="prompt-path">{p_path}</span> <span class="prompt-git">git:❯main</span> |
"""
    else:
        terminal_content = f"""
<span class="prompt-path">{p_path}</span> <span class="prompt-git">git:❯main</span> <span class="prompt-cmd">{escape_html(q['cmd_input'])}</span>
<div class="output-text">{escape_html(q['verify_out'])}</div>
<span class="prompt-path">{p_path}</span> <span class="prompt-git">git:❯main</span> |
"""

    html_blocks.append(f"""
    <div class="item-block">
        <div class="question-title">{q_title}</div>
        <div class="terminal-box">
            {terminal_content.strip()}
        </div>
    </div>
    """)

full_html = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
    @page {{
        size: A4 portrait;
        margin: 20mm 16mm 20mm 16mm;
        @bottom-right {{
            content: counter(page);
            font-family: 'Courier New', monospace;
            font-size: 9pt;
            color: #777;
        }}
    }}
    body {{
        font-family: 'Courier New', monospace;
        color: #111;
        line-height: 1.4;
        margin: 0;
        padding: 0;
    }}
    .doc-title {{
        font-family: 'Courier New', monospace;
        font-size: 20pt;
        font-weight: bold;
        font-style: italic;
        text-align: center;
        margin-bottom: 25px;
        color: #000;
    }}
    .item-block {{
        margin-bottom: 22px;
        page-break-inside: avoid;
    }}
    .question-title {{
        font-family: 'Courier New', monospace;
        font-size: 11pt;
        font-weight: bold;
        font-style: italic;
        margin-bottom: 8px;
        color: #111;
        line-height: 1.3;
    }}
    .terminal-box {{
        background-color: #1c1d22;
        color: #e0e6ed;
        border-radius: 6px;
        padding: 10px 14px;
        font-family: 'DejaVu Sans Mono', 'Consolas', 'Courier New', monospace;
        font-size: 9.5pt;
        line-height: 1.45;
        white-space: pre-wrap;
        word-break: break-all;
    }}
    .prompt-path {{
        color: #4ecdc4;
        font-weight: bold;
    }}
    .prompt-git {{
        color: #bd93f9;
        font-weight: bold;
    }}
    .prompt-cmd {{
        color: #ffffff;
        font-weight: bold;
    }}
    .typing {{
        color: #f1fa8c;
    }}
    .output-text {{
        color: #c3cee3;
        margin-top: 4px;
        margin-bottom: 4px;
    }}
</style>
</head>
<body>
    <div class="doc-title">Component 1 - Linux Command Assignment</div>
    {''.join(html_blocks)}
</body>
</html>
"""

weasyprint.HTML(string=full_html).write_pdf(OUT_PDF_1)
weasyprint.HTML(string=full_html).write_pdf(OUT_PDF_2)
print("Generated Component 1 PDFs successfully!")
