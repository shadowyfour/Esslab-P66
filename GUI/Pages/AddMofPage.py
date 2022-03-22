import tkinter as tk
from pathlib import Path
from tkinter.filedialog import askopenfilenames

from DAOsAndServices.MOFDatabase import MOFDatabase
from GUI import Settings
from GUI.Utility import FrameWithProcess, StyledButton, MultipleAutoCompleteSearch, AutoCompleteComboBox
from GUI.Views import MultiMofView
from DAOsAndServices import MOFDAO
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
        open_btn = StyledButton.make(self, text='Open Mof(s)', command=self.open_mofs)
        open_btn.pack()
        self.mofs = []
        self.mof_preview = MultiMofView.View(self)
        self.mof_preview.pack(fill=tk.X)
        row1 = tk.Frame(self)
        source_name_instructions = tk.Label(row1, text="Source Database: ", justify=tk.LEFT)
        source_name_instructions.pack(side=tk.LEFT)
        self.source_name_ent = AutoCompleteComboBox.Box(row1)
        self.set_source_name_suggestions()
        self.source_name_ent.pack(side=tk.LEFT)
        row1.pack()
        self.add_btn = StyledButton.make(self, text='Upload to DB', command=lambda: self.start_process(self.mofs))
        self.add_btn['state'] = "disabled"
        self.add_btn.pack()

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
                    return
        for mof in mofs:
            if MOFDAO.get_MOF(mof.label) is not None:
                self._show_error(f'A mof by the name of {mof.label} already exists in the database, and we are unable '
                                 f'to add it again (for now)')
                return
        self.mofs = mofs
        mofs_for_display = [MOFDatabase.from_mof(mof) for mof in mofs]
        self.mof_preview.display_results(mofs_for_display)
        if len(mofs) > 0:
            self.add_btn['state'] = "normal"

    def add_mofs_to_db(self, mofs):
        source_name = self.source_name_ent.get()
        if source_name == "":
            self._show_error("Must input a name for the source database")
            return
        else:
            self.source_name_ent.delete(0, tk.END)
        Settings.add_source_name(source_name)
        self.parent.winfo_toplevel().update_sources_settings()
        self.add_btn['state'] = "disabled"
        self.mof_preview.display_results([])
        for mof in mofs:
            MOFDAO.add_mof(mof, source_name)
        self.parent.winfo_toplevel().forget_history()
        self.mofs = []

    def refresh_attributes_shown(self):
        self.mof_preview.display_results(self.mofs)

    def set_source_name_suggestions(self):
        self.source_name_ent.set_completion_list(Settings.current_source_states().keys())
