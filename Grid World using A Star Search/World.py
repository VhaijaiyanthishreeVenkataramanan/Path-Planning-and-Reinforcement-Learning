import time
from Tkinter import *
from tkFileDialog import askopenfilename
from PIL import Image, ImageTk
import numpy as np
import tkMessageBox
import tkSimpleDialog
import os

master = Tk()
master.wm_title("Path Planing and reinforcement Learning | Vhaijaiyanthishree | Intelligent Systems 2018")

result = tkMessageBox.askyesno("Search in Grid World", "Do you want to create a new map?")

grid = []
path = os.getcwd() + "/images/"

triangle_size = 0.3
text_offset = 17
cell_score_min = -0.2
cell_score_max = 0.2
Width = 70
actions = ["up", "left", "down", "right"]

if not result:
    filename = askopenfilename(title = "Select map file")
    print(filename)
    if len(filename) == 0:
        tkMessageBox.showwarning('Error', 'No map selected!')
        quit()
    ins = open(filename, "r")
    for line in ins:
        number_strings = line.split()
        numbers = [int(n) for n in number_strings]
        grid.append(numbers)
    (x, y) = (len(grid[0]), len(grid))
    board = Canvas(master, width=x*Width, height=y*Width)
else:
    x_str = tkSimpleDialog.askstring('Size', 'Enter grid size')
    if x_str == None:
        tkMessageBox.showwarning('Error', 'No size found!')
        quit()
    x = int(x_str)
    (x, y) = (x, x)
    path = os.getcwd() + "/images/"
    ghost_pic = ImageTk.PhotoImage(file=path+'ghost.png')
    end_pic = ImageTk.PhotoImage(file=path+'cry.png')
    haunted_pic = ImageTk.PhotoImage(file=path+'haunted_house.png')
    start_pic = ImageTk.PhotoImage(file=path+'ninja.png')

    board = Canvas(master, width=x*Width, height=y*Width)
    start_count = 0
    goal_count = 0

    for i in range(x):
        for j in range(y):
            board.create_rectangle(i*Width, j*Width, (i+1)*Width, (j+1)*Width, fill="grey", width=1)

    board.pack(side=LEFT)
    grid = [[0 for row in range(x)] for col in range(y)]
    item_grid = [[0 for row in grid[0]] for col in grid]

    var = StringVar(master)
    var.set("Select item")

    option = OptionMenu(master, var, "Start", "Ghosts", "End", "Haunted House")
    option.pack()

    robot = 0
    def create_item(event):
        global robot, start_count, goal_count
        x, y = event.x/75, event.y/75
        if item_grid[y][x] == 0:
            if var.get() == "Ghosts":
                item_grid[y][x] = board.create_image(x*Width+35, y*Width+35, image=ghost_pic)
                grid[y][x] = 1
            elif var.get() == "Start":
                item_grid[y][x] = board.create_image(x*Width+35, y*Width+35, image=start_pic)
                # item_grid[y][x] = board.create_rectangle(x*Width+Width*4/10, y*Width+Width*4/10, x*Width+Width*6/10, y*Width+Width*6/10, fill="blue", width=1, tag="me")
                grid[y][x] = 2
                start_count+=1
            elif var.get() == "End":
                item_grid[y][x] = board.create_image(x*Width+35, y*Width+35, image=end_pic)
                grid[y][x] = 3
                goal_count+=1
            elif var.get() == "Haunted House":
                item_grid[y][x] = board.create_image(x*Width+35, y*Width+35, image=haunted_pic)
                grid[y][x] = 4

    board.bind('<Button-1>', create_item)

    def delete_item(event):
        global start_count, goal_count
        x, y = event.x/75, event.y/75
        if item_grid[y][x] != 0:
            board.delete(item_grid[y][x])
            item_grid[y][x] = 0
            grid[y][x] = 0
            if var.get == "start":
                start_count-=1
            elif var.get() == "goal":
                goal_count-=1

    board.bind('<Button-3>', delete_item)
    Label(text="Note: Please close \nthis window once you choose the parameters",font = "Verdana 12").pack(side=BOTTOM)
    master.mainloop()
    master = Tk()
    board = Canvas(master, width=x*Width, height=y*Width)

    if start_count < 1:
        tkMessageBox.showwarning('Error', 'No start found!')
        quit()
    elif goal_count <1:
        tkMessageBox.showwarning('Error', 'No end found!')
        quit()

print (x, y)
walls = []
start = ()
specials = []
pit = []

for i in range(y):
    for j in range(x):
        if grid[i][j] == 1:
            walls.append((j, i))
        if grid[i][j] == 2:
            start = (j, i)
        if grid[i][j] == 3:
            specials.append((j, i, "green", 1))
            goal = (j, i)
        if grid[i][j] == 4:
            specials.append((j, i, "red", -1))
            pit.append((j, i))


