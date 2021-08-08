from pydantic import BaseModel
from typing import Dict, List, Callable, TypedDict


class Observer(TypedDict):
    callback: Callable
    args: List
    kwards: Dict


class ObserverModel(BaseModel):
    _observers: Dict[str, Observer] = {}

    def __setattr__(self, name, value):
        super().__setattr__(name, value)
        if name in self._observers:
            observer = self._observers[name]
            observer["callback"](*observer["args"], **observer["kwargs"])

    def observe(self, name, callback, args=[], kwargs={}):
        self._observers[name] = {
            "callback": callback,
            "args": args,
            "kwargs": kwargs,
        }

    def on_change(self, *names):
        def deco(func):
            for name in names:
                self.observe(name, func)

        return deco
