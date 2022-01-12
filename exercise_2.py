import simpy
import sys
import random
import math
from EdgeNode import EdgeNode
from DataCenter import DataCenter
from TrafficScheduler import TrafficScheduler
from Stats import Stats


class SchedulingPolicy:
    def __init__(self):
        self.idx = 1

    def schedule(self, request, destinations):
        idle_destinations = [d for d in destinations if d.get_spare_capacity() > 0]
        if(len(idle_destinations) == 0):
            idx = random.randint(0, len(destinations)-1)
            return destinations[idx].id
        else:
            idx = random.randint(0, len(idle_destinations)-1)
            return idle_destinations[idx].id


if __name__ == '__main__':
    run_number = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    random.seed(run_number)
    env = simpy.Environment()
    policy = SchedulingPolicy()
    scheduler = TrafficScheduler(policy)

    d1 = DataCenter(env, resource_capacity=2, service_rate=1, has_queue=False)
    d2 = DataCenter(env, resource_capacity=2, service_rate=1, has_queue=False)

    scheduler.set_destinations([d1, d2])

    e1 = EdgeNode(env, scheduler, arrival_rate=3, min_demand=1, max_demand=1)

    env.run(until=2000)

    Stats.set_experiment_name('exercise_2')
    Stats.evaluate([d1, d2], verbose=True)

    
