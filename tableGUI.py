import tkinter as tk


class TableGUI(tk.Tk):
    """
    The secondary GUI with a Truth Table.

    Attributes:
        rows    (int): number of rows
        colomns (int): number of colomns
        data    (List): list of rows to put in table.
    """
    def __init__(self, rows, colomns, data):
        tk.Tk.__init__(self)
        t = SimpleTable(self, rows, colomns)
        t.pack(side="top", fill="x")
        for i, row in enumerate(data):
            for j, colomn in enumerate(row):
                t.set(i, j, colomn)


class SimpleTable(tk.Frame):
    """
    A table class.

    Args:
        _widgets             (List): List of widgets
        grid_columnconfigure (Grid): Grid on form.

    Attributes:
        parent  (Tk): parent of a table
        rows    (int): number of rows
        columns (List): number of colomns.
    """
    def __init__(self, parent, rows, columns):
        # use black background so it "peeks through" to 
        # form grid lines
        tk.Frame.__init__(self, parent, background="black")
        self._widgets = []
        for row in range(rows):
            current_row = []
            for column in range(columns):
                label = tk.Label(self, text="%s/%s" % (row, column), 
                                 borderwidth=0, width=10)
                label.grid(row=row, column=column, sticky="nsew", padx=1, pady=1)
                current_row.append(label)
            self._widgets.append(current_row)

        for column in range(columns):
            self.grid_columnconfigure(column, weight=1)

    def set(self, row, column, value):
        widget = self._widgets[row][column]
        widget.configure(text=value)
