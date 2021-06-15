import tkinter as tk
from pathlib import Path
from tkinter.filedialog import askopenfilenames

from GUI import UploadLigandView, FrameWithProcess, SearchResultsView, MultiMofView
from MofIdentifier.fileIO import CifReader

instruction_text = """Choose one or more .cif files from your computer. The MOFs will be loaded onto the database, and 
many of their properties will be calculated. The calculations will take some time (expect 2-10 minutes per MOF), so 
please be patient."""


class Page(FrameWithProcess.Frame):
    def __init__(self, parent):
        self.parent = parent
        super().__init__(self.parent, lambda mofs: self.add_mofs_to_db(mofs))
        instructions = tk.Label(self, text=instruction_text, justify=tk.LEFT)
        instructions.pack()
        open_btn = tk.Button(self, text='Open Mof(s)', command=self.open_mofs)
        open_btn.pack()
        self.mofs = []
        self.mof_preview = MultiMofView.View(self)
        self.mof_preview.pack(fill=tk.X)
        add_btn = tk.Button(self, text='Upload to DB', command=lambda: self.start_process(self.mofs))
        add_btn.pack()

    def open_mofs(self):
        filenames = askopenfilenames(filetypes=[('CIF Files', '*.cif')])
        mofs = []
        if filenames is not None and len(filenames) > 0:
            for filename in filenames:
                try:
                    mof = CifReader.get_mof(str(Path(filename)))
                    mofs.append(mof)
                except:
                    self._show_error('Unable to extract MOF from ' + filename)
        self.mofs = mofs
        self.mof_preview.display_results(self.mofs)

    def add_mofs_to_db(self, mofs):
        print(*mofs)
        pass  # TODO: hook this up to DB
