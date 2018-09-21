# -*- generated by 1.0.12 -*-
import da
PatternExpr_215 = da.pat.TuplePattern([da.pat.ConstantPattern('request'), da.pat.FreePattern('c2'), da.pat.FreePattern('p')])
PatternExpr_306 = da.pat.TuplePattern([da.pat.ConstantPattern('ack'), da.pat.FreePattern('c2'), da.pat.BoundPattern('_BoundPattern310_')])
PatternExpr_392 = da.pat.TuplePattern([da.pat.ConstantPattern('release'), da.pat.FreePattern('c'), da.pat.FreePattern('p')])
PatternExpr_451 = da.pat.TuplePattern([da.pat.ConstantPattern('done')])
PatternExpr_456 = da.pat.BoundPattern('_BoundPattern458_')
PatternExpr_459 = da.pat.TuplePattern([da.pat.FreePattern(None), da.pat.TuplePattern([da.pat.FreePattern(None), da.pat.FreePattern(None), da.pat.BoundPattern('_BoundPattern465_')]), da.pat.TuplePattern([da.pat.ConstantPattern('done')])])
PatternExpr_553 = da.pat.TuplePattern([da.pat.ConstantPattern('done'), da.pat.BoundPattern('_BoundPattern556_')])
PatternExpr_559 = da.pat.TuplePattern([da.pat.FreePattern(None), da.pat.TuplePattern([da.pat.FreePattern(None), da.pat.FreePattern(None), da.pat.FreePattern(None)]), da.pat.TuplePattern([da.pat.ConstantPattern('done'), da.pat.BoundPattern('_BoundPattern569_')])])
_config_object = {'channnel': 'fifo', 'clock': 'lamport'}
import sys

