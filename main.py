import os
import time
from tkinter import *
from tkinter.ttk import *
import tkinter.filedialog as filedialog
import tkinter.messagebox as messagebox

root = Tk()
root.title("Multiple choices widget")
root.geometry('+' + str(round(root.winfo_screenwidth() / 2 - 250)) +
              '+' + str(round(root.winfo_screenheight() / 2 - 150)))
root.geometry("500x300")

root.resizable(False, False)
for i in range(12):
    root.grid_rowconfigure(i, minsize=20)
for i in range(10):
    root.grid_columnconfigure(i, minsize=50)

# ---------- SETUP ----------
timeLimit = 60 * 90
curTime = 0
timeStr = StringVar()
timeStr.set(time.strftime('%H:%M:%S', time.gmtime(max(0, timeLimit - curTime))))


def changeBrowserState(newState):
    browseButton["state"] = newState
    file["state"] = newState


def browse():
    filename = filedialog.askopenfilename()
    file.delete(0, "end")
    file.insert(0, filename)


path = StringVar()
file = Entry(root, textvariable=path)
file.grid(row=0, column=0, columnspan=8, sticky=(N, W, S, E))
browseButton = Button(root, text="Browse", command=browse)
browseButton.grid(row=0, column=8, columnspan=2, sticky=(N, W, S, E))
clock = Label(root, textvariable=timeStr, anchor=CENTER)
clock.grid(row=1, column=6, columnspan=2, sticky=(N, W, S, E))


def getKeys(path):
    if path == None or path == "":
        path = "keys.txt"
    s = ""
    if not os.path.exists(path):
        f = open(path, "w")
    with open(path, "r") as file:
        s = file.read()
    while len(s) < 50:
        s += ' '
    return s


def changeAnswersOptionMenuState(newState):
    submitButton['state'] = newState
    for answer in answersOptionMenu:
        answer.config(state=newState)


keys = ""
answers = []


def countCorrect(keys):
    for answer in answersVar:
        answers.append(answer.get())
    correct = 0
    for i in range(min(50, len(keys), len(answers))):
        if answers[i].lower() == keys[i].lower():
            correct += 1
            answersLabel[i].config(background="lime green")
        else:
            answersLabel[i].config(background="orange red")
    return correct


viewType = 0
titles = ["Keys", "My Answers"]


submitted = False


def submit():
    global submitted
    # ---------- DISABLING ----------
    startTimerButton['state'] = DISABLED
    submitted = True
    changeAnswersOptionMenuState(DISABLED)
    # ---------- SHOW GRADE ----------
    cntCorrect = countCorrect(keys)
    grade = "{:.1f}".format(cntCorrect * 0.2)
    with open("grades.txt", "a") as file:
        file.write(grade)
        file.write('\n')
    newLabel = Label(root, text="Your grade: " + grade +
                     " (" + str(cntCorrect) + "/50)")
    newLabel.grid(row=12, column=0, columnspan=3)
    # ---------- VIEW KEYS ----------
    viewTitle = StringVar()
    viewTitle.set(titles[viewType])
    #

    def switch():
        global viewType
        viewType ^= 1
        viewTitle.set(titles[viewType])
        if viewType == 0:
            for i in range(50):
                answersVar[i].set(answers[i].upper())
        else:
            for i in range(50):
                answersVar[i].set(keys[i].upper())

    viewKeys = Button(root, textvariable=viewTitle, command=switch)
    viewKeys.grid(row=12, column=6, columnspan=2)


def verifySubmission():
    res = messagebox.askyesno(
        title="Submit", message="Do you want to submit?")
    if res == True:
        submit()


style = Style()
style.configure("TButton", font=("TkDefaultFont", 10, "bold"))
style.configure("TLabel", font=("TkDefaultFont", 10))
style.configure("TMenubutton", font=("TkDefaultFont", 10, "bold"))
answersVar = [StringVar() for i in range(50)]
answersLabel = []
answersOptionMenu = [OptionMenu(
    root, answersVar[i], " ", "A", "B", "C", "D") for i in range(50)]
submitButton = Button(root, text="Submit",
                      command=verifySubmission, state=DISABLED)
changeAnswersOptionMenuState(DISABLED)

# ---------- TIMER ----------


def startTimer():
    global keys
    changeBrowserState(DISABLED)
    keys = getKeys(file.get())
    startTimerButton['state'] = DISABLED
    changeAnswersOptionMenuState(NORMAL)
    updateTimer()


def updateTimer():
    global submitted, curTime, timeLimit
    if submitted == False and bar['value'] <= 100:
        curTime += 1
        timeStr.set(time.strftime(
            '%H:%M:%S', time.gmtime(max(0, timeLimit - curTime))))
        bar['value'] += 100 / timeLimit
        root.after(1000, updateTimer)
    else:
        submit()


startTimerButton = Button(root, text="Start Timer", command=startTimer)
startTimerButton.grid(row=1, column=8, columnspan=2, sticky=(N, W, S, E))
bar = Progressbar(root)
bar.grid(row=1, column=0, columnspan=6, sticky=(N, W, S, E))

# ---------- INPUT ----------


for i in range(50):
    answersLabel.append(Label(root, text=str(i+1), anchor=CENTER))
    answersLabel[i].grid(row=2*(i//10)+2, column=i % 10, sticky=(N, W, S, E))
    answersOptionMenu[i].config(width=2)
    answersOptionMenu[i].grid(row=2*(i//10)+3, column=i % 10)

submitButton.grid(row=12, column=8, columnspan=2, sticky=(N, W, S, E))


def on_closing():
    if messagebox.askyesno("Quit", "Do you want to quit?") == True:
        root.destroy()


root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
