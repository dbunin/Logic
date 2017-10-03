from tkinter import *
from tkinter import font as tkFont
from node import Tree
from automota import Automota
from PIL import ImageTk
from PIL import Image


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
        self.root.geometry("1160x625+30+30")
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
        self.regexField = Entry(regexFrame, width=80,
                                textvariable=self.regexVar)
        buildRegexButton = Button(regexFrame, text="Build", width=10,
                                  command=self.handleBuildRegexButton)
        enterRegexLabel.grid(row=0, column=0, sticky=W)
        self.regexField.grid(row=1, column=0, sticky=W)
        buildRegexButton.grid(row=1, column=1, padx=5)
        self.status = StringVar()
        self.statusLabel = Label(parentFrame, textvariable=self.status)

        buttonGroup = Frame(parentFrame)
        nfaButton = Button(buttonGroup, text="Show Image", width=15,
                           command=self.handleShowImage)
        dfaButton = Button(buttonGroup, text="TBD", width=15,
                           command=self.handledfaButton)
        minDFAButton = Button(buttonGroup, text="TBD", width=15,
                              command=self.handleminDFAButton)
        nfaButton.grid(row=0, column=1)
        dfaButton.grid(row=0, column=2)
        minDFAButton.grid(row=0, column=3)

        automataCanvasFrame = Frame(parentFrame, height=100, width=100)
        self.cwidth = int(self.FrameSizeX - (2*padX + 20))
        self.cheight = int(self.FrameSizeY * 0.6)
        self.automataCanvas = Canvas(automataCanvasFrame, bg='#FFFFFF',
                                     width=self.cwidth,
                                     height=self.cheight,
                                     scrollregion=(0, 0, self.cwidth,
                                                   self.cheight))
        self.canvasitems = []
        self.automataCanvas.pack()
        
        regexFrame.grid(row=0, column=0, sticky=W, padx=(50,0))
        self.statusLabel.grid(row=2, column=0, sticky=W, padx=(50,0))
        buttonGroup.grid(row=3, column=0)
        automataCanvasFrame.grid(row=4, column=0, sticky=E+W+N+S)
        

    def handleBuildRegexButton(self):
        self.automota.counter = 0
        self.automota.tree = None
        self.status.set('')
        regexStr = self.regexVar.get()
        regexStr = regexStr.replace(" ", "")
        try:
            self.automota.parseString(regexStr)
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

    def handlenfaButton(self):
        pass

    def handledfaButton(self):
        pass

    def handleminDFAButton(self):
        pass

    def createAutomata(self, inp):
        pass

    def displayAutomata(self):
        pass


def main():
    root = Tk()
    app = AutomataGUI(root)
    root.mainloop()


if __name__ == '__main__':
    main()