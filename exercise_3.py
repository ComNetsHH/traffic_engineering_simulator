import simpy
import sys
import random
from EdgeNode import EdgeNode
from DataCenter import DataCenter
from TrafficScheduler import TrafficScheduler
from Stats import Stats


class SchedulingPolicy:
    def __init__(self):
        self.idx = 1

    def schedule(self, request, destinations):
        ''' IMPLEMENT THIS
        This is your scheduling policy. Whenever a request is created, this function will be called to decide where it should be processed.
        It receives the request and a list of all possible data centers.
        If you wan't to see where the request came from, use `request['from']`.
        You can use statistics from the data centers for your scheduling decision:
        E.g. `destinations[0].get_used_capacity()` gives you the currently occupied capacity or `destinations[0].get_utilization()` returns the utilization.
        Consult the `DataCenter` class for more methods.
        '''
        self.idx = (self.idx +1) % len(destinations)
        return destinations[self.idx].id



if __name__ == '__main__':
    run_number = sys.argv[1] if len(sys.argv) > 1 else 1
    random.seed(run_number)
    env = simpy.Environment()
    policy = SchedulingPolicy()
    scheduler = TrafficScheduler(policy)

    d1 = DataCenter(env, resource_capacity=19, service_rate=3, has_queue=False)
    d2 = DataCenter(env, resource_capacity=9, service_rate=3, has_queue=False)
    d3 = DataCenter(env, resource_capacity=8, service_rate=3, has_queue=False)

    scheduler.set_destinations([d1, d2, d3])

    e1 = EdgeNode(env, scheduler, arrival_rate=4, min_demand=2, max_demand=4)
    e2 = EdgeNode(env, scheduler, arrival_rate=3, min_demand=2, max_demand=4)
    e3 = EdgeNode(env, scheduler, arrival_rate=5, min_demand=2, max_demand=4)
    e4 = EdgeNode(env, scheduler, arrival_rate=3, min_demand=2, max_demand=4)
    e5 = EdgeNode(env, scheduler, arrival_rate=1, min_demand=2, max_demand=4)

    env.run(until=1000)

    Stats.set_experiment_name('exercise_3')
    Stats.evaluate([d1, d2, d3], verbose=True)

    
