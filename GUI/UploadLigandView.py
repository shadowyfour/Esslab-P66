import tkinter as tk
from tkinter.filedialog import askopenfilename
from tkinter import messagebox

from MofIdentifier.fileIO import CifReader, LigandReader


class View(tk.Frame):
    def __init__(self, parent):
        self.parent = parent
        tk.Frame.__init__(self, self.parent, bd=2, relief=tk.SOLID)

        btn = tk.Button(self, text='Open Ligand', command=lambda: self.open_file())
        btn.pack()

    def open_file(self):
        filename = askopenfilename(filetypes=[('XYZ Files', '*.xyz'), ('SMILES Files', '*.txt')])
        if filename is not None and len(filename) > 0:
            try:
                mol = LigandReader.get_mol_from_file(filename)
            except:
                messagebox.showerror("Bad File", "Unable to extract a molecule from this file")
                return
            self.parent.add_custom_ligand(mol)