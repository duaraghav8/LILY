![alt text](https://cloud.githubusercontent.com/assets/12758282/16018532/779eb666-31c2-11e6-9ec5-231260c35ed8.png "Screenshot")

This is an early version of LILY. I would upload the full software, but only after a LONG time

# Lion-Identification-Loss-less-Yield

**Intro**

Lion Identification Loss less Yield or LILY is a Digital Image Processing based Software Project developed for Scientists at the Wildlife Institute of India (WII) for the purpose of conducting Lion Census.

The project has been programmed entirely in Python 3.4 with support of PILLOW Image processing Library. Works perfectly on Windows, but I haven't tested it for Linux or Mac.

**NOTE**
  1. There has been negligible focus on security, since it wasn't really a concern. The Login Screen and credentials database are just a mere formality. The application simply checks for the existence of a particular environment variable based on which, it will allow access to the main engine.
  2. Pardon the occasional freezing of the Application. I'm a bit of a noob when it comes to multithreading, so I handled it quite poorly.

**Installing and Running**

Copy the folder in your work Directory. Open up CMD. Switch to the Application's directory and run lily_login.py like:

python lily_login.py

(make sure your PATH Environment Variable is configured to point to the Python 3 Directory).

#Background
http://livingwithlions.org/mara/how-to/identify-lions/

http://www.livingwithlions.org/mara-predator-project.html


**Usage**

Click on "Upload side face Image" to upload an image of a lion facing left or right. Based on the direction of the facing, click on "Create Right / Left Profile". In the grid, mark the first point as the tip of the lion's nose. The second point should be the single black spot in the Top row. Next, mark all the spots in the middle row and then, mark the single spot in the 3rd row. If you mess up, there's always a "Clean up" option available. If you've done that successfully, click on "Calculate Distances". This displays the Euclidean and Manhattan Distances. You can then select "Compare with existing Right/Left Profiles" to check whether a profile marked in this pattern already exists or not, which will tell whether the lion profile we created is a new one or an already existing one.
You then have the option of saving this profile if it is indeed unique.

**Lisence**

MIT
