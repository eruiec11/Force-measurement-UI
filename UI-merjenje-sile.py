import tkinter as tk
from tkinter import *
from tkinter import ttk
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
import matplotlib.animation as animation
import serial
import serial.tools.list_ports
import time
import warnings

warnings.filterwarnings("ignore", ".*GUI is implemented.*")

ser = serial.Serial('COM4', 9600, timeout=1) #posluša serijsko povezavo
#ser = '2.63,1'
k1 = 2.29
k2 = 2.21                                                                                                               #F =k1*U +k2



x = []
y = []
fig = Figure(figsize=(10, 6), dpi=100)

ax = fig.add_subplot(111)

#ax.set_title('$GRAF$', fontsize=16, color='r')
ax.set_xlabel('$Čas [s]$', fontsize=16)
ax.set_ylabel('$Sila [N]$', fontsize=16)
ax.set_ylim(0., 50.)

class App(tk.Frame):
    def __init__(self, master=None):                                                                                    #Oblikovanje okvirja
        tk.Frame.__init__(self, master)
        self.pack()
        self.button1()
        self.button2()
        self.button5()
        self.button4()
        self.label1()

        self.canvas = FigureCanvasTkAgg(fig, self)                                                                      #platno za matplotlib graf
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=2, column=1, columnspan=7, rowspan=1)

    def button1(self):                                                                                                  #gumb
        self.button1 = ttk.Button(self, text="začni/nadaljuj", command=self.start_animation)
        self.button1.grid(row=0, column=3, padx=1, pady=5)

    def button2(self):                                                                                                  #gumb
        self.button2 = ttk.Button(self, text="pavza", command=self.pause_animation)
        self.button2.grid(row=0, column=4, padx=1, pady=5)

    def button4(self):                                                                                                  #gumb
        self.button4 = ttk.Button(self, text="izhod", command=exit)
        self.button4.grid(row=0, column=6, padx=1, pady=5)

    def button5(self):                                                                                                  #gumb
        self.button5 = ttk.Button(self, text="shrani graf", command=self.save)
        self.button5.grid(row=0, column=5, padx=1, pady=5)

    def label1(self):
        force = 0
        self.label1 = ttk.Label( self, text='Sila  = ' + '%.2f' %force + ' N', width = 15, font=20)
        self.label1.grid(row=1, column=5, padx=1, pady=5)

    def start_animation(self):                                                                                          #Začetek vzorčenja podatkov iz arduina
        ser.write(b's')                                                                                                 #Pošlje na arduino preko serijske povezave črko "s", ki da pin 12 in 13 na 1 stanje
        ser.reset_input_buffer()                                                                                        #izbris vsebine medpomnilnika
        time.sleep(0.1)                                                                                                 #delay po izbrisu vsebine medpolnilnika. po želji
        data = ser.readline().decode()                                                                                  #bere vrstice serijske povezave.
        #print(data)
        #data = ser
        #data_list = [ser.readline().decode().strip().split(',')]
        data_list = [float(i) for i in data.split(',')]                                                                 #Loči podatke o čas in napetosti, itd.
        x.append(data_list[1])                                                                                          #oblikovnje seznama iz podatkov časa
        y.append(data_list[0]*k1 +k2)                                                                                        #Oblikovanje seznama iz podatkov napetosti, itd.
        x1 = np.asarray(x)                                                                                              #asarray pretvori python list v numpy array zaradi lažjega računanja
        y1 = np.asarray(y)                                                                                              #asarray pretvori python list v numpy array zaradi lažjega računanja
        ax.plot(x1-x1[0], y1, 'ro')                                                                                     #x1-x1[0] trenuten čas odšteje od začetnega časa da se začne meritev z časom 0s
        ax.plot(x1-x1[0], y1, 'b-')
        #ax.set_title('$GRAF$', fontsize=16)
        ax.set_xlabel('$Čas [s]$', fontsize=16)
        ax.set_ylim(0., 50.)
        ax.set_ylabel('$Sila [N]$', fontsize=16)
        #print(x1)
        #print(y1)
        #ani = animation.FuncAnimation(fig, animate, interval=10)
        fig.canvas.draw()
        global loop
        loop = root.after(250, self.start_animation)
        force = data_list[0]*k1+k2
        self.label1['text']= 'Sila  = ' + '%.2f' %force + ' N'                                                          #Osveži tekst naslova label1
        np.savetxt("Podatki_sila_cas.csv", np.column_stack((y1, x1-x1[0])), delimiter=",", fmt="%.2f")                        #Shrani podatke v .csv datoteki v obliki "sila,čas"

    def pause_animation(self):                                                                                          #Vstavi vzorčenje
        ser.write(b'p')                                                                                                 #Pošlje na arduino preko serijske povezave črko "p", ki da pin 12 in 13 na 0 stanje
        root.after_cancel(loop)                                                                                         #ustavi animcaijo

    def save(self):
        fig.savefig('Graf.png', format='png', dpi=200)                                                                  #sharani sliko grafa


    def exit(self):
        #ser.write(b'p')
        #root.after_cancel(loop)
        #time.sleep(1)
        self.exit = root.destroy()                                                                                      #ustavi cikel uporebniškega vmesnika




if __name__ == "__main__":
    root = tk.Tk()
    App(master=root)
    root.title("Čitalec napetosti")
    root.mainloop()

# root = tk.Tk()
# App(master = root)
# root.title("Čitalec napetosti")
# root.mainloop()

