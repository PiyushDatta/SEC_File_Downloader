# Used to run all the files in src for SEFD program

from src.AppGUI.MainGUI import MainGUIApp


def main():
    main_window = MainGUIApp(window_title="SEC Edgar File Downloader", window_width=975, window_length=600)
    main_window.mainloop()


if __name__ == '__main__':
    main()
