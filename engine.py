#Application Requirements:
#   Python 3.X (Latest is recommended)
#   Pillow Image Library
#   Tkinter GUI Library (comes by default with Python Build, just make sure though

import sys, os;
import time;
from multiprocessing import Process;
import _thread as thread;
#from tkinter import Tk, Button, Menu, Canvas, NW;
from tkinter import *;
from tkinter.filedialog import askopenfilename;
from PIL import Image, ImageTk;
from shutil import copyfile;
from functools import partial;
from tkinter.messagebox import askquestion;
import dbm;

#global variables
canvas = "";
set = False;
points = [];
display_image = "";

#FRONT END
def display_alert (title, string):
	temp = Tk ();
	temp.title (title);
	
	msg = Message (temp, text = string);
	msg.config (width = "700", pady = "30", padx = "50");
	msg.pack ();
		
	temp.mainloop ();
	#temp.quit ();

def display_version ():
	version = "LILY 1.0, the first release. For reporting bugs, contact duaraghav8@gmail.com";
	display_alert ("Version Information", version);

def display_credits ():
	credits = '''
Raghav Dua (duaraghav8@gmail.com)		B.Tech, UPES, Dehradun''';
	display_alert ("Credits", credits);

def upload_img (x):
	thread.start_new_thread (upload_image, ());

def upload_image ():
	Tk ().withdraw ();
	global win_width;
	global win_height;
	
	try:
		file_path = askopenfilename ();
		if (file_path == ""):
			thread.exit ();
	except Exception as fnf:
		#print ("File was not uploaded");
		#print ("Verbose: " + str (fnf));
		thread.exit ();
	else:	
		file_name = file_path.split ("/") [-1];
		print (file_name);
		test = Image.open (file_path);
		
		width, height = test.size;
		max_width = int ( (80.7446 / 100) * win_width );
		max_height = int ( (98.6651 / 100) * win_height );

		if (width > max_width or height > max_height):
			final = test.resize ( (max_width, max_height) );
			final.save ("image_db/" + file_name);
			test.close ();
			final.close ();
			
			print ("Verbose: " + file_path + " has been added to the local DataBase");
			successfully_uploaded ();
			thread.exit ();
			
		try:
			copyfile (file_path, "image_db/" + file_name);
		except Exception as e:
			print ("The application has encountered an un-expected error. Please contact the application developer at duaraghav8@gmail.com");
			print ("Verbose: \n" + str (e));
		else:
			print ("Verbose: " + file_path + " has been added to the local DataBase");
			successfully_uploaded ();

def successfully_uploaded ():
	display_alert ("Upload Successful", "Image has been uploaded to local database successfully.");

def clear_image_db (x):
	thread.start_new_thread (empty_database, ());

def empty_database ():
	confirm = askquestion ("Clear Local Database", "This operation effectively removes all the images and their corresponding profiles from the database. Would you like to proceed?", icon = "warning");
	
	if (confirm == "yes"):
		try:
			os.chdir ("image_db");
			files = os.listdir ();
		except FileNotFoundError:
			display_alert ("Error", "The directory 'image_db' was not found.");
		except Exception as e:
			pass;
		else:
			for f in files:
				if (f == "crops"):
					cropped_files = os.listdir ("crops");
					for g in cropped_files:
						os.remove ("crops/" + g);
					continue;

				os.remove (f);
			print ("Database has successfully been cleared");
		os.chdir ("..");

		try:
			os.chdir ("profiles");
			files = os.listdir ();
		except FileNotFoundError:
			display_alert ("Error", "The directory 'image_db' was not found.");
		except Exception as e:
			pass;
		else:
			for f in files:
				os.remove (f);
		
		display_alert ('Update', 'Database was successfully cleared');
		thread.exit ();

