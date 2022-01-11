import random
from Server import Server

class DataCenter(object):
    index = 0
    def __init__(self, env, num_servers = 1, service_rate= 10, queue_size=100, verbose=False):
        self.env = env
        self.verbose = verbose
        self.id = f'data_center_{DataCenter.index}'
        DataCenter.index += 1

        self.queue = []
        self.queue_size = queue_size

        self.ts = []
        self.num_dropped = 0
        self.num_processed = 0
        self.num_received = 0

        self.delays = []
        self.servers = []

        for i in range(num_servers):
            s = Server(env, self, service_rate, verbose)
            self.servers.append(s)

        self.record_state()

    def get_delays(self):
        delays = []

        for s in self.servers:
            delays += s.delays

        return delays

    def get_queue_size(self):
        result = 0
        for pkt in self.queue:
            result += pkt['size']
        return result

    def has_idle_server(self):
        for s in self.servers:
            if s.is_idle():
                return True
        return False


    def record_state(self):
        in_service = 0
        for s in self.servers:
            if not s.is_idle():
                in_service += 1
        self.ts.append({
            'time': self.env.now,
            'queued': self.get_queue_size(),
            'in_service': in_service
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

        is_idle = True
        for s in self.servers:
            if not s.is_idle():
                is_idle = False

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

    def get_average_packets_in_system(self):
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

    def request_packet(self, server):
        self.record_state()
        if len(self.queue) == 0:
            return None
        pkt = self.queue.pop(0)
        self.num_processed += 1
        self.record_state()
        return pkt

    def on_receive(self, packet):
        self.record_state()
        self.num_received += 1
        # 1) if any server is idle, put packet there
        for s in self.servers:
            if s.is_idle():
                s.on_receive(packet)
                self.num_processed += 1
                self.record_state()
                return

        # 2) if queue is not full, put it there
        current_queue_size = self.get_queue_size()
        if current_queue_size + packet['size'] <= self.queue_size:
            self.queue.append(packet)
            self.record_state()
            return

        # 3) else drop it
        self.num_dropped += 1



