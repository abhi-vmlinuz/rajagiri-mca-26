#!/usr/bin/env python3
import os
import re
import shutil
import subprocess
import fitz
import weasyprint

BASE_DIR = "/home/elish4h/Rajagiri/Assignments/OS-With-Linux/Commands word files/command_pdfs"
WORKGROUND = os.path.join(BASE_DIR, "workground")
COMPLETED_DIR = os.path.join(BASE_DIR, "completed_pdf")

os.makedirs(COMPLETED_DIR, exist_ok=True)
os.makedirs(WORKGROUND, exist_ok=True)

def setup_workground():
    """Ensure workground has realistic test files and subdirectories."""
    # Reset/Create workground directories
    dirs_to_create = [
        "Documents/geeksforgeeks/example",
        "My Documents",
        "My songs",
        "subdirectory",
        ".config",
        "backup",
        "new",
        "Folder1",
        "Dest_directory",
        "Src_directory",
        "geeksforgeeks",
        "jkj",
        "Linux/dirtest1/dirtest2",
        "test"
    ]
    for d in dirs_to_create:
        os.makedirs(os.path.join(WORKGROUND, d), exist_ok=True)

    # Standard test files
    files_content = {
        "file1": "this is file1\n",
        "file2": "this is file2\n",
        "file_name": "this is a file\n",
        "file_name2": "this is file2\n",
        "jayesh.txt": "this is Jayesh from GfG\n",
        "jayesh1": "Jayesh from GfG\n",
        "-dashfile": "dash file content\n",
        "-jayesh2": "jayesh2 content\n",
        "merged.txt": "this is file2\nthis is file1\nthis is Jayesh from GfG\n",
        "merged_file.txt": "this is file2\nthis is file1\n",
        "newfile_name": "hi this is abhishek\n",
        "a.txt": "Apple\nBanana\nCherry\n",
        "b.txt": "Dog\nElephant\nFox\n",
        "c.txt": "Giraffe\nHippo\nIguana\n",
        "file.txt": "Sample file content for backup\n",
        "Src_file1": "Source file 1 content\n",
        "Src_file2": "Source file 2 content\n",
        "Src_file3": "Source file 3 content\n",
        "state.txt": "Andhra Pradesh\nArunachal Pradesh\nAssam\nBihar\nGoa\nGujarat\nKarnataka\nKerala\nMaharashtra\nTamil Nadu\n",
        "number": "1\n2\n3\n4\n5\n",
        "state": "Andhra Pradesh\nBihar\nGujarat\nKarnataka\nKerala\n",
        "capital": "Amaravati\nPatna\nGandhinagar\nBengaluru\nThiruvananthapuram\n",
        "d.txt": "d file content\n",
        "e.txt": "e file content\n",
        "-file.txt": "dash file.txt content\n",
        "Geek.txt": "Geek text content\n",
        "first_file_name": "First file content\n",
        "second_file_name": "Second file content\n",
        "fileName": "fileName content\n"
    }

    for fname, content in files_content.items():
        fpath = os.path.join(WORKGROUND, fname)
        if not os.path.exists(fpath):
            with open(fpath, "w") as f:
                f.write(content)

def escape_html(text):
    return (text.replace("&", "&amp;")
                .replace("<", "&lt;")
                .replace(">", "&gt;")
                .replace('"', "&quot;"))

def run_cmd_in_workground(cmd_str, current_cwd=None):
    """Executes or simulates command execution in workground context."""
    if current_cwd is None:
        current_cwd = WORKGROUND

    # Simulated/Syntax placeholder cases
    cmd_strip = cmd_str.strip()
    
    # Placeholders like cut OPTION... [FILE]..
    if "OPTION..." in cmd_strip or "[FILE]" in cmd_strip or "[directory]" in cmd_strip or "[options]" in cmd_strip:
        if cmd_strip.startswith("cut"):
            return "cut: missing list of positions\nTry 'cut --help' for more information."
        elif cmd_strip.startswith("cd"):
            return "cd: directory placeholder usage"
        elif cmd_strip.startswith("cp"):
            return "cp: missing file operand\nTry 'cp --help' for more information."
        elif cmd_strip.startswith("locate"):
            return "locate: no pattern specified"
        elif cmd_strip.startswith("man"):
            return "What manual page do you want?\nFor example, try 'man man'."
        elif cmd_strip.startswith("mkdir"):
            return "mkdir: missing operand\nTry 'mkdir --help' for more information."
        elif cmd_strip.startswith("mv"):
            return "mv: missing file operand\nTry 'mv --help' for more information."
        elif cmd_strip.startswith("paste"):
            return "paste: missing file operand\nTry 'paste --help' for more information."
        elif cmd_strip.startswith("rm"):
            return "rm: missing operand\nTry 'rm --help' for more information."
        elif cmd_strip.startswith("touch"):
            return "touch: missing file operand\nTry 'touch --help' for more information."

    if cmd_strip == 'cd /path/to/directory' or cmd_strip == 'cd /absolute/path':
        return 'bash: cd: /path/to/directory: No such file or directory'
    if cmd_strip == 'cd /var/l':
        return 'bash: cd: /var/l: No such file or directory'
    if cmd_strip == 'cd /path/to/directory && ls':
        return 'bash: cd: /path/to/directory: No such file or directory'
    if cmd_strip.startswith("rm -i"):
        fname = cmd_strip.split()[-1]
        return f"rm: remove regular file '{fname}'? y"
    if cmd_strip.startswith("cp -i") and len(cmd_strip.split()) == 4:
        parts = cmd_strip.split()
        return f"cp: overwrite '{parts[3]}'? y"
    if cmd_strip.startswith("mv -i") and len(cmd_strip.split()) == 4:
        parts = cmd_strip.split()
        return f"mv: overwrite '{parts[3]}'? y"
    if cmd_strip == "vim empty_file.txt":
        return "~                                                                               \n~                                                                               \n\"empty_file.txt\" [New File] 0L, 0C written"

    # Actual bash command execution
    try:
        res = subprocess.run(
            cmd_str,
            shell=True,
            cwd=current_cwd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            timeout=5
        )
        out = res.stdout
        # Clean up output if long (e.g. man pages)
        if "man " in cmd_str and len(out.splitlines()) > 20:
            lines = out.splitlines()[:20]
            lines.append("... [output truncated for display]")
            out = "\n".join(lines) + "\n"
        return out
    except Exception as e:
        return str(e)

