# -*- generated by 1.0.12 -*-
import da
PatternExpr_424 = da.pat.TuplePattern([da.pat.ConstantPattern('CTL_Ready')])
PatternExpr_429 = da.pat.FreePattern('source')
PatternExpr_451 = da.pat.TuplePattern([da.pat.ConstantPattern('CTL_Done'), da.pat.FreePattern('rudata'), da.pat.FreePattern('rugroup_id')])
PatternExpr_460 = da.pat.FreePattern('source')
PatternExpr_692 = da.pat.TuplePattern([da.pat.ConstantPattern('CTL_Start')])
PatternExpr_747 = da.pat.TuplePattern([da.pat.ConstantPattern('CTL_Terminate')])
PatternExpr_769 = da.pat.TuplePattern([da.pat.ConstantPattern('CTL_Stop')])
PatternExpr_697 = da.pat.TuplePattern([da.pat.FreePattern(None), da.pat.TuplePattern([da.pat.FreePattern(None), da.pat.FreePattern(None), da.pat.FreePattern(None)]), da.pat.TuplePattern([da.pat.ConstantPattern('CTL_Start')])])
PatternExpr_752 = da.pat.TuplePattern([da.pat.FreePattern(None), da.pat.TuplePattern([da.pat.FreePattern(None), da.pat.FreePattern(None), da.pat.FreePattern(None)]), da.pat.TuplePattern([da.pat.ConstantPattern('CTL_Terminate')])])
_config_object = {}
import sys
import time
import json
from itertools import chain

class WinResourceUsageData():
    'Tracks process time only.'

    def start(self):
        self.start_cputime = time.process_time()

    def end(self):
        self.end_cputime = time.process_time()
        self.results = {'Total_process_time': (self.end_cputime - self.start_cputime)}

    @classmethod
    def aggregate(cls, rudata_points):
        return {'Total_process_time': sum((p.results['Total_process_time'] for p in rudata_points)), 'Total_processes': len(rudata_points)}

class PosixResourceUsageData():
    'Tracks utime, stime, and maxrss.'

    def start(self):
        self.start_data = resource.getrusage(resource.RUSAGE_SELF)

    def end(self):
        self.end_data = resource.getrusage(resource.RUSAGE_SELF)

        def diff(attr):
            return (getattr(self.end_data, attr) - getattr(self.start_data, attr))
        self.results = {'Total_user_time': diff('ru_utime'), 'Total_system_time': diff('ru_stime'), 'Total_process_time': (diff('ru_utime') + diff('ru_stime')), 'Total_memory': self.end_data.ru_maxrss}

    @classmethod
    def aggregate(cls, rudata_points):

        def sumof(attr):
            return sum((p.results[attr] for p in rudata_points))
        aggr_results = {k: sumof(k) for k in ['Total_user_time', 'Total_system_time', 'Total_process_time', 'Total_memory']}
        aggr_results['Total_processes'] = len(rudata_points)
        return aggr_results
if (sys.platform == 'win32'):
    ResourceUsageData = WinResourceUsageData
else:
    import resource
    ResourceUsageData = PosixResourceUsageData

class Controller(da.DistProcess):

    def __init__(self, procimpl, props):
        super().__init__(procimpl, props)
        self._events.extend([da.pat.EventPattern(da.pat.ReceivedEvent, '_ControllerReceivedEvent_0', PatternExpr_424, sources=[PatternExpr_429], destinations=None, timestamps=None, record_history=None, handlers=[self._Controller_handler_423]), da.pat.EventPattern(da.pat.ReceivedEvent, '_ControllerReceivedEvent_1', PatternExpr_451, sources=[PatternExpr_460], destinations=None, timestamps=None, record_history=None, handlers=[self._Controller_handler_450])])

    def setup(self, nprocs, threshold=None, **rest_834):
        super().setup(nprocs=nprocs, threshold=threshold, **rest_834)
        self._state.nprocs = nprocs
        self._state.threshold = threshold
        if (self._state.threshold is None):
            self._state.threshold = self._state.nprocs
        self._state.ps = set()
        self._state.done_ps = set()
        self._state.readys = 0
        self._state.dones = 0
        self._state.sent_stop = False
        self._state.rudata_points = {}
        self._state.ctl_verbose = True

    def run(self):
        super()._label('_st_label_534', block=False)
        _st_label_534 = 0
        while (_st_label_534 == 0):
            _st_label_534 += 1
            if (self._state.readys == self._state.nprocs):
                _st_label_534 += 1
            else:
                super()._label('_st_label_534', block=True)
                _st_label_534 -= 1
        self.verboutput('Controller starting everyone')
        t1 = time.perf_counter()
        self.send(('CTL_Start',), to=self._state.ps)
        super()._label('_st_label_554', block=False)
        _st_label_554 = 0
        while (_st_label_554 == 0):
            _st_label_554 += 1
            if (self._state.dones == self._state.nprocs):
                _st_label_554 += 1
            else:
                super()._label('_st_label_554', block=True)
                _st_label_554 -= 1
        t2 = time.perf_counter()
        self.verboutput('Everyone done')
        self.send(('CTL_Terminate',), to=self._state.ps)
        jsondata = {}
        for (rugroup_id, points) in self._state.rudata_points.items():
            if (rugroup_id is None):
                continue
            jsondata[rugroup_id] = ResourceUsageData.aggregate(points)
        allpoints = list(chain(*self._state.rudata_points.values()))
        jsondata['All'] = ResourceUsageData.aggregate(allpoints)
        jsondata['Wallclock_time'] = (t2 - t1)
        jsonoutput = json.dumps(jsondata)
        print(('###OUTPUT: ' + jsonoutput))
        time.sleep(1)

    def verboutput(self, s):
        if self._state.ctl_verbose:
            self.output(s)

    def _Controller_handler_423(self, source):
        self._state.ps.add(source)
        self._state.readys += 1
        self.verboutput('Got Ready from {} ({}/{})'.format(source, self._state.readys, self._state.nprocs))
    _Controller_handler_423._labels = None
    _Controller_handler_423._notlabels = None

    def _Controller_handler_450(self, rudata, rugroup_id, source):
        self._state.dones += 1
        self._state.done_ps.add(source)
        self._state.rudata_points.setdefault(rugroup_id, []).append(rudata)
        if (self._state.threshold == self._state.nprocs):
            self.verboutput('Got Done from {} ({}/{})'.format(source, self._state.dones, self._state.nprocs))
        else:
            self.verboutput('Got Done from {} ({}/{}, need {} to stop)'.format(source, self._state.dones, self._state.nprocs, self._state.threshold))
        if ((self._state.dones >= self._state.threshold) and (not self._state.sent_stop)):
            rest_ps = (self._state.ps - self._state.done_ps)
            self.verboutput('Controller stopping everyone')
            self.send(('CTL_Stop',), to=rest_ps)
            self._state.sent_stop = True
    _Controller_handler_450._labels = None
    _Controller_handler_450._notlabels = None

