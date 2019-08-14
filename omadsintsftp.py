import Tkinter,tkFileDialog

root = Tkinter.Tk()
filez = tkFileDialog.askopenfilenames(parent=root,title='Choose a file')
print root.tk.splitlist(filez)