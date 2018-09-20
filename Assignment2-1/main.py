# -*- generated by 1.0.12 -*-
import da
PatternExpr_224 = da.pat.TuplePattern([da.pat.ConstantPattern('request'), da.pat.FreePattern('c2'), da.pat.FreePattern('p')])
PatternExpr_310 = da.pat.TuplePattern([da.pat.ConstantPattern('ack'), da.pat.FreePattern('c2'), da.pat.BoundPattern('_BoundPattern314_')])
PatternExpr_384 = da.pat.TuplePattern([da.pat.ConstantPattern('release'), da.pat.FreePattern(None), da.pat.FreePattern('p')])
PatternExpr_454 = da.pat.TuplePattern([da.pat.ConstantPattern('done')])
PatternExpr_459 = da.pat.BoundPattern('_BoundPattern461_')
PatternExpr_462 = da.pat.TuplePattern([da.pat.FreePattern(None), da.pat.TuplePattern([da.pat.FreePattern(None), da.pat.FreePattern(None), da.pat.BoundPattern('_BoundPattern468_')]), da.pat.TuplePattern([da.pat.ConstantPattern('done')])])
PatternExpr_544 = da.pat.TuplePattern([da.pat.ConstantPattern('done'), da.pat.BoundPattern('_BoundPattern547_')])
PatternExpr_550 = da.pat.TuplePattern([da.pat.FreePattern(None), da.pat.TuplePattern([da.pat.FreePattern(None), da.pat.FreePattern(None), da.pat.FreePattern(None)]), da.pat.TuplePattern([da.pat.ConstantPattern('done'), da.pat.BoundPattern('_BoundPattern560_')])])
_config_object = {'channnel': 'fifo', 'clock': 'lamport'}
import sys

