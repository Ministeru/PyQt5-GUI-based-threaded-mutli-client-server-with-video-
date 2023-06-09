import subprocess
import sys

modules = [
    'PyQt5',
    'screeninfo',
    'opencv-python',
    'Pillow',
    'turtle',
    'numpy',
    'pyttsx3',
    'rsa'
]

def install_module(module):
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', module])

def install_modules(modules):
    for module in modules:
        try:
            __import__(module)
            print(f"{module} is already installed.")
        except ImportError:
            print(f"Installing {module}...")
            install_module(module)
            print(f"{module} installed successfully.")

if __name__ == "__main__":
    install_modules(modules)