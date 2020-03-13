import tkinter	
import testScript 

top = tkinter.Tk()
top.geometry('350x200')

variable1 = tkinter.StringVar()
txt0 = tkinter.Text(top,width=30,height=5)
txt0.grid(column=0, row=0)


#Button
def clicked():
    testScript.start(txt0.get("1.0",'end-1c'))

btn = tkinter.Button(top, text="Bấm", command = clicked)
btn.grid(column=1, row=1)


top.mainloop()
