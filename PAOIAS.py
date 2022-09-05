import tkinter as tk
import random, time
        
class PopupWindow(object):
    def __init__(self, master, line, obj):
        self.pop = tk.Toplevel(master)
        self.parent = obj
        self.pop.title("Popup")
        self.line = line[0]
        self.l = tk.Label(self.pop, text="Change line "+str(self.line))
        self.l.pack()
        self.e = tk.Entry(self.pop)
        self.e.insert(tk.END, line[1])
        self.e.pack()
        self.b = tk.Button(self.pop, text='Ok', command=self.cleanup)
        self.b.pack()
    def cleanup(self):
        self.v = self.e.get()
        self.parent.data[self.line-self.parent.offset] = self.v
        self.parent.cmem.delete(self.line-self.parent.offset)
        self.parent.cmem.insert(self.line-self.parent.offset, (self.line, self.v))
        self.parent.cmem.itemconfig(self.line-self.parent.offset, {'fg':'blue'})
        self.parent.bmem.delete(self.line-self.parent.offset)
        self.parent.bmem.insert(self.line-self.parent.offset, (self.line, self.parent.com2bin(self.v)))
        self.parent.bmem.itemconfig(self.line-self.parent.offset, {'fg':'blue'})
        self.pop.destroy()

class Window:
    def __init__(self):
        self.window = tk.Tk()
        # self.offset = random.randint(0, 100)
        self.offset = 0
        self.regs = ["PC", "AX", "BX", "CF", "DX", "EX", "FX", "GX", "M1", "M2"]
        self.comment = ["Program Conter (line)", "current number", "current max", "compare flag",
        "in array position", "array left", "loop address", "skip address", "mult1", "mult2"]
        self.coms = ["MOV", "LEA", "INC", "DEC", "ADD", "SUB", "LBL", "IFN", "IFP", "JOC", "MUL", "END"]
                 
        self.reg = {}
        self.reg_lab = {}
        for i in self.regs:
            # exec('''self.'''+i+''' = random.randint(0,200)''')
            exec('''self.'''+i+''' = 0''')
            exec('''self.label_'''+i+''' = tk.Label(self.window, text=self.'''+i+''', width=15)''')
            exec('''self.reg["'''+i+'''"] = self.'''+i)
            exec('''self.reg_lab["'''+i+'''"] = self.label_'''+i)
        exec('''self.'''+self.regs[0]+''' = self.offset''')
        self.cmem = tk.Listbox(self.window, width=30, height=35)
        self.bmem = tk.Listbox(self.window, width=30, height=35)
        
        self.finish = False
        self.buttonhold = False
        self.dbg = tk.Label(self.window, text="dbg", width=30, wraplength=200)
        
        self.commands()
        self.draw()
        self.fillmems()
        self.window.mainloop()
        
    def commands(self):
        self.data = []
        com1 = ["BEGIN",
        "ADD DX,PC,18", # Записать в регистр D адрес начала массива
        "LEA EX,DX", # Записать в регистр E значение начала массива
        "LBL FX,Loop:",
        "INC DX", # Сдвинуть текущий адрес на 1.
        "LEA AX,DX", # Получить число в текущей позиции
        "SUB AX,AX,BX", # Сравнить A и B, если B больше значение будет отрицательным
        "IFN CF,AX", # Проверить что число отрицательное
        "JOC GX,Skip", # Если не новое максимальное значение
        "ADD BX,AX,BX", # Заменить максимальное значение
        "LBL GX,Skip:",
        "DEC EX", # Убавить оставшийся размер
        "IFP CF,EX", # Если массив закончился
        "JOC FX,Loop", # Если не ноль, продолжить
        "ADD DX,PC,3",
        "WRT BX,DX"]        
        self.data.extend(com1)
        self.data.append(0)  
        self.data.append(0)
        self.data.append(0)      
        self.numbers = []
        for i in range(random.randint(5,15)):
        	self.numbers.append(random.randint(0, 254))
        self.data.append(len(self.numbers))
        self.data.extend(self.numbers)
        self.data.append(0)
        
        com2 = [
        "BEGIN",
        "ADD DX,PC,22", # Записать в регистр D адрес начала массива
        "ADD GX,PC,15", # Записать в регистр G адрес результата
        "LEA EX,DX", # Записать в регистр E значение начала массива
        "LBL FX,Loop:",
        "INC DX", # Сдвинуть текущий адрес на 1.
        "LEA AX,DX", #Записать из первого массива в A
        "ADD DX,DX,6",
        "LEA BX,DX", #Записать из первого массива в B
        "SUB DX,DX,6",
        "MUL GX,AX,BX",
        "INC GX",
        "DEC EX", # Убавить оставшийся размер
        "IFP CF,EX", # Если массив закончился
        "JOC FX,Loop", # Если не ноль, продолжить
        "END"] # Завершить выполнение и выйти из программы
        self.data.extend(com2)
        self.data.append(0)  
        self.data.append(0)
        self.data.append(0)
        self.data.append(0)
        self.data.append(0)
        self.data.append(0)
        self.data.append(0)      
        self.numbers1 = []
        for i in range(5):
        	self.numbers1.append(random.randint(1, 60))
        self.data.append(len(self.numbers1))
        self.data.extend(self.numbers1)
        self.numbers2 = []
        for i in range(5):
        	self.numbers2.append(random.randint(1, 60))
        self.data.append(len(self.numbers2))
        self.data.extend(self.numbers2)
        self.data.append(0)
        
    def draw(self):  
        self.window.title("Фон Неймана, 3-адресная, Макс значение")
        self.dbg.grid(row=0, column=0, columnspan=2)
        data_text = tk.Label(self.window, text="Memory", width=20).grid(row=0, column=2)
        bin_text = tk.Label(self.window, text="Memory (bin)", width=20).grid(row=0, column=3)
        
        for i in range(len(self.regs)):
            exec('''label_'''+self.regs[i]+'''_text = tk.Label(self.window, text="'''+
            self.regs[i]+": "+self.comment[i]+'''").grid(row='''+str(i+1)+''', column=0)''')
            exec('''self.label_'''+self.regs[i]+'''.grid(row='''+str(i+1)+''', column=1)''')
            
        self.cmem.grid(row=1, column=2, rowspan=13)
        self.bmem.grid(row=1, column=3, rowspan=13)
        
        fastbutton = tk.Button(self.window, text=" >> ", width=10)
        fastbutton.grid(row=11, column=0, columnspan=2)
        fastbutton.bind('<ButtonPress-1>',self.start_fast)
        fastbutton.bind('<ButtonRelease-1>',self.stop_fast)
        forwardbutton = tk.Button(self.window, text=" > ", width=10, command=self.commandup).grid(row=12, column=0, columnspan=2)
        
        self.cmem.bind('<Double-1>', self.edit)
        
    def fillmems(self):
        for i in range(len(self.data)):
            self.cmem.insert(tk.END, (i+self.offset, self.data[i]))
            self.bmem.insert(tk.END, (i+self.offset, self.com2bin(self.data[i])))
        self.reg["PC"] = int(self.cmem.get(0)[0])
        self.update("PC")
        self.cmem.itemconfig(0, {'bg':'red'})
        self.bmem.itemconfig(0, {'bg':'red'})
         
    def command(self, command):
        debug = ""
        if isinstance(command, str) == True:
            cmd = command.split()[0]
            if cmd == "END":
                debug = "END, Finish operations"
                self.finish = True
            elif cmd == "MOV":
                arg1 = command.split()[1].split(',')[0]
                arg2 = command.split()[1].split(',')[1]
                debug = "MOV, Write "+arg2+" to "+arg1
                if arg2 in self.regs:
                    self.reg[arg1] = int(self.reg[arg2])
                elif arg2:
                    self.reg[arg1] = int(arg2)
                self.update(arg1)
            elif cmd == "LEA":
                arg1 = command.split()[1].split(',')[0]
                arg2 = command.split()[1].split(',')[1]
                debug = "LEA, Copy from address in "+arg2+" to "+arg1
                if arg2 in self.regs:
                    arg2 = int(self.cmem.get(self.reg[arg2]+self.offset)[1])
                else:
                    arg2 = int(self.cmem.get(arg2+self.offset)[1])
                self.reg[arg1] = arg2
                self.update(arg1)
            elif cmd == "INC":
                arg1 = command.split()[1]
                debug = "INC, Increment "+arg1
                self.reg[arg1] += 1
                self.update(arg1)
            elif cmd == "DEC":
                arg1 = command.split()[1]
                debug = "DEC, Decrement "+arg1
                self.reg[arg1] -= 1
                self.update(arg1)
            elif cmd == "LBL":
                arg1 = command.split()[1].split(',')[0]
                debug = "LBL, Save label at "+str(self.reg["PC"])+" to "+arg1
                self.reg[arg1] = self.reg["PC"]
                self.update(arg1)
            elif cmd == "ADD":
                arg1 = command.split()[1].split(',')[0]
                arg2 = command.split()[1].split(',')[1]
                arg3 = command.split()[1].split(',')[2]
                debug = "ADD, Add "+arg2+" and "+arg3+", write to "+arg1
                if arg2 in self.regs:
                    a = int(self.reg[arg2])
                else:
                    a = int(arg2)
                if arg3 in self.regs:
                    b = int(self.reg[arg3])
                else:
                    b = int(arg3)
                self.reg[arg1] = int(a+b)
                self.update(arg1)
            elif cmd == "SUB":
                arg1 = command.split()[1].split(',')[0]
                arg2 = command.split()[1].split(',')[1]
                arg3 = command.split()[1].split(',')[2]
                debug = "SUB, Subtract "+arg3+" from "+arg2+", write to "+arg1
                if arg2 in self.regs:
                    a = int(self.reg[arg2])
                else:
                    a = int(arg2)
                if arg3 in self.regs:
                    b = int(self.reg[arg3])
                else:
                    b = int(arg3)
                self.reg[arg1] = int(a-b)
                self.update(arg1)
            elif cmd == "IFN":
                arg1 = command.split()[1].split(',')[0]
                arg2 = command.split()[1].split(',')[1]
                debug = "IFN, Check if "+arg2+" negative, write to "+arg1
                if self.reg[arg2]<0:
                    self.reg[arg1] = 1
                else:
                    self.reg[arg1] = 0
                self.update(arg1)
            elif cmd == "IFP":
                arg1 = command.split()[1].split(',')[0]
                arg2 = command.split()[1].split(',')[1]
                debug = "IFP, Check if "+arg2+" negative, write to "+arg1
                if self.reg[arg2]>0:
                    self.reg[arg1] = 1
                else:
                    self.reg[arg1] = 0
                self.update(arg1)
            elif cmd == "JOC":
                arg1 = command.split()[1].split(',')[0]
                debug = "JOC, Jump to "+arg1+" if CF raised"
                if self.reg["CF"]==1:
                    self.cmem.itemconfig(self.reg["PC"]-self.offset, {'bg':'white'})
                    self.bmem.itemconfig(self.reg["PC"]-self.offset, {'bg':'white'})
                    self.reg["PC"] = self.reg[arg1]
                    self.cmem.itemconfig(self.reg["PC"]-self.offset, {'bg':'red'})
                    self.bmem.itemconfig(self.reg["PC"]-self.offset, {'bg':'red'})
                    self.update("PC")
                    self.cmem.see(self.PC-self.offset)
                    self.bmem.see(self.PC-self.offset)
            elif cmd == "MUL":
                arg1 = command.split()[1].split(',')[0]
                arg2 = command.split()[1].split(',')[1]
                arg3 = command.split()[1].split(',')[2]
                debug = "MUL, multiply "+arg2+" and "+arg3+", save to"+arg1
                if arg1 in self.regs:
                    line = int(self.reg[arg1])
                else:
                    line = int(arg1)
                if arg2 in self.regs:
                    arg2 = int(self.reg[arg2])
                else:
                    arg2 = int(arg2)
                if arg3 in self.regs:
                    arg3 = int(self.reg[arg3])
                else:
                    arg3 = int(arg23)
                r = str(format(int(arg2)*int(arg3), '16b'))
                r = r.replace(" ", "0")
                self.reg["M1"] = r[0:8]
                self.reg["M2"] = r[8:16]
                self.update("M1")
                self.update("M2")
                while len(str(r))<16: w = "0"+r
                self.cmem.delete(line-self.offset)
                self.cmem.insert(line-self.offset, (line, str(int(r, 2))))
                self.cmem.itemconfig(line-self.offset, {'fg':'blue'})
                r = r[0:4] + " " + r[4:8] + " " + r[8:12] + " " + r[12:16]
                self.bmem.delete(line-self.offset)
                self.bmem.insert(line-self.offset, (line, r))
                self.bmem.itemconfig(line-self.offset, {'fg':'blue'})
            elif cmd == "WRT":
                arg1 = command.split()[1].split(',')[0]
                arg2 = command.split()[1].split(',')[1]
                debug = "WRT, Write "+arg1+" to address "+arg2
                if arg1 in self.regs:
                    w = int(self.reg[arg1])
                else:
                    w = int(arg1)
                if arg2 in self.regs:
                    line = int(self.reg[arg2])
                else:
                    line = int(arg2)
                self.cmem.delete(line-self.offset)
                self.cmem.insert(line-self.offset, (line, w))
                self.cmem.itemconfig(line-self.offset, {'fg':'blue'})
                while len(str(w))<16: w = "0"+str(w)
                w = w[0:4] + " " + w[4:8] + " " + w[8:12] + " " + w[12:16]
                self.bmem.delete(line-self.offset)
                self.bmem.insert(line-self.offset, (line, w))
                self.bmem.itemconfig(line-self.offset, {'fg':'blue'})
        self.dbg.config(text=debug)
        # print(command)
        # print(self.reg)
               
    def update(self, reg):
        self.reg_lab[reg].config(text=self.reg[reg])
        
    def com2bin(self, com):
        ret = "0000 0000 0000 0000"
        if isinstance(com, str) == True:
            if com[0:3] in self.coms:
                ret = format(self.coms.index(com[0:3])+1, '04b')
                if com[4:6] in self.regs:
                    ret += " "+format(self.regs.index(com[4:6])+1, '04b')
                    if com[7:9] in self.regs:
                        ret += " "+format(self.regs.index(com[7:9])+1, '04b')
                        if com[10:12] in self.regs:
                            ret += " "+format(self.regs.index(com[10:12])+1, '04b')
                        elif com[10:].isnumeric() == True:
                            ret += " "+format(int(com[10:]), '04b')                            
                    elif com[7:].isnumeric() == True:
                        ret += " "+format(int(com[7:]), '08b')                        
                elif com[4:].isnumeric() == True:
                    ret += " "+format(int(com[4:]), '08b')
        else:
            ret = format(int(com), '016b')
            ret = ret[0:4] + " " + ret[4:8] + " " + ret[8:12] + " " + ret[12:16]
        while len(ret) < 16:
            ret = ret+" 0000"
        return ret
        
    def edit(self, event):
        # print("click click")
        # print("focus is:", self.cmem.get(self.cmem.curselection()))
        self.popup = PopupWindow(self.window, self.cmem.get(self.cmem.curselection()), self)
        
    def commandup(self):
        if self.reg["PC"] < len(self.data)+self.offset-1 and self.finish != True:
            self.cmem.itemconfig(self.reg["PC"]-self.offset, {'bg':'white'})
            self.bmem.itemconfig(self.reg["PC"]-self.offset, {'bg':'white'})
            self.reg["PC"] += 1
            self.cmem.itemconfig(self.reg["PC"]-self.offset, {'bg':'red'})
            self.bmem.itemconfig(self.reg["PC"]-self.offset, {'bg':'red'})
            self.update("PC")
            self.cmem.see(self.reg["PC"]-self.offset)
            self.bmem.see(self.reg["PC"]-self.offset)
            self.command(self.cmem.get(self.reg["PC"]-self.offset)[1])

    def fast(self):
        if self.buttonhold:
            self.commandup()
            self.window.after(10, self.fast)

    def start_fast(self, event):
        self.buttonhold = True
        self.fast()

    def stop_fast(self, event):
        self.buttonhold = False
        
if __name__ == "__main__":
    w = Window()
