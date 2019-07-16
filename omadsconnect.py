from pexpect import pxssh
from Tkinter import *
from PIL import Image, ImageTk
import os
import select
import sys

window = Tk()

window.title("Omadsconnect")
icon=PhotoImage("photo",file='logo.gif')
window.tk.call('wm', 'iconphoto', window._w, icon)
window.geometry('680x460')
# host
lblhost = Label(window, text="host")
lblhost.grid(column=0, row=1)
txthost = Entry(window, width=15)
txthost.grid(column=1, row=1)
# usr
lblusr = Label(window, text="User")
lblusr.grid(column=0, row=2)
txtusr = Entry(window, width=15)
txtusr.grid(column=1, row=2)
# password
lblpwd = Label(window, text="Password")
lblpwd.grid(column=0, row=3)
txtpwd = Entry(window, show="*", width=15)
txtpwd.grid(column=1, row=3)
# port
lblprt = Label(window, text="Port")
lblprt.grid(column=0, row=4)
txtprt = Entry(window, width=15)
txtprt.grid(column=1, row=4)

# def
def connect():
    def ingcom(mostrar):
        print mostrar
        s.PROMPT = '#'
        s.prompt()
        s.sendline('calcula')
        s.wait(ingcom)
        s.PROMPT = '#'
        s.prompt()
        print s.before     
        s.logout()
        return


    try:
        s = pxssh.pxssh()
        s.SSH_OPTS = "%s -X -o 'StrictHostKeyChecking=no'" % ""
        s.login(txthost.get(), txtusr.get(), txtpwd.get(), port=txtprt.get(), auto_prompt_reset=False)
        mensaje = "SSH OK via port 22"
        ingcom(mensaje)

    except Exception, e:
        print "SSH failed on login."
        print str(e)

# button
btn = Button(window, text="Conectar", command=connect)
btn.grid(column=2, row=5)

# image
image = Image.open("omadsl1.png")
photo = ImageTk.PhotoImage(image)
lblimag = Label(image=photo)
lblimag.image = photo
lblimag.grid(row=0, column=0, columnspan=3, sticky=NW)
#icono


window.mainloop()
