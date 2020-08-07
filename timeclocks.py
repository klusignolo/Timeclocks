from tkstyles import *
from tkinter import StringVar
from tkinter import filedialog
import time
import datetime


clocks = Main()
clocks.wm_title("Timeclocks  (Ctrl+S to export time as .txt)")
clocks.iconbitmap(file_path('clock.ico'))

font = ("arial", 9)
timefont = ("arial", 14)
headerfont = ("arial", 12, 'bold')
headerfont2 = ("arial", 10, 'bold')
today = datetime.datetime.now().strftime("%m-%d-%Y")
# 0 - Synchronous, 1 - Asynchronous
MODE = 0

set_theme("light")

def export_time(event=None):
    print(event)
    if clock1.timelabel.cget('text') == '00:00:00':
        row1 = ''
    else:
        row1 = "Time spent on " + clock1.clock_label.cget('text') + ": " + clock1.timelabel.cget('text') + '\n'
    if clock2.timelabel.cget('text') == '00:00:00':
        row2 = ''
    else:
        row2 = "Time spent on " + clock2.clock_label.cget('text') + ": " + clock2.timelabel.cget('text') + '\n'
    if clock3.timelabel.cget('text') == '00:00:00':
        row3 = ''
    else:
        row3 = "Time spent on " + clock3.clock_label.cget('text') + ": " + clock3.timelabel.cget('text') + '\n'
    if clock4.timelabel.cget('text') == '00:00:00':
        row4 = ''
    else:
        row4 = "Time spent on " + clock4.clock_label.cget('text') + ": " + clock4.timelabel.cget('text') + '\n'
    if clock5.timelabel.cget('text') == '00:00:00':
        row5 = ''
    else:
        row5 = "Time spent on " + clock5.clock_label.cget('text') + ": " + clock5.timelabel.cget('text') + '\n'
    if clock6.timelabel.cget('text') == '00:00:00':
        row6 = ''
    else:
        row6 = "Time spent on " + clock6.clock_label.cget('text') + ": " + clock6.timelabel.cget('text')

    data = row1 + row2 + row3 + row4 + row5 + row6

    filename = filedialog.asksaveasfilename(defaultextension=".txt", initialfile="Time Spent - " + today,
                                            filetypes=[('TXT Files', '.txt'), ('All Files', '.*')],
                                            initialdir=os.getcwd() + '\\timecards')
    # This if statement makes sure that a file name has been specified. If not, no export is attempted.
    if filename:
        my_file = open(filename, "w")
        my_file.write(data)
    else:
        return


# Sets the background to the hover color when mouse is over btn. Doesn't work for disabled buttons.
def on_enter(btn, color):
    btn.configure(background=color)


# Sets the background back to default background when mouse leaves.
def on_leave(btn, color):
    btn.configure(background=color)


def change_cat(label, new):
    label.configure(text=new)