player = start
tri_objects = {}
text_objects = {}
flag = True
restart = False

path = os.getcwd() + "/images/"
ghost_pic = ImageTk.PhotoImage(file=path+'ghost.png')
end_pic = ImageTk.PhotoImage(file=path+'cry.png')
haunted_pic = ImageTk.PhotoImage(file=path+'haunted_house.png')
start_pic = ImageTk.PhotoImage(file=path+'ninja.png')


def create_triangle(i, j, action):
    if action == actions[0]:
        return (board.create_polygon((i+0.5-triangle_size)*Width, (j+triangle_size)*Width,
                                    (i+0.5+triangle_size)*Width, (j+triangle_size)*Width,
                                    (i+0.5)*Width, j*Width,
                                    fill="grey", width=1),
                board.create_text((i+0.5)*Width, j*Width+text_offset, text=str(Width), fill="grey"))
    elif action == actions[2]:
        return (board.create_polygon((i+0.5-triangle_size)*Width, (j+1-triangle_size)*Width,
                                    (i+0.5+triangle_size)*Width, (j+1-triangle_size)*Width,
                                    (i+0.5)*Width, (j+1)*Width,
                                    fill="grey", width=1),
                board.create_text((i+0.5)*Width, (j+1)*Width-text_offset, text=str(Width), fill="grey"))
    elif action == actions[1]:
        return (board.create_polygon((i+triangle_size)*Width, (j+0.5-triangle_size)*Width,
                                    (i+triangle_size)*Width, (j+0.5+triangle_size)*Width,
                                    i*Width, (j+0.5)*Width,
                                    fill="grey", width=1),
                board.create_text(i*Width+text_offset, (j+0.5)*Width, text=str(Width), fill="grey"))
    elif action == actions[3]:
        return (board.create_polygon((i+1-triangle_size)*Width, (j+0.5-triangle_size)*Width,
                                    (i+1-triangle_size)*Width, (j+0.5+triangle_size)*Width,
                                    (i+1)*Width, (j+0.5)*Width,
                                    fill="grey", width=1),
                board.create_text((i+1)*Width-text_offset, (j+0.5)*Width, text=str(Width), fill="grey"))


def visualize_grid():
    global specials, walls, Width, x, y, player
    for i in range(x):
        for j in range(y):
            board.create_rectangle(i*Width, j*Width, (i+1)*Width, (j+1)*Width, fill="grey", width=1)
            temp = {}
            temp_val = {}
            for action in actions:
                (temp[action], temp_val[action]) = create_triangle(i, j, action)
            tri_objects[(i,j)] = temp
            text_objects[(i,j)] = temp_val
    for (i, j, c, w) in specials:
        # board.create_rectangle(i*Width, j*Width, (i+1)*Width, (j+1)*Width, fill=c, width=1)
        if w == -1:
            board.create_image(i*Width+35, j*Width+35, image=haunted_pic)
        else:
            board.create_image(i*Width+35, j*Width+35, image=end_pic)
    for (i, j) in walls:
        # board.create_rectangle(i*Width, j*Width, (i+1)*Width, (j+1)*Width, fill="black", width=1)
        board.create_image(i*Width+35, j*Width+35, image=ghost_pic)

visualize_grid()


def set_color(state, action, val):
    global cell_score_min, cell_score_max
    triangle = tri_objects[state][action]
    text = text_objects[state][action]
    turquoise = int(min(255, max(0, (val - cell_score_min) * 255.0 / (cell_score_max - cell_score_min))))
    magenta = hex(255-turquoise)[2:]
    spring_green = hex(turquoise)[2:]
    if len(spring_green) == 1:
        spring_green += "0"
    if len(magenta) == 1:
        magenta += "0"
    color = "#" + magenta + spring_green + "bf"
    board.itemconfigure(triangle, fill=color)
    board.itemconfigure(text, text = str(format(val, '.2f')), fill="black")


def move_bot(new_x, new_y):
    global player, x, y, score, walk_reward, robot, restart

    if (new_x >= 0) and (new_x < x) and (new_y >= 0) and (new_y < y) and not ((new_x, new_y) in walls):
        board.coords(robot, new_x*Width+35, new_y*Width+35)
        player = (new_x, new_y)


def restart_game():
    global player, score, robot, restart
    player = (0, y-1)
    score = 1
    restart = False
    # board.coords(robot, start[0]*Width+Width*4/10, start[1]*Width+Width*4/10, start[0]*Width+Width*6/10, start[1]*Width+Width*6/10)
    board.coords(robot, start[0]*Width+35, start[1]*Width+35)


