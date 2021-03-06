from tkinter import *
from time import *

master = Tk() 
w = Canvas(master, width=600, height=600) 
w.pack() 
radius = 10
sleep(5)

x_vals = []
y_vals = []
# top line of the square
for x in range(100, 500, 80):
	x_vals.append(x)
for y in range(5):
	y_vals.append(100)

# right line of the square
for x in range(6):
	x_vals.append(500)
for y in range(100, 580, 80):
	y_vals.append(y)

# bottom line of the square
for x in range(100, 500, 80):
	x_vals.append(x)
for y in range(5):
	y_vals.append(500)	

# left line of the square
for x in range(5):
	x_vals.append(100)
for y in range(100, 500, 80):
	y_vals.append(y)		

comm = [[1, 1, 0, 1, 0, 1, 0, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 1, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 1], 
[1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1], 
[1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1], 
[1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1], 
[1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1], 
[1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1], 
[1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1]]

text_id = w.create_text(300, 50, text="")
for j in range(len(comm)):
	label = "Round " + str(j)
	w.itemconfigure(text_id, text=label)
	for i in range(len(x_vals)):
		if i == 0:
			sleep(3)
		if comm[j][i] == 0:
			w.create_oval(x_vals[i] - radius, y_vals[i] - radius, x_vals[i] + radius, y_vals[i] + radius, fill="black")
		else:
			w.create_oval(x_vals[i] - radius, y_vals[i] - radius, x_vals[i] + radius, y_vals[i] + radius, fill="red")
	sleep(2)
	w.update()

mainloop()