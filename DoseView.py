import sys
import subprocess
import importlib.util

print("Checking dependencies...")
required = ['pydicom', 'tkinter', 'matplotlib']

for name in required:
    if spec := importlib.util.find_spec(name) is None:
        subprocess.check_call([sys.esys.executable, '-m', 'pip', 'install', '--upgrade'] + name)

print("Launching app...")
        
from pydicom import dcmread
from matplotlib.figure import Figure
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import filedialog, W
from tkinter.ttk import *

root = tk.Tk()

root.title("Scrollable Dose Map DICOM Viewer")
root.minsize(750,450)

filename = tk.StringVar(root)
e1 = Entry(root, textvariable=filename)
e1.grid(row=0, column=1, columnspan=2)
e1.config(state="readonly")

def browse():
    f = filedialog.askopenfilename()
    filename.set(f)

b1 = Button(root, text="Select Dose File", command=browse)
b1.grid(row=0, column=0)

fig = Figure(figsize=(8,6), dpi=100)
ax = fig.add_subplot(111)
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().grid(row=1, column=1, columnspan=2)
canvas.draw()

slices, rows, cols = [0, 0, 0]
ind = slices//2
data = None
im = None
    
def onscroll(event):
    global ind, slices, ax, im
    if event.button == 'up':
        ind = (ind + 1) % slices
    else:
        ind = (ind - 1) % slices
    im.set_data(data[ind, :, :])
    ax.set_ylabel("Slice %s" % ind)
    im.axes.figure.canvas.draw()
      
fig.canvas.mpl_connect('scroll_event', onscroll)
    
def plot_dcm():
    global slices, rows, cols, ind, im, ax, data
    ds = dcmread(e1.get())
    data = ds.pixel_array
    slices, rows, cols = data.shape
    ind = slices//2
    im = ax.imshow(data[ind, :, :])
    canvas.draw()
    
b2 = Button(root, text="Plot", command=plot_dcm)
b2.grid(row=1, column=0)

root.mainloop()