class P(da.DistProcess):

    def __init__(self, procimpl, props):
        super().__init__(procimpl, props)
        self._PReceivedEvent_1 = []
        self._PReceivedEvent_3 = []
        self._events.extend([da.pat.EventPattern(da.pat.ReceivedEvent, '_PReceivedEvent_0', PatternExpr_215, sources=None, destinations=None, timestamps=None, record_history=None, handlers=[self._P_handler_214]), da.pat.EventPattern(da.pat.ReceivedEvent, '_PReceivedEvent_1', PatternExpr_306, sources=None, destinations=None, timestamps=None, record_history=True, handlers=[]), da.pat.EventPattern(da.pat.ReceivedEvent, '_PReceivedEvent_2', PatternExpr_392, sources=None, destinations=None, timestamps=None, record_history=None, handlers=[self._P_handler_391]), da.pat.EventPattern(da.pat.ReceivedEvent, '_PReceivedEvent_3', PatternExpr_451, sources=[PatternExpr_456], destinations=None, timestamps=None, record_history=True, handlers=[])])

    def setup(self, s, nrequests, **rest_575):
        super().setup(s=s, nrequests=nrequests, **rest_575)
        self._state.s = s
        self._state.nrequests = nrequests
        self._state.q = set()
        self._state.timedOut = 0
        self._state.minimumTimeStamp = 100000

    def run(self):
        for i in range(self._state.nrequests):
            self.request()
            self.cs()
            self.release()
        self.send(('done', self._id), to=self.parent())
        super()._label('_st_label_448', block=False)
        _st_label_448 = 0
        while (_st_label_448 == 0):
            _st_label_448 += 1
            if PatternExpr_459.match_iter(self._PReceivedEvent_3, _BoundPattern465_=self.parent(), SELF_ID=self._id):
                _st_label_448 += 1
            else:
                super()._label('_st_label_448', block=True)
                _st_label_448 -= 1
        self.output(((('Number of requests timed out for process ' + str(self._id)) + ' is :') + str(self._state.timedOut)))
        self.output('terminating')

    def request(self):
        c = self.logical_clock()
        self.send(('request', c, self._id), to=self._state.s)
        self._state.q.add(('request', c, self._id))

    def cs(self):
        super()._label('cs', block=False)
        self._state.minimumTimeStamp = 100000
        for (tag, c, p2) in self._state.q:
            if ((tag == 'request') and (p2 == self._id) and (c < self._state.minimumTimeStamp)):
                self._state.minimumTimeStamp = c
        c = self._state.minimumTimeStamp
        super()._label('_st_label_271', block=False)
        p = c2 = None

        def UniversalOpExpr_273():
            nonlocal p, c2
            for (_ConstantPattern277_, c2, p) in self._state.q:
                if (_ConstantPattern277_ == 'request'):
                    if (not (((c2, p) == (c, self._id)) or ((c, self._id) < (c2, p)))):
                        return False
            return True
        p = c2 = None

        def UniversalOpExpr_299():
            nonlocal p, c2
            for p in self._state.s:

                def ExistentialOpExpr_304(p):
                    nonlocal c2
                    for (_, _, (_ConstantPattern321_, c2, _BoundPattern324_)) in self._PReceivedEvent_1:
                        if (_ConstantPattern321_ == 'ack'):
                            if (_BoundPattern324_ == p):
                                if (c2 > c):
                                    return True
                    return False
                if (not ExistentialOpExpr_304(p=p)):
                    return False
            return True
        _st_label_271 = 0
        self._timer_start()
        while (_st_label_271 == 0):
            _st_label_271 += 1
            if (UniversalOpExpr_273() and UniversalOpExpr_299()):
                self.output(((('In CS of process: ' + str(self._id)) + ' with timestamp : ') + str(c)))
                _st_label_271 += 1
            elif self._timer_expired:
                self._state.timedOut = (self._state.timedOut + 1)
                self.output(('Timed out for process: ' + str(self._id)))
                _st_label_271 += 1
            else:
                super()._label('_st_label_271', block=True, timeout=15)
                _st_label_271 -= 1

    def release(self):
        super()._label('release', block=False)
        for (tag, c, p) in self._state.q:
            if ((tag == 'request') and (p == self._id)):
                self._state.q.remove(('request', c, self._id))
                self.send(('release', self.logical_clock(), self._id), to=self._state.s)
                break

    def _P_handler_214(self, c2, p):
        super()._label('receive', block=False)
        self._state.q.add(('request', c2, p))
        self.send(('ack', self.logical_clock(), self._id), to=p)
    _P_handler_214._labels = None
    _P_handler_214._notlabels = None

    def _P_handler_391(self, c, p):
        for x in {('request', c, p) for (_ConstantPattern409_, c, _BoundPattern411_) in self._state.q if (_ConstantPattern409_ == 'request') if (_BoundPattern411_ == p)}:
            self._state.q.remove(x)
            break
    _P_handler_391._labels = None
    _P_handler_391._notlabels = None

class Node_(da.NodeProcess):

    def __init__(self, procimpl, props):
        super().__init__(procimpl, props)
        self._Node_ReceivedEvent_0 = []
        self._events.extend([da.pat.EventPattern(da.pat.ReceivedEvent, '_Node_ReceivedEvent_0', PatternExpr_553, sources=None, destinations=None, timestamps=None, record_history=True, handlers=[])])

    def run(self):
        nprocs = (int(sys.argv[1]) if (len(sys.argv) > 1) else 10)
        nrequests = (int(sys.argv[2]) if (len(sys.argv) > 2) else 10)
        ps = self.new(P, num=nprocs)
        for p in ps:
            self._setup(p, ((ps - {p}), nrequests))
        self._start(ps)
        super()._label('_st_label_545', block=False)
        p = None

        def UniversalOpExpr_546():
            nonlocal p
            for p in ps:
                if (not PatternExpr_559.match_iter(self._Node_ReceivedEvent_0, _BoundPattern569_=p)):
                    return False
            return True
        _st_label_545 = 0
        while (_st_label_545 == 0):
            _st_label_545 += 1
            if UniversalOpExpr_546():
                _st_label_545 += 1
            else:
                super()._label('_st_label_545', block=True)
                _st_label_545 -= 1
        self.send(('done',), to=ps)
