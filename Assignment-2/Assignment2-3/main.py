# -*- generated by 1.0.12 -*-
import da
PatternExpr_234 = da.pat.TuplePattern([da.pat.ConstantPattern('request'), da.pat.FreePattern('c2'), da.pat.FreePattern('p')])
PatternExpr_325 = da.pat.TuplePattern([da.pat.ConstantPattern('ack'), da.pat.FreePattern('c2'), da.pat.BoundPattern('_BoundPattern329_')])
PatternExpr_411 = da.pat.TuplePattern([da.pat.ConstantPattern('release'), da.pat.FreePattern('c'), da.pat.FreePattern('p')])
PatternExpr_507 = da.pat.TuplePattern([da.pat.ConstantPattern('request'), da.pat.FreePattern('c2'), da.pat.FreePattern('p')])
PatternExpr_532 = da.pat.TuplePattern([da.pat.ConstantPattern('release'), da.pat.BoundPattern('_BoundPattern535_'), da.pat.BoundPattern('_BoundPattern536_')])
PatternExpr_566 = da.pat.TuplePattern([da.pat.ConstantPattern('ack'), da.pat.BoundPattern('_BoundPattern569_'), da.pat.BoundPattern('_BoundPattern570_')])
PatternExpr_599 = da.pat.TuplePattern([da.pat.ConstantPattern('request'), da.pat.FreePattern('c'), da.pat.FreePattern('p')])
PatternExpr_539 = da.pat.TuplePattern([da.pat.FreePattern(None), da.pat.TuplePattern([da.pat.FreePattern(None), da.pat.FreePattern(None), da.pat.FreePattern(None)]), da.pat.TuplePattern([da.pat.ConstantPattern('release'), da.pat.BoundPattern('_BoundPattern549_'), da.pat.BoundPattern('_BoundPattern550_')])])
PatternExpr_573 = da.pat.TuplePattern([da.pat.FreePattern(None), da.pat.TuplePattern([da.pat.FreePattern(None), da.pat.FreePattern(None), da.pat.FreePattern(None)]), da.pat.TuplePattern([da.pat.ConstantPattern('ack'), da.pat.BoundPattern('_BoundPattern583_'), da.pat.BoundPattern('_BoundPattern584_')])])
PatternExpr_791 = da.pat.TuplePattern([da.pat.ConstantPattern('done'), da.pat.BoundPattern('_BoundPattern794_')])
PatternExpr_797 = da.pat.TuplePattern([da.pat.FreePattern(None), da.pat.TuplePattern([da.pat.FreePattern(None), da.pat.FreePattern(None), da.pat.FreePattern(None)]), da.pat.TuplePattern([da.pat.ConstantPattern('done'), da.pat.BoundPattern('_BoundPattern807_')])])
_config_object = {}
import sys
from random import randint
controller = da.import_da('controller')