def showExpand(expanded_list, fgh_dict):
    expanded_list = expanded_list[1:]
    for e in expanded_list:
        board.create_rectangle(e[0]*Width, e[1]*Width, (e[0]+1)*Width, (e[1]+1)*Width, fill="Cyan")
        board.create_text((e[0]+0.5)*Width, e[1]*Width+text_offset, text='f=' + str(format(fgh_dict[e]['f'], '.1f')), fill="black")
        board.create_text((e[0]+0.5)*Width, e[1]*Width+text_offset+20, text='g=' + str(fgh_dict[e]['g']), fill="black")
        board.create_text((e[0]+0.5)*Width, e[1]*Width+text_offset+40, text='h=' + str(format(fgh_dict[e]['h'], '.1f')), fill="black")
        # board.coords(robot, start[0]*Width+35, start[1]*Width+35)
        time.sleep((w1.get() + 0.1)/ 100)

    for (i, j, c, w) in specials:
        if w == -1:
            board.create_image(i*Width+35, j*Width+35, image=haunted_pic)
        else:
            board.create_image(i*Width+35, j*Width+35, image=end_pic)


robot = board.create_image(start[0]*Width+35, start[1]*Width+35, image=start_pic)

def move():
    global robot
    board.delete(robot)
    robot = board.create_image(player[0]*Width+35, player[1]*Width+35, image=start_pic)

def noPath():
    nopath = Label(master, text="OOPS! There's no path", fg="black", bg="green", font = "Verdana 14 bold")
    nopath.pack(side=BOTTOM)

board.pack(side=LEFT)
################# Control widgets ##################
panel = Frame(master)
panel.pack(side=RIGHT)
Label(text="Controls\n", font = "Verdana 12 bold").pack()

q1frame = Frame(master)
q1frame.pack()
b1 = Button(text="Play / Pause")
def printName(event):
    global flag
    flag = not flag

b1.bind("<Button-1>", printName)
b1.pack()


#   Sliders for speed and Epsilon
q3frame = Frame(master)
q3frame.pack()
w1 = Scale(q3frame, from_=0, to=50, orient=HORIZONTAL)
w1.pack(side=LEFT)
Label(text="Speed").pack()

# Label(text='\n').pack()
separator = Frame(height=2, bd=1, relief=SUNKEN)
separator.pack(fill=X, padx=2, pady=2)

Label(text="A Star\n",font = "Verdana 12 bold").pack()
eu_or_mh = 'Manhattan'
def toggle_h():
    global eu_or_mh
    if t_btn.config('text')[-1] == 'Euclidean Distance':
        t_btn.config(text='Manhattan Distance')
        eu_or_mh = 'Manhattan'
        print eu_or_mh
    else:
        t_btn.config(text='Euclidean Distance')
        eu_or_mh = 'Euclidean'
        print eu_or_mh

t_btn = Button(text="Manhattan Distance", width=15, command=toggle_h)
t_btn.pack(pady=3)

################# Q Learning widgets ##################
# Label(text='\n').pack()
separator = Frame(height=2, bd=1, relief=SUNKEN)
separator.pack(fill=X, padx=2, pady=2)

Label(text="Q Learning Parameters\n",font = "Verdana 12 bold").pack()

#   Discount text entry and button
qframe = Frame(master)
qframe.pack()
e = Entry(qframe, width=5)
e.pack(side=LEFT)
e.insert(0, "0.8")

discount = 0.8
def getDiscount(event):
    global discount
    discount = float(e.get())
    print discount
b3 = Button(qframe, text="Discount")
b3.bind("<Button-1>", getDiscount)
b3.pack(side=LEFT)

#  Change start panel
q2frame = Frame(master)
q2frame.pack()
def setStart(event):
    global start
    new_start = (int(x_entry.get()), int(y_entry.get()))
    if new_start not in walls:
        start = new_start
b4 = Button(q2frame, text="Change Start")
b4.bind("<Button-1>", setStart)

x_entry = Entry(q2frame, width=4)
x_entry.pack(side=LEFT)
x_entry.insert(0, str(start[0]))
y_entry = Entry(q2frame, width=4)
y_entry.pack(side=LEFT)
y_entry.insert(0, str(start[1]))

b4.pack(side=LEFT)
Label(text="").pack()

q4frame = Frame(master)
q4frame.pack()
w2 = Scale(q4frame, from_=0.0, to=0.9, orient=HORIZONTAL, resolution=0.1)
w2.pack()
Label(text="Exploration (eps)").pack()



def begin():
    global flag
    master.mainloop()
    flag = None
    time.sleep(0.1)    # hold time for linked program to read flag and close
