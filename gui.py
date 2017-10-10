from tkinter import *
from tkinter import font as tkFont
from node import Tree
from automota import Automota
from tableGUI import TableGUI
from PIL import ImageTk
from PIL import Image
from TruthTable import TruthTable


class AutomataGUI:
    """
    The main gui form.

    Args:
        root       (Tk): root of a form
        automota   (Automota): an Automota object
        right      (Tree): right child.
        regexVar   (StringVar): value of a line edit
        status     (StringVar): value of a status label
        FrameSizeX (Integer): width of a form
        FrameSizeY (Integer): height of a form.

    Attributes:
        root       (Tk): root of a form.
    """
    def __init__(self, root=None):
        self.root = root
        self.automota = Automota()
        self.initUI()
        startRegex = "&(A, B)"
        self.regexVar.set(startRegex)

    def initUI(self):
        """
        Creates all the widgets of a form.
        """
        self.root.title("Truth table from regular expressions")
        ScreenSizeX = self.root.winfo_screenwidth()
        ScreenSizeY = self.root.winfo_screenheight()
        ScreenRatioX = 0.7
        ScreenRatioY = 0.8
        self.FrameSizeX = int(ScreenSizeX * ScreenRatioX)
        self.FrameSizeY = int(ScreenSizeY * ScreenRatioY)
        padX = 10
        padY = 10
        self.root.geometry("890x150+30+30")
        self.root.resizable(width=False, height=False)

        parentFrame = Frame(self.root,
                            width=int(self.FrameSizeX - 2*padX),
                            height=int(self.FrameSizeY-2*padY))
        parentFrame.grid(padx=padX, pady=padY, stick=E+W+N+S)

        regexFrame = Frame(parentFrame)
        enterRegexLabel = Label(regexFrame,
                                text=("Enter regular expression [operators" +
                                      " allowed are ¬ (~), > (⇒)," +
                                      " = (⇔), & (⋀) and | (⋁)]:"))
        self.regexVar = StringVar()
        self.regexField = Entry(regexFrame, width=70,
                                textvariable=self.regexVar)
        buildRegexButton = Button(regexFrame, text="Build", width=15,
                                  command=self.handleBuildRegexButton)
        enterRegexLabel.grid(row=0, column=0, sticky=W)
        self.regexField.grid(row=1, column=0, sticky=W)
        buildRegexButton.grid(row=1, column=1, padx=5)
        self.status = StringVar()
        self.statusLabel = Label(parentFrame, textvariable=self.status)

        buttonGroup = Frame(parentFrame)
        nfaButton = Button(buttonGroup, text="Show Image", width=15,
                           command=self.handleShowImage)
        dfaButton = Button(buttonGroup, text="Show Table", width=15,
                           command=self.handleGenerateTable)
        minDFAButton = Button(buttonGroup, text="Simplify Table", width=15,
                              command=self.handleSimplifyTable)
        newBtn = Button(buttonGroup, text="Get Normal Form", width=15,
                        command=self.handleNormalForm)
        simplifiedNormalFormBtn = Button(buttonGroup, text="Get Simplified Normal Form", width=20,
                                         command=self.handleSimplifiedNormalForm)
        nandBtn = Button(buttonGroup, text="NANDify", width=15,
                                         command=self.handleNandify)
        nfaButton.grid(row=0, column=1)
        dfaButton.grid(row=0, column=2)
        minDFAButton.grid(row=0, column=3)
        newBtn.grid(row=0, column=4)
        simplifiedNormalFormBtn.grid(row=0, column=5)
        nandBtn.grid(row=1, column=1)
        regexFrame.grid(row=0, column=0, sticky=W, padx=(50, 0))
        self.statusLabel.grid(row=2, column=0, sticky=W, padx=(50, 0))
        buttonGroup.grid(row=3, column=0, sticky=W, padx=(50, 0))

    def handleBuildRegexButton(self):
        """
        Creates a tree using user's input.
        """
        self.automota.counter = 0
        self.automota.tree = None
        self.status.set('')
        regexStr = self.regexVar.get()
        regexStr = regexStr.replace(" ", "")
        try:
            self.automota.parseString(regexStr)
            infix = self.automota.tree.getInfix()
            self.status.set(infix)
            lines = ['graph logic {']
            lines = lines + self.automota.traverseTree(self.automota.tree)
            lines.append('}')
            self.automota.writeToFile(lines)
            self.automota.drawFile()
        except ValueError:
            self.status.set('The input is incorrect')

    def handleShowImage(self):
        """
        Opens a file with the tree.
        """
        image = Image.open('outTree.png')
        image.show()

    def handleGenerateTable(self):
        """
        Generates a table from a tree and
        opens another form with a table.
        """
        tree = self.automota.tree
        variables = tree.findVariables()
        tt = TruthTable(variables, tree)
        self.status.set(tt.getHashCode(tt.rows))
        rows = []
        row = []
        variables.sort()
        for variable in variables:
            row.append(variable)
        row.append('Result')
        rows.append(row)
        rows.extend(tt.rows)
        tableGUI = TableGUI(len(rows), len(rows[0]), rows)
        title = self.automota.tree.getInfix()
        tableGUI.title(title)
        tableGUI.mainloop()

    def handleSimplifyTable(self):
        """
        Generates a simplified table from a tree
        and opens another form with a table.
        """
        tree = self.automota.tree
        variables = tree.findVariables()
        tt = TruthTable(variables, tree)
        simplifiedRows = tt.simplify(tt.rows)
        self.status.set(tt.getHashCode(simplifiedRows))
        rows = []
        row = []
        variables.sort()
        for variable in variables:
            row.append(variable)
        row.append('Result')
        rows.append(row)
        rows.extend(simplifiedRows)
        tableGUI = TableGUI(len(rows), len(rows[0]), rows)
        title = self.automota.tree.getInfix()
        tableGUI.title(title)
        tableGUI.mainloop()

    def handleNormalForm(self):
        """
        Generetes normal form.
        """
        tree = self.automota.tree
        variables = tree.findVariables()
        tt = TruthTable(variables, tree)
        normalTree = tt.getNormalForm(tt.rows, variables)
        self.status.set(normalTree.getInfix())

    def handleSimplifiedNormalForm(self):
        """
        Generetes simplified normal form.
        """
        tree = self.automota.tree
        variables = tree.findVariables()
        tt = TruthTable(variables, tree)
        normalTree = tt.getNormalForm(tt.simplify(tt.rows), variables)
        self.status.set(normalTree.getInfix())

    def handleNandify(self):
        """
        Generetes a nandified form.
        """
        tree = self.automota.tree
        variables = tree.findVariables()
        tt = TruthTable(variables, tree)
        normalTree = tt.getNormalForm(tt.simplify(tt.rows), variables)
        normalTree.clearDoubleNegation()
        nanTree = normalTree.nanDify(normalTree)
        self.automota.tree = nanTree
        self.status.set(nanTree.getInfix())
        lines = ['graph logic {']
        lines = lines + self.automota.traverseTree(self.automota.tree)
        lines.append('}')
        self.automota.writeToFile(lines)
        self.automota.drawFile()


def main():
    root = Tk()
    app = AutomataGUI(root)
    root.mainloop()


if __name__ == '__main__':
    main()
    