class StopWatch(Frame):
    def __init__(self, parent=None):
        Frame.__init__(self, parent)
        self._start = 0.0
        self._elapsedtime = 0.0
        self.running = 0
        self.timestr = StringVar()
        self.makewidgets()

        self.clock_label = Label(self, font=headerfont, text="Category")
        self.clock_label.grid(row=0, columnspan=2)
        startbtn = Button(self, text='Start', font=headerfont2, width=10, command=lambda: StopWatch.start(self))
        startbtn.grid(row=2, column=0, padx=5)
        startbtn.configure(background='#e0ffe0')
        startbtn.bind("<Enter>", lambda x: on_enter(startbtn, '#23e046'))
        startbtn.bind("<Leave>", lambda x: on_leave(startbtn, '#e0ffe0'))
        stopbtn = Button(self, text='Stop', font=headerfont2, width=10, command=lambda: StopWatch.stop(self))
        stopbtn.grid(row=2, column=1, padx=5)
        stopbtn.configure(background='#ffcccc')
        stopbtn.bind("<Enter>", lambda x: on_enter(stopbtn, '#e81919'))
        stopbtn.bind("<Leave>", lambda x: on_leave(stopbtn, '#ffcccc'))
        Button(self, text='Rename Category', font=font,
               command=lambda: cat_popup(self.clock_label)).grid(row=3, columnspan=2, pady=5)
        self.timelabel = Label(self, font=timefont, textvariable=self.timestr)
        self.timelabel.grid(row=1, columnspan=3, pady=5)

    def makewidgets(self):
        """ Make the time label. """
        self._settime(self._elapsedtime)

    def _update(self):
        """ Update the label with elapsed time. """
        self._elapsedtime = time.time() - self._start
        self._settime(self._elapsedtime)
        self._timer = self.after(50, self._update)

    def _settime(self, elap):
        """ Set the time string to Minutes:Seconds:Hundreths """
        hours = int(elap / 3600)
        minutes = int(elap / 60 - hours * 60)
        seconds = int(elap - (hours * 3600 + minutes * 60))
        self.timestr.set('%02d:%02d:%02d' % (hours, minutes, seconds))

    def start(self):
        """ Start the stopwatch, ignore if running. """
        if MODE == 0:
            clock1.stop()
            clock2.stop()
            clock3.stop()
            clock4.stop()
            clock5.stop()
            clock6.stop()
        if not self.running:
            self._start = time.time() - self._elapsedtime
            self._update()
            self.running = 1

    def stop(self):
        """ Stop the stopwatch, ignore if stopped. """
        if self.running:
            self.after_cancel(self._timer)
            self._elapsedtime = time.time() - self._start
            self._settime(self._elapsedtime)
            self.running = 0


def cat_popup(label):
    cat = Popup()
    center_popup(cat, clocks)
    cat.wm_title("Category Picker")

    def set_cat():
        label.configure(text=cat_entry.get())
        cat.destroy()

    cat_label = Label(cat, font=headerfont2, text="Category name:")
    cat_entry = Entry(cat, font=font, width=20)
    cat_btn = Button(cat, font=font, text="Set Category", command=set_cat)

    cat_label.grid(row=0)
    cat_entry.grid(row=1)
    cat_btn.grid(row=2)
    cat_entry.focus()


def toggle_mode():
    global MODE
    MODE = not MODE
    if MODE == 0:
        running_count = 0
        if clock1.running:
            running_count += 1
        if clock2.running:
            running_count += 1
        if clock3.running:
            running_count += 1
        if clock4.running:
            running_count += 1
        if clock5.running:
            running_count += 1
        if clock6.running:
            running_count += 1
        if running_count > 1:
            clock1.stop()
            clock2.stop()
            clock3.stop()
            clock4.stop()
            clock5.stop()
            clock6.stop()

        mode_btn.configure(text="Mode: Synchronous")
    else:
        mode_btn.configure(text="Mode: Asynchronous")


mode_btn = Button(clocks, text='Mode: Synchronous', width=20, font=headerfont2, command=toggle_mode)

clock1 = StopWatch(clocks)
change_cat(clock1.clock_label, "JIRA Issue 1")

clock2 = StopWatch(clocks)
change_cat(clock2.clock_label, "JIRA Issue 2")

clock3 = StopWatch(clocks)
change_cat(clock3.clock_label, "Other")

clock4 = StopWatch(clocks)
change_cat(clock4.clock_label, "Support Escalation")

clock5 = StopWatch(clocks)
change_cat(clock5.clock_label, "Testing")

clock6 = StopWatch(clocks)
change_cat(clock6.clock_label, "Regression")

clock1.grid(row=1, column=0)
clock2.grid(row=1, column=1)
clock3.grid(row=1, column=2)
clock4.grid(row=2, column=0)
clock5.grid(row=2, column=1)
clock6.grid(row=2, column=2)
mode_btn.grid(row=0, columnspan=3)

clocks.bind('<Control-s>', export_time)
clocks.mainloop()
