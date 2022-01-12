import simpy
import sys
import random
from EdgeNode import EdgeNode
from DataCenter import DataCenter
from TrafficScheduler import TrafficScheduler
from Stats import Stats


class SchedulingPolicy:
    def schedule(self, request, destinations):
        return destinations[0].id


if __name__ == '__main__':
    run_number = sys.argv[1] if len(sys.argv) > 1 else 1
    random.seed(run_number)
    env = simpy.Environment()
    policy = SchedulingPolicy()
    scheduler = TrafficScheduler(policy)

    d1 = DataCenter(env, service_rate=3, resource_capacity=4, has_queue=True)

    scheduler.set_destinations([d1])

    e1 = EdgeNode(env, scheduler, arrival_rate=4, min_demand=2, max_demand=2)

    env.run(until=100)

    Stats.set_experiment_name('example')
    Stats.evaluate([d1], verbose=True)

    
