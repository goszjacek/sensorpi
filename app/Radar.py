import threading
import RPi.GPIO as GPIO
import time


class Radar(threading.Thread):
    pulses_speed = 17150

    def __init__(self, period, trigger_pin, echo_pin):
        super(Radar, self).__init__()
        GPIO.setmode(GPIO.BCM)
        self.period = max(0.1, period)
        self.__trigger_pin = trigger_pin
        self.__echo_pin = echo_pin
        GPIO.setup(trigger_pin, GPIO.OUT)
        GPIO.setup(echo_pin, GPIO.IN)
        GPIO.output(trigger_pin, GPIO.LOW)
        self.busy = False
        self.last_result = 0
        self.__do_job = 0
        self.__stop_event = threading.Event()
        # self.__thread_results_generator()
        self.__thread = threading.Thread(target=self.__thread_results_generator)
        self.__thread.start()

    def __thread_results_generator(self):
        while True:
            while not self.__stop_event.is_set():
                print("loop")
                pass
            temp = self.get_avg_distance(1)
            self.last_result = temp

    def run(self):
        self.__stop_event.set()

    def stop(self):
        self.__stop_event.clear()

    def prepare_result(self):
        self.__do_job = 1

    def read_distance(self):
        GPIO.output(self.__trigger_pin, GPIO.HIGH)
        time.sleep(0.000001)
        GPIO.output(self.__trigger_pin, GPIO.LOW)
        pulse_start = time.time()
        pulse_end = time.time()
        while GPIO.input(self.__echo_pin) == 0:
            pulse_start = time.time()
        while GPIO.input(self.__echo_pin) == 1:
            pulse_end = time.time()
        result = round((pulse_end - pulse_start) * Radar.pulses_speed)
        # if result > 450:
        #     return self.read_distance();
        return result

    def get_avg_distance(self, how_many=3):
        sum_of_measurments = 0
        for i in range(how_many):
            sum_of_measurments += self.read_distance()
            time.sleep(self.period)
        return round(sum_of_measurments / how_many)
