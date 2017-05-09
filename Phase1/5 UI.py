import pandas as pd
import numpy as np

try:
    # Python2
    from Tkinter import *
except ImportError:
    # Python3
    from tkinter import *

#
direc = r'C:\\Users\\DD\\OneDrive\\Documents\\Rapid_Assessment_Tools\\UI\\'
input_excel = pd.ExcelFile(direc+'result_test_2.xlsx')
input_df = input_excel.parse("Sheet1")
goal_df = pd.read_csv(direc+'SDG_Goal.csv')


template = pd.read_excel(direc+'template_namibia.xlsx')

def rename(input):
    l = list(input.keys())
    for i in range(0,len(l)-1):
        key = str(l[i]).split('_')[0]
        input[str(key)]=input.pop(l[i])

def match(input, goal_no, template):
    for row in range(1,len(template)):
        if str(template['sector'][row]) in input:
            template[str(goal_no)][row] = 'X'

def get_top(input_dict:dict, input_df, goal_no, index_col_name:str, sentence_col_name:str):
    i = 0
    n = 0

    while i < len(input_df) and n < 10:
        input_df_top = input_df.sort(columns=goal_no, ascending=False).head(10).reset_index(drop=True)
        # this slice is just for test
        if input_df_top[goal_no][i] != 0:
            total_index = input_df_top[index_col_name][i]
            p = input_df_top[sentence_col_name][i]
            input_dict[total_index] = p
            n += 1
        i += 1

running = True
def stop():
    """Stop scanning by setting the global flag to False."""
    global running
    running = False

#def show_entry_fields():
#   root.quit
#   print("Goal is: %s\n" % e1.get())

output_dict = {}
for goal_no in list(input_df.columns)[3:6]:

    input_dict = {}
    get_top(input_dict, input_df, goal_no, 'sector_sent', 'sentence')


    goal = goal_df['SDG sub Goal content'][goal_df['Number'] == float(goal_no)].item()

    root = Tk()
    root.title("Sustainable Development Goal Matching")

    global j
    j = []

    x_dict = input_dict.copy()
    x_list = list(x_dict.values())

    def checked(text):
        return lambda : j.append(text)

    def quit():
        root.quit()

#    goal_df = pd.ExcelFile(direc+'SDG_Features_0.xlsx').parse("Sheet1")
#    string = goal_df['SDG sub Goal content'][goal_df['Number'] == goal_no]
    number = str(goal_no)
    w_label1 = Label(root, text="Check the box if sentence addressed goal %s :"%number,
                     pady=5, wraplength = 800, justify = LEFT, font = ("Helvetica", 16, "bold","italic")
                    ).pack(side=TOP, anchor=W, fill=X, expand=YES)
    w_label2 = Label(root, text="%s"%goal,
                    wraplength = 750, justify = LEFT, font = ("Helvetica", 12)
                    ).pack(side=TOP, anchor=W, fill=X, expand=YES)

    for i in x_list:
        c = Checkbutton(root, text=i, command=checked(i),
                        bd = 3, justify = LEFT, pady = 5, wraplength = 950,anchor=W,
                        onvalue = 1, offvalue = 0)
        c.pack(side=TOP, anchor=W, fill=X, expand=YES)

    # w_close = Button(root, text='Quit', command=stop, justify=CENTER).pack()
    w_confirm = Button(root, text="Confirm", fg="green",command=quit).pack()
    # w_text = Text(root, "Confirm", fg="green").grid(row = 1)


    mainloop()


    # output_dict = {}
    for k, v in input_dict.items():
        if v in j:
            output_dict[k] = v
            # print(k, v)

    # print(goal_no)
    rename(output_dict)
    match(output_dict, goal_no, template)

template.to_excel(direc+'t2.xlsx')
