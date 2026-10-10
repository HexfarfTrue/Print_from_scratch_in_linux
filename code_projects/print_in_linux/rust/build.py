from dataclasses import dataclass
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parent

C_SOURCE = ROOT / "print.c"
C_OBJECT = ROOT / "c_print.o"
RUST_SOURCE = ROOT / "main.rs"
OUTPUT = ROOT / "print-bin"

@dataclass
class command:
    programm: str
    arguments: list[str]

    def run(self):
        command = [self.programm, *self.arguments]

        print("$", " ".join(command))

        process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
        )

        stdout, stderr = process.communicate()

        if stdout:
            print(stdout, end="")
        if stderr:
            print(stderr, end="")
        if process.returncode != 0:
            raise SystemExit(
            f"Command failed: {process.returncode}"
            )

def require(programm):
    if shutil.which(programm) is None:
        raise SystemExit(
            f"Missing required program: {programm}"
        )

def compile_c():
    command(
        "clang",
        [
            "-ffreestanding","-fPIC","-fno-stack-protector",
            "-c",str(C_SOURCE),
            "-o",str(C_OBJECT)
        ],
    ).run()

def build_library():
    command(
        "clang",[
            "-c",
            "-nostdlib",
            "-fPIC",
            "-ffreestanding",
            str(C_SOURCE),
            "-o",str(C_OBJECT),
            ]
    ).run()

def build_rust():
    command(
        "rustc",[
            str(RUST_SOURCE),
            "-C","panic=abort",
            "-C","link-arg=-nostartfiles",
            "-C",f"link_arg={str(C_OBJECT)}",
            "-o", str(OUTPUT),
           ]
    ).run()

def main():
    for programm in ("clang", "rustc"):
        require(programm)
    print("Компилируем С")
    compile_c()
    print("\nКомпилируем библиотеку сборки")
    build_library()
    print("\nКомпилируем Rust")
    build_rust()
    print("\nКомпиляция прошшла")

if __name__ == "__main__" :
    main()