class Controllee(da.DistProcess):

    def __init__(self, procimpl, props):
        super().__init__(procimpl, props)
        self._ControlleeReceivedEvent_0 = []
        self._ControlleeReceivedEvent_1 = []
        self._events.extend([da.pat.EventPattern(da.pat.ReceivedEvent, '_ControlleeReceivedEvent_0', PatternExpr_692, sources=None, destinations=None, timestamps=None, record_history=True, handlers=[]), da.pat.EventPattern(da.pat.ReceivedEvent, '_ControlleeReceivedEvent_1', PatternExpr_747, sources=None, destinations=None, timestamps=None, record_history=True, handlers=[]), da.pat.EventPattern(da.pat.ReceivedEvent, '_ControlleeReceivedEvent_2', PatternExpr_769, sources=None, destinations=None, timestamps=None, record_history=None, handlers=[self._Controllee_handler_768])])

    def setup(self, ctl, **rest_834):
        super().setup(ctl=ctl, **rest_834)
        self._state.ctl = ctl
        self._state.rudata = ResourceUsageData()
        self._state.ctl_verbose = True
        self._state.ctl_done = False

    def run(self):
        pass

    def verboutput(self, s):
        if self._state.ctl_verbose:
            self.output(s)

    def ctl_begin(self):
        self.send(('CTL_Ready',), to=self._state.ctl)
        super()._label('_st_label_689', block=False)
        _st_label_689 = 0
        while (_st_label_689 == 0):
            _st_label_689 += 1
            if PatternExpr_697.match_iter(self._ControlleeReceivedEvent_0, SELF_ID=self._id):
                _st_label_689 += 1
            else:
                super()._label('_st_label_689', block=True)
                _st_label_689 -= 1
        self._state.rudata.start()

    def ctl_end(self):
        self._state.ctl_done = True
        self._state.rudata.end()
        rugroup_id = getattr(self._id, 'ctl_rugroup_id', None)
        self.send(('CTL_Done', self._state.rudata, rugroup_id), to=self._state.ctl)
        super()._label('_st_label_744', block=False)
        _st_label_744 = 0
        while (_st_label_744 == 0):
            _st_label_744 += 1
            if PatternExpr_752.match_iter(self._ControlleeReceivedEvent_1, SELF_ID=self._id):
                _st_label_744 += 1
            else:
                super()._label('_st_label_744', block=True)
                _st_label_744 -= 1
        self.verboutput('Terminating...')

    def _Controllee_handler_768(self):
        self.verboutput('Received stop')
        if self._state.ctl_done:
            return
        self.ctl_end()
        self.exit()
    _Controllee_handler_768._labels = None
    _Controllee_handler_768._notlabels = None

def run(func):
    'Decorator for Process.run() to call controllee hooks.'

    def ctl_run(self):
        self.ctl_begin()
        func(self)
        self.ctl_end()
    return ctl_run

def rugroup(rugroup_id):
    'Decorator for annotating a process controllee subclass\n    with a resource usage group identifier. Results for processes\n    in the same group will be aggregated reported together.\n    '

    def f(proc):
        proc.ctl_rugroup_id = rugroup_id
        return proc
    return f