class P(da.DistProcess):

    def __init__(self, procimpl, props):
        super().__init__(procimpl, props)
        self._PReceivedEvent_1 = []
        self._PReceivedEvent_3 = []
        self._events.extend([da.pat.EventPattern(da.pat.ReceivedEvent, '_PReceivedEvent_0', PatternExpr_224, sources=None, destinations=None, timestamps=None, record_history=None, handlers=[self._P_handler_223]), da.pat.EventPattern(da.pat.ReceivedEvent, '_PReceivedEvent_1', PatternExpr_310, sources=None, destinations=None, timestamps=None, record_history=True, handlers=[]), da.pat.EventPattern(da.pat.ReceivedEvent, '_PReceivedEvent_2', PatternExpr_384, sources=None, destinations=None, timestamps=None, record_history=None, handlers=[self._P_handler_383]), da.pat.EventPattern(da.pat.ReceivedEvent, '_PReceivedEvent_3', PatternExpr_454, sources=[PatternExpr_459], destinations=None, timestamps=None, record_history=True, handlers=[])])

    def setup(self, s, nrequests, **rest_566):
        super().setup(s=s, nrequests=nrequests, **rest_566)
        self._state.s = s
        self._state.nrequests = nrequests
        self._state.q = set()

    def run(self):
        for i in range(self._state.nrequests):
            super()._label('request', block=False)
            c = self.logical_clock()
            self.request(c)
        self.send(('done', self._id), to=self.parent())
        super()._label('_st_label_451', block=False)
        _st_label_451 = 0
        while (_st_label_451 == 0):
            _st_label_451 += 1
            if PatternExpr_462.match_iter(self._PReceivedEvent_3, _BoundPattern468_=self.parent(), SELF_ID=self._id):
                _st_label_451 += 1
            else:
                super()._label('_st_label_451', block=True)
                _st_label_451 -= 1
        self.output('terminating')

    def request(self, c):
        self.output(((('Request resource message sent from:' + str(self._id)) + ' with timestamp: ') + str(c)))
        self.send(('request', c, self._id), to=self._state.s)
        self._state.q.add(('request', c, self._id))
        self.output(((('Queue of process: ' + str(self._id)) + ' is: ') + str(self._state.q)))

    def cs(self, c):
        super()._label('cs', block=False)
        p = c2 = None

        def UniversalOpExpr_277():
            nonlocal p, c2
            for (_ConstantPattern281_, c2, p) in self._state.q:
                if (_ConstantPattern281_ == 'request'):
                    if (not (((c2, p) == (c, self._id)) or ((c, self._id) < (c2, p)))):
                        return False
            return True
        p = c2 = None

        def UniversalOpExpr_303():
            nonlocal p, c2
            for p in self._state.s:

                def ExistentialOpExpr_308(p):
                    nonlocal c2
                    for (_, _, (_ConstantPattern325_, c2, _BoundPattern328_)) in self._PReceivedEvent_1:
                        if (_ConstantPattern325_ == 'ack'):
                            if (_BoundPattern328_ == p):
                                if (c2 > c):
                                    return True
                    return False
                if (not ExistentialOpExpr_308(p=p)):
                    return False
            return True
        _st_label_275 = 0
        while (_st_label_275 == 0):
            _st_label_275 += 1
            if (UniversalOpExpr_277() and UniversalOpExpr_303()):
                _st_label_275 += 1
            else:
                super()._label('cs', block=True)
                _st_label_275 -= 1
        self.output(('In CS of process' + str(self._id)))

    def release(self, c):
        super()._label('release', block=False)
        self.output(((('Releasing resource :' + str(self._id)) + ' which had timestamp: ') + str(c)))
        self._state.q.remove(('request', c, self._id))
        self.output(((('Queue of process: ' + str(self._id)) + ' is: ') + str(self._state.q)))
        self.send(('release', self.logical_clock(), self._id), to=self._state.s)

    def _P_handler_223(self, c2, p):
        super()._label('receive', block=False)
        self.output(((('Request resource message received at:' + str(p)) + ' which had timestamp: ') + str(c2)))
        self._state.q.add(('request', c2, p))
        self.output(((('Queue of process: ' + str(p)) + ' is: ') + str(self._state.q)))
        self.send(('ack', self.logical_clock(), self._id), to=p)
    _P_handler_223._labels = None
    _P_handler_223._notlabels = None

    def _P_handler_383(self, p):
        for x in {('request', c, p) for (_ConstantPattern400_, c, _BoundPattern403_) in self._state.q if (_ConstantPattern400_ == 'request') if (_BoundPattern403_ == p)}:
            self._state.q.remove(x)
            self.output(((('Queue of process: ' + str(p)) + ' is: ') + str(self._state.q)))
            break
    _P_handler_383._labels = None
    _P_handler_383._notlabels = None

class Node_(da.NodeProcess):

    def __init__(self, procimpl, props):
        super().__init__(procimpl, props)
        self._Node_ReceivedEvent_0 = []
        self._events.extend([da.pat.EventPattern(da.pat.ReceivedEvent, '_Node_ReceivedEvent_0', PatternExpr_544, sources=None, destinations=None, timestamps=None, record_history=True, handlers=[])])

    def run(self):
        nprocs = (int(sys.argv[1]) if (len(sys.argv) > 1) else 10)
        nrequests = (int(sys.argv[2]) if (len(sys.argv) > 2) else 10)
        ps = self.new(P, num=nprocs)
        for p in ps:
            self._setup(p, ((ps - {p}), nrequests))
        self._start(ps)
        super()._label('_st_label_536', block=False)
        p = None

        def UniversalOpExpr_537():
            nonlocal p
            for p in ps:
                if (not PatternExpr_550.match_iter(self._Node_ReceivedEvent_0, _BoundPattern560_=p)):
                    return False
            return True
        _st_label_536 = 0
        while (_st_label_536 == 0):
            _st_label_536 += 1
            if UniversalOpExpr_537():
                _st_label_536 += 1
            else:
                super()._label('_st_label_536', block=True)
                _st_label_536 -= 1
        self.send(('done',), to=ps)
