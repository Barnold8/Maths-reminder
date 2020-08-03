from tkinter import *
from tkinter import messagebox
import time
import threading
from win32api import GetSystemMetrics
from random import randint
from winsound import *


class Window(Tk):

    def __init__(self, geom="530x480+500+500", debug=False, title="Debug version", backGroundcolour="black",
                 mStrip=False):
        super().__init__()

        self.globalBG = backGroundcolour
        self.geometry(geom)
        self.config(bg=self.globalBG)
        self.resizable(0, 0)
        self.title(title)

        if debug:
            self.debug_func()

        if mStrip:
            self.menuStrip()

    def endF(self):
        self.destroy()
        exit()

    def Main_menu(self):

        self.destroy()
        New_Window = Main()

   # def getPrevWindow(self, GUIArr):

       # return GUIArr[len(GUIArr) - 1]

    def debug_func(self):
        # TODO Add all debug info in here and other debug functions
        print("Debug passed (GUI)")
        self.resizable(1, 1)

        debug_label_BG = Label(self, width=40, text="BackgroundError: Class, window, init func", bg=self.globalBG,
                               fg="black")
        debug_label_BG.pack()
        debug_label_BG.place(relx=0.25, rely=0.25, x=0, y=0)

        debug_clarification = Label(self, width=40, text="Debug Active", bg=self.globalBG, fg="red")
        debug_clarification.pack()
        debug_clarification.place(relx=0.0, rely=0.0, x=0, y=0)

    def menuStrip(self):  # TODO Add menu strip and allow for file titles and commands

        print("\nMenu strip init...\n")

        self.menubar = Menu(self)

        self.config(bg="black", menu=self.menubar)  # CONFIG IS NEEDED HERE TO ADD MENU ONTO FRAME

        fileMenu = Menu(self.menubar, tearoff=False)
        miscMenu = Menu(self.menubar, tearoff=False)
        self.menubar.add_cascade(label="Main", menu=fileMenu)

        # Menu ---------------------------------------------------
        fileMenu.add_command(label="Main Menu", command=self.Main_menu)
        fileMenu.add_command(label="Exit", command=self.endF)

        # MiscMenu ------------------------------------------------
        self.menubar.add_cascade(label="Misc", menu=miscMenu)
        miscMenu.add_command(label="DrawBoard",
                             command=self.DBoard)  # TODO, THESE WILL BE SEPERATE WINDOWS THAT DONT DESTROY THE PREVIOUS WINDOW
        miscMenu.add_command(label="Calculator", command=self.Calc)

        print("Menu strip init successful \n\n")

    def DBoard(self):

        New_Window = DrawBoard()

    def Calc(self):
        pass


class Main(Window):

    def __init__(self, geom="300x480+500+200", debug=False, title="Main Menu", backGroundcolour="black", mStrip=True,
                 b_int=5):

        super().__init__(geom=geom, debug=debug, title=title, backGroundcolour=backGroundcolour, mStrip=mStrip)

        try:
            self.menubar.destroy()
        except Exception as e:
            print(e)

        self.Start = Button(self, text="Start", width=b_int * 2, height=b_int, command=self.start_Game,
                            foreground="black", background="#9fafc9", activebackground="#717c8f",
                            activeforeground="white")
        self.Start.pack()
        self.Start.place(x=120, y=100)

        self.ExitButton = Button(self, text="Exit", width=b_int * 2, height=b_int, command=self.endF,
                                 foreground="black", background="#9fafc9", activebackground="#717c8f",
                                 activeforeground="white")
        self.ExitButton.pack()
        self.ExitButton.place(x=120, y=300)

    def start_Game(self):
        if messagebox.askyesno("Play type", "Would you like to play a predetermined game?") == True:

            timeBool = messagebox.askyesno("Timer",
                                           "Would you like a real time timer to run in real time with your progress? (This may impact performance)")
            self.destroy()

            New_Window = Game(pred=True, useTime=timeBool)
            #New_Window.resizable(1,1) #TODO REMOVE THIS AFTER DEBUG
            New_Window.mainloop()
        else:
            timeBool = messagebox.askyesno("Timer",
                                           "Would you like a real time timer to run in real time with your progress? (This may impact performance)")
            self.destroy()

            New_Window = Game(pred=False, useTime=timeBool)
            New_Window.mainloop()


