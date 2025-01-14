import re
import tkinter as tk
import tkinter.ttk as ttk

"""
tkentrycomplete.py

A tkinter widget that features autocompletion.

Created by Mitja Martini on 2008-11-29.
Updated by Russell Adams, 2011/01/24 to support Python 3 and Combobox.
   Licensed same as original (not specified?), or public domain, whichever is less restrictive.
Some code snippets from stackoverflow.com/questions/58428545/clarify-functionality-of-tkinter-autocomplete-entry
"""


class Box(ttk.Combobox):

    def __init__(self, master, my_font=("Arial", 10), on_select=None):
        super().__init__(master, font=my_font)
        self.on_select = on_select
        if on_select is not None:
            self.bind("<<ComboboxSelected>>", lambda e: on_select(self.get()))

    def set_completion_list(self, completion_list):
        """Use our completion list as our drop down selection menu, arrows move through menu."""
        def naturalsortable(key):
            return [int(text) if text.isdigit() else text.lower() for text in re.split('([0-9]+)', key)]
        self._completion_list = sorted(completion_list, key=naturalsortable)  # Work with a sorted list
        self._hits = []
        self._hit_index = 0
        self.position = 0
        self.detect_pressed_filled = False
        self.bind('<KeyRelease>', self.handle_keyrelease)
        self['values'] = self._completion_list  # Setup our popup menu

    def autocomplete(self, delta=0):
        """autocomplete the Combobox, delta may be 0/1/-1 to cycle through possible hits"""
        if delta:  # need to delete selection otherwise we would fix the current position
            self.delete(self.position, tk.END)
        else:  # set position to end so selection starts where textentry ended
            self.position = len(self.get())
        # collect hits
        _hits = []
        for element in self._completion_list:
            if element.lower().startswith(self.get().lower()):  # Match case insensitively
                _hits.append(element)
        # if we have a new hit list, keep this in mind
        if _hits != self._hits:
            self._hit_index = 0
            self._hits = _hits
        # only allow cycling if we are in a known hit list
        if _hits == self._hits and self._hits:
            self._hit_index = (self._hit_index + delta) % len(self._hits)
        # now finally perform the auto completion
        if self._hits:
            self.delete(0, tk.END)
            self.insert(0, self._hits[self._hit_index])
            self.select_range(self.position, tk.END)

    def handle_keyrelease(self, event):
        """event handler for the keyrelease event on this widget"""
        if event.keysym == "BackSpace":
            self.delete(self.index(tk.INSERT), tk.END)
            self.position = self.index(tk.END)
        elif event.keysym == "Left":
            if self.position < self.index(tk.END):  # delete the selection
                self.delete(self.position, tk.END)
            else:
                self.position = self.position - 1  # delete one character
                self.delete(self.position, tk.END)
        elif event.keysym == "Right":
            self.position = self.index(tk.END)  # go to end (no selection)
        elif event.keysym == "Up":
            self.autocomplete(-1)  # cycle to previous hit
        elif len(event.keysym) == 1:
            self.autocomplete()
        elif event.keysym == "Return":  # Tab doesn't work because it cycles to next entry/button
            if self.on_select is not None:
                self.on_select(self.get())


def test(test_list):
    """Run a mini application to test the AutocompleteEntry Widget."""
    root = tk.Tk(className=' AutocompleteEntry demo')
    combo = Box(root, ('Arial', 12))
    combo.set_completion_list(test_list)
    combo.pack()
    combo.focus_set()
    # I used a tiling WM with no controls, added a shortcut to quit
    root.bind('<Control-Q>', lambda event=None: root.destroy())
    root.bind('<Control-q>', lambda event=None: root.destroy())
    root.mainloop()


if __name__ == '__main__':
    test_list = ('apple', 'banana', 'CranBerry', 'dogwood', 'alpha', 'Acorn', 'Anise')
    test(test_list)
