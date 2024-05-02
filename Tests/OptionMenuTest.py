import tkinter as tk

def Refresh():
    UpdatedOptions = []
    for option in options:
            UpdatedOptions.append(option)
    ChooseOption.set(UpdatedOptions[0])

    OptionMenu.destroy()
    NewOptionMenu = tk.OptionMenu(testWidget, ChooseOption, *UpdatedOptions)
    NewOptionMenu.pack()

testWidget = tk.Tk()
testWidget.title("OptionMenu Test")
testWidget.geometry("200x200")

# Create a list of options
options = ["Option 1", "Option 2", "Option 3", "Option 4", "Option 5"]
SelectLabel = tk.Label(testWidget, text="Select an option:")
SelectLabel.pack()
ChooseOption = tk.StringVar()
ChooseOption.set(options[0])
OptionMenu = tk.OptionMenu(testWidget, ChooseOption, *options)
OptionMenu.pack()
RefreshButton = tk.Button(testWidget, text="Refresh", command=lambda: Refresh())
RefreshButton.pack()

testWidget.mainloop()