class Game(Window):

    def __init__(self, pred=False, useTime=False):
        super().__init__(title="Game")

        self.a = randint(1,10)
        self.b = randint(1, 10)

        self.predeterminedQuestionData = {

            "Q1": {

                "Question" : f"What's {self.a}x{self.b}?",
                "Answer" :  self.a * self.b

            },
            "Q2": {

                "Question": f"What's {self.a * self.b} / {self.a}?",
                "Answer": self.b

            }
        }


        self.Q = Question(self)

        self.Game = True
        self.tStart = time.time()
        self.tEnd = 0
        self.timeTaken = 0
        self.useTime = useTime
        self.time = StringVar()

        self.counter = 1

        if pred:
            self.predetermined()
            self.data = self.predeterminedQuestionData
        else:
            pass  # todo READ JSON FILE TO DETERMINE CODE EXECUTION <----------

        if self.useTime:
            self.timeThread()
        else:
            self.geometry("530x480+500+200")

    def WindowSetup(self):
        self.menuStrip()


        if self.useTime:
            aLabel = Label(self, width=20, text="Enter your answer below", bg="black", fg="white", font=("Roboto", 12))
            aLabel.pack()
            aLabel.place(relx=0.05, rely=0.35)

            self.QEnter = Entry(self, width=20)
            self.QEnter.pack()
            self.QEnter.place(relx=0.1, rely=0.45)
            self.startButton = Button(text="Start Game",command=self.startGameWithTimer,width=10)
            self.startButton.pack()
            self.startButton.place(relx=0.38, rely=0.8)

            self.AnsButton = Button(text="Enter",command=self.answerQuest,width=10)
            self.AnsButton.pack()
            self.AnsButton.place(relx=0.14,rely=0.55)

        else:                                                                                                                     #TODO, work on the questions, meaning
            aLabel = Label(self, width=20, text="Enter your answer below", bg="black", fg="white", font=("Roboto", 12))           #TODO the predetermined ones and how they work 02/08/2020
            aLabel.pack()
            aLabel.place(relx=0.05, rely=0.30)

            self.QEnter = Entry(self, width=20)
            self.QEnter.pack()
            self.QEnter.place(relx=0.1, rely=0.45)
            self.startButton = Button(text="Start Game",command=self.startGame,width=10)
            self.startButton.pack()
            self.startButton.place(relx=0.38,rely=0.8)

            self.AnsButton = Button(text="Enter",command=self.answerQuest,width=10)
            self.AnsButton.pack()
            self.AnsButton.place(relx=0.14,rely=0.55)

    def startGameWithTimer(self):
        self.startButton.destroy()

        self.Q.grabQuestion(self.data["Q1"]["Question"],self.data["Q1"]["Answer"])
        print(self.data)
        self.startGame()
        self.timerWidget()

    def startGame(self):

        print(f"DATA IS {self.data}")
        self.startButton.destroy()
        self.Q.grabQuestion(self.data["Q1"]["Question"],self.data["Q1"]["Answer"])

    def timeGet(self):
        print(threading.active_count())
        while self.Game:

            pastsixtytime = self.timeTaken / 60
            pasthour = self.timeTaken / (60 * 60)

            self.tEnd = time.time()

            self.timeTaken = self.tEnd - self.tStart
            # This fucking code took me 1h 37m to fucking figure out
            if self.timeTaken < 60:
                placement = round(self.timeTaken, 2)
                self.timeTaken = placement
                self.time.set(f"{self.timeTaken} second(s)")

            elif self.timeTaken >= 60:
                self.time.set(f"{round(pastsixtytime, 2)} minute(s)")
            # print(f"{pastsixtytime}")

            elif self.timeTaken >= 60 * 60:
                self.time.set(f"{round(pasthour, 2)} hour(s)")
                # print(f"{pasthour}")

    def timeThread(self):
        threading.Thread(target=self.timeGet).start()

    def timerWidget(self):
        lab = Label(self, width=20, text="Time taken:", bg="black", fg="white", font=("Roboto", 16))
        lab.pack()

        timeLabel = Label(self, width=20, textvariable=self.time, bg="black", fg="white", font=("Roboto", 16))
        timeLabel.pack()
        # timeLabel.place(relx=x,rely=y)

    def predetermined(self):  # TODO This is going to be all of the game, this will have questions, these are going to be predetermined.

        self.WindowSetup()

    def answerQuest(self):
        global toIntAns
        Answer =self.QEnter.get()
        print(f"Answer IS : {Answer}")

        if self.Q.checkAns(Answer):
            self.counter += 1
            if self.counter > len(self.data):
                messagebox.showinfo("WINNER!!!", "Congrats you completed the challenge... Ending the program")
                print(self.counter, len(self.data))
                self.destroy()
                exit()

            self.Q.grabQuestion(self.data[f"Q{self.counter}"]["Question"],self.data[f"Q{self.counter}"]["Answer"])

        else:
            try:
                toIntAns = int(Answer)
            except Exception as e:
                messagebox.showinfo("ERROR",f"No value was entered.\nProgram error {e}")
            try:
                if self.Q.checkAns(toIntAns):
                    self.counter += 1
                    print(self.counter)
                    if self.counter > len(self.data):
                        messagebox.showinfo("WINNER!!!","Congrats you completed the challenge... Ending the program")
                        print(self.counter, len(self.data))
                        self.destroy()
                        exit()
                    else:
                        self.Q.grabQuestion(self.data[f"Q{self.counter}"]["Question"], self.data[f"Q{self.counter}"]["Answer"])

                else:
                    print("Wrong")
            except Exception as e:
                print(f"Unimportant error : {e}")

        self.update()

        #TODO add a way to interact with question object to check the answer and move onto the next question | DONEEEE 03/08/2020

