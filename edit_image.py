from tkinter import *;
import sys, os;
from tkinter.filedialog import askopenfilename;
import _thread as thread;
from PIL import ImageTk, Image;
from math import ceil, sqrt;
import dbm;
from functools import partial;

nose = [0,0];	#nose is a 2-lists, nose [0] holds x pos, nose [1] holds y pos
nose_block = [0, 0];	#nose_block is 2-list, nose_block [0] holds x axis block number, [1] y axis
whiskers = [];	#whiskers is list of 2 list, whiskers [pos] [0] holds x pos, [1] y pos
whisker_dist_man = [];	#list of 2-list, [0] holds x distance, [1] y distance
whisker_dist_euc = [];	#list of numbers (eucl. dists btw point and nose)
output_string = '''Manhattan Distance (units)			Euclidean Distance
  X-Axis	Y-Axis\t\t\t\t     (mm)\n''';
data_string = '''''';
grid_pixel_distance = 22;
pixel_in_one_mm = 4.4
profile = os.getenv ("LION_PROFILE_SIDE");

def fresh_variables ():
	global nose, nose_block, whiskers, whisker_dist_euc, whisker_dist_man, output_string, data_string;
	
	nose = [0,0];	#nose is a 2-lists, nose [0] holds x pos, nose [1] holds y pos
	nose_block = [0, 0];	#nose_block is 2-list, nose_block [0] holds x axis block number, [1] y axis
	whiskers = [];	#whiskers is list of 2 list, whiskers [pos] [0] holds x pos, [1] y pos
	whisker_dist_man = [];	#list of 2-list, [0] holds x distance, [1] y distance
	whisker_dist_euc = [];	#list of numbers (eucl. dists btw point and nose)
	output_string = '''Manhattan Distance (units)			Euclidean Distance
  X-Axis	Y-Axis\t\t\t\t     (mm)\n''';
	data_string = '''''';

def display_alert (title, string):
	temp = Tk ();
	temp.title (title);
	
	msg = Message (temp, text = string);
	msg.config (width = "700", pady = "30", padx = "50");
	msg.pack ();
		
	temp.mainloop ();
	temp.quit ();

def calculate ():
	counter = 0;
	global data_string, output_string;
	
	data_string = '''''';
	output_string = '''Manhattan Distance (units)			Euclidean Distance
  X-Axis	Y-Axis\t\t\t\t     (mm)\n''';
  
	for whisker in whiskers:
		#Manhattan
		block_x = ceil (whisker [0] / grid_pixel_distance);
		block_y = ceil (whisker [1] / grid_pixel_distance);
		
		whisker_dist_man.append ([0, 0]);
		whisker_dist_man [counter] [0] = abs (nose_block [0] - block_x);
		whisker_dist_man [counter] [1] = abs (nose_block [1] - block_y);
		
		#euclidean
		temp = sqrt ( ((nose [0] - whisker [0]) ** 2) + ((nose [1] - whisker [1]) ** 2) );
		#whisker_dist_euc.append  ( round ((temp / pixel_in_one_mm), 2) );
		whisker_dist_euc.append  ( (temp / pixel_in_one_mm) );
		
		#print (whisker_dist_man [counter] [0], ", ", whisker_dist_man [counter] [1]);
		#print (whisker_dist_euc [counter]);
		data_string += str (whisker_dist_man [counter] [0]) + "-" + str (whisker_dist_man [counter] [1]) + "-";
		data_string += str (int (whisker_dist_euc [counter])) + "-";
		
		output_string += "    " + str (whisker_dist_man [counter] [0]) + "\t  " + str (whisker_dist_man [counter] [1]) + "\t\t\t\t     ";
		output_string += str (round (whisker_dist_euc [counter], 2)) + "\n";
		
		counter += 1;
	
	#print (data_string);
	display_alert ("Calculations", output_string);

def fresh_canvas ():
	canvas.delete (ALL);
	canvas.create_image (0, 0, image = lion, anchor = NW);
	draw_grid ();
	canvas.bind ("<Button-1>", callback);
	fresh_variables ();

def save_end_exit ():
	global data_string, file_path;
	image_name = file_path.split ("/") [-1];
	database = dbm.open ("profiles/" + profile, 'c');

	database [image_name] = data_string;
	database.close ();
	#print (data_string);
	
	#display_alert ("Done", "The profile has been added to the database");
	root.quit ();
	os._exit (0);

