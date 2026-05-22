from tkinter import *
from functools import partial  # to prevent unwanted windows
import all_constant as c
import conversion_rounding as cr
from datetime import date


class Converter:

    def __init__(self):
        """
        Currency converter GUI
        """

        self.all_calculations_list = []

        self.temp_frame = Frame(padx=20, pady=20)
        self.temp_frame.grid()

        self.temp_heading = Label(self.temp_frame,
                                  text="Currency Convertor",
                                  font=("Arial", "20", "bold"),
                                  fg="#111111"
                                  )
        self.temp_heading.grid(row=0)

        instructions = ("Please enter an amount below and then press "
                        "one of the buttons to convert it between "
                        "NZD and ILS.")
        self.temp_instructions = Label(self.temp_frame,
                                       text=instructions,
                                       wraplength=250, width=40,
                                       justify="left",
                                       font=("Arial", "13"),
                                       fg="#222222")
        self.temp_instructions.grid(row=1)

        self.temp_entry = Entry(self.temp_frame,
                                font=("Arial", "16")
                                )
        self.temp_entry.grid(row=2, padx=10, pady=12)

        error = "Please enter a number"
        self.answer_error = Label(self.temp_frame, text=error,
                                  fg="#004C99", font=("Arial", "16", "bold"))
        self.answer_error.grid(row=3)

        # Conversion, help and history / export buttons
        self.button_frame = Frame(self.temp_frame)
        self.button_frame.grid(row=4)

        # button list (button text | bg colour | command | row | column)
        button_details_list = [
            ["To ILS", "#990099", lambda: self.check_amount("nzd_to_ils"), 0, 0],
            ["To NZD", "#009900", lambda: self.check_amount("ils_to_nzd"), 0, 1],
            ["Help / Info", "#CC6600", self.to_help, 1, 0],
            ["History / Export", "#004C99", self.to_history, 1, 1]
        ]

        # List to hold buttons once they have been made
        self.button_ref_list = []

        for item in button_details_list:
            self.make_button = Button(self.button_frame,
                                      text=item[0], bg=item[1],
                                      fg="#FFFFF0", font=("Arial", "14", "bold"),
                                      width=14, command=item[2])
            self.make_button.grid(row=item[3], column=item[4], padx=3, pady=3)

            self.button_ref_list.append(self.make_button)

        # retrieve to_help button
        self.to_help_button = self.button_ref_list[2]

        # retrieve 'history / export' button and disable it at start
        self.to_history_button = self.button_ref_list[3]
        self.to_history_button.config(state=DISABLED)

    def check_amount(self, direction):

        # Retrieve amount to be converted
        to_convert = self.temp_entry.get()

        # Reset Label and entry box (if we had an error)
        self.answer_error.config(fg="#004C99", font=("Arial", "15", "bold"))
        self.temp_entry.config(bg="#FFFFFF")

        error = f"Enter a number more than / equal to {c.MIN_AMOUNT} \n and less than or equal to {c.MAX_AMOUNT}"
        has_errors = "no"

        # checks that amount to be converted
        try:
            to_convert = float(to_convert)
            if c.MIN_AMOUNT <= to_convert <= c.MAX_AMOUNT:
                self.convert(direction, to_convert)
            else:
                has_errors = "yes"

        except ValueError:
            has_errors = "yes"

        if has_errors == "yes":
            self.answer_error.config(text=error, fg="#9C0000", font=("Arial", "12", "bold"))
            self.temp_entry.config(bg="#F4CCCC")
            self.temp_entry.delete(0, END)

    def convert(self, direction, to_convert):
        """
        Converts currency and updates answer label. Also stores
        calculations for Export / History feature
        """

        if direction == "nzd_to_ils":
            answer = cr.to_ils(to_convert)
            answer_statement = f"{to_convert}$ NZD is {answer}₪ ILS"
        else:
            answer = cr.to_nzd(to_convert)
            answer_statement = f"{to_convert}₪ ILS is {answer}$ NZD"

        # enable history export button as soon as we have a valid calculation
        self.to_history_button.config(state=NORMAL)

        self.answer_error.config(text=answer_statement)
        self.all_calculations_list.append(answer_statement)
        print(self.all_calculations_list)

    def to_help(self):
        DisplayHelp(self)
        """
        Opens help dialogue box and disables help button
        (so that users can't create multiple help boxes).
        """

    def to_history(self):
        """
        Opens history dialogue box and disables history button
        (so that users can't create multiple history boxes).
        """
        HistoryExport(self, self.all_calculations_list)