def initialize_menu (window):
	top = Menu (window);
	window.config (menu = top);
	upload_command = partial (upload_img, 0);
	edit_command_right = partial (spawn_process, 'RIGHT', 0);
	edit_command_left = partial (spawn_process, 'LEFT', 0);

	file = Menu (top);
	file.add_command (label = 'Upload New Side Face Image', command = upload_command, underline = 0);
	file.add_command (label = 'Create Right Profile', command = edit_command_right, underline = 0);
	file.add_command (label = 'Create Left Profile', command = edit_command_left, underline = 0);
	file.add_command (label = 'Quit', command = window.quit, underline = 0);
	
	help = Menu (top);
	help.add_command (label = 'Credits', command = display_credits, underline = 0);
	help.add_command (label = 'Version', command = display_version, underline = 0);
	
	top.add_cascade (label = 'File', menu = file, underline = 0);
	top.add_cascade (label = 'Help', menu = help, underline = 0);

def initialize_buttons (root):
	global win_width;
	button_width = int ((2.221 / 100) * win_width);
	
	edit_command_right = partial (spawn_process, False, 'RIGHT');
	edit_command_left = partial (spawn_process, False, 'LEFT');
	edit_cropped_command_left = partial (spawn_process, True, 'LEFT');
	edit_cropped_command_right = partial (spawn_process, True, 'RIGHT');

	upload_image_button = Button (root, text = "Upload Side Face Image", width = button_width);
	upload_image_button.pack ();
	upload_image_button.place (relx=.1, rely=.12, anchor="c");
	upload_image_button.bind ("<Button-1>", upload_img);	#have to use upload_image () here
	
	clear_imagedb_button = Button (root, text = "Clear Local Database", width = button_width);
	clear_imagedb_button.pack ();
	clear_imagedb_button.place (relx=.1, rely=.18, anchor="c");
	clear_imagedb_button.bind ("<Button-1>", clear_image_db);
	
	edit_image_button_r = Button (root, text = "Create Right Profile", width = button_width);
	edit_image_button_r.pack ();
	edit_image_button_r.place (relx=.1, rely=.24, anchor="c");
	edit_image_button_r.bind ("<Button-1>", edit_command_right);
	
	edit_image_button_l = Button (root, text = "Create Left Profile", width = button_width);
	edit_image_button_l.pack ();
	edit_image_button_l.place (relx=.1, rely=.30, anchor="c");
	edit_image_button_l.bind ("<Button-1>", edit_command_left);
	
	temp = Button (root, text = "Display new Image", width = button_width);
	temp.pack ();
	temp.place (relx=.1, rely=.36, anchor="c");
	temp.bind ("<Button-1>", temp_func_launcher);
	
	clear = Button (root, text = "Clear Preview", width = button_width);
	clear.pack ();
	clear.place (relx=.1, rely=.42, anchor="c");
	clear.bind ("<Button-1>", clear_preview);
	
	crop = Button (root, text = "Crop Selected Region", width = button_width);
	crop.pack ();
	crop.place (relx=.1, rely=.48, anchor="c");
	crop.bind ("<Button-1>", crop_region);
	
	edit_cropped = Button (root, text = "Edit Cropped Region as Right Profile", width = button_width);
	edit_cropped.pack ();
	edit_cropped.place (relx=.1, rely=.54, anchor="c");
	edit_cropped.bind ("<Button-1>", edit_cropped_command_right);
	
	edit_cropped = Button (root, text = "Edit Cropped Region as Left Profile", width = button_width);
	edit_cropped.pack ();
	edit_cropped.place (relx=.1, rely=.60, anchor="c");
	edit_cropped.bind ("<Button-1>", edit_cropped_command_left);

#BACK END
def crop_region (x):
	global points, display_image;
	image = Image.open (display_image);
	xlist = [i [0] for i in points];
	xmin = min (xlist);
	xmax = max (xlist);
	ylist = [i [1] for i in points]
	ymax = max (ylist);
	ymin = min (ylist);
	
	#print (xmin, xmax, ymin, ymax);
	box = (xmin - 240, ymin - 40, xmax - 240, ymax - 40);
	print (image.size);
	print (ymax, ymin);
	new = image.crop (box);
	new.save ('image_db/crops/' + (display_image.split ('/')[-1]));
	
	new.close ();
	image.close ();
	