def compare_profile ():
	global data_string;
	database = dbm.open ("profiles/" + profile, "c");
	found = False;
	
	keys = [i.decode () for i in database.keys ()];
	for key in keys:
		if (database [key].decode () == data_string):
			display_alert ("Match Found", "This profile is NOT UNIQUE");
			found = True;
			break;
	if (not found):
		display_alert ("Match Not Found", "This profile is UNIQUE");
	database.close ();

def compare_profile_2 ():
	global data_string;
	local_string = data_string.split ("-");
	local_string = local_string [:-1];
	local_string = [int (i) for i in local_string];
	
	database = dbm.open ("profiles/" + profile, "c");
	match_found = True;
	
	#print (local_string);
	#print ("-----------------------------------------");
	
	keys = [i.decode () for i in database.keys ()];
	for key in keys:
		values = database [key].decode ();
		values = values.split ("-");
		values = values [:-1];
		values = [int (i) for i in values];
		
		#print ("local_string = ", local_string);
		#print ("values = ", values);
		
		#print (values);
		#print (len (local_string), len (values));
		
		if (len (local_string) == len (values)):
			#print ("length good");
			for i in range (0, len (values)):
				difference = abs (values [i] - local_string [i]);
				#print (difference);
				
				if (difference > 1):
					match_found = False
					break;
		else:
			match_found = False;

	if (not match_found):
		display_alert ("Match Not Found", "This profile is UNIQUE");
	else:
		display_alert ("Match Found", "This profile is NOT UNIQUE");

	database.close ();

def initialize_editor_menu (window):
	top = Menu (window);
	window.config (menu = top);
	#compare = partial (display_alert, "Result", "Current Profile is UNIQUE");

	file = Menu (top);
	file.add_command (label = "Calculate Distances", command = calculate, underline = 0);
	file.add_command (label = "Compare with existing " + profile + " profiles", command = compare_profile_2, underline = 0);
	file.add_command (label = "Clear Spots", command = fresh_canvas, underline = 0);
	file.add_command (label = "Quit", command = root.quit, underline = 0);
	file.add_command (label = "Save and Exit", command = save_end_exit, underline = 0);
	
	top.add_cascade (label = "File", menu = file, underline = 0);

def callback (event):
	radius = 2;	
	#print (event.x, " ", event.y);
	canvas.create_oval (event.x - radius, event.y - radius, event.x + radius, event.y + radius, fill = "red", outline = "#DDD", width = 0);

	global nose;
	global whiskers;
	if (nose [0] == 0):
		nose = (event.x, event.y);
		nose_block [0] = ceil (nose [0] / grid_pixel_distance);
		nose_block [1] = ceil (nose [1] / grid_pixel_distance);
		
	else:
		whiskers.append ( (event.x, event.y) );

def draw_grid ():
	for i in range (0, x, grid_pixel_distance):
		canvas.create_line (i, 0, i, x, fill = "white", dash = (4, 4));
	for i in range (0, y, grid_pixel_distance):
		canvas.create_line (0, i, x, i, fill = "white", dash = (4, 4));

def clean_up ():
	#print ("Closing and wrapping up...");
	root.destroy ();
	os._exit (0);

if (__name__ == "__main__"):
	if (not os.getenv ("LILY_LOGIN")):
		display_alert ("Access Denied", "You are not authorized to use the application. Kindly Log in via the home screen.");
		os._exit (0);

	Tk ().withdraw ();
	cropped_file_name = os.getenv ("CROPPED");
	
	if (cropped_file_name):
		#print ("we have a cropped region");
		file_path = "image_db/crops/" + cropped_file_name;
	else:	
		image_db = "image_db";
		file_path = askopenfilename (initialdir=image_db);
		
		if (not file_path):
			#print ("No file chosen");
			os._exit (1);

	temp = Image.open (file_path);
	x, y = temp.size;
	temp.close ();

	root = Toplevel ();
	root.geometry (str (x) + "x" + str (y));
	root.wm_resizable (FALSE, FALSE);
	root.wm_protocol ("WM_DELETE_WINDOW", clean_up);
	
	initialize_editor_menu (root);
	
	canvas = Canvas (root, width = x, height = y, bg = "blue");
	canvas.pack ();
	
	lion = ImageTk.PhotoImage (file = file_path);
	fresh_canvas ();

	root.mainloop ();
	#root.quit ();
	os._exit(0);