@controller.rugroup('My Implementation')
class PMine(controller.Controllee, da.DistProcess):

    def __init__(self, procimpl, props):
        super().__init__(procimpl, props)
        self._PMineReceivedEvent_1 = []
        self._events.extend([da.pat.EventPattern(da.pat.ReceivedEvent, '_PMineReceivedEvent_0', PatternExpr_234, sources=None, destinations=None, timestamps=None, record_history=None, handlers=[self._PMine_handler_233]), da.pat.EventPattern(da.pat.ReceivedEvent, '_PMineReceivedEvent_1', PatternExpr_325, sources=None, destinations=None, timestamps=None, record_history=True, handlers=[]), da.pat.EventPattern(da.pat.ReceivedEvent, '_PMineReceivedEvent_2', PatternExpr_411, sources=None, destinations=None, timestamps=None, record_history=None, handlers=[self._PMine_handler_410])])

    def setup(self, ctl, s, nrequests, **rest_813):
        super().setup(ctl=ctl, s=s, nrequests=nrequests, **rest_813)
        self._state.ctl = ctl
        self._state.s = s
        self._state.nrequests = nrequests
        super().setup(self._state.ctl)
        self._state.q = set()
        self._state.timedOut = 0
        self._state.minimumTimeStamp = 100

    @controller.run
    def run(self):
        for i in range(self._state.nrequests):
            self.request()
            self.cs()
            self.release()

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
        super()._label('_st_label_290', block=False)
        p = c2 = None

        def UniversalOpExpr_292():
            nonlocal p, c2
            for (_ConstantPattern296_, c2, p) in self._state.q:
                if (_ConstantPattern296_ == 'request'):
                    if (not (((c2, p) == (c, self._id)) or ((c, self._id) < (c2, p)))):
                        return False
            return True
        p = c2 = None

        def UniversalOpExpr_318():
            nonlocal p, c2
            for p in self._state.s:

                def ExistentialOpExpr_323(p):
                    nonlocal c2
                    for (_, _, (_ConstantPattern340_, c2, _BoundPattern343_)) in self._PMineReceivedEvent_1:
                        if (_ConstantPattern340_ == 'ack'):
                            if (_BoundPattern343_ == p):
                                if (c2 > c):
                                    return True
                    return False
                if (not ExistentialOpExpr_323(p=p)):
                    return False
            return True
        _st_label_290 = 0
        self._timer_start()
        while (_st_label_290 == 0):
            _st_label_290 += 1
            if (UniversalOpExpr_292() and UniversalOpExpr_318()):
                self.output(((('In CS of process: ' + str(self._id)) + ' with timestamp : ') + str(c)))
                _st_label_290 += 1
            elif self._timer_expired:
                self._state.timedOut = (self._state.timedOut + 1)
                self.output(('Timed out for process: ' + str(self._id)))
                _st_label_290 += 1
            else:
                super()._label('_st_label_290', block=True, timeout=15)
                _st_label_290 -= 1

    def release(self):
        super()._label('release', block=False)
        for (tag, c, p) in self._state.q:
            if ((tag == 'request') and (p == self._id)):
                self._state.q.remove(('request', c, self._id))
                self.send(('release', self.logical_clock(), self._id), to=self._state.s)
                break

    def _PMine_handler_233(self, c2, p):
        super()._label('receive', block=False)
        self._state.q.add(('request', c2, p))
        self.send(('ack', self.logical_clock(), self._id), to=p)
    _PMine_handler_233._labels = None
    _PMine_handler_233._notlabels = None

    def _PMine_handler_410(self, c, p):
        for x in {('request', c, p) for (_ConstantPattern428_, c, _BoundPattern430_) in self._state.q if (_ConstantPattern428_ == 'request') if (_BoundPattern430_ == p)}:
            self._state.q.remove(x)
            break
    _PMine_handler_410._labels = None
    _PMine_handler_410._notlabels = None

