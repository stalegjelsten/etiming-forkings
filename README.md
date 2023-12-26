# Assign multiple courses to a single class in eTiming

When setting a mass start course with forkings in [Purple Pen](https://purple-pen.org/) and exporting them to the IOF XML 3.0 format, it seems [eTiming](https://www.eqtiming.com/no/Arrangoer-verktoey/eTiming-Windows-tidtakerprogram/ag32a264) is unable to assign the different courses to the participants.

This python script automates the process of assigning different courses to the runners in a single class. The script distributes the courses such that there are an equal amount of runners with each forking.

## System requirements

- A Windows computer 
- Python 3. The script is tested with Python 3.10
- [Microsoft Access database ODBC drivers](https://www.microsoft.com/en-us/download/details.aspx?id=54920). A driver is automatically installed by eTiming. If you already have eTiming installed, you should *not* need to install the [Microsoft Access database ODBC drivers](https://www.microsoft.com/en-us/download/details.aspx?id=54920) separately.
- `pip` for python. `pip` is automatically installed with Python 3.5 and newer so it should not be necessary to install it separately.

## Usage

### Course setting in Purple Pen

- Set the courses in Purple Pen. Use the *Variation* tool to create forkings.
- Export courses using `File → Create IOF XML file` and choose `IOF XML 3.0` as the file format.

### Preparations in eTiming

- Import runners from Eventor or from another source. 
- (Create and assign classes if this is not done automatically)
- Import courses from the `IOF XML 3.0` file. Choose `Keep course ID / course variations` when importing.

In eTiming there should now be a number of courses with course names consisting of the course name from Purple Pen + a forking designation. If the course is called `Long` in Purple Pen, and the forking variant is `ABB`, then the name in eTiming will be `Long ABB`. 

### Setup for this script

First and foremost: **CREATE A BACKUP OF THE `etime.mdb` ACCESS DATABASE**. This script updates the database file, and this *can* lead to data corruption.

- Ensure that the `etime.mdb` file is in a directory with no spaces or special characters in its path. It's completely safe to move the file to another directory as long as you have exited eTiming.
- Clone this repo or download the `main.py` file and `requirements.txt`
- Highly recommended: Create a python virtual environment (to isolate the necessary modules from your python installation) by opening a terminal and running:
  - `pip install virtualenv` to install the virutalenv module
  - `python -m venv env` to create a virtual enviroment
  - `source env/bin/activate` to activate the new virtual environment
- Install all necessary modules by runnning `pip install -r requirements.txt`

You should now be ready to use the script.

### Script usage

- Edit line 10 in `main.py` to the correct path to the `etime.mdb` file. Remember: no spaces/special characters and make a backup before running the script!
- Run `python main.py` to start the script
- The script lists all the classes in the database. Type the number of a class and press Enter to assign courses to this class.
  - If you type `-1`, the script will exit without writing any changes to the database. 
  - If you type `-2`, the script will write all changes to the database and exit.
- After selecting a class, you are presented with the following choices:
  - Type `l` to list all courses and the course numbers
  - Type `n` to abort and choose another class
  - Type `y` to assign course numbers to the class
- After typing `y` you need to type the lowest course number and the highest course number to assign to the class.
- Repeat for all classes with forkings
- Type `-2` when selecting class to write all changes back to the database file.