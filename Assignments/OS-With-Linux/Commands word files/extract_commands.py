#!/usr/bin/env python3
"""
Extract command examples from docx files and create individual PDFs.
Only commands are shown - no outputs, no redundant content.
"""

import os
import re
from docx import Document
from fpdf import FPDF

# Input directory
INPUT_DIR = "/home/elish4h/Rajagiri/Assignments/OS-With-Linux/Commands word files"
OUTPUT_DIR = "/home/elish4h/Rajagiri/Assignments/OS-With-Linux/Commands word files/command_pdfs"

os.makedirs(OUTPUT_DIR, exist_ok=True)

# Map of docx files to command names
files_map = {
    "ls Command in Linux.docx": "ls",
    "cat Command.docx": "cat",
    "echo command in Linux with Examples - GeeksforGeeks.docx": "echo",
    "cp Command.docx": "cp",
    "cd Command.docx": "cd",
    "mkdir.docx": "mkdir",
    "rm command.docx": "rm",
    "mv command.docx": "mv",
    "Touch Command.docx": "touch",
    "man Command.docx": "man",
    "locate command in Linux with Examples.docx": "locate",
    "Paste command in Linux with examples.docx": "paste",
    "cut command in Linux with examples.docx": "cut",
}

# Basic commands that should not be repeated in other PDFs
BASIC_COMMANDS = {"ls", "cd", "pwd", "cat"}

def filter_basic_commands(commands, current_cmd):
    """Remove basic commands from non-basic command PDFs."""
    if current_cmd in BASIC_COMMANDS:
        return commands
    filtered = []
    for cmd in commands:
        # Get the base command (first word)
        base_cmd = cmd.split()[0] if cmd.split() else ""
        # Also check for commands with options like "ls -l"
        if base_cmd not in BASIC_COMMANDS:
            filtered.append(cmd)
    return filtered


