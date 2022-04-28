from timeclocks.app import App
from timeclocks.utils.file_utils import file_path

def main() -> None:
    app = App()
    app.iconbitmap(file_path("clock.ico"))
    app.mainloop()

if __name__ == "__main__":
    main()
