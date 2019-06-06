import threading
import pigpio
import time
import math


class Serwo(threading.Thread):
    __min_cycle = 1000
    __max_cycle = 2000
    __cycle_to_radian_multiplier = math.pi / 2000.0
    __cycle_to_degree_multiplier = 0.09

    def __init__(self, period, step, control_pin):
        super(Serwo, self).__init__()
        self.__gpio = pigpio.pi()
        self.__period = period
        self.__control_pin = control_pin
        self.__step = step
        self.busy = False
        self.cycle = Serwo.__min_cycle
        self.rotation_no = 0
        self.__backward = 0
        self.__do_job = 0
        self.__stop_event = threading.Event()
        # self.__thread_results_generator()
        self.__thread = threading.Thread(target=self.__thread_results_generator)
        self.__thread.start()

    def __thread_results_generator(self):
        while True:
            while not self.__stop_event.is_set():
                pass
            if self.__backward == 0 and self.cycle >= Serwo.__max_cycle:
                self.__backward = 1
                self.rotation_no += 1
            elif self.__backward == 1 and self.cycle <= Serwo.__min_cycle:
                self.__backward = 0
                self.rotation_no += 1
            new_cycle = self.cycle
            if self.__backward == 0:
                new_cycle += self.__step
            else:
                new_cycle -= self.__step
            self.move_to(new_cycle)

    def get_position_in_radian(self):
        return (self.cycle - Serwo.__min_cycle) * Serwo.__cycle_to_radian_multiplier

    def get_position_in_degree(self):
        return (self.cycle - Serwo.__min_cycle) * Serwo.__cycle_to_degree_multiplier

    def move_to(self, cycle):
        cycle = max(Serwo.__min_cycle, cycle)
        cycle = min(Serwo.__max_cycle, cycle)
        self.busy = True
        self.__gpio.set_servo_pulsewidth(self.__control_pin, cycle)
        time.sleep(self.__period)
        self.cycle = cycle
        self.busy = False

    def run(self):
        self.__stop_event.set()

    def stop(self):
        self.__stop_event.clear()
