import simpy
import sys
import random
from EdgeNode import EdgeNode
from DataCenter import DataCenter
from TrafficScheduler import TrafficScheduler
from Stats import Stats


class SchedulingPolicy:
    def schedule(self, packet, destinations):
        return destinations[0].id


if __name__ == '__main__':
    run_number = sys.argv[1] if len(sys.argv) > 1 else 1
    random.seed(run_number)
    env = simpy.Environment()
    policy = SchedulingPolicy()
    scheduler = TrafficScheduler(policy)

    d1 = DataCenter(env, service_rate=4, queue_size=40)

    scheduler.set_destinations([d1])

    e1 = EdgeNode(env, scheduler, arrival_rate=4, min_packet_size=2, max_packet_size=3)

    env.run(until=100)

    Stats.set_experiment_name('example')
    Stats.evaluate([d1], verbose=True)

    
