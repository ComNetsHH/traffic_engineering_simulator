class TrafficScheduler:
    def __init__(self, policy):
        self.policy = policy
        self.destinations = []
        return

    def set_destinations(self, destinations):
        self.destinations = destinations

    def on_receive(self, request):
        decision = self.policy.schedule(request, self.destinations)
        request['to'] = decision

        selection = [d for d in self.destinations if d.id == decision]

        if len(selection) > 0:
            selection[0].on_receive(request)
        else:
            raise ValueError(f'Cannot schedule to {decision}') 
        
