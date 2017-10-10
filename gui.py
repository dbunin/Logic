from tkinter import *
from tkinter import font as tkFont
from node import Tree
from automota import Automota
from tableGUI import TableGUI
from PIL import ImageTk
from PIL import Image
from TruthTable import TruthTable


class AutomataGUI:
    def __init__(self, root=None):
        self.root = root
        self.automota = Automota()
        self.initUI()
        self.selectedButton = 0
        startRegex = "&(A, B)"
        self.regexVar.set(startRegex)

    def initUI(self):
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
        simplifiedNormalFormBtn = Button(buttonGroup, text="Get Simplified Normal Form", width=15,
                              command=self.handleSimplifiedNormalForm)
        nfaButton.grid(row=0, column=1)
        dfaButton.grid(row=0, column=2)
        minDFAButton.grid(row=0, column=3)
        newBtn.grid(row=0, column=4)
        simplifiedNormalFormBtn.grid(row=0, column=5)
        regexFrame.grid(row=0, column=0, sticky=W, padx=(50, 0))
        self.statusLabel.grid(row=2, column=0, sticky=W, padx=(50, 0))
        buttonGroup.grid(row=3, column=0, sticky=W, padx=(50, 0))

    def handleBuildRegexButton(self):
        self.automota.counter = 0
        self.automota.tree = None
        self.status.set('')
        regexStr = self.regexVar.get()
        regexStr = regexStr.replace(" ", "")
        try:
            self.automota.parseString(regexStr)
            infix = self.automota.getInfix(self.automota.tree)
            self.status.set(infix)
            lines = ['graph logic {']
            lines = lines + self.automota.traverseTree(self.automota.tree)
            lines.append('}')
            self.automota.writeToFile(lines)
            self.automota.drawFile()
        except ValueError:
            self.status.set('The input is incorrect')

    def handleShowImage(self):
        image = Image.open('outTree.png')
        image.show()

    def handleGenerateTable(self):
        tree = self.automota.tree
        variables = self.automota.findVariables(tree)
        tt = TruthTable(variables, tree)
        rows = []
        row = []
        variables.sort()
        for variable in variables:
            row.append(variable)
        row.append('Result')
        rows.append(row)
        rows.extend(tt.rows)
        tableGUI = TableGUI(len(rows), len(rows[0]), rows)
        title = self.automota.getInfix(self.automota.tree)
        tableGUI.title(title)
        tableGUI.mainloop()

    def handleSimplifyTable(self):
        tree = self.automota.tree
        variables = tree.findVariables()
        tt = TruthTable(variables, tree)
        rows = []
        row = []
        variables.sort()
        for variable in variables:
            row.append(variable)
        row.append('Result')
        rows.append(row)
        rows.extend(tt.simplify(tt.rows))
        tableGUI = TableGUI(len(rows), len(rows[0]), rows)
        title = self.automota.getInfix(self.automota.tree)
        tableGUI.title(title)
        tableGUI.mainloop()

    def handleNormalForm(self):
        tree = self.automota.tree
        variables = tree.findVariables()
        tt = TruthTable(variables, tree)
        normalForm = tt.getNormalForm(tt.rows, variables)
        self.status.set(normalForm)

    def handleSimplifiedNormalForm(self):
        tree = self.automota.tree
        variables = tree.findVariables(tree)
        tt = TruthTable(variables, tree)
        normalForm = tt.getNormalForm(tt.simplify(tt.rows), variables)
        self.status.set(normalForm)


def main():
    root = Tk()
    app = AutomataGUI(root)
    root.mainloop()


if __name__ == '__main__':
    main()