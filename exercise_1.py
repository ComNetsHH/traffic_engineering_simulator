import simpy
import sys
import random
import math
from EdgeNode import EdgeNode
from DataCenter import DataCenter
from TrafficScheduler import TrafficScheduler
from Stats import Stats


class SchedulingPolicy:
    def schedule(self, request, destinations):
        return destinations[0].id


if __name__ == '__main__':
    run_number = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    random.seed(run_number)
    env = simpy.Environment()
    policy = SchedulingPolicy()
    scheduler = TrafficScheduler(policy)

    d1 = DataCenter(env, service_rate=12, resource_capacity=1, has_queue=True)

    scheduler.set_destinations([d1])

    e1 = EdgeNode(env, scheduler, arrival_rate=2, min_demand=1, max_demand=1)
    e2 = EdgeNode(env, scheduler, arrival_rate=2, min_demand=1, max_demand=1)
    e3 = EdgeNode(env, scheduler, arrival_rate=2, min_demand=1, max_demand=1)
    e4 = EdgeNode(env, scheduler, arrival_rate=2, min_demand=1, max_demand=1)
    e5 = EdgeNode(env, scheduler, arrival_rate=2, min_demand=1, max_demand=1)

    env.run(until=2000)

    Stats.set_experiment_name('exercise_1')
    Stats.evaluate([d1], verbose=True)

    
