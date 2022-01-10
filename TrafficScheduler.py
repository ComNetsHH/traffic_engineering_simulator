class TrafficScheduler:
    def __init__(self, policy):
        self.policy = policy
        self.destinations = []
        return

    def set_destinations(self, destinations):
        self.destinations = destinations

    def on_receive(self, packet):
        decision = self.policy.schedule(packet, self.destinations)
        packet['to'] = decision

        selection = [d for d in self.destinations if d.id == decision]

        if len(selection) > 0:
            selection[0].on_receive(packet)
        else:
            raise ValueError(f'Cannot schedule to {decision}') 
        
