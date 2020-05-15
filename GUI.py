"""
REFERENCES READINGS:

https://www.analyticsvidhya.com/blog/2018/08/a-simple-introduction-to-facial-recognition-with-python-codes/
https://effbot.org/tkinterbook/photoimage.htm
https://www.tutorialspoint.com/python/python_gui_programming.htm
https://pythonbasics.org/tkinter-image/, https://effbot.org/tkinterbook/button.htm
https://stackoverflow.com/questions/48723923/align-a-button-to-the-bottom-using-tkinter
https://www.python-course.eu/tkinter_buttons.php, http://effbot.org/tkinterbook/label.htm
https://www.python-course.eu/tkinter_layout_management.php
https://stackabuse.com/python-gui-development-with-tkinter-part-2/
https://stackoverflow.com/questions/42600739/how-do-i-upload-an-image-on-python-using-tkinter
https://stackoverflow.com/questions/50123315/how-do-i-create-an-import-file-button-with-tkinter
https://docs.python.org/3/library/tk.html,  https://www.tutorialsteacher.com/python/os-module
https://pypi.org/project/face_recognition/
https://en.wikipedia.org/wiki/Python_Imaging_Library
https://pillow.readthedocs.io/en/stable/
https://stackoverflow.com/questions/49498296/what-does-the-tearoff-attribute-do-in-a-tkinter-menu
https://pillow.readthedocs.io/en/3.1.x/reference/Image.html
https://stackoverflow.com/questions/3493092/convert-image-to-a-matrix-in-python
https://stackoverflow.com/questions/55220797/how-to-display-multiple-images-with-y-scrollbar-in-tkinter


"""
# import all objects from tkinter module
from tkinter import *
import tkinter as tk

#  messagebox & fileDialog are tk support module it's imported separately
from tkinter import messagebox, filedialog

# os module provides functions for interacting with the operating system.it comes under Python’s default modules
import os

# module for recognizing and manipulating faces from Python or from the command line
import face_recognition

# PIL is a python imaging Library that adds support for opening, manipulating, and saving many different image file
# formats

# The Image module provides a class with the same name which is used to represent a PIL image.
# The module also provides a number of factory functions, including functions to load images from files,
# and to create new images.

# The ImageTk module contains support to create and modify Tkinter BitmapImage and PhotoImage objects from PIL images
from PIL import ImageTk, Image

# constructor Tk() will build our main window
base = Tk()
base.title('Match That Image')

# Icon can be used under free licence taken from https://icon-icons.com/icon/face-recognition-exploration/2443#32

base.iconbitmap('icons&images/face_recognition_exploration_3005.ico')


# adjust size of GUI main window in tkinter
# base.geometry("600x600")


# function to display the message in about section
def about_message():
    messagebox.showinfo("ABOUT ", "'Match That Image' : Created as a Python GUI Learning Project")


# Base Menu
menu = Menu(base)

# File menu
menu_file = Menu(menu, tearoff=0)
menu.add_cascade(label="File", menu=menu_file)
menu_file.add_command(label="Exit", command=base.quit)

# About Menu
about_menu = Menu(menu, tearoff=0)
menu.add_cascade(label="About", menu=about_menu)
about_menu.add_command(label='About', command=about_message)

# Listing all the images present in given path, listdir will list all the photos present in directory
img = os.listdir('images_compared')

# Create Canvas
canvas = Canvas(base, width=207, height=307)
# Add Canvas text
canvas.create_text(100, 150, fill="black", font="Times 10 italic bold",
                   text="Image goes here")

# Give canvas an outline  through shapes
canvas.create_rectangle(2, 2, 207, 307, outline='black')
canvas.grid(padx=10, pady=20)


# Switch to Normal state once an image is selected
def switch_btn_state():
    if matchButton['state'] == tk.DISABLED:
        matchButton['state'] = tk.NORMAL


def select_image():
    global img_to_match
    global directory
    # load the image from the directory in tkinter
    base.match = filedialog.askopenfilename(initialdir="images_to_match/",
                                            title='Please Select The Image You Want To Match',
                                            filetypes=(("jpeg Files", "*.jpg"), ("png Files", "*.png")))

    # Get the path of the image in the directory at index 1, also we can use something like askdirectory()
    directory = os.path.split(base.match)[1]

    # Resize the loaded image
    # Image.ANTIALIAS - a high-quality downsampling filter

    img_loaded = Image.open(base.match)
    img_resized = img_loaded.resize((200, 300), Image.ANTIALIAS)
    # open the image in tkinter window
    img_to_match = ImageTk.PhotoImage(img_resized)
    # The Canvas method create_image(x0,y0, options ...) is used to draw an image on a canvas
    canvas.create_image(5, 5, image=img_to_match, anchor=NW)
    # img_to_match_label = Label(image=img_to_match).pack()