class DrawBoard(Window):  # This has been fully done

    def __init__(self):

        super().__init__(title="Draw Board")
        self.resizable(1, 1)
        defW = 1920
        defH = 1080

        self.colARR = ["#FF0000", "#FF9E00", "#ECFF00", "#36FF00",
                       "#00FF9E", "#00FFFF", "#003AFF", "#7400FF",
                       "#FF00D1", "#FF0068", "#000000", "#FFFFFF"]
        self.fg = 0  # This is all colour related data, fg and bg are just index counters for the self.collARR array
        self.bg = 0  # fg = PEN, bg = background

        self.col = self.colARR[0]

        try:
            self.canvasMAP = Canvas(self, width=GetSystemMetrics(0), height=GetSystemMetrics(1), bg="white")
        except Exception as e:
            print(f"The error most likely occurred due to the OS not being Windows\n\nProgram return error: {e}")
            self.canvasMAP = Canvas(self, width=defW, height=defH, bg="white")

        self.canvasMAP.pack()

        self.bind("<B1-Motion>", self.draw)

        self.menubar = Menu(self)
        self.config(bg="black", menu=self.menubar)  # CONFIG IS NEEDED HERE TO ADD MENU ONTO FRAME
        fileMenu = Menu(self.menubar, tearoff=False)
        self.menubar.add_cascade(label="Config", menu=fileMenu)
        fileMenu.add_command(label="Clear page", command=lambda: self.canvasMAP.delete("all"))
        fileMenu.add_command(label="Change pen colour", command=self.changePen)
        fileMenu.add_command(label="Change page colour", command=self.changePage)

    def changePen(self):
        self.fg += 1
        self.col = self.colARR[self.fg]
        if self.fg >= len(self.colARR) - 1:
            self.fg = -1
        self.update()

    def changePage(self):
        self.bg += 1
        self.col = self.colARR[self.bg]
        if self.bg >= len(self.colARR) - 1:
            self.bg = -1
        self.canvasMAP.config(bg=self.col)
        self.update()

    def draw(self, event):
        x1, y1 = (event.x - 1), (event.y - 1)
        x2, y2 = (event.x + 1), (
                    event.y + 1)  # Code obtained from https://www.youtube.com/watch?v=OdDCsxfI8S0 (VERY helpful)
        pen = self.canvasMAP.create_oval(x1, y1, x2, y2, fill=self.col, width=0)
        self.canvasMAP.itemconfig(pen, fill=self.col)  # t

class Question:

    def __init__(self,canvasROOT):

        self.question = ""
        self.answer = 0

        self.canv = Canvas(canvasROOT, bg="black", width=250,height=250,highlightthickness=0) #250
        self.canv.pack()
        self.canv.place(relx=0.45,rely=0.2)

    def grabQuestion(self,questionStr,questionAns):

        self.question = questionStr
        self.answer = questionAns

        self.canv.create_text(125,60,fill="white",font=("Roboto", 15),text=self.question)

    def checkAns(self,ans):

        answer = ans
        if answer == self.answer:
            print("TRUE")
            self.canv.delete("all")
            self.Tick()
            return True
        else:
            print(f"ANS = {ans}, self.answer = {self.answer}")

            self.Buzzer()
            return False

    def Tick(self):
        print("Tick executed")
        try:
            photo = PhotoImage(file="tick.gif")
            photo.image = photo
            self.img = self.canv.create_image(160,160,image=photo)
            try:
                self.playsoundThread()
            except Exception as OSError:
                print(OSError)
        except Exception as e:
            print(e)

    def playsoundThread(self):
        threading.Thread(target=lambda:PlaySound("win.wav", SND_FILENAME)).start()


    def Buzzer(self):
        try:
            self.canv.delete(self.img)
        except Exception as e:
            print(f"Unimportant error {e}")
        try:
            photo = PhotoImage(file="buzzer.gif")
            photo.image = photo
            self.img = self.canv.create_image(125,160,image=photo)
        except Exception as e:
            print(e)


class Calculator(Window):

    def __init__(self):
        super().__init__()
