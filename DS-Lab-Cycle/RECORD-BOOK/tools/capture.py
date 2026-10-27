import os
import sys

import pexpect


def capture(number):
    executable = f"/tmp/opencode/ds{number}"
    input_path = f"inputs/p{number}.txt"
    output_path = f"outputs/p{number}.txt"

    lines = []
    if os.path.exists(input_path):
        with open(input_path, "r", encoding="utf-8") as handle:
            lines = handle.read().splitlines()

    child = pexpect.spawn(executable, encoding="utf-8", timeout=10, dimensions=(40, 100))

    for line in lines:
        child.sendline(line)

    child.expect(pexpect.EOF)

    text = child.before.replace("\r\n", "\n").replace("\r", "\n")
    text = "\n".join(line.rstrip() for line in text.split("\n"))

    with open(output_path, "w", encoding="utf-8") as handle:
        handle.write(text.rstrip() + "\n")


if __name__ == "__main__":
    capture(sys.argv[1])
