from tkinter import *
from functools import partial
import all_constant as c
import conversion_rounding as cr


class Converter:

    def __init__(self):
        """
        Currency converter GUI
        """

        self.all_calculations_list = []

        self.temp_frame = Frame(padx=15, pady=15)
        self.temp_frame.grid()

        self.temp_heading = Label(self.temp_frame,
                                  text="Currency Convertor",
                                  font=("Arial", "18"),
                                  fg="#222222"
                                  )
        self.temp_heading.grid(row=0)

        instructions = ("Please enter an amount below and then press "
                        "one of the buttons to convert it between "
                        "NZD and ILS.")
        self.temp_instructions = Label(self.temp_frame,
                                       text=instructions,
                                       wraplength=250, width=40,
                                       justify="left",
                                       font=("Arial", "12"),
                                       fg="#333333")
        self.temp_instructions.grid(row=1)

        self.temp_entry = Entry(self.temp_frame,
                                font=("Arial", "15")
                                )
        self.temp_entry.grid(row=2, padx=10, pady=10)

        error = "Please enter a number"
        self.answer_error = Label(self.temp_frame, text=error,
                                  fg="#004C99", font=("Arial", "15"))
        self.answer_error.grid(row=3)

        # Conversion, help and history / export buttons
        self.button_frame = Frame(self.temp_frame)
        self.button_frame.grid(row=4)

        # button list (button text | bg colour | command | row | column)
        button_details_list = [
            ["To ILS", "#990099", lambda: self.check_amount("nzd_to_ils"), 0, 0],
            ["To NZD", "#009900", lambda: self.check_amount("ils_to_nzd"), 0, 1],
            ["Help / Info", "#CC6600", "", 1, 0],
            ["History / Export", "#004C99", self.to_history, 1, 1]
        ]

        # List to hold buttons once they have been made
        self.button_ref_list = []

        for item in button_details_list:
            self.make_button = Button(self.button_frame,
                                      text=item[0], bg=item[1],
                                      fg="#FFFFFF", font=("Arial", "13"),
                                      width=13, command=item[2])
            self.make_button.grid(row=item[3], column=item[4], padx=7, pady=7)

            self.button_ref_list.append(self.make_button)

        # retrieve 'history / export' button and disable it at start
        self.to_history_button = self.button_ref_list[3]
        self.to_history_button.config(state=DISABLED)

    def check_amount(self, direction):

        # Retrieve amount to be converted
        to_convert = self.temp_entry.get()

        # Reset Label and entry box (if we had an error)
        self.answer_error.config(fg="#004C99", font=("Arial", "14", "bold"))
        self.temp_entry.config(bg="#FFFFFF")

        error = f"Enter a number greater than {c.MIN_AMOUNT}"
        has_errors = "no"

        # checks that amount to be converted
        try:
            to_convert = float(to_convert)
            if to_convert >= c.MIN_AMOUNT:
                self.convert(direction, to_convert)
            else:
                has_errors = "yes"

        except ValueError:
            has_errors = "yes"

        if has_errors == "yes":
            self.answer_error.config(text=error, fg="#9C0000", font=("Arial", "11", "bold"))
            self.temp_entry.config(bg="#F4CCCC")
            self.temp_entry.delete(0, END)

    def convert(self, direction, to_convert):
        """
        Converts currency and updates answer label. Also stores
        calculations for Export / History feature
        """

        if direction == "nzd_to_ils":
            answer = cr.to_ils(to_convert)
            answer_statement = f"NZD {to_convert} is ILS {answer}"
        else:
            answer = cr.to_nzd(to_convert)
            answer_statement = f"ILS {to_convert} is NZD {answer}"

        # enable history export button as soon as we have a valid calculation
        self.to_history_button.config(state=NORMAL)

        self.answer_error.config(text=answer_statement)
        self.all_calculations_list.append(answer_statement)
        print(self.all_calculations_list)

    def to_history(self):
        HistoryExport(self, self.all_calculations_list)


class HistoryExport:

    def __init__(self, partner, calculations):

        self.history_box = Toplevel()

        partner.to_history_button.config(state=DISABLED)

        self.history_box.protocol("WM_DELETE_WINDOW",
                                  partial(self.close_history, partner))

        calculations_string = ""
        for item in calculations:
            calculations_string += item + "\n"

        Label(self.history_box, text="History / Export",
              font=("Arial", "16", "bold"),
              pady=10, padx=20).grid(row=0)

        Label(self.history_box, text=calculations_string,
              font=("Arial", "13"),
              pady=10, padx=20, justify="left").grid(row=1)

        button_frame = Frame(self.history_box)
        button_frame.grid(row=2)

        Button(button_frame, text="Export", bg="#004C99", fg="#FFFFFF",
               font=("Arial", "12", "bold"), width=12,
               command=lambda: self.export_data(calculations)).grid(row=0, column=0, padx=10, pady=10)

        Button(button_frame, text="Close", bg="#666666", fg="#FFFFFF",
               font=("Arial", "12", "bold"), width=12,
               command=partial(self.close_history, partner)).grid(row=0, column=1, padx=10, pady=10)

        self.export_label = Label(self.history_box, text="",
                                  font=("Arial", "11"), pady=5, padx=20)
        self.export_label.grid(row=3)

    def export_data(self, calculations):

        file_name = "calculations.txt"

        with open(file_name, "w") as text_file:
            for item in calculations:
                text_file.write(item + "\n")

        self.export_label.config(text=f"Exported to {file_name}", fg="#009900")

    def close_history(self, partner):
        partner.to_history_button.config(state=NORMAL)
        self.history_box.destroy()


if __name__ == "__main__":
    root = Tk()
    root.title("Currency Converter")
    Converter()
    root.mainloop()