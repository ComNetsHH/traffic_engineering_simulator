import random

class EdgeNode(object):
    index = 0
    def __init__(self, env, scheduler, arrival_rate= 10, min_packet_size = 10, max_packet_size=10, verbose=False):
        self.env = env
        self.scheduler = scheduler
        self.verbose = verbose
        self.id = f'edge_node_{EdgeNode.index}'
        EdgeNode.index += 1
        self.arrival_rate = arrival_rate
        self.min_packet_size = min_packet_size
        self.max_packet_size = max_packet_size

        # Start Node
        self.action = env.process(self.run())


    def run(self):
        while True:
            t = random.expovariate(self.arrival_rate)
            yield self.env.timeout(t)
            size = self.min_packet_size + round((self.max_packet_size - self.max_packet_size) * random.random())
            self.scheduler.on_receive({
                'from': self.id,
                'arrival_time': self.env.now,
                'size': size
            })