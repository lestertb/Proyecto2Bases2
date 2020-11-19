#Selected GUI libs to build graphical interface
import tkinter as tk
from tkinter import ttk,messagebox
#Used as connector driver between SQL server and Python
import pyodbc
#Used to convert XML from SQL server to python dictionary
import xmltodict
#Used to convert XML or list, to JSON Struct
import json
#Used to call an external python file
import os
#Used to call a regular expression library, to evaluate strings
#https://docs.python.org/3/library/re.html
import re

#This is the main function, that includes create window to display the sctucture
#this window contains 2 TextBox, 2 Buttons, and a comboBox to interact with user
#all the consults may be written in the first TextBox, the second TextBox is only used to show results
#the consults may be 3 diferent types, estimated, actual and simple
#and the indexes uses compare the table index vs used by system indexes

def execution_plan(conn):
    root = tk.Tk()
    root.minsize(800, 400)
    root.title("Execution Plan window")
    style = ttk.Style()
    style.theme_use('clam')

    queryFrame = tk.Frame(root, bd=10, bg="black")
    queryFrame.config(cursor="pirate")
    queryFrame.pack(pady=10, anchor="center")

    cLabel = tk.Label(queryFrame, text="Tipo de reporte: ",font='Courier 12')
    cLabel.grid(row=0, column=0, padx=10, pady=10)

    comboBoxTypes = ttk.Combobox(queryFrame, width="20", values=["Detallado/Estimado","Detallado/Actual","Simple"],justify='center',font='Courier 12')
    comboBoxTypes.grid(row=0, column=1, padx=10, pady=10)
    comboBoxTypes.current(0)

    queryLabel = tk.Label(queryFrame, text="SQl Query: ",font='Courier 12')
    queryLabel.grid(row=1, column=0, padx=10, pady=10)

    queryEntry = tk.Text(queryFrame)
    queryEntry.config(width=120, height=5, padx=25, pady=15)
    queryEntry.grid(row=1, column=1, padx=10)

    scrollb = ttk.Scrollbar(queryFrame, command=queryEntry.yview)
    scrollb.grid(row=1, column=2, sticky='nsew')
    queryEntry['yscrollcommand'] = scrollb.set

    resultFrame = tk.Frame(root, bd=10, bg="black")
    resultFrame.config(relief="sunken")
    resultFrame.pack(pady=2, anchor="center")

    textResult = tk.Text(resultFrame)
    textResult.config(width=120, height=5, padx=25, pady=15)
    textResult.grid(row=0, column=0, padx=10)

    scrollb = ttk.Scrollbar(resultFrame, command=textResult.yview)
    scrollb.grid(row=0, column=2, sticky='nsew')
    queryEntry['yscrollcommand'] = scrollb.set

    #This function gets an execution plan from SQL server an the show to user, using an external lib called json_viwer
    #with this is posible show SQL info into tree_view
    def executeConsult():
        query = queryEntry.get("1.0", 'end-1c')
        queryConfig = ""

        if (comboBoxTypes.current() == 0):
            queryConfig = "SET SHOWPLAN_XML ON"
            queryConfig1 = "SET STATISTICS XML OFF"
            queryConfig2 = "SET SHOWPLAN_ALL OFF"
        elif(comboBoxTypes.current() == 1):
            queryConfig = "SET STATISTICS XML ON"
            queryConfig1 = "SET SHOWPLAN_XML OFF"
            queryConfig2 = "SET SHOWPLAN_ALL OFF"
        else:
            queryConfig = "SET SHOWPLAN_ALL ON"
            queryConfig1 = "SET STATISTICS XML OFF"
            queryConfig2 = "SET SHOWPLAN_XML OFF"

        try:

            res = conn.cursor()
            res.execute(queryConfig1)
            res.execute(queryConfig2)
            res.execute(queryConfig)
            res.execute(query)
            xmlHelper = ""

            if (comboBoxTypes.current() == 0):
                resultSet = res.fetchone()
                xmlHelper = '<root>' + resultSet[0] + '</root>'
            elif (comboBoxTypes.current() == 1):
                res.nextset()
                resultSet = res.fetchone()
                xmlHelper = '<root>' + resultSet[0] + '</root>'



            json_convert = ""
            if(comboBoxTypes.current()<2):
                dictionary = xmltodict.parse(xmlHelper)
                json_convert = json.dumps(dictionary)

            if (comboBoxTypes.current() == 2):
                dictionary = res.fetchall()
                acc = []
                for x in dictionary:
                    split = x[0].split(",")
                    for e in split:
                        acc.append(e)
                json_convert = json.dumps(acc)
            file = open(r"functions/treeView.json", "wt")
            file.write(json_convert)
            file.close()
            #For Linux
            #TODO This can cause an error when is used on Linux or Windows
            #os.system("python functions/json_viewer.py functions/treeView.json")
            #For windows, python is added to PATH as python
            os.system("python functions/json_viewer.py functions/treeView.json")
            return json_convert

        except pyodbc.Error as err:
            tk.messagebox.showerror(title="Error", message=err)

    # This function executes consult to get the execution plan from SQL server, and when the callback comes from server
    # this refresh the layout an put the data to the final user. This is used to show indexes uses in a consult vs the indexes from table
    def indexesConsult():
        textResult.delete('1.0', tk.END)

        queryConfig = "SET SHOWPLAN_ALL ON"
        queryConfig1 = "SET STATISTICS XML OFF"
        queryConfig2 = "SET SHOWPLAN_XML OFF"

        try:

            query = queryEntry.get("1.0", 'end-1c')
            res = conn.cursor()
            res.execute(queryConfig1)
            res.execute(queryConfig2)
            res.execute(queryConfig)
            res.execute(query)

            dictionary = res.fetchall()
            list_ = []
            for x in dictionary:
                stringBuilder = str(x)
                encountered = re.findall("OBJECT:\(\[.*?\]\.\[.*?\]\.\[.*?\]\.\[.*?\]\)", stringBuilder)
                list_ = list_ + encountered
            filteredList = (list(set(list_)))
            textResult.insert(tk.END,"Index usados:\n")
            for y in filteredList:
                splitedE = y.split(".")
                treated = splitedE[3].replace("[","")
                treated = treated.replace("]", "")
                textResult.insert(tk.END, "   ->"+treated + "\n")

            param = queryEntry.get("1.0", 'end-1c')

            if(re.search("FROM",param)):
                param = param.split("FROM")
            else:
                param = param.split("from")
            param = param[1].split(" ")
            val = param[1].replace(" ","")
            val = val.replace(";","")
            query = "SELECT name AS Index_Name,type_desc  As Index_Type,is_unique,OBJECT_NAME(object_id) As Table_Name FROM sys.indexes WHERE is_hypothetical = 0 AND index_id != 0 AND object_id = OBJECT_ID('"+val+"');"
            queryConfig = "SET SHOWPLAN_ALL OFF"
            res.execute(queryConfig)
            res.execute(query)
            textResult.insert(tk.END, "Index de la tabla:\n")
            response = res.fetchall()
            for i in response:
                textResult.insert(tk.END, "   ->" + i[0] + "\n")

        except pyodbc.Error as err:
            tk.messagebox.showerror(title="Error", message=err)
            return None

    queryButton = tk.Button(queryFrame, text="Plan",command = executeConsult,font='Courier 12')
    queryButton.grid(row=1, column=3, padx=10)

    resultButton = tk.Button(resultFrame, text="Index", command=indexesConsult, font='Courier 12')
    resultButton.grid(row=0, column=3, padx=10)


    root.mainloop()

