from tkinter import *

# from tkinter.tix import LabelEntry

# recipe_dictionary ={'Recipe Name': recipeName, 'Strike Temperature':stkTemp, "Mash Temperature": mash1Temp, "Mash Time":mash1Time, 'Boil Time': boilTime, 'Bitter Hopper': bitterTime}
recipelist = []


def getrecipe():
    fields = (
        'Recipe Name', 'Strike Temperature', 'Mash Temperature', 'Mash Time', 'Boil Time', 'Bitter Hopper',
        'Flavor Hopper',
        'Aroma Hopper', 'Ferm Temperature', "Start Code")

    '''
    phaseoptions = ("Heat to Strike", "Fill Mashtun", "Mix Mashtun", "Filter Mashtun", "Mash",
                    "Ready to Transfer to Boiler",
                    "Transfer to Boiler", "Heat to Boil", "Boil", "Cool to Fermentation Temperature",
                    "Ready to Transfer to Fermenter", "Transfer to Boiler")
    '''

    def use_recipe(entries):

        global recipelist

        for field in fields:
            value = (entries[field].get())
            recipelist.append(value)


    def makeform(root, fields):
        entries = {}
        for field in fields:
            row = Frame(root)
            lab = Label(row, width=22, text=field + ": ", anchor='w')
            ent = Entry(row)
            # lab1 = LabelEntry(row, width=22, text=field+": ", anchor='w')
            ent.insert(0, "0")
            row.pack(side=TOP, fill=X, padx=5, pady=5)
            lab.pack(side=LEFT)
            ent.pack(side=RIGHT, expand=YES, fill=X)
            entries[field] = ent
        return entries

    if __name__ == '__main__' or 'recipe':
        root = Tk()
        ents = makeform(root, fields)
        root.bind('<Return>', (lambda event, e=ents: fetch(e)))
        b1 = Button(root, text='Save Recipe',
                    command=(lambda e=ents: use_recipe(e)))
        b1.pack(side=LEFT, padx=5, pady=5)

        b3 = Button(root, text='Quit', command=root.quit)
        b3.pack(side=LEFT, padx=5, pady=5)
        root.mainloop()

    print(__name__)
    filterTime = 15  #need to check units
    adjustlist = [3, 4, 5, 6, 7, 10]

    recipelist.append(filterTime)
    for i in range(6):
        recipelist[adjustlist[i]] = int(recipelist[adjustlist[i]]) * 60
    recipelist[1] = int(recipelist[1])
    recipelist[2] = int(recipelist[2])
    recipelist[8] = int(recipelist[8])


    return recipelist

def gettestrecipe():
    recipelist = ['Test Recipe', 100, 90, 5, 30, 25, 15, 10, 70, 0, 20]
    return recipelist
