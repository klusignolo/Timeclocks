import tkinter as tk
from tkinter import StringVar
from tkinter import filedialog
from timeclocks.utils.tkinter_utils import center_popup, update_widget_text, configure_for_hover
import time
import datetime
from enum import Enum
import os

FONT_PRIMARY = ("arial", 9)
FONT_TIME = ("arial", 14)
FONT_HEADER1 = ("arial", 12, 'bold')
FONT_HEADER2 = ("arial", 10, 'bold')
TODAY_STRING = datetime.datetime.now().strftime("%m-%d-%Y")

class StopwatchOperationMode(Enum):
    SYNCHRONOUS = 0
    ASYNCHRONOUS = 1

class MainFrame(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master=master)
        self.mode: StopwatchOperationMode = StopwatchOperationMode.SYNCHRONOUS
        self.mode_btn = tk.Button(self, text='Mode: Synchronous', width=20, font=FONT_HEADER2, command=self.toggle_mode)
        configure_for_hover(self.mode_btn, primary_color='#b3f2ff', hover_color='#d1f7ff')

        self.clock1 = StopWatch(self, main_frame=self)
        self.clock2 = StopWatch(self, main_frame=self)
        self.clock3 = StopWatch(self, main_frame=self)
        self.clock4 = StopWatch(self, main_frame=self)
        self.clock5 = StopWatch(self, main_frame=self)
        self.clock6 = StopWatch(self, main_frame=self)

        self.all_clocks: list[StopWatch] = [self.clock1, self.clock2, self.clock3, self.clock4, self.clock5, self.clock6]

        self.clock1.grid(row=1, column=0)
        self.clock2.grid(row=1, column=1)
        self.clock3.grid(row=1, column=2)
        self.clock4.grid(row=2, column=0)
        self.clock5.grid(row=2, column=1)
        self.clock6.grid(row=2, column=2)
        self.mode_btn.grid(row=0, columnspan=3, pady=3)

        update_widget_text(self.clock1.clock_label, "Category 1")
        update_widget_text(self.clock2.clock_label, "Category 2")
        update_widget_text(self.clock3.clock_label, "Category 3")
        update_widget_text(self.clock4.clock_label, "Category 4")
        update_widget_text(self.clock5.clock_label, "Category 5")
        update_widget_text(self.clock6.clock_label, "Category 6")

        master.bind('<Control-s>', self.export_time)


    def toggle_mode(self):
        if self.mode == StopwatchOperationMode.SYNCHRONOUS:
            self.mode = StopwatchOperationMode.ASYNCHRONOUS
        else:
            self.mode = StopwatchOperationMode.SYNCHRONOUS
            
        if self.mode == StopwatchOperationMode.SYNCHRONOUS:
            update_widget_text(self.mode_btn, "Mode: Synchronous")
            for clock in self.all_clocks:
                if clock.is_running:
                    self.stop_all_clocks()
        else:
            update_widget_text(self.mode_btn, "Mode: Asynchronous")

    def export_time(self, event=None):
        exportable_text = "\n".join([clock.get_exportable_text() for clock in self.all_clocks])

        filename = filedialog.asksaveasfilename(defaultextension=".txt", initialfile="Time Spent - " + TODAY_STRING,
                                                filetypes=[('TXT Files', '.txt'), ('All Files', '.*')],
                                                initialdir=os.getcwd())

        if filename:
            my_file = open(filename, "w")
            my_file.write(exportable_text)
        else:
            return
        
    def stop_all_clocks(self):
        [clock.stop() for clock in self.all_clocks]

    
class StopWatch(tk.Frame):
    def __init__(self, parent=None, main_frame: MainFrame=None):
        tk.Frame.__init__(self, parent)
        self.main_frame = main_frame
        self._start = 0.0
        self._elapsedtime = 0.0
        self.is_running = False
        self.time_string_var = StringVar()
        self.update_time_label()

        self.clock_label = tk.Label(self, font=FONT_HEADER1, text="Category")
        self.timelabel = tk.Label(self, font=FONT_TIME, textvariable=self.time_string_var)
        self.startbtn = tk.Button(self, text='Start', font=FONT_HEADER2, width=10, command=self.start)
        self.stopbtn = tk.Button(self, text='Reset', font=FONT_HEADER2, width=10, command=self.stop_btn_pressed)
        self.change_category_btn = tk.Button(self, text='Rename Category', font=FONT_PRIMARY,
               command=self.category_popup)
               
        configure_for_hover(self.startbtn, primary_color='#e0ffe0', hover_color='#23e046')
        configure_for_hover(self.stopbtn, primary_color='#ffcccc', hover_color='#e81919')
        configure_for_hover(self.change_category_btn, primary_color='#b3f2ff', hover_color='#d1f7ff')

        self.clock_label.grid(row=0, columnspan=2)
        self.timelabel.grid(row=1, columnspan=3, pady=5)
        self.startbtn.grid(row=2, column=0, padx=5)
        self.stopbtn.grid(row=2, column=1, padx=5)
        self.change_category_btn.grid(row=3, columnspan=2, pady=5)

    def update_time_label(self):
        """ Make the time label. """
        self._settime(self._elapsedtime)

    def _update(self):
        """ Update the label with elapsed time. """
        self._elapsedtime = time.time() - self._start
        self._settime(self._elapsedtime)
        self._timer = self.after(50, self._update)

    def _settime(self, elap):
        """ Set the time string to Hours:Minutes:Seconds """
        hours = int(elap / 3600)
        minutes = int(elap / 60 - hours * 60)
        seconds = int(elap - (hours * 3600 + minutes * 60))
        self.time_string_var.set('%02d:%02d:%02d' % (hours, minutes, seconds))

    def start(self):
        """ Start the stopwatch, ignore if running. """
        if self.main_frame.mode == StopwatchOperationMode.SYNCHRONOUS:
            self.main_frame.stop_all_clocks()
        if not self.is_running:
            self._start = time.time() - self._elapsedtime
            self._update()
            self.is_running = True
            self.stopbtn.configure(text="Stop")

    def stop(self):
        """ Stop the stopwatch, ignore if stopped. """
        if self.is_running:
            self.after_cancel(self._timer)
            self._elapsedtime = time.time() - self._start
            self._settime(self._elapsedtime)
            self.is_running = False
            self.stopbtn.configure(text="Reset")

    def reset(self):
        self._elapsedtime = 0.0
        self._settime(self._elapsedtime)

    def stop_btn_pressed(self):
        if self.stopbtn.cget('text') == "Reset":
            self.reset()
        else:
            self.stop()
            
    def get_exportable_text(self) -> str:
        if self._elapsedtime > 0:
            return f"Time spent on {self.clock_label.cget('text')}: {self.timelabel.cget('text')}"
        else:
            return ""


    def category_popup(self):
        popup = tk.Toplevel()
        center_popup(popup, self)
        popup.wm_title("Change Category")

        def set_cat(event=None):
            self.clock_label.configure(text=cat_entry.get())
            popup.destroy()

        cat_label = tk.Label(popup, font=FONT_HEADER2, text="Category name:")
        cat_entry = tk.Entry(popup, font=FONT_PRIMARY, width=20)
        cat_btn = tk.Button(popup, font=FONT_PRIMARY, text="Set Category", command=set_cat)

        cat_label.grid(row=0, pady=3)
        cat_entry.grid(row=1, padx=5)
        cat_btn.grid(row=2, pady=3)
        cat_entry.focus()

        popup.bind('<Return>', set_cat)
