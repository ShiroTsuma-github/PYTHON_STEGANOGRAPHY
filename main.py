import sys
import os


ROOT_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(ROOT_DIR)
from src.GUI import App     # noqa: E402

if __name__ == "__main__":
    app = App()
    app.mainloop()
