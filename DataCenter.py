import random
from Process import Process

class DataCenter(object):
    index = 0
    def __init__(self, env, resource_capacity, service_rate=10, has_queue=False, verbose=False):
        self.env = env
        self.verbose = verbose
        self.id = f'data_center_{DataCenter.index}'
        DataCenter.index += 1

        self.service_rate = service_rate
        self.has_queue = has_queue
        self.queue = []
        self.resource_capacity = resource_capacity

        self.ts = []
        self.num_dropped = 0
        self.num_processed = 0
        self.num_queued = 0
        self.num_received = 0

        self.delays = []
        self.processes = []

        self.record_state()

    def get_delays(self):
        return self.delays

    def get_used_capacity(self):
        result = 0
        for p in self.processes:
            result += p.current_request['demand']
        return result

    def get_spare_capacity(self):
        return self.resource_capacity - self.get_used_capacity()

    def record_state(self):
        self.ts.append({
            'time': self.env.now,
            'queued': len(self.queue),
            'in_service': len(self.processes)
        })

    def get_utilization(self):
        if len(self.ts) == 0:
            return 0
        time_idle = 0
        for idx in range(1, len(self.ts)):
            last_entry = self.ts[idx-1]
            this_entry = self.ts[idx]

            if last_entry['in_service'] == 0 and this_entry['in_service'] == 0:
                time_idle += this_entry['time'] - last_entry['time']

        is_idle = len(self.processes) == 0

        current_idle_time = 0 if not is_idle else self.env.now - self.ts[-1]['time']
        time_idle += current_idle_time
        return 1 -(time_idle / self.env.now)

    def get_average_queue_length(self):
        curr = 0
        if len(self.ts) == 0:
            return 0
        time_idle = 0
        for idx in range(1, len(self.ts)):
            last_entry = self.ts[idx-1]
            this_entry = self.ts[idx]

            last_entry_v = last_entry['queued']

            curr += (this_entry['time'] - last_entry['time']) * last_entry_v

        current_time = self.env.now - self.ts[-1]['time']
        last_entry_v = self.ts[-1]['in_service'] + self.ts[-1]['queued']
        curr += current_time * last_entry_v
        return curr / self.env.now

    def get_average_requests_in_system(self):
        curr = 0
        if len(self.ts) == 0:
            return 0
        time_idle = 0
        for idx in range(1, len(self.ts)):
            last_entry = self.ts[idx-1]
            this_entry = self.ts[idx]

            last_entry_v = last_entry['in_service'] + last_entry['queued']

            curr += (this_entry['time'] - last_entry['time']) * last_entry_v

        current_time = self.env.now - self.ts[-1]['time']
        last_entry_v = self.ts[-1]['in_service'] + self.ts[-1]['queued']
        curr += current_time * last_entry_v
        return curr / self.env.now

    def on_complete(self, process):
        self.processes = [p for p in self.processes if p.id != process.id]
        self.delays += process.delays

        if len(self.queue) == 0:
            return

        current_request = self.queue[0]
        while self.get_spare_capacity() >= current_request['demand'] and len(self.queue) > 0:
            p = Process(self.env, self, self.service_rate, self.verbose)
            p.on_receive(current_request)
            self.processes.append(p)
            self.num_processed += 1
            self.queue.pop(0)
            if len(self.queue) == 0:
                return
            current_request = self.queue[0]
            
    def on_receive(self, request):
        self.record_state()
        self.num_received += 1

        if request['demand'] > self.resource_capacity:
            self.num_dropped += 1
            return

        spare_capacity = self.resource_capacity - self.get_used_capacity()
        if spare_capacity >= request['demand']:
            p = Process(self.env, self, self.service_rate, self.verbose)
            p.on_receive(request)
            self.processes.append(p)
            self.num_processed += 1
            self.record_state()
            return

        if self.has_queue:
            self.queue.append(request)
            self.num_queued += 1
            self.record_state()
            return

        self.num_dropped += 1



