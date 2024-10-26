import os
import shutil
import datetime
import time as tm
import logging as lg
from logging.handlers import RotatingFileHandler
import time
import sys
import subprocess

from PyQt5.QtCore import pyqtSignal, QObject  # Warning causer (deprecation)
sys.stderr = open(os.devnull, 'w')  # bye-bye warnings!


class Auto_Flusher_1(QObject):
    progress_signal = pyqtSignal(int, int)  # Signal to emit (cleaned_items, total_items)
    status_signal = pyqtSignal(str)         # Signal to emit status messages

    # Version: 1.0.0

    def __init__(self):
        super().__init__()
        self.total_items = 0
        self.cleaned_items = 0
        self.processed_items = 0

        self.user_profile = os.getenv("USERPROFILE")

        self.folders_to_clean = [

            os.path.join(self.user_profile, 'AppData', 'Local', 'Temp'),

            'C:\\Windows\\Temp',

            'A:\\$RECYCLE.BIN', 'B:\\$RECYCLE.BIN', 'C:\\$RECYCLE.BIN', 'D:\\$RECYCLE.BIN', 'E:\\$RECYCLE.BIN', 'F:\\$RECYCLE.BIN',
            'G:\\$RECYCLE.BIN', 'H:\\$RECYCLE.BIN', 'I:\\$RECYCLE.BIN', 'J:\\$RECYCLE.BIN', 'K:\\$RECYCLE.BIN', 'L:\\$RECYCLE.BIN',
            'M:\\$RECYCLE.BIN', 'N:\\$RECYCLE.BIN', 'O:\\$RECYCLE.BIN', 'P:\\$RECYCLE.BIN', 'Q:\\$RECYCLE.BIN', 'R:\\$RECYCLE.BIN',
            'S:\\$RECYCLE.BIN', 'T:\\$RECYCLE.BIN', 'U:\\$RECYCLE.BIN', 'V:\\$RECYCLE.BIN', 'W:\\$RECYCLE.BIN', 'X:\\$RECYCLE.BIN',
            'Y:\\$RECYCLE.BIN', 'Z:\\$RECYCLE.BIN',

            'C:\\Windows\\System32\\winevt\\Logs'
        ]
        self.setup_logging()

    def setup_logging(self):
        log_file = 'cleaner.log'

        # Set up basic logging configuration
        lg.basicConfig(
            level=lg.DEBUG,  # Log all levels DEBUG and above
            format="%(asctime)s - %(levelname)s - %(message)s",
            handlers=[
                RotatingFileHandler(
                    log_file,  # Log file path
                    maxBytes=1024 * 1024,  # Max size before rotating (1MB)
                    backupCount=1  # Keep just 1 backup of logs
                )
            ]
        )

    def browsers_clean(self):

        time.sleep(0.05)  # SLOWDOWN TIMER - REDUCES RAM/CPU IMPACT

        """
        
        Cleans browser caches.
        
        """

        ### CHROME, EDGE, FIREFOX LOCAL
        chrome_folders = [
            os.path.join(self.user_profile, 'AppData', 'Local', 'Google', 'Chrome',
                         'User Data', 'Default', 'Cache', 'Cache_Data'),  # Standard Cache (images and files cached)
            os.path.join(self.user_profile, 'AppData', 'Local', 'Google', 'Chrome',
                         'User Data', 'Default', 'Code Cache'),  # Cached JavaScript
            os.path.join(self.user_profile, 'AppData', 'Local', 'Google', 'Chrome',
                         'User Data', 'Default', 'GPUCache'),  # GPU cache
            os.path.join(self.user_profile, 'AppData', 'Local', 'Google', 'Chrome',
                         'User Data', 'Default', 'Media Cache'),  # Media files cache
            os.path.join(self.user_profile, 'AppData', 'Local', 'Google', 'Chrome',
                         'User Data', 'Default', 'Service Worker', 'CacheStorage')  # Service workers cache
        ]

        # Loop through possible additional Edge profiles from 'Profile 2' to 'Profile 10'
        for i in range(1, 11):
            time.sleep(0.01)  # SLOWDOWN TIMER - REDUCES RAM/CPU IMPACT
            profile_name = f'Profile {i}'
            edge_folders = [
                os.path.join(self.user_profile, 'AppData', 'Local', 'Microsoft', 'Edge', 'User Data', profile_name, 'Cache', 'Cache_Data'),
                os.path.join(self.user_profile, 'AppData', 'Local', 'Microsoft', 'Edge', 'User Data', profile_name, 'Code Cache'),
                os.path.join(self.user_profile, 'AppData', 'Local', 'Microsoft', 'Edge', 'User Data', profile_name, 'GPUCache'),
                os.path.join(self.user_profile, 'AppData', 'Local', 'Microsoft', 'Edge', 'User Data', profile_name, 'Media Cache'),
                os.path.join(self.user_profile, 'AppData', 'Local', 'Microsoft', 'Edge', 'User Data', profile_name, 'Service Worker', 'CacheStorage'),
            ]

            for folder in edge_folders:
                if os.path.exists(folder):
                    time.sleep(0.01)  # SLOWDOWN TIMER - REDUCES RAM/CPU IMPACT
                    self.folders_to_clean.append(folder)

        for folder in chrome_folders:
            if os.path.exists(folder):
                time.sleep(0.01)  # SLOWDOWN TIMER - REDUCES RAM/CPU IMPACT
                self.folders_to_clean.append(folder)
        ###

        ### FIREFOX - ROAMING
        firefox_profile = os.path.join(self.user_profile, 'AppData', 'Roaming',
                                       'Mozilla', 'Firefox', 'Profiles')

            # Clean caches inside profiles
        if os.path.exists(firefox_profile):
            for profile_dir in os.listdir(firefox_profile):
                profile_path = os.path.join(firefox_profile, profile_dir)
                if os.path.isdir(profile_path):
                    time.sleep(0.01)  # SLOWDOWN TIMER - REDUCES RAM/CPU IMPACT
                    firefox_folders = [
                        os.path.join(profile_path, 'cache2'),  # Standard cache
                        os.path.join(profile_path, 'OfflineCache'),  # Offline cache for web apps
                        os.path.join(profile_path, 'storage', 'default', 'cache'),  # IndexedDB and local storage cache
                        os.path.join(profile_path, 'storage', 'permanent', 'cache'),  # Persistent storage cache
                        os.path.join(profile_path, 'cache')  # Legacy cache directory
                    ]

                    # Add these folders to the clean list and clean 'em.
                    for folder in firefox_folders:
                        if os.path.exists(folder):
                            time.sleep(0.01)  # SLOWDOWN TIMER - REDUCES RAM/CPU IMPACT
                            self.folders_to_clean.append(folder)
        ###

        ### FIREFOX - LOCAL
        firefox_local_profile = os.path.join(self.user_profile, 'AppData', 'Local', 'Mozilla', 'Firefox', 'Profiles')

        if os.path.exists(firefox_local_profile):
            for profile_dir in os.listdir(firefox_local_profile):
                profile_path = os.path.join(firefox_local_profile, profile_dir)
                if os.path.isdir(profile_path):
                    time.sleep(0.01)  # SLOWDOWN TIMER - REDUCES RAM/CPU IMPACT
                    firefox_local_folders = [
                        os.path.join(profile_path, 'cache2'),  # Standard cache
                        os.path.join(profile_path, 'jumpListCache'),  # "Jump list" cache
                        os.path.join(profile_path, 'startupCache'),  # Startup cache
                        os.path.join(profile_path, 'thumbnails')  # Thumbnails cache
                    ]

                    # Add Firefox Local folders to the list for cleaning
                    for folder in firefox_local_folders:
                        if os.path.exists(folder):
                            self.folders_to_clean.append(folder)
        ###

    def InternetExplorer_clean(self):
        # subprocess instead of os.system() prevents the annoying cmd console to appear during the execution
        subprocess.call('RunDll32.exe InetCpl.cpl,ClearMyTracksByProcess 255', creationflags=subprocess.CREATE_NO_WINDOW)

    def calculate_total_items(self):
        total_items = 0
        for folder in self.folders_to_clean:
            if os.path.exists(folder):
                for root, dirs, files in os.walk(folder):
                    total_items += len(files) + len(dirs)
        return total_items

    def folders_clean(self, folder):

        """
        Cleans folders/files from the list + appended folders/files to the list
        """

        time.sleep(0.05)  # SLOWDOWN TIMER - REDUCES RAM/CPU IMPACT
        """
        Cleans what's inside the list of folders given
        """
        try:
            for root, dirs, files in os.walk(folder, topdown=False):
                # Remove files
                for file in files:
                    file_path = os.path.join(root, file)
                    try:
                        time.sleep(0.01)  # SLOWDOWN TIMER - REDUCES RAM/CPU IMPACT
                        os.unlink(file_path)
                        self.cleaned_items += 1  # Increment cleaned items counter
                        self.progress_signal.emit(self.cleaned_items, self.total_items)
                        self.status_signal.emit(f"Deleted file: {file_path}")
                    except Exception as e:
                        lg.error(f"Skipped file {file_path}. Reason: {e}. Time: {datetime.datetime.now()}")
                        self.status_signal.emit(f"Skipped file: {file_path}")

                    self.processed_items += 1
                    self.progress_signal.emit(self.processed_items, self.total_items)

                # Remove directories
                for d in dirs:
                    dir_path = os.path.join(root, d)
                    try:
                        time.sleep(0.01)  # SLOWDOWN TIMER - REDUCES RAM/CPU IMPACT
                        shutil.rmtree(dir_path)
                        self.cleaned_items += 1  # Increment cleaned items counter
                        self.progress_signal.emit(self.cleaned_items, self.total_items)
                        self.status_signal.emit(f"Deleted directory: {dir_path}")
                    except Exception as e:
                        lg.error(f"Skipped directory {dir_path}. Reason: {e}. Time: {datetime.datetime.now()}")
                        self.status_signal.emit(f"Skipped directory: {dir_path}")

                    self.processed_items += 1
                    self.progress_signal.emit(self.processed_items, self.total_items)

        except Exception as e:
            lg.error(f"Error while cleaning folder {folder}. Reason: {e}. Time: {datetime.datetime.now()}")

    ### MAIN LOGIC SECTION
    def main(self):
        try:
            """
            Cleans all specified folders in `folders_to_clean` list every 15 seconds.
            """
            while True:
                self.cleaned_items = 0  # Reset cleaned items counter
                self.processed_items = 0  # Reset processed items counter
                self.InternetExplorer_clean()
                self.browsers_clean()
                # Calculate total items after appending browser folders
                self.total_items = self.calculate_total_items()
                self.progress_signal.emit(self.processed_items, self.total_items)
                self.status_signal.emit(f"Total items to clean: {self.total_items}")

                for folder in self.folders_to_clean:
                    if os.path.exists(folder):
                        self.status_signal.emit(f"Cleaning folder: {folder}")
                        self.folders_clean(folder)

                self.status_signal.emit("Waiting for next cleaning cycle...")
                tm.sleep(15)
        except Exception as e:
            lg.error(f'Exception while running the main func. Reason: {e}. Time: {datetime.datetime.now()}.')
    ###

# if __name__ == '__main__':
#     cleaner = Auto_Flusher_1()
#     cleaner.main()
