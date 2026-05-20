from tkinter import *
from functools import partial


class Converter:
    """
    Currency conversion tool (NZD to ILS or ILS to NZD)
    """

    def __init__(self):
        """
        Currency converter GUI
        """

        self.temp_frame = Frame(padx=10, pady=10)
        self.temp_frame.grid()

        self.to_history_button = Button(self.temp_frame,
                                        text="History / Export",
                                        bg="#CC6600",
                                        fg="#FFFFFF",
                                        font=("Arial", "14", "bold"), width=12,
                                        )
        self.to_history_button.grid(row=1, padx=5, pady=5)


# main routine
if __name__ == "__main__":
    root = Tk()
    root.title("Currency Converter")
    Converter()
    root.mainloop()
