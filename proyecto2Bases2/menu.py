import tkinter as tk
from proyecto2Bases2 import tablePrivileges
from proyecto2Bases2 import  executionPlan

def menu(conn):
    root = tk.Tk()
    root.minsize(400, 200)
    root.maxsize(400,200)
    root.title("Selection menu")

    selectionFrame = tk.Frame(root, bd=10, bg="black")
    selectionFrame.config(relief="sunken")
    selectionFrame.config(cursor="pirate")
    selectionFrame.pack(pady=10, anchor="center")

    def monitorAction():
        tablePrivileges.tablePrivileges(conn)



    def planAction():
        executionPlan.execution_plan(conn)



    monitor = tk.PhotoImage(file="monitor.png")
    monitor = monitor.subsample(1, 1)
    monitorButton = tk.Button(selectionFrame, text='Monitor de permisos', command = monitorAction, image=monitor)
    monitorButton.pack(pady=5,padx = 10 , side = "left")

    plan = tk.PhotoImage(file="plan.png")
    plan = plan.subsample(1, 1)
    planButton = tk.Button(selectionFrame, text='Plan de ejecucion', command = planAction, image=plan)
    planButton.pack(pady=5,padx = 10, side="left")



    root.mainloop()

