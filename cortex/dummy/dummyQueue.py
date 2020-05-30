class DummyQueue:

    def __init__(self):
        self.queues = dict()

    def publish(self, *args, **kwrags):
        self.ex_name = kwrags['ex_name']
        self.queues[kwrags['q_name']] = kwrags['msg']
