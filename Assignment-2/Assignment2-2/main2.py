# -*- generated by 1.0.12 -*-
import da
PatternExpr_218 = da.pat.TuplePattern([da.pat.ConstantPattern('request'), da.pat.FreePattern('c2'), da.pat.FreePattern('p')])
PatternExpr_309 = da.pat.TuplePattern([da.pat.ConstantPattern('ack'), da.pat.FreePattern('c2'), da.pat.BoundPattern('_BoundPattern313_')])
PatternExpr_401 = da.pat.TuplePattern([da.pat.ConstantPattern('release'), da.pat.FreePattern('c'), da.pat.FreePattern('p')])
PatternExpr_463 = da.pat.TuplePattern([da.pat.ConstantPattern('done')])
PatternExpr_468 = da.pat.BoundPattern('_BoundPattern470_')
PatternExpr_471 = da.pat.TuplePattern([da.pat.FreePattern(None), da.pat.TuplePattern([da.pat.FreePattern(None), da.pat.FreePattern(None), da.pat.BoundPattern('_BoundPattern477_')]), da.pat.TuplePattern([da.pat.ConstantPattern('done')])])
PatternExpr_570 = da.pat.TuplePattern([da.pat.ConstantPattern('done'), da.pat.BoundPattern('_BoundPattern573_')])
PatternExpr_576 = da.pat.TuplePattern([da.pat.FreePattern(None), da.pat.TuplePattern([da.pat.FreePattern(None), da.pat.FreePattern(None), da.pat.FreePattern(None)]), da.pat.TuplePattern([da.pat.ConstantPattern('done'), da.pat.BoundPattern('_BoundPattern586_')])])
_config_object = {'channnel': 'fifo', 'clock': 'lamport'}
import sys
import time

class P(da.DistProcess):

    def __init__(self, procimpl, props):
        super().__init__(procimpl, props)
        self._PReceivedEvent_1 = []
        self._PReceivedEvent_3 = []
        self._events.extend([da.pat.EventPattern(da.pat.ReceivedEvent, '_PReceivedEvent_0', PatternExpr_218, sources=None, destinations=None, timestamps=None, record_history=None, handlers=[self._P_handler_217]), da.pat.EventPattern(da.pat.ReceivedEvent, '_PReceivedEvent_1', PatternExpr_309, sources=None, destinations=None, timestamps=None, record_history=True, handlers=[]), da.pat.EventPattern(da.pat.ReceivedEvent, '_PReceivedEvent_2', PatternExpr_401, sources=None, destinations=None, timestamps=None, record_history=None, handlers=[self._P_handler_400]), da.pat.EventPattern(da.pat.ReceivedEvent, '_PReceivedEvent_3', PatternExpr_463, sources=[PatternExpr_468], destinations=None, timestamps=None, record_history=True, handlers=[])])

    def setup(self, s, nrequests, **rest_592):
        super().setup(s=s, nrequests=nrequests, **rest_592)
        self._state.s = s
        self._state.nrequests = nrequests
        self._state.q = set()
        self._state.timedOut = 0
        self._state.minimumTimeStamp = 100000

    def run(self):
        for i in range(self._state.nrequests):
            self.request()
            self.cs()
            self.request()
            self.release()
        self.send(('done', self._id), to=self.parent())
        super()._label('_st_label_460', block=False)
        _st_label_460 = 0
        while (_st_label_460 == 0):
            _st_label_460 += 1
            if PatternExpr_471.match_iter(self._PReceivedEvent_3, _BoundPattern477_=self.parent(), SELF_ID=self._id):
                _st_label_460 += 1
            else:
                super()._label('_st_label_460', block=True)
                _st_label_460 -= 1
        self.output(((('Number of requests timed out for process ' + str(self._id)) + ' is :') + str(self._state.timedOut)))

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
        super()._label('_st_label_274', block=False)
        c2 = p = None

        def UniversalOpExpr_276():
            nonlocal c2, p
            for (_ConstantPattern280_, c2, p) in self._state.q:
                if (_ConstantPattern280_ == 'request'):
                    if (not (((c2, p) == (c, self._id)) or ((c, self._id) < (c2, p)))):
                        return False
            return True
        c2 = p = None

        def UniversalOpExpr_302():
            nonlocal c2, p
            for p in self._state.s:

                def ExistentialOpExpr_307(p):
                    nonlocal c2
                    for (_, _, (_ConstantPattern324_, c2, _BoundPattern327_)) in self._PReceivedEvent_1:
                        if (_ConstantPattern324_ == 'ack'):
                            if (_BoundPattern327_ == p):
                                if (c2 > c):
                                    return True
                    return False
                if (not ExistentialOpExpr_307(p=p)):
                    return False
            return True
        _st_label_274 = 0
        self._timer_start()
        while (_st_label_274 == 0):
            _st_label_274 += 1
            if (UniversalOpExpr_276() and UniversalOpExpr_302()):
                self.output(((((('In CS of process: ' + str(self._id)) + ' with timestamp : ') + str(c)) + ' at time:') + str(self.logical_clock())))
                _st_label_274 += 1
            elif self._timer_expired:
                self._state.timedOut = (self._state.timedOut + 1)
                self.output(('Timed out for process: ' + str(self._id)))
                _st_label_274 += 1
            else:
                super()._label('_st_label_274', block=True, timeout=15)
                _st_label_274 -= 1

    def release(self):
        super()._label('release', block=False)
        for (tag, c, p) in self._state.q:
            if ((tag == 'request') and (p == self._id)):
                self._state.q.remove(('request', c, self._id))
                self.send(('release', self.logical_clock(), self._id), to=self._state.s)
                break

    def _P_handler_217(self, c2, p):
        super()._label('receive', block=False)
        self._state.q.add(('request', c2, p))
        self.send(('ack', self.logical_clock(), self._id), to=p)
    _P_handler_217._labels = None
    _P_handler_217._notlabels = None

    def _P_handler_400(self, c, p):
        for x in {('request', c, p) for (_ConstantPattern418_, c, _BoundPattern420_) in self._state.q if (_ConstantPattern418_ == 'request') if (_BoundPattern420_ == p)}:
            self._state.q.remove(x)
            break
    _P_handler_400._labels = None
    _P_handler_400._notlabels = None

class Node_(da.NodeProcess):

    def __init__(self, procimpl, props):
        super().__init__(procimpl, props)
        self._Node_ReceivedEvent_0 = []
        self._events.extend([da.pat.EventPattern(da.pat.ReceivedEvent, '_Node_ReceivedEvent_0', PatternExpr_570, sources=None, destinations=None, timestamps=None, record_history=True, handlers=[])])

    def run(self):
        nprocs = (int(sys.argv[1]) if (len(sys.argv) > 1) else 10)
        nrequests = (int(sys.argv[2]) if (len(sys.argv) > 2) else 10)
        nrequests = int((nrequests / 2))
        ps = self.new(P, num=nprocs)
        for p in ps:
            self._setup(p, ((ps - {p}), nrequests))
        self._start(ps)
        super()._label('_st_label_562', block=False)
        p = None

        def UniversalOpExpr_563():
            nonlocal p
            for p in ps:
                if (not PatternExpr_576.match_iter(self._Node_ReceivedEvent_0, _BoundPattern586_=p)):
                    return False
            return True
        _st_label_562 = 0
        while (_st_label_562 == 0):
            _st_label_562 += 1
            if UniversalOpExpr_563():
                _st_label_562 += 1
            else:
                super()._label('_st_label_562', block=True)
                _st_label_562 -= 1
        self.send(('done',), to=ps)
