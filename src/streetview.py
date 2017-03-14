import os
import time
import pickle
import argparse
import pyscreenshot as ImageGrab
from pymouse import PyMouse

class StreetViewCapture:
    def __init__(self, time=2, click=True):
        self.mouse = PyMouse()

        self.x, self.y = self.mouse.screen_size()
        self.x = int(self.x/2) - 150
        self.y = self.y - 100

        self.wait = time
        self.click = click
        self.picke_file = "data"

        try:
            self.run_number = pickle.load(open(self.picke_file, "rb"))
        except FileNotFoundError:
            self.run_number = 0

        self.folder_name = "run-%03d" % self.run_number

        self.dir = os.path.abspath(os.path.join(os.path.dirname("."), 'img', self.folder_name))
        print(self.dir)

        try:
            os.makedirs(self.dir)
        except FileExistsError:
            pass


    def click_screen(self):
        self.mouse.click(self.x, self.y, 1)

    def save_screenshot(self):
        img = ImageGrab.grab()
        filename = self.get_filename()
        path = os.path.join(self.dir, filename)
        img.save(path)

        print(path)

    def get_filename(self):
        filename = 'screenshot-'
        filename += time.strftime("%d%m%Y-%H%M%S")
        filename += '.jpg'

        return filename

    def capture(self, n):
        input("Click any key. StreetView Image Capture will start capturing " + str(n) + " images.")
        time.sleep(1)

        for i in range(n):
            self.click_screen()
            time.sleep(self.wait)
            self.save_screenshot()

    def start(self):
        input("StreetView Image Capture will start NOW.\nPress CTRL+C to stop.")
        time.sleep(1)

        try:
            while True:
                if self.click:
                    self.click_screen()
                    
                time.sleep(self.wait)
                self.save_screenshot()
        except KeyboardInterrupt:
            self.run_number += 1
            file_handler =  open(self.picke_file, "wb")
            pickle.dump(self.run_number, file_handler)



if __name__ == '__main__':
    # Parse arguments
    parser = argparse.ArgumentParser(description='street-view-capture')

    parser.add_argument('-t', '--time', type=int, default=2,
                        help='time in seconds between screen captures')

    parser.add_argument('-c', '--click', action='store_true',
                        help='clicks on the middle of the screen')

    args = parser.parse_args()

    sv = StreetViewCapture(time=args.time, click=args.click)
    sv.start()
