from tkinter import *;
from PIL import Image, ImageTk;
import sys, os;
from multiprocessing import Process;
import hashlib;

def display_alert (title, string):
	temp = Tk ();
	temp.title (title);
	
	msg = Message (temp, text = string);
	msg.config (width = "700", pady = "30", padx = "50");
	msg.pack ();
		
	temp.mainloop ();
	temp.quit ();

def login ():
	global username, password;
	uname = username.get ();
	passwd = password.get ();
	
	try:
		user_file = open ("users/" + uname, "rb");
	except:
		display_alert ("Non Existent", "Error: Username does not exist");
	else:
		hash = hashlib.md5 ();
		hash.update (passwd.encode ());
	
		if (hash.digest () == user_file.read ()):
			p = Process (target = open_engine, args = (uname,));
			p.start ();
			p.join ();
		else:
			display_alert ("Incorrect credentials", "Login Credentials do not match. Access denied.");
	
def open_engine (uname):
	os.environ ["LILY_LOGIN"] = uname;
	os.system ("python engine.py");

def clean_up ():
	#print ("Closing and wrapping up...");
	root.destroy ();
	os._exit (0);

if (__name__ == "__main__"):
	root = Tk ();
	
	root.wm_protocol ("WM_DELETE_WINDOW", clean_up);
	root.title ("LILY - Login");
	root.geometry ("800x500");
	root.wm_resizable (False, False);
	
	canvas = Canvas (root, height = 500, width = 800);
	canvas.pack ();
	
	username = Entry (canvas, width = 20);
	password = Entry (canvas, show = "*", width = 20);
	button = Button (canvas, width = 15, text = "Log In", command = login);
	
	photo = ImageTk.PhotoImage (file = "application_data/login_screen_bg_final.jpg");
	canvas.create_image (0, 0, image = photo, anchor = NW);
	
	canvas.create_window (120, 245, anchor = NW, window = username);
	canvas.create_window (120, 275, anchor = NW, window = password);
	canvas.create_window (100, 320, anchor = NW, window = button);
	
	root.mainloop ();
