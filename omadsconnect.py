# coding=utf-8
from Tkinter import *
import tkMessageBox
from ttk import *
from PIL import Image, ImageTk
import os
import select
import sys
import getpass
import paramiko
import socket
import logging
import Xlib.support.connect as xlib_connect
import webbrowser


LOGGER = logging.getLogger(__name__)

window = Tk()

window.title("Omadsconnect")
window.configure(background='#F0F8FF')
icon=PhotoImage("photo",file='./images/logo.gif')
window.tk.call('wm', 'iconphoto', window._w, icon)
window.geometry('550x400+400+200')
window.resizable(width=False, height=False)
#style
style= Style()
style.configure('TButton', font = 
               ('calibri', 16, 'bold'), 
                    borderwidth = '2',
                    background='#F0F8FF') 
style.configure('TMenubutton', background="#F0F8FF")
style.configure('TEntry', borderwidth=3, highlightbackground='black')
window.grid_columnconfigure(0, weight=1)
window.grid_columnconfigure(4, weight=1)
window.grid_rowconfigure(0,weight=1)
window.grid_rowconfigure(3,weight=1)
window.grid_rowconfigure(10,weight=1)
window.grid_rowconfigure(12,weight=1)



# host
lblhost = Label(window, text="Host ", background='#F0F8FF', font='bold')
lblhost.grid(column=1, row=4, sticky='e')
txthost = Entry(window, width=15, style='TEntry')
txthost.focus()
txthost.grid(column=2, row=4)
# usr
lblusr = Label(window, text="User ", background='#F0F8FF', font='bold')
lblusr.grid(column=1, row=5, sticky='e')
txtusr = Entry(window, width=15)
txtusr.grid(column=2, row=5)
# password
lblpwd = Label(window, text="Password ", background='#F0F8FF', font='bold')
lblpwd.grid(column=1, row=6, sticky='e')
txtpwd = Entry(window, show="*", width=15)
txtpwd.grid(column=2, row=6)
# port
lblprt = Label(window, text="Port ", background='#F0F8FF', font='bold')
lblprt.grid(column=1, row=7, sticky='e')
txtprt = Entry(window, width=15)
txtprt.grid(column=2, row=7)
#labels
lblwel=Label(window, text='Welcome to OmadsConnect', background='#F0F8FF', font=('calibri', 12, 'bold'))
lblwel.grid(row=1, column=1, columnspan=3)
lblley=Label(window,text='Innovation ...\nTechnology...\nSolution...', background='#F0F8FF', font=('calibri', 12, 'bold'))
lblley.grid(column=1,row=11,sticky='es')
lbloma=Label(window, text='Visit: ', background='#F0F8FF', font=('calibri', 14))
lbloma.grid(column=3, row=11)
def callback(url):
    webbrowser.open_new(url)
lblhyp=Label(window, text='https://omads.co', background='#F0F8FF', font=('calibri', 14))
lblhyp.grid(column=3, row=11, sticky='ws')
lblhyp.bind("<Button-1>", lambda e: callback("https://omads.co/shop"))
#opcion
progList=[
    "Programs",
    "labview64",
    "matlab",
    "calcula",
    "octave --force-gui"
]
selProg = StringVar()
selProg.set(progList[0])

proMenu= OptionMenu(window,selProg,*progList, style="TMenubutton")
proMenu.grid(column=2,row=8)
lblprog=Label(window,text="Select Program ", background='#F0F8FF', font='bold')
lblprog.grid(column=1,row=8 , sticky='e')

# def
def conne():
    if selProg.get()=='Programs':
        tkMessageBox.showerror("Error","Select a Program")
    else:


        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(txthost.get(), username=txtusr.get(), password=txtpwd.get(), port=txtprt.get())
        #del password

        # maintain map
        # { fd: (channel, remote channel), ... }
        channels = {}

        poller = select.poll()
        def x11_handler(channel, (src_addr, src_port)):
            '''handler for incoming x11 connections
            for each x11 incoming connection,
            - get a connection to the local display
            - maintain bidirectional map of remote x11 channel to local x11 channel
            - add the descriptors to the poller
            - queue the channel (use transport.accept())'''
            x11_chanfd = channel.fileno()
            local_x11_socket = xlib_connect.get_socket(*local_x11_display[:4])
            local_x11_socket_fileno = local_x11_socket.fileno()
            channels[x11_chanfd] = channel, local_x11_socket
            channels[local_x11_socket_fileno] = local_x11_socket, channel
            poller.register(x11_chanfd, select.POLLIN)
            poller.register(local_x11_socket, select.POLLIN)
            LOGGER.debug('x11 channel on: %s %s', src_addr, src_port)
            transport._queue_incoming_channel(channel)

        def flush_out(session):
            while session.recv_ready():
                sys.stdout.write(session.recv(4096))
            while session.recv_stderr_ready():
                sys.stderr.write(session.recv_stderr(4096))

        # get local disply
        local_x11_display = xlib_connect.get_display(os.environ['DISPLAY'])
        # start x11 session
        transport = ssh_client.get_transport()
        session = transport.open_session()
        session.request_x11(handler=x11_handler)
        session.exec_command(selProg.get())
        session_fileno = session.fileno()
        poller.register(session_fileno, select.POLLIN)
        # accept first remote x11 connection
        transport.accept()

        # event loop
        while not session.exit_status_ready():
            poll = poller.poll()
            # accept subsequent x11 connections if any
            if len(transport.server_accepts) > 0:
                transport.accept()
            if not poll: # this should not happen, as we don't have a timeout.
                break
            for fd, event in poll:
                if fd == session_fileno:
                    flush_out(session)
                # data either on local/remote x11 socket
                if fd in channels.keys():
                    channel, counterpart = channels[fd]
                    try:
                        # forward data between local/remote x11 socket.
                        data = channel.recv(4096)
                        counterpart.sendall(data)
                    except socket.error:
                        channel.close()
                        counterpart.close()
                        del channels[fd]

        print 'Exit status:', session.recv_exit_status()
        flush_out(session)
        session.close()
#no sirve

# button
btn = Button(window, text="Connect", style="TButton",command=conne)
btn.grid(column=3, row=9)

# image
image = Image.open("./images/omadsl1.png")
photo = ImageTk.PhotoImage(image)
lblimag = Label(image=photo, background='#F0F8FF')
lblimag.image = photo
lblimag.grid(row=2, column=1, columnspan=3)
#icono


window.mainloop()
