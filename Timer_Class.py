import time

class Timer:
    def __init__(self):
        self.start_sec = None
        self.stop_sec = 0
        self.sec_elapsed = 0
        self.min_elapsed = 0
        self.str_sec = ''
        self.str_min = ''
        self.timer = ''

    #start timer
    def start_timer(self):
        if self.start_sec == None:
            self.start_sec = time.perf_counter()
            self.sec_elapsed = self.start_sec
            
    #stop timer
    def stop_timer(self):
        if self.start_sec != None:
            self.stop_sec = time.perf_counter() 
            self.sec_elapsed = int(self.stop_sec - self.start_sec)
            self.start_sec = None

    #transform timer (sec) into string, format min:sec
    def calculate_time(self):
        if self.sec_elapsed > 60:
            self.min_elapsed = int(self.sec_elapsed / 60)
            self.sec_elapsed -= 60 * int(self.min_elapsed)
        
        if self.min_elapsed > 9: self.str_min = str(int(self.min_elapsed))
        else: self.str_min = "0" + str(int(self.min_elapsed))
        if self.sec_elapsed > 9: self.str_sec = ":" + str(int(self.sec_elapsed))
        else: self.str_sec = ":0" + str(int(self.sec_elapsed))
        self.timer = self.str_min + self.str_sec

    #update timer and return string version of timer
    def get_time(self):
        self.sec_elapsed = int(time.perf_counter()  - self.start_sec)
        self.calculate_time()
        
        return self.timer
        

