import random

IDLE_STATE = 'IDLE'
BUSY_STATE = 'BUSY'

class Process(object):
    index = 0
    def __init__(self, env, data_center, service_rate= 10, verbose=False):
        self.env = env
        self.verbose = verbose
        self.data_center = data_center
        self.id = f'process_{Process.index}'
        Process.index += 1
        self.state = IDLE_STATE
        self.service_rate = service_rate
        self.current_request = None
        self.delays = []

    def is_idle(self):
        return self.state == IDLE_STATE

    def on_receive(self, request):
        if self.state == IDLE_STATE:
            self.current_request = request
            self.action = self.env.process(self.run())
        else:
            raise Exception(f'{self.id} received request while busy')

    def run(self):
        while True:
            if self.current_request == None:
                self.state = IDLE_STATE
                self.data_center.record_state()
                return
            else:
                self.state = BUSY_STATE
                duration = random.expovariate(self.service_rate)
                yield self.env.timeout(duration)
                delay = self.env.now - self.current_request['arrival_time']
                self.delays.append(delay)
                self.data_center.on_complete(self)
                self.data_center.record_state()
                return

