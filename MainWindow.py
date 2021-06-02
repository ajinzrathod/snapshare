import sys
from tkinter import (
    Button, Label, Frame, Toplevel,
    FLAT, IntVar, Radiobutton, OptionMenu,
    messagebox, filedialog, E, W)
from SecondaryWindow import SecondaryWindow
from CustomWidgets import HoverButton, Seperator
from pathlib import Path
import pyautogui
import time
from datetime import datetime
from threading import Thread
from appdirs import user_data_dir
from configparser import ConfigParser
import os
from sys import platform
# import platform as pf  # If necessary
from getpass import getuser
import settings
import shutil
# create shortcut
import win32com.client  # pip install pywin32 


# saved_directory = /home/ajinkya/Desktop/HurryWorld  # screenshot_directory
# screenshot_duration = 15  # time in minutes
# start_at = 1  # to show user in GUI
# is_running = 0  # for program, to see whether code is already started

# !!! CAUTION: read all value in `str`, later convert the number to int


class MainWindow:
    def __init__(self, master, AUTO_START, ROOT_DIR):
        self.APP_NAME = settings.APP_NAME
        self.APP_AUTHOR = settings.APP_AUTHOR
        self.DEBUG = settings.DEBUG
        # self.ROOT_DIR = settings.ROOT_DIR

        self.ROOT_DIR = ROOT_DIR
        self.AUTO_START = AUTO_START

        if self.AUTO_START:
            print("GUI will not be visible")

            # tkinter window will not be displayed
            # but code will still be running
            master.withdraw()

        self.master = master
        # Getting Home directory
        home = str(Path.home())
        default_path = os.path.join(home, "Desktop")

        self.options = [1, 3, 5, 10, 15, 20, 30, 45, 60]

        # ===== Config file Setting Starts =====
        self.config = ConfigParser()
        self.config_file_path = user_data_dir()
        print(user_data_dir(self.APP_NAME, self.APP_AUTHOR))
        self.saved_directory = None

        # If config file exists
        self.config_file = os.path.join(self.APP_NAME, "config.ini")

        self.check_config_file_and_insert(default_path)

        # Default Variables
        self.root_width = settings.ROOT_WIDTH
        self.master = master
        self.frame = Frame(self.master)
        self.xPadding, self.yPadding = 10, 10
        self.font_size = settings.FONT_SIZE
        self.start_record_text = "Start Recording"
        self.stop_record_text = "Stop Recording"

        # Open New Window Button
        self.button1 = Button(self.frame,
                              text='New Window',
                              width=25,
                              command=self.new_window)

        # Screenshots Status (Label)
        self.record_text = Label(
            master,
            text=self.start_record_text + " Screenshots")

        # ===== Custom HoverButton Starts =====

        # relief=FLAT:
        # https://www.tutorialspoint.com/python/tk_relief.htm

        # HoverButton:
        # https://stackoverflow.com/questions/49888623/tkinter-hovering-over-button-color-change
        # if self.saved_is_running and self.saved_take_ss:
        if self.saved_take_ss:
            self.record_status = True
            self.record_button = HoverButton(
                master,
                activebackground='#FF0000',
                activeforeground='#000',
                text=self.stop_record_text + " Screenshots",
                bg="#df534f",
                fg="#fff",
                font=("Verdana", self.font_size),
                highlightthickness=0,
                relief=FLAT,
                width=25,
                command=lambda: self.record_button_click())
        else:
            self.record_status = False
            self.record_button = HoverButton(
                master,
                activebackground='#65D366',
                activeforeground='#fff',
                text=self.start_record_text + " Screenshots",
                bg="#25D366",
                fg="#fff",
                font=("Verdana", self.font_size),
                highlightthickness=0,
                relief=FLAT,
                width=25,
                command=lambda: self.record_button_click())
        # ===== Custom HoverButton Ends =====

        # Already running informations
        self.already_running_info = Label(
            master,
            text=("App is already running due to Autostart enabled."))

        # If this condition is ignored, it will never to if condition of
        # "if self.record_status is False:" in `record_button_click`
        if self.AUTO_START:
            self.record_status = False

        # ===== Seperator Line  =====
        self.w1 = Seperator.draw_seperator(self.root_width, master)

        # ===== Radiobutton for "When to Record" Starts =====
        r = IntVar()
        r.set("2")
        print(type(r))

        self.record_when1 = Radiobutton(
            master, text="Autostart on boot(You can stop anytime)", variable=r, value=1,
            bg="#fff", highlightthickness=0,
            command=lambda: self.record_when_clicked(r.get())
        )

        self.record_when2 = Radiobutton(
            master, text="Record when I press Record", variable=r, value=2,
            bg="#fff", highlightthickness=0,
            command=lambda: self.record_when_clicked(r.get())
        )
        r.set(self.saved_start_at)
        # ===== Radiobutton for "When to Record" Ends =====

        # ===== Save to Directory Starts =====
        self.save_directory_text = Label(
            text="Directory to save",
            highlightthickness=0,
            bg="#fff"
        )
        self.save_directory = HoverButton(
            master,
            activebackground='#ddd',
            activeforeground='#fff',
            text="Browse",
            fg="#fff",
            bg="#808080",
            font=("Verdana", self.font_size),
            highlightthickness=0,
            relief=FLAT,
            command=self.save_directory_click)

        # Creating Directory safely
        create_directory = self.saved_directory
        print("change_directory: ", self.saved_directory)
        Path(create_directory).mkdir(parents=True, exist_ok=True)

        self.current_directory = Label(
            text=create_directory,
            wraplength=self.root_width-50, justify="center")
        # ===== Save to Directory Ends =====

        # ===== Seperator Line  =====
        self.w2 = Seperator.draw_seperator(self.root_width, master, transparent=False)

        # ===== Time Duration Dropdown Starts =====
        # Screenshots Label
        self.dropdown_label = Label(text="Take Screenshots every ",
                                    highlightthickness=0,
                                    bg="#fff")

        self.time_selected = IntVar()
        self.time_selected.set(self.saved_ss_duration)

        self.time_duration_dropdown = OptionMenu(
            master,
            self.time_selected,
            *self.options,
            command=self.time_duration_dropdown_click
        )

        # Minutes Text
        self.minutes_label = Label(text="mins")
        # ===== Time Duration Dropdown Ends =====

        # Seperator
        self.w3 = Seperator.draw_seperator(self.root_width, master, transparent=True)

        # ===== Radio Button Right click Event Starts =====
        # Button-3: Secondary Button
        # Binding a function with arguments to a widget
        # https://stackoverflow.com/questions/7299955/tkinter-binding-a-function-with-arguments-to-a-widget
        self.record_when1.bind(
            "<Button-3>",
            lambda event:
            self.record_when_clicked(r.get())
        )
        self.record_when2.bind(
            "<Button-3>",
            lambda event:
            self.record_when_clicked(r.get())
        )
        # ===== Radio Button Right click Event Ends =====

        # Status of radio buttons when clicked 
        self.when_to_start_status = Label(
            text="",
            wraplength=self.root_width-50,
            highlightthickness=0,
            # bg="#fff"
        )

        self.set_grids()

        # Now, Start taking ss if AUTO_START is enabled 
        if self.AUTO_START:
            self.record_button_click()

        self.toggle_running_info()

    # ******************** Grids Starts ********************
    def set_grids(self):
        current_row = 1

        # self.button1.grid()
        self.frame.grid(row=current_row)
        # self.record_text.grid(row=2, column=1,
        #                       padx=self.xPadding,
        #                       pady=self.yPadding)

        current_row += 1
        print(current_row)
        self.record_button.grid(row=current_row, column=0, columnspan=3,
                                padx=self.xPadding,
                                pady=self.yPadding, sticky=W)

        # Already running info
        current_row += 1
        self.already_running_info.grid(row=current_row, column=0, columnspan=3,
                                       padx=self.xPadding,
                                       pady=self.yPadding, sticky=W)
        # Seperator Grid
        current_row += 1
        self.w1.grid(row=current_row, column=0, columnspan=3)

        # Directory Text Grid
        current_row += 1
        self.save_directory_text.grid(row=current_row, column=0,
                                      sticky=W, padx=self.xPadding)

        # Browse Directory Button Grid
        self.save_directory.grid(row=current_row, column=1, sticky=E)

        # Current Directory Text
        current_row += 1
        self.current_directory.grid(row=current_row, column=0, columnspan=3,
                                    padx=self.xPadding, pady=self.yPadding,
                                    sticky=W)

        # Seperator Grid
        current_row += 1
        self.w2.grid(row=current_row, column=0,
                     columnspan=3, pady=self.yPadding)

        # Time Duration Dropdown
        current_row += 1
        self.dropdown_label.grid(row=current_row, column=0,
                                 padx=self.xPadding, columnspan=1, sticky=W)
        self.time_duration_dropdown.grid(row=current_row, column=1,
                                         columnspan=1, padx=self.xPadding)
        self.minutes_label.grid(row=current_row, column=2, columnspan=1)

        current_row += 1
        self.w3.grid(row=current_row, column=0, columnspan=3,
                     sticky=W, pady=self.yPadding)

        # ===== "When to save" Radiobutton Grids Starts=====
        # Save at Start
        current_row += 1
        self.record_when1.grid(row=current_row, column=0, columnspan=1,
                               padx=self.xPadding, sticky=W)

        # Save when clicked "Start"
        current_row += 1
        self.record_when2.grid(row=current_row, column=0, columnspan=1,
                               padx=self.xPadding, sticky=W)
        # ===== "When to save" Radiobutton Grids Ends =====

        current_row += 1
        self.when_to_start_status.grid(row=current_row, column=0, columnspan=3,
                                    padx=self.xPadding, pady=self.yPadding,
                                    sticky=W)
    # ******************** Grids Ends ********************

    def record_when_clicked(self, value):
        # ===== Changing Config File Starts =====
        self.config['default']['start_at'] = str(value)
        print("Config File path: ", os.path.join(self.config_file_path, self.config_file))
        with open(os.path.join(self.config_file_path, self.config_file), 'w') as cf:
            self.config.write(cf)
        # ===== Changing Config File Ends =====

        if value == 1:
            self.add_to_start()
        if value == 2:
            self.remove_from_start()

    def record_button_click(self):
        if self.record_status is False:

            # no need to ask permission to user if AUTO_START is enabled
            if self.AUTO_START: 
                response = True
                if self.DEBUG:
                    print("AUTO_START and DEBUG True")
                    response = messagebox.askyesno(
                        "Warning",
                        "Debug on. Started from autostart. Press anything. Wont matter.")
                    response = True
            else:
                response = messagebox.askyesno(
                    "Warning",
                    "This will start recording screenshots. Are you sure?")

            if response:
                self.record_status = True
                self.record_button.config(
                    background='#ff0000',
                    foreground='#000',
                    activebackground='#d9534f',
                    activeforeground='#fff',
                    text=self.stop_record_text + " Screenshots")

                # daemon
                # The Daemon Thread does not block the main thread from 
                # exiting and continues to run in the background

                # Example: Read "themefield's" answer
                # https://stackoverflow.com/questions/5127401/setdaemon-method-of-threading-thread 
                Thread(target=self.capture_screenshots, daemon=True,
                       args=()).start()

                print("Thread Startss")
                # to make "root.mainloop" keep running to show GUI
                Thread(target=self.continue_code).start()

                # self.record_text.config(
                #     text=self.start_record_text + "Screenshots")

        elif self.record_status is True:
            response = messagebox.askyesno(
                "Warning",
                "This will STOP recording screenshots. Are you sure?")
            if response:
                self.record_status = False
                self.record_button.config(
                    bg="#25D366",
                    foreground='#fff',
                    activebackground='#5cb85c',
                    activeforeground='#fff',
                    text=self.start_record_text + " Screenshots")
                self.config['default']['take_ss'] = "0"
                with open(os.path.join(self.config_file_path, self.config_file), 'w') as cf:
                    self.config.write(cf)

                print("Removing already_running_info")
                self.toggle_running_info()
                # self.record_text.config(
                #     text=self.stop_record_text + "Screenshots")
        return response

    def new_window(self):
        self.newWindow = Toplevel(self.master)
        self.app = SecondaryWindow(self.newWindow)

    def save_directory_click(self):
        self.folder_selected = filedialog.askdirectory()
        if type(self.folder_selected) == tuple:
            pass
        elif type(self.folder_selected) == str:
            self.folder_selected = self.folder_selected.strip()
            if self.folder_selected:
                print("Directory Changed")

                # ===== Changing Config File Starts =====
                self.config['default']['saved_directory'] = "\"" + self.folder_selected + "\""
                with open(os.path.join(self.config_file_path, self.config_file), 'w') as cf:
                    self.config.write(cf)
                # ===== Changing Config File Ends =====

                self.current_directory.config(
                    text=self.folder_selected,
                    wraplength=self.root_width-50, justify="center")

    def time_duration_dropdown_click(self, event):
        new_time = str(self.time_selected.get())
        print(new_time)
        self.config['default']['screenshot_duration'] = new_time
        with open(os.path.join(self.config_file_path, self.config_file), 'w') as cf:
            self.config.write(cf)

    def capture_screenshots(self):
        self.saved_is_running = 1
        self.config['default']['is_running'] = "1"
        self.config['default']['take_ss'] = "1"
        print("capture_screenshots started so \"is_running\" changed to 1")
        print("capture_screenshots started so \"take_ss\" changed to 1")
        with open(os.path.join(self.config_file_path, self.config_file), 'w') as cf:
            self.config.write(cf)

        # Getting Text from `current_directory` Label
        curr_dir_cget_text = self.current_directory.cget("text")
        print(">>", curr_dir_cget_text)
        if not curr_dir_cget_text.rstrip("/").rstrip("\\").endswith(self.APP_NAME):
           curr_dir_cget_text = os.path.join(curr_dir_cget_text, self.APP_NAME)

        while self.record_status:
            break_loop = self.stop_if_take_ss_disabled()
            if break_loop:
                break

            myScreenshot = pyautogui.screenshot()

            # Get Current time
            now = datetime.now()

            # Creating Directory in case date changes
            today_month_year = now.strftime("%b-%Y")
            today_date = now.strftime("%d")

            # Creating Directory safely
            new_directory = os.path.join(curr_dir_cget_text,
                                         str(today_month_year),
                                         str(today_date))
            # new_directory = (curr_dir_cget_text +
            #                  str(today_month_year) + "/" +
            #                  str(today_date) + "/")
            Path(new_directory).mkdir(parents=True, exist_ok=True)

            # setting current datetime as image_filename
            image_filename = now.strftime("%b-%d-%Y - %H-%M-%S")

            cc = 1
            cc += 1
            try:
                myScreenshot.save(
                    new_directory + "/" + str(image_filename) + ".jpg",
                    'JPEG', optimize=True, quality=70)
                    # 'JPEG', optimize=True, quality=35)
            except Exception as e:
                print(e)
                print("Error in ss save")
                self.on_closing()
            print(new_directory + "/" + str(image_filename) + ".jpg saved")

            # Each screenshot Every N seconds
            seconds_to_wait = self.time_selected.get() * 60

            # 2nd answer:
            # https://stackoverflow.com/questions/5127401/setdaemon-method-of-threading-thread
            time.sleep(seconds_to_wait)
            # Thread will wait for N minutes to complete if user terminates main code,
            # This problem will arise when time.sleep is set to greater value
            # thus daemon helps here.

    def continue_code(self):
        pass

    def stop_if_take_ss_disabled(self):
        # if auto script is running, clicking on "stop" will stop taking ss
        # Check config file status
        self.config.read(os.path.join(self.config_file_path, self.config_file))
        self.take_ss = int(self.config['default']['take_ss'])
        print(self.take_ss)
        print(type(self.take_ss))

        # if application is running in 2 windows, clicking STOP in any one app will stop
        # other running process Like
        if self.take_ss == 0:
            print("Screenshots stopped")
            # if other process is started in AUTO_START, program will be stopped
            if self.AUTO_START:
                print("Exiting")
                self.on_closing()
            else:
                print("Script Breaked")
                return True
        return False

    def check_config_file_and_insert(self, default_path):
        if os.path.exists(os.path.join(self.config_file_path, self.config_file)):
            self.config.read(os.path.join(self.config_file_path, self.config_file))
            print("cConfig file exist")

            self.saved_directory = self.config['default']['saved_directory'].strip("\"")
            print("saved_directory", self.saved_directory)
            if not os.path.isdir(self.saved_directory):
                print("Directroy Not Exists")
                self.saved_directory = default_path

            self.saved_ss_duration = self.config['default']['screenshot_duration']
            self.saved_ss_duration = int(self.saved_ss_duration)
            if self.saved_ss_duration not in self.options:
                print("Not in options. Setting 10")
                self.saved_ss_duration = 10

            self.saved_start_at = int(self.config['default']['start_at'])
            # if some user does monkey business. Like setting value to 3
            if self.saved_start_at != 1 and self.saved_start_at != 2:
                print("saved_start_at value Changed")
                self.saved_start_at = 2

            self.saved_is_running = int(self.config['default']['is_running'])
            self.saved_take_ss = int(self.config['default']['take_ss'])

        # If config file does NOT exists
        else:
            print("Config file NOT exist")
            self.saved_directory = default_path
            self.saved_ss_duration = 10
            self.saved_start_at = 2
            self.saved_is_running = 1
            self.saved_take_ss = 0

        self.master.protocol("WM_DELETE_WINDOW", self.on_closing)
        print("saved_directory:", self.saved_directory)
        print("saved_ss_duration", self.saved_ss_duration)
        print("saved_is_running", self.saved_is_running)
        print("saved_take_ss", self.saved_take_ss)

        self.config['default'] = {
            'saved_directory': self.saved_directory,
            'screenshot_duration': self.saved_ss_duration,
            'start_at': self.saved_start_at,
            'is_running': self.saved_is_running,
            'take_ss': self.saved_take_ss,
        }

        Path(self.config_file_path).mkdir(parents=True, exist_ok=True)
        with open(os.path.join(self.config_file_path, self.config_file), 'w') as cf:
            self.config.write(cf)
        # ===== Config file Setting Ends =====

    def add_to_start(self):
        print("Changed Config.ini File to start at boot")
        print("Trying to Add shortcut at startup app Directory")
        if platform == "linux":
            # conf file path
            start_at_boot_config = ConfigParser()
            autostart_conf_path = os.path.expanduser('~/.config/autostart/')
            Path(autostart_conf_path).mkdir(parents=True, exist_ok=True)
            # conf file path

            # Getting "main" file path Starts
            description = self.APP_NAME + " Startup"
            if self.DEBUG:
                autostart_conf_file = os.path.join(autostart_conf_path, self.APP_NAME + "-debug.desktop")
                # main.py must be "+x" to work
                app_startup_path = os.path.join(self.ROOT_DIR, "main.py") + " autostart"
            else:
                autostart_conf_file = os.path.join(autostart_conf_path, self.APP_NAME + ".desktop")
                app_startup_path = os.path.join("/usr/bin/", self.APP_NAME,  "main") + " autostart"
            # Getting "main" file path Ends

            # editing conf file for startup
            start_at_boot_config['Desktop Entry'] = {
                'Type': "Application".strip("\""),
                'Exec': app_startup_path.strip("\""),
                'X-GNOME-Autostart-enabled': "true".strip("\""),
                'Comment': description.strip("\""),
            }
            # editing conf file for startup

            with open(autostart_conf_file, 'w') as cf:
                start_at_boot_config.write(cf)
            print(app_startup_path)
            print("Above Linux path added to: ", autostart_conf_file)
        elif platform == "darwin":
            # OS X
            pass
        elif platform == "win32" or platform == "cygwin":
            # https://stackoverflow.com/questions/67555101/tkinter-exe-added-to-startup-shows-console-window
            # # Windows...
            USER_NAME = getuser()
            if self.DEBUG:
                file_path = '%localappdata%\\Programs\\Swaminarayan\\Swaminarayan.exe'
            else:
                # to ignore lib and and library.zip
                # file_path = os.path.join(self.ROOT_DIR, "..", "..", self.APP_NAME + ".exe")
                file_path = os.path.join(self.ROOT_DIR, self.APP_NAME + ".exe")

            startup_path = r'C:\Users\%s\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup' % (USER_NAME)
            print(startup_path)
            # self.when_to_start_status.config(text="FilePath:\n" + file_path + "\n\n" + " Startup_path:\n" + startup_path)

            # create shortcut starts
            # pythoncom.CoInitialize() # remove the '#' at the beginning of the line if running in a thread.
            shortcut_name = self.APP_NAME + ".lnk"
            # destination_path = os.path.dirname(os.path.realpath(__file__)) # path to where you want to put the .lnk
            destination_path = self.ROOT_DIR # path to where you want to put the .lnk
            path = os.path.join(destination_path, shortcut_name)
            target = file_path
            icon = os.path.join(file_path , "images", "snapshare.ico") # not needed, but nice


            try:
                self.when_to_start_status.config(text="Creating shortcut...")
                shell = win32com.client.Dispatch("WScript.Shell")
                shortcut = shell.CreateShortCut(path)
                shortcut.Targetpath = target
                shortcut.Arguments = '--autostart'
                shortcut.WorkingDirectory = destination_path
                shortcut.IconLocation = os.path.join(self.ROOT_DIR, "images", "snapshare.ico")
                shortcut.WindowStyle = 7  # 7 - Minimized, 3 - Maximized, 1 - Normal
                self.when_to_start_status.config(text="Creating shortcut.....")
                shortcut.save()
                self.when_to_start_status.config(text="Shortcut created. ")
                print("shortcut saved")
            except:
                self.when_to_start_status.config(text="Unexpected error:" + sys.exc_info()[0])
            # create shortcut ends

            file_path = path
            print(file_path)
            
            try:
                shutil.copyfile(file_path, os.path.join(startup_path, shortcut_name))
                self.when_to_start_status.config(text="Screenshots will be taken when system starts.")
                print("file_path", file_path)
                print("Above Windows path added to startup path which is: ", startup_path)
            except PermissionError as e:
                print(e)
            # with open(startup_path + '\\' + "open.bat", "w+") as fw:
                # fw.write(r'start "" "%s" autostart' % file_path)


    def remove_from_start(self):
        print(platform)
        USER_NAME = getuser()    

        if platform == "linux":
            autostart_conf_path = os.path.expanduser('~/.config/autostart/')
            if self.DEBUG:
                autostart_conf_file = os.path.join(autostart_conf_path, self.APP_NAME + "-debug.desktop")
            else:
                autostart_conf_file = os.path.join(autostart_conf_path, self.APP_NAME + ".desktop")
            if(os.path.exists(autostart_conf_file)):
                print("Autostart Conf file exists in linux. So deleting File")
                os.remove(autostart_conf_file)
                print("Deleted")
            else:
                print("Linux Conf NOT exists in %s" % (autostart_conf_file))

        elif platform == "darwin":
            # OS X
            pass
        elif platform == "win32" or platform == "cygwin":
            # windows
            startup_file = r'C:\Users\%s\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\%s.lnk' % (USER_NAME, self.APP_NAME)
            if(os.path.exists(startup_file)):
                self.when_to_start_status.config(text="Startup exists. Removing...")
                self.when_to_start_status.config(text=startup_file + "exists")
                os.remove(startup_file)
                print("Deleted")
                self.when_to_start_status.config(text="Screenshots will be taken manually.")
            else:
                self.when_to_start_status.config(text="Screenshots will be taken manually")
                print("Startup file NOT exists in %s" % (startup_file))

    def toggle_running_info(self):    
        self.config.read(os.path.join(self.config_file_path, self.config_file))
        self.saved_take_ss = int(self.config['default']['take_ss'])    
        
        if self.saved_take_ss:
            self.warn_on_close = False
            self.already_running_info.grid()
        else:
            self.warn_on_close = True
            self.already_running_info.grid_remove()

    def on_closing(self):
        self.config.read(os.path.join(self.config_file_path, self.config_file))
        self.saved_take_ss = int(self.config['default']['take_ss'])

        # So that if autostart is enabled, it is allowed to close, 
        # or if screenshots tasks is yet not started.
        response = True

        if self.warn_on_close and self.saved_take_ss:
            # if user clicks NO, it will not be closed
            response = self.record_button_click()
            if response:
                self.config['default']['take_ss'] = '0'
            print(response)

        print("on_closing() function invoked")
        if response:
            print("response to close is",  response)
            self.config['default']['is_running'] = '0'
            with open(os.path.join(self.config_file_path, self.config_file), 'w') as cf:
                self.config.write(cf)

            print("Destryoing master")
            self.master.quit()
            self.master.destroy()
            print("Destryed")