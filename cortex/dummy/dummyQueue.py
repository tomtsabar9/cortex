class DummyQueue:

    def __init__(self):
        pass

    def publish(self, *args, **kwrags):
        self.ex_name = kwrags['ex_name']
        self.q_name = kwrags['q_name']
        self.msg = kwrags['msg']