# Known command patterns for each command - these are the actual command examples from the docs
COMMAND_EXAMPLES = {
    "ls": [
        "ls",
        "ls -t",
        "ls -t | head -1",
        "ls -1",
        "ls -l",
        "ls -lh",
        "ls -l /etc",
        "ls -ld /etc",
        "ls -lt",
        "ls -ltr",
        "ls -a",
        "ls -A",
        "ls /etc/apt",
        "ls -R /etc/apt",
        "ls -i",
        "ls -i /etc/apt",
        "ls -q",
        "ls -n ~/kv",
        "ls -F",
        "ls --color=auto",
        "ls -l --time-style=long-iso",
    ],
    "cat": [
        "cat file_name",
        "cat jayesh.txt",
        "cat file1 file2",
        "cat -n file_name",
        "cat -n file2",
        "cat > newfile_name",
        "cat > jayesh1",
        "cat file1.txt file2.txt > merged_file.txt",
        "cat -s file_name",
        "cat file_name1 >> file_name2",
        "cat file1 >> file2",
        "tac file_name",
        "tac file2",
        "cat -E \"filename\"",
        "cat -A \"filename\"",
        "cat -- \"-dashfile\"",
        "cat -- \"-jayesh2\"",
        "cat \"filename\" | more",
        "cat \"filename1\" \"filename2\" \"filename3\" > \"merged_filename\"",
        "cat \"file1\" \"file2\" \"file3\" > \"merged123\"",
        "cat *.txt",
        "cat >> geeks.txt",
    ],
    "echo": [
        "echo \"Geeks for Geeks\"",
        "echo -e \"Geeks \\bfor \\bGeeks\"",
        "echo -e \"Geeks \\cfor Geeks\"",
        "echo -e \"Geeks \\nfor \\nGeeks\"",
        "echo -e \"Geeks \\tfor \\tGeeks\"",
        "echo -e \"Geeks \\rfor Geeks\"",
        "echo -e \"Geeks \\vfor \\vGeeks\"",
        "echo -e \"\\aGeeks for Geeks\"",
        "echo *",
        "echo -n \"Geeks for Geeks\"",
        "echo \"Welcome GFG\" > output.txt",
        "echo \"Append text\" >> output.txt",
    ],
    "cp": [
        "cp source_file destination",
        "cp a.txt b.txt",
        "cp a.txt c.txt",
        "cp Src_file1 Src_file2 Src_file3 Dest_directory",
        "cp a.txt b.txt c.txt new/",
        "cp -R Src_directory Dest_directory",
        "cp -i file.txt backup/file.txt",
        "cp -v file.txt backup/file.txt",
        "cp -n file.txt backup/file.txt",
        "cp -p file.txt backup/file.txt",
        "cp -u file.txt backup/file.txt",
        "cp -b file.txt backup/file.txt",
        "cp -i a.txt b.txt",
        "cp -f a.txt b.txt",
        "cp -r geeksforgeeks gfg",
        "cp -p a.txt c.txt",
        "cp *.txt Folder1",
    ],
    "cd": [
        "cd [directory]",
        "cd /path/to/directory",
        "cd /var/log",
        "cd",
        "cd ~",
        "cd -",
        "cd ..",
        "cd subdirectory",
        "cd Documents",
        "cd /absolute/path",
        "cd /usr/local/bin",
        "cd /var/l",
        "pwd",
        "cd \"My Documents\"",
        "cd My\\ Documents",
        "cd .config",
        "cd /",
        "cd /path/to/directory && ls",
        "alias docs=\"cd ~/Documents\"",
        "cd Documents",
        "cd /",
        "cd Documents/geeksforgeeks/example",
        "cd ~",
        "cd ..",
        "cd \"My songs\"",
        "cd My\\ songs",
    ],
    "mkdir": [
        "mkdir [options] dir_name",
        "mkdir Linux",
        "ls -l",
        "mkdir /tmp/example",
        "cd /tmp",
        "ls -l",
        "mkdir dir1 dir2 dir3",
        "mkdir {test1,test2,test3}",
        "mkdir dir{1..15}",
        "mkdir $USER",
        "mkdir -p Linux/dirtest1/dirtest2",
        "ls -R",
        "mkdir -m777 DirM",
        "ls -l",
        "mkdir -v Details",
        "ls",
    ],
    "rm": [
        "rm [OPTION]... FILE...",
        "ls",
        "rm a.txt",
        "ls",
        "rm b.txt c.txt",
        "ls",
        "rm -i d.txt",
        "ls",
        "ls -l",
        "rm e.txt",
        "ls",
        "rm -f e.txt",
        "ls",
        "ls",
        "cd A",
        "ls",
        "ls B",
        "ls C",
        "rm *",
        "rm -r *",
        "ls",
        "rm --version",
        "ls",
        "rm -file.txt",
        "rm -- -file.txt",
        "ls",
    ],
    "mv": [
        "mv [options(s)] [source_file_name(s)] [Destination_file_name]",
        "mv [source_file_name(s)] [Destination_file_name]",
        "mv jayesh_gfg geeksforgeeks",
        "mv [source_file_name(s)] [Destination_path]",
        "mv geeksforgeeks /home/jayeshkumar/jkj/",
        "mv [source_file_name_1] [source_file_name_2] [Destination_path]",
        "mv gfg_1 gfg_2 /home/jayeshkumar/jkj/",
        "mv [source_directory_name(s)] [Destination_directory_name]",
        "mv jkj new_gfg",
        "mv -i [source_file/directory_name(s)] [Destination_file/directory_name/path]",
        "mv -i jayesh_gfg geeksforgeeks",
        "mv -f [source_file/directory_name(s)] [Destination_file/directory_name/path]",
        "mv -f gfg geeksforgeeks",
        "mv -n [source_file/directory_name(s)] [Destination_file/directory_name/path]",
        "mv -n oldfile newfile",
        "mv -b [source_file/directory_name(s)] [Destination_file/directory_name/path]",
        "mv -b first_file second_file",
        "mv --version",
    ],
    "touch": [
        "touch [options] file_name",
        "touch File1",
        "touch File1_name File2_name File3_name",
        "touch Doc1 Doc2 Doc3",
        "touch -a fileName",
        "touch -a Doc1",
        "touch -c fileName",
        "touch -c -d fileName",
        "touch -m fileName",
        "touch -d \"17 Mar 2023\" Geek.txt",
        "touch -r second_file_name first_file_name",
        "touch -t YYMMDDHHMM fileName",
        "cat > empty_file.txt",
        "> filename",
        "> /path/to/filename",
        "> empty_file.txt",
        "vim empty_file.txt",
    ],
    "man": [
        "man [option] [command]",
        "man [command]",
        "man ls",
        "man [SECTION-NUM] [COMMAND NAME]",
        "man 2 intro",
        "man -f [COMMAND NAME]",
        "man -f ls",
        "man -a [COMMAND NAME]",
        "man -a intro",
        "man -k [COMMAND NAME]",
        "man -k cd",
        "man -w [COMMAND NAME]",
        "man -w ls",
        "man -I [COMMAND NAME]",
        "man -I printf",
    ],
    "locate": [
        "locate [OPTION]... PATTERN...",
        "locate sample.txt",
        "locate \"*.html\" -n 20",
        "locate -c [.txt]*",
        "locate -i *SAMPLE.txt*",
        "locate -i -0 *sample.txt*",
    ],
    "paste": [
        "paste [OPTION]... [FILES]...",
        "cat number",
        "cat state",
        "cat capital",
        "paste number state capital",
        "paste -d \":\" number state capital",
        "paste -s number state capital",
        "paste -s -d \":\" number state capital",
        "paste --version",
        "cat capital | paste - -",
        "cut -f 1 state | paste - capital",
    ],
    "cut": [
        "cut OPTION... [FILE]..",
        "cut -b 1,2,3 state.txt",
        "cut -b 1-3,5-7 state.txt",
        "cut -b 1- state.txt",
        "cut -b -3 state.txt",
        "cut -c 2,5,7 state.txt",
        "cut -c 1-7 state.txt",
        "cut -c 1- state.txt",
        "cut -c -5 state.txt",
        "cut -f 1 state.txt",
        "cut -d \" \" -f 1 state.txt",
        "cut -d \" \" -f 1-4 state.txt",
        "cut --version",
        "cat state.txt | cut -d ' ' -f 1 | sort -r",
        "cat state.txt | head -n 3 | cut -d ' ' -f 1 > list.txt",
        "cat list.txt",
    ],
}