def extract_commands_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    lines = []
    for page in doc:
        text = page.get_text()
        for line in text.splitlines():
            line_str = line.strip()
            if line_str and not line_str.endswith("- Examples"):
                lines.append(line_str)
    return lines

def generate_pdf_for_command(cmd_name):
    input_pdf = os.path.join(BASE_DIR, f"{cmd_name}_command_examples.pdf")
    output_pdf = os.path.join(COMPLETED_DIR, f"{cmd_name}.pdf")
    
    if not os.path.exists(input_pdf):
        print(f"File not found: {input_pdf}")
        return

    commands = extract_commands_from_pdf(input_pdf)
    title = f"{cmd_name} Command - Examples"

    html_blocks = []
    curr_path_display = "~/. /../../workground"
    simulated_cwd = WORKGROUND

    for cmd in commands:
        output = run_cmd_in_workground(cmd, current_cwd=simulated_cwd)
        
        # Track simulated cwd for display if cd was called
        display_path = curr_path_display
        if cmd.startswith("cd "):
            target = cmd.split(maxsplit=1)[1]
            if target == "/" or target == "/var/log" or target == "/usr/local/bin":
                display_path = target
            elif target == "~":
                display_path = "~"
            elif target == "..":
                display_path = "~/. /../../workground"
            elif not target.startswith("-") and not target.startswith("[") and not "/" in target:
                display_path = f"~/. /../../workground/{target}"

        # Escaping
        cmd_esc = escape_html(cmd)
        out_esc = escape_html(output.rstrip())

        # Construct terminal content
        out_html = f"\n<div class=\"output-text\">{out_esc}</div>" if out_esc else ""
        
        terminal_html = f"""
        <div class="terminal-box">
            <span class="prompt-path">{display_path}</span> <span class="prompt-git">git:❯main</span> <span class="prompt-cmd">{cmd_esc}</span>{out_html}
            <div><span class="prompt-path">{display_path}</span> <span class="prompt-git">git:❯main</span> |</div>
        </div>
        """

        html_blocks.append(f"""
        <div class="item-block">
            <div class="question-title">{cmd_esc}</div>
            {terminal_html}
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
            margin: 18mm 15mm 18mm 15mm;
            @bottom-right {{
                content: counter(page);
                font-family: 'Courier New', monospace;
                font-size: 9pt;
                color: #888;
            }}
        }}
        body {{
            font-family: 'Courier New', monospace;
            color: #111;
            line-height: 1.35;
            margin: 0;
            padding: 0;
        }}
        .doc-title {{
            font-family: 'Courier New', monospace;
            font-size: 18pt;
            font-weight: bold;
            font-style: italic;
            text-align: center;
            margin-bottom: 22px;
        }}
        .item-block {{
            margin-bottom: 18px;
            page-break-inside: avoid;
        }}
        .question-title {{
            font-family: 'Courier New', monospace;
            font-size: 12pt;
            font-weight: bold;
            font-style: italic;
            margin-bottom: 6px;
            color: #000;
        }}
        .terminal-box {{
            background-color: #1c1d22;
            color: #e0e6ed;
            border-radius: 5px;
            padding: 8px 12px;
            font-family: 'DejaVu Sans Mono', 'Consolas', 'Courier New', monospace;
            font-size: 9pt;
            line-height: 1.4;
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
        .output-text {{
            color: #c3cee3;
            margin-top: 3px;
            margin-bottom: 3px;
        }}
    </style>
    </head>
    <body>
        <div class="doc-title">{escape_html(title)}</div>
        {''.join(html_blocks)}
    </body>
    </html>
    """

    weasyprint.HTML(string=full_html).write_pdf(output_pdf)
    print(f"Generated: {output_pdf}")

if __name__ == "__main__":
    setup_workground()
    target_commands = [
        "cd", "cp", "cut", "echo", "locate", 
        "man", "mkdir", "mv", "paste", "rm", "touch"
    ]
    for cmd in target_commands:
        generate_pdf_for_command(cmd)