@controller.rugroup('Orig.da')
class POrig(controller.Controllee, da.DistProcess):

    def __init__(self, procimpl, props):
        super().__init__(procimpl, props)
        self._POrigReceivedEvent_0 = []
        self._POrigReceivedEvent_1 = []
        self._POrigReceivedEvent_2 = []
        self._events.extend([da.pat.EventPattern(da.pat.ReceivedEvent, '_POrigReceivedEvent_0', PatternExpr_507, sources=None, destinations=None, timestamps=None, record_history=True, handlers=[]), da.pat.EventPattern(da.pat.ReceivedEvent, '_POrigReceivedEvent_1', PatternExpr_532, sources=None, destinations=None, timestamps=None, record_history=True, handlers=[]), da.pat.EventPattern(da.pat.ReceivedEvent, '_POrigReceivedEvent_2', PatternExpr_566, sources=None, destinations=None, timestamps=None, record_history=True, handlers=[]), da.pat.EventPattern(da.pat.ReceivedEvent, '_POrigReceivedEvent_3', PatternExpr_599, sources=None, destinations=None, timestamps=None, record_history=None, handlers=[self._POrig_handler_598])])

    def setup(self, ctl, s, nrequests, **rest_813):
        super().setup(ctl=ctl, s=s, nrequests=nrequests, **rest_813)
        self._state.ctl = ctl
        self._state.s = s
        self._state.nrequests = nrequests
        super().setup(self._state.ctl)

    @controller.run
    def run(self):

        def task():
            self.output('in cs')
        for i in range(self._state.nrequests):
            self.mutex(task)

    def mutex(self, task):
        super()._label('request', block=False)
        c = self.logical_clock()
        self.send(('request', c, self._id), to=self._state.s)
        super()._label('_st_label_503', block=False)
        p = c2 = None

        def UniversalOpExpr_505():
            nonlocal p, c2
            for (_, _, (_ConstantPattern524_, c2, p)) in self._POrigReceivedEvent_0:
                if (_ConstantPattern524_ == 'request'):
                    if (not (PatternExpr_539.match_iter(self._POrigReceivedEvent_1, _BoundPattern549_=c2, _BoundPattern550_=p, SELF_ID=self._id) or ((c, self._id) < (c2, p)))):
                        return False
            return True
        p = None

        def UniversalOpExpr_559():
            nonlocal p
            for p in self._state.s:
                if (not PatternExpr_573.match_iter(self._POrigReceivedEvent_2, _BoundPattern583_=c, _BoundPattern584_=p, SELF_ID=self._id)):
                    return False
            return True
        _st_label_503 = 0
        while (_st_label_503 == 0):
            _st_label_503 += 1
            if (UniversalOpExpr_505() and UniversalOpExpr_559()):
                _st_label_503 += 1
            else:
                super()._label('_st_label_503', block=True)
                _st_label_503 -= 1
        super()._label('critical_section', block=False)
        task()
        super()._label('release', block=False)
        self.send(('release', c, self._id), to=self._state.s)

    def _POrig_handler_598(self, c, p):
        self.send(('ack', c, self._id), to=p)
    _POrig_handler_598._labels = None
    _POrig_handler_598._notlabels = None

class Node_(da.NodeProcess):

    def __init__(self, procimpl, props):
        super().__init__(procimpl, props)
        self._Node_ReceivedEvent_0 = []
        self._events.extend([da.pat.EventPattern(da.pat.ReceivedEvent, '_Node_ReceivedEvent_0', PatternExpr_791, sources=None, destinations=None, timestamps=None, record_history=True, handlers=[])])
    _config_object = {'channel': 'fifo', 'clock': 'Lamport'}

    def run(self):
        nprocs = (int(sys.argv[1]) if (len(sys.argv) > 1) else 10)
        nrequests = (int(sys.argv[2]) if (len(sys.argv) > 2) else 10)
        nruns = (int(sys.argv[3]) if (len(sys.argv) > 3) else 10)
        nparamvalues = (int(sys.argv[4]) if (len(sys.argv) > 4) else 10)
        nreps = (int(sys.argv[5]) if (len(sys.argv) > 5) else 10)
        ctl = self.new(controller.Controller, num=1)
        for i in range(nruns):
            numOfProcesses = randint(1, nprocs)
            numOfRequests = randint(1, nrequests)
            self._setup(ctl, (numOfProcesses,))
            self._start(ctl)
            psPMine = self.new(PMine, num=numOfProcesses)
            for p in psPMine:
                self._setup(p, (ctl, (psPMine - {p}), numOfRequests))
            self._start(psPMine)
            super()._label('_st_label_783', block=False)
            p = None

            def UniversalOpExpr_784():
                nonlocal p
                for p in psPMine:
                    if (not PatternExpr_797.match_iter(self._Node_ReceivedEvent_0, _BoundPattern807_=p)):
                        return False
                return True
            _st_label_783 = 0
            while (_st_label_783 == 0):
                _st_label_783 += 1
                if UniversalOpExpr_784():
                    _st_label_783 += 1
                else:
                    super()._label('_st_label_783', block=True)
                    _st_label_783 -= 1
            else:
                if (_st_label_783 != 2):
                    continue
            if (_st_label_783 != 2):
                break
            self.send(('done',), to=psPMine)