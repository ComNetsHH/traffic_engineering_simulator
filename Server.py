import random

IDLE_STATE = 'IDLE'
BUSY_STATE = 'BUSY'

class Server(object):
    index = 0
    def __init__(self, env, data_center, service_rate= 10, verbose=False):
        self.env = env
        self.verbose = verbose
        self.data_center = data_center
        self.id = f'server_{Server.index}'
        Server.index += 1
        self.state = IDLE_STATE
        self.service_rate = service_rate
        self.current_packet = None
        self.delays = []

    def is_idle(self):
        return self.state == IDLE_STATE

    def on_receive(self, packet):
        if self.state == IDLE_STATE:
            self.current_packet = packet
            self.action = self.env.process(self.run())
        else:
            raise Exception(f'{self.id} received packet while busy')

    def run(self):
        while True:
            if self.current_packet == None:
                self.state = IDLE_STATE
                self.data_center.record_state()
                return
            else:
                self.state = BUSY_STATE
                duration = random.expovariate(self.service_rate)
                yield self.env.timeout(duration)
                delay = self.env.now - self.current_packet['arrival_time']
                self.delays.append(delay)
                self.current_packet = self.data_center.request_packet(self)

