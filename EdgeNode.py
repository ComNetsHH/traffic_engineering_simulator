import random

class EdgeNode(object):
    index = 0
    def __init__(self, env, scheduler, arrival_rate=10, min_demand=10, max_demand=10, verbose=False):
        self.env = env
        self.scheduler = scheduler
        self.verbose = verbose
        self.id = f'edge_node_{EdgeNode.index}'
        EdgeNode.index += 1
        self.arrival_rate = arrival_rate
        self.min_demand = min_demand
        self.max_demand = max_demand

        # Start Node
        self.action = env.process(self.run())


    def run(self):
        while True:
            t = random.expovariate(self.arrival_rate)
            yield self.env.timeout(t)
            demand = self.min_demand + round((self.max_demand - self.min_demand) * random.random())
            self.scheduler.on_receive({
                'from': self.id,
                'arrival_time': self.env.now,
                'demand': demand
            })