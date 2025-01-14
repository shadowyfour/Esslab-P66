import tkinter as tk
import tkinter.font as tkFont

from GUI import os_specific_settings, Settings, SourceCheck
from DAOsAndServices import MOFDAO, SBUDatabase
from GUI.Utility.HorizontalScrollFrame import HorizontalScrollFrame
from MofIdentifier.fileIO import FileOpen


def select_for_edit(parent, sbu):
    parent.winfo_toplevel().select_sbu_for_edit(sbu)


class View(HorizontalScrollFrame):
    def __init__(self, parent, sbu: SBUDatabase.SBUDatabase):
        self.parent = parent
        self.mol = sbu
        self.top_page = parent.winfo_toplevel()
        super().__init__(self.parent, height=40, bd=1, relief=tk.SOLID)
        self.frame = self.get_frame()

        row1 = tk.Frame(master=self.frame)
        name = tk.Label(row1, text=sbu.name)
        name.pack(side='left')

        search = tk.Label(row1, text="Search", cursor=os_specific_settings.LINK_CURSOR, padx=8)
        f = tkFont.Font(search, search["font"])
        f.configure(underline=True)
        search.configure(font=f)
        search.bind('<Button-1>', lambda e: parent.winfo_toplevel().force_search_sbu(sbu.name))
        search.pack(side='left')

        tk.Label(row1, text="  ", font=("Arial", 16)).pack(side='left')
        edit = tk.Label(row1, text=os_specific_settings.EDIT_ICON, cursor=os_specific_settings.LINK_CURSOR, padx=2,
                        font=("Arial", 16), height=0)
        edit.bind('<Button-1>', lambda e: select_for_edit(parent, sbu))
        edit.pack(side='left')

        tk.Label(row1, text="  ", font=("Arial", 16)).pack(side='left')
        see = tk.Label(row1, text=os_specific_settings.SEE_ICON, cursor=os_specific_settings.LINK_CURSOR, padx=2,
                       font=("Arial", 14), height=0)
        see.bind('<Button-1>', lambda e: FileOpen.make_and_see(sbu.get_sbu()))
        see.pack(side='left')

        open = tk.Label(row1, text=os_specific_settings.OPEN_ICON, cursor=os_specific_settings.LINK_CURSOR, padx=2, font=("Arial", 14), height=0)
        open.bind('<Button-1>', lambda e: FileOpen.make_and_open(sbu.get_sbu()))
        open.pack(side='left')

        row1.pack(fill=tk.X)

        row2 = tk.Frame(master=self.frame)
        file_first_line = sbu.file_content.partition('\n')[0]
        first_line_label = tk.Label(row2, text=f"({file_first_line} atoms total:) ")
        first_line_label.pack(side=tk.LEFT)
        elements = tk.Label(row2, text=sbu.get_sbu().atoms_string())
        elements.pack(side=tk.LEFT)
        row2.pack(fill=tk.X)

        self.generate_mof_row().pack(side='left')

    def generate_mof_row(self):
        mof_row = tk.Frame(master=self.frame, height=10)
        if all(Settings.current_source_states().values()):
            mofs = self.mol.mofs
        else:
            mofs = list(SourceCheck.enabled_mofs_of_sbu(self.mol))
        mof_label = tk.Label(mof_row, text=f"In {len(mofs)} MOFs: ")
        mof_label.pack(side='left')
        for name in mofs:
            self.display_mof_name(mof_row, name)
        return mof_row

    def display_mof_name(self, parent, name):
        text = name
        mof_label = tk.Label(parent, text=text, cursor=os_specific_settings.LINK_CURSOR, padx=3)
        f = tkFont.Font(mof_label, mof_label["font"])
        f.configure(underline=True)
        mof_label.configure(font=f)
        event_function = self.have_page_highlight_mof(name)
        mof_label.bind('<Button-1>', event_function)
        mof_label.pack(side='left')

    def have_page_highlight_mof(self, clicked_name):
        def fun(*args):
            mof = MOFDAO.get_MOF(clicked_name)
            self.top_page.highlight_molecule(mof)

        return fun