def create_pdf(command_name, commands):
    """Create a PDF with only the commands."""
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Courier", size=11)
    
    # Title
    pdf.set_font("Courier", style="B", size=14)
    pdf.cell(0, 10, f"{command_name} Command - Examples", new_x="LMARGIN", new_y="NEXT", align="C")
    pdf.ln(5)
    
    pdf.set_font("Courier", size=11)
    
    for cmd in commands:
        # Wrap long lines
        if len(cmd) > 85:
            words = cmd.split(' ')
            line = ""
            for word in words:
                if len(line) + len(word) + 1 > 85:
                    pdf.cell(0, 6, line, new_x="LMARGIN", new_y="NEXT")
                    line = word
                else:
                    line = line + " " + word if line else word
            if line:
                pdf.cell(0, 6, line, new_x="LMARGIN", new_y="NEXT")
        else:
            pdf.cell(0, 6, cmd, new_x="LMARGIN", new_y="NEXT")
        pdf.ln(1)
    
    output_path = os.path.join(OUTPUT_DIR, f"{command_name}_command_examples.pdf")
    pdf.output(output_path)
    print(f"Created: {output_path} ({len(commands)} commands)")


def main():
    for cmd_name, commands in COMMAND_EXAMPLES.items():
        # Filter out basic commands from non-basic command PDFs
        commands = filter_basic_commands(commands, cmd_name)
        print(f"\nProcessing {cmd_name}...")
        print(f"  {len(commands)} commands")
        for cmd in commands[:5]:
            print(f"    {cmd}")
        if len(commands) > 5:
            print(f"    ... and {len(commands) - 5} more")
        create_pdf(cmd_name, commands)

    print(f"\nAll PDFs created in: {OUTPUT_DIR}")

if __name__ == "__main__":
    main()