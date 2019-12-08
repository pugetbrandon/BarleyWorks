from tkinter import *

# from tkinter.tix import LabelEntry

# recipe_dictionary ={'Recipe Name': recipeName, 'Strike Temperature':stkTemp, "Mash Temperature": mash1Temp, "Mash Time":mash1Time, 'Boil Time': boilTime, 'Bitter Hopper': bitterTime}
recipelist = []


def getrecipe():
    fields = (
        'Recipe Name', 'Strike Temperature', 'Mash Temperature', 'Mash Time', 'Boil Time', 'Bitter Hopper',
        'Flavor Hopper',
        'Aroma Hopper', 'Ferm Temperature')


    def use_recipe(entries):

        global recipelist

        for field in fields:
            value = (entries[field].get())
            recipelist.append(value)

        print("in recipe file ", recipelist)

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
    adjustlist = [3, 4, 5, 6, 7, 9]

    recipelist.append(filterTime)
    print(recipelist)
    for i in range(6):
        recipelist[adjustlist[i]] = int(recipelist[adjustlist[i]]) * 60
    print(recipelist)
    return recipelist #TODO  need to adjust the times from seconds to minutes before return

def gettestrecipe():
    recipelist = ['Test Recipe', 75, 150, 60, 5, 4, 3, 2, 70, 1]
    return recipelist