# frame = LabelFrame(base, text="Hello", padx=100, pady=150)
# frame.pack(padx=10, pady=0)
# Button for selection of an image

my_img_button = Button(base, text='Select an Image', command=lambda: [select_image(), switch_btn_state()])
my_img_button.grid()


# function for match button
def find_image_match():
    #  img_to_load = imageio.imread('images_to_match/' + directory)
    # imageio.imread also returns a NumPy array value, can be used as an alternative to face_recognition.load_image_file

    # load the image to match
    img_to_load = face_recognition.load_image_file('images_to_match/' + directory)

    # convert the previously loaded image into the feature vector which will return the value in array
    img_to_match_vectored = face_recognition.face_encodings(img_to_load)[0]

    i = 0
    n = 250

    frame = Frame(base)

    frame.grid(row=0, column=1, pady=20)
    canvas = Canvas(frame)

    # loop over every image

    for image in img:

        # load the image from directory img
        current_img = face_recognition.load_image_file('images_compared/' + image)

        # convert loaded image into a feature vector
        current_img_vectored = face_recognition.face_encodings(current_img)[0]

        # match the images in directory with the image that is to be matched and check if they both match
        match_outcome = face_recognition.compare_faces(
            [img_to_match_vectored], current_img_vectored)

        # check if both images matched

        if match_outcome[0]:

            c = Canvas(canvas, width=n, height=n)
            frame_img = LabelFrame(c, text='Results...')
            frame_img.pack(padx=10, pady=10, side=LEFT)
            load_img = Image.open("images_compared/" + image)
            loaded = load_img.resize((100, 150), Image.ANTIALIAS)
            display = ImageTk.PhotoImage(loaded)

            label = Label(frame_img, image=display)

            # When a PhotoImage object is garbage-collected by Python (e.g. when you return from a function which stored
            # an image in a local variable), the image is cleared even if it’s being displayed by a Tkinter widget.
            # To avoid this, the program must keep an extra reference to the image object
            label.image = display
            label.pack()

            my_match_label = Label(frame_img, text="Matched : " + image, bg='#50FF33')
            my_match_label.pack()

            canvas.create_window(0, n * i, window=c)

            i += 1

        else:
            c = Canvas(canvas, width=n, height=n)
            frame_img = LabelFrame(c, text='Results...')
            frame_img.pack(padx=10, pady=10, side=LEFT)
            load_img = Image.open("images_compared/" + image)
            loaded = load_img.resize((100, 150), Image.ANTIALIAS)
            display = ImageTk.PhotoImage(loaded)

            label = Label(frame_img, image=display)

            # When a PhotoImage object is garbage-collected by Python (e.g. when you return from a function which stored
            # an image in a local variable), the image is cleared even if it’s being displayed by a Tkinter widget.
            # To avoid this, the program must keep an extra reference to the image object
            label.image = display
            label.pack()
            my_match_label = Label(frame_img, text="Not Matched : " + image, bg='#F53213')
            my_match_label.pack()

            canvas.create_window(0, n * i, window=c)

            i += 1

    my_match_label = Label(base, text="Matching Completed", bg='#1B0DE3')
    my_match_label.grid()

    vsb = Scrollbar(frame, orient=VERTICAL)
    vsb.pack(side=RIGHT, fill=Y)
    vsb.config(command=canvas.yview)
    canvas.config(width=n * 2, height=n * 2)
    canvas.config(yscrollcommand=vsb.set, scrollregion=canvas.bbox(ALL))
    canvas.pack(side=LEFT, expand=True, fill=BOTH)


# creating a Match button for the image to be matched
# Add frame to Match button

frame = LabelFrame(base, text='Click to Match...', padx=5, pady=5)
frame.grid(padx=15, pady=15)

matchButton = Button(frame, text='Match', padx=50, pady=10, state=tk.DISABLED, command=find_image_match)

matchButton.grid()

# config is used to access an object's attributes after its initialisation
base.config(menu=menu)

# Display the GUI results
base.mainloop()