class DisplayHelp:
    """
    Displays help dialogue box
    """

    def __init__(self, partner):
        # setup dialogue box and background colour
        background = "#ffe6cc"
        self.help_box = Toplevel()

        # disable help button
        partner.to_help_button.config(state=DISABLED)

        # If users press the cross at the top, close help and
        # 'release' the help button
        self.help_box.protocol("WM_DELETE_WINDOW",
                               partial(self.close_help, partner))

        self.help_frame = Frame(self.help_box, width=300,
                                height=200)
        self.help_frame.grid()

        self.help_heading_label = Label(self.help_frame,
                                        text="Help / Info",
                                        font=("Arial", "16", "bold"))
        self.help_heading_label.grid(row=0)

        help_text = "To use the program, simply enter the amount " \
                    "you wish to convert and then choose to convert " \
                    "to either NZD (New Zealand Dollars) or " \
                    "ILS (Israeli New Shekel).\n\n" \
                    "Note that the exchange rate used is 1 NZD = 2.07 ILS. " \
                    "Only amounts of 0 or more can be converted.\n\n" \
                    "To see your " \
                    "calculation history and export it to a text " \
                    "file, please click the 'History / Export' button."

        self.help_text_label = Label(self.help_frame,
                                     text=help_text, wraplength=350,
                                     justify="left",
                                     font=("Arial", "12"))
        self.help_text_label.grid(row=1, padx=10)

        self.dismiss_button = Button(self.help_frame, font=("Arial", "13", "bold"),
                                     text="Dismiss", bg="#CC6600",
                                     fg="#FFFFFF",
                                     command=partial(self.close_help, partner))

        self.dismiss_button.grid(row=2, padx=10, pady=10)

        # List and loop to set background colour on
        # everything except the buttons.
        recolour_list = [self.help_frame, self.help_heading_label,
                         self.help_text_label]

        for item in recolour_list:
            item.config(bg=background)

    def close_help(self, partner):
        """
        Closes help dialogue box (and enables help button)
        """
        # put help button back to normal...
        partner.to_help_button.config(state=NORMAL)
        self.help_box.destroy()


class HistoryExport:
    """
    Displays history dialogue box
    """

    def __init__(self, partner, calculations):

        self.history_box = Toplevel()

        # disable history button
        partner.to_history_button.config(state=DISABLED)

        # If users press cross at top, closes history and
        # 'releases' history button
        self.history_box.protocol('WM_DELETE_WINDOW',
                                  partial(self.close_history, partner))

        self.history_frame = Frame(self.history_box)
        self.history_frame.grid()

        # background colour and text for calculation area
        if len(calculations) <= c.MAX_CALCS:
            calc_back = "#8EE47C"
            calc_amount = "all your"
        else:
            calc_back = "#ffe6cc"
            calc_amount = (f"your recent calculations - "
                           f"showing {c.MAX_CALCS} / {len(calculations)}")

        # strings for 'long' labels...
        recent_intro_txt = (f"Below are your {calc_amount} calculations "
                            "(to 2 decimal places).")

        # Create string from calculations list (new calculations first)
        newest_first_string = ""
        newest_first_list = list(reversed(calculations))

        if len(newest_first_list) <= c.MAX_CALCS:

            for item in newest_first_list[:-1]:
                newest_first_string += item + "\n"

            newest_first_string += newest_first_list[-1]

        else:
            for item in newest_first_list[:c.MAX_CALCS - 1]:
                newest_first_string += item + "\n"

            newest_first_string += newest_first_list[c.MAX_CALCS - 1]

        export_instruction_txt = ("Please push <Export> to save your calculations in "
                                  "a file. If the filename already exists, it will be overwritten.")

        calculations_for_export = list(calculations)

        # Label list (label text | format | bg)
        history_labels_list = [
            ["History / Export", ("Arial", "18", "bold"), None],
            [recent_intro_txt, ("Arial", "12"), None],
            [newest_first_string, ("Arial", "15"), calc_back],
            [export_instruction_txt, ("Arial", "12"), None]
        ]

        history_label_ref = []
        for count, item in enumerate(history_labels_list):
            make_label = Label(self.history_box, text=item[0], font=item[1],
                               bg=item[2],
                               wraplength=300, justify="left", pady=10, padx=20)
            make_label.grid(row=count)

            history_label_ref.append(make_label)

        # Retrieve export instructions label so that we can
        # configure it to show the filename if the user exports the file
        self.export_filename_label = history_label_ref[3]

        # make frame to hold buttons (two columns)
        self.hist_button_frame = Frame(self.history_box)
        self.hist_button_frame.grid(row=4)

        # button list (button text | bg colour | command | row | column)
        button_details_list = [
            ["Export", "#004C99", lambda: self.export_data(calculations_for_export), 0, 0],
            ["Close", "#666666", partial(self.close_history, partner), 0, 1],
        ]

        for btn in button_details_list:
            self.make_button = Button(self.hist_button_frame,
                                      font=("Arial", "13", "bold"),
                                      text=btn[0], bg=btn[1],
                                      fg="#FFFFFF", width=12,
                                      command=btn[2])
            self.make_button.grid(row=btn[3], column=btn[4], padx=10, pady=10)

    def export_data(self, calculations):

        # **** Get current date for heading and filename ****
        today = date.today()

        # Get day, month and year as individual strings
        day = today.strftime("%d")
        month = today.strftime("%m")
        year = today.strftime("%Y")

        file_name = f"currencies_{year}_{month}_{day}"

        # edit label so users know that their export has been done
        success_string = ("Export Successful! The file is called "
                          f"{file_name}.txt")
        self.export_filename_label.config(fg="#009900", text=success_string,
                                          font=("Arial", "13", "bold"))

        write_to = f"{file_name}.txt"

        with open(write_to, "w", encoding="utf-8") as text_file:
            text_file.write("***** Currency Calculations ******\n")
            text_file.write(f"Generated: {day}/{month}/{year}\n\n")
            text_file.write("Here is your calculation history (oldest to newest)... \n")

            # write the items to file
            for item in calculations:
                text_file.write(item)
                text_file.write("\n")

    def close_history(self, partner):
        """
        Closes history dialogue box (and enables history button)
        """
        # Put history button back to normal
        partner.to_history_button.config(state=NORMAL)
        self.history_box.destroy()


# main routine
if __name__ == "__main__":
    root = Tk()
    root.title("Currency Converter")
    Converter()
    root.mainloop()
