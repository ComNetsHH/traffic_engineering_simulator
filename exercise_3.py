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

    def schedule(self, packet, destinations):
        ''' IMPLEMENT THIS
        This is your scheduling policy. Whenever a packet was created, this function will be called to decide where it should be processed.
        It receives the packet and a list of all possible destinations.
        If you wan't to see where the packet came from, use `packet['from']`.
        You can use statistics from the data centers for your scheduling decision:
        E.g. `destinations[0].get_queue_size()` gives you the current queue size or `destinations[0].get_utilization()` returns the utilization
        '''
        self.idx = (self.idx +1) % len(destinations)
        return destinations[self.idx].id


if __name__ == '__main__':
    run_number = sys.argv[1] if len(sys.argv) > 1 else 1
    random.seed(run_number)
    env = simpy.Environment()
    policy = SchedulingPolicy()
    scheduler = Scheduler(policy)

    d1 = DataCenter(env, num_servers=6, service_rate=2, queue_size=100)
    d2 = DataCenter(env, num_servers=3, service_rate=2, queue_size=120)
    d3 = DataCenter(env, num_servers=1, service_rate=2, queue_size=50)

    scheduler.set_destinations([d1, d2, d3])

    e1 = EdgeNode(env, scheduler, arrival_rate=4, min_packet_size=20, max_packet_size=30)
    e2 = EdgeNode(env, scheduler, arrival_rate=3, min_packet_size=30, max_packet_size=40)
    e3 = EdgeNode(env, scheduler, arrival_rate=5, min_packet_size=15, max_packet_size=15)
    e4 = EdgeNode(env, scheduler, arrival_rate=3, min_packet_size=30, max_packet_size=35)
    e5 = EdgeNode(env, scheduler, arrival_rate=1, min_packet_size=50, max_packet_size=90)

    env.run(until=1000)

    Stats.set_experiment_name('exercise_3')
    Stats.evaluate([d1, d2, d3], verbose=True)

    
