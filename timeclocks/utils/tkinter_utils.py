import tkinter as tk

def update_widget_text(widget: tk.Widget, value):
    """Takes updates the widget's text to equal whatever Value is specified."""
    if isinstance(widget, tk.Entry):
        if widget.cget("state") == "disabled":
            widget.config(state="normal")
            widget.delete(0, tk.END)
            widget.insert(0, value)
            widget.config(state="disabled")
        else:
            widget.delete(0, tk.END)
            widget.insert(0, value)
    elif isinstance(widget, tk.Text):
        if widget.cget("state") == "disabled":
            widget.config(state="normal")
            widget.delete("1.0", tk.END)
            widget.insert("1.0", value)
            widget.config(state="disabled")
        else:
            widget.delete("1.0", tk.END)
            widget.insert("1.0", value)
    elif isinstance(widget, tk.Label) or isinstance(widget, tk.Button):
        widget.config(text=value)

def configure_for_hover(button: tk.Widget, primary_color: str, hover_color: str):
    def on_enter(button: tk.Widget, color: str):
        """Sets the background to the hover color when mouse is over btn. Doesn't work for disabled buttons."""
        button.configure(background=color)

    def on_leave(button: tk.Widget, color: str):
        """Sets the background back to default background when mouse leaves."""
        button.configure(background=color)
    
    button.configure(background=primary_color)
    button.bind("<Enter>", lambda x: on_enter(button, hover_color))
    button.bind("<Leave>", lambda x: on_leave(button, primary_color))
    
def center_popup(pop, parent):
    """Takes the measurements of the parent Frame and adjusts the popup's geometry to center within it."""
    positionright = int(parent.winfo_rootx()) + int(parent.winfo_width() / 3)
    positiondown = int(parent.winfo_rooty())
    pop.geometry("+{}+{}".format(positionright, positiondown))