def callback (event):
	radius = 2;	
	global points;
	
	#print (event.x, " ", event.y);
	if (len (points) < 4):
		canvas.create_oval (event.x - radius, event.y - radius, event.x + radius, event.y + radius, fill = "red", outline = "#DDD", width = 0);
		points.append ( (event.x, event.y) );
	else:
		display_alert ('Error', 'Crop tool does not allow more than 4 marks');

def spawn_process (cropped, side, x):
	if (cropped):
		p = Process (target = mark_spots_cropped, args = (side,));
	else:	
		p = Process (target = mark_spots, args = (side, ));
	
	p.start ();
	p.join ();
	
def mark_spots_cropped (side):
	display_image = dbm.open ('application_data/cropped_image_name', 'r');
	file_name = display_image ['image'].decode ();
	file_name = file_name.split ('/') [-1];
	print (file_name);
	
	os.environ ['CROPPED'] = file_name;
	mark_spots (side);

def mark_spots (side):	
	os.environ ['LION_PROFILE_SIDE'] = side;
	os.system ('python edit_image.py');

def mark_image_point (event):
	spot_radius = 1;
	canvas.create_oval (event.x - spot_radius, event.y - spot_radius, event.x + spot_radius, event.y + spot_radius, fill = "red", outline = "#DDD", width = 0);

def clear_preview (x):
	global points;
	
	canvas.delete (ALL);
	canvas.create_rectangle (int ( (18.1347 / 100) * win_width), int ( (4.491 / 100) * win_height), win_width - int (2.5906 / 100 * win_width), win_height + int ( (4.491 / 100) * win_height), fill = "white");
	points = [];

def temp_func_launcher (x):
	thread.start_new_thread (temp_func, (0, ));

def browse ():
	global display_image, buffer;
	crop_file = dbm.open ('application_data/cropped_image_name', 'c');
	
	display_image = askopenfilename (initialdir = 'image_db');
	crop_file ['image'] = display_image;
	crop_file.close ();
	
	return (display_image);
	
def temp_func (x):
	global set;
	global win_height;
	global win_width;
	global photo;
	
	img = Image.open (browse ());
	photo = ImageTk.PhotoImage (img);
	
	lion = canvas.create_image (int ( (18.1347 / 100) * win_width) + 4, int ((5.2395 / 100) * win_height), image = photo, anchor = NW);
	canvas.bind ("<Button-1>", callback);

def clean_up ():
	#print ("Closing and wrapping up...");
	root.destroy ();
	os._exit (0);

if (__name__ == '__main__'):
	if (not os.getenv ('LILY_LOGIN')):
		display_alert ('Access Denied', "You are not authorized to use the application. Kindly Log in via the home screen.");
		os._exit (0);
	
	if (os.path.exists ('application_data/cropped_image_name')):
		os.remove ('application_data/cropped_image_name');

	root = Tk ();
	
	root.wm_protocol ("WM_DELETE_WINDOW", clean_up);
	root.title ("Lion Identification Lossless Yield - Main Menu");
	win_width = root.winfo_screenwidth () - int ( (1.0981 / 100) * root.winfo_screenwidth ());	#15
	win_height = root.winfo_screenheight () - int ( (13.0208 / 100) * root.winfo_screenheight ());	#100
	#print (root.winfo_screenwidth ());
	#print (root.winfo_screenheight ());
	#print ("-----");
	#print (win_width, win_height);
	#print (win_width - int (2.5906 / 100 * win_width), win_height + int ( (4.491 / 100) * win_height));

	root.title ("WII");
	root.state ('zoomed');
	root.wm_resizable (False, False);

	initialize_menu (root);
	
	canvas = Canvas (root, width = win_width - int ((2.2206 / 100) * win_width), height = win_height + int ( (4.491 / 100) * win_height));
	canvas.pack ();
	canvas.create_rectangle (int ( (18.1347 / 100) * win_width), int ( (4.491 / 100) * win_height), win_width - int (2.5906 / 100 * win_width), win_height + int ( (4.491 / 100) * win_height), fill = "white");
	
	#photo = ImageTk.PhotoImage (file = 'image_db/lion.jpg');
	#photo = ImageTk.PhotoImage (file = 'lion_big.jpg');
	
	initialize_buttons (root);
	root.mainloop ();
