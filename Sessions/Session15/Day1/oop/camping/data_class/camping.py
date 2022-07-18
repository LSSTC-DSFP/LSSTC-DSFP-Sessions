from dataclasses import dataclass
from typing import ClassVar
import operator

@dataclass
class Camper:

    name: str
    paid: float = 0.0

    max_name_len: ClassVar[int] = 0
    template = '{name:>{name_len}} paid ${paid:7.2f}'

    def __post_init__(self):
        if len(self.name) > Camper.max_name_len:
            Camper.max_name_len = len(self.name)

    def pay(self, amount):
        self.paid += float(amount)

    def display(self):
        return Camper.template.format(
            name = self.name,
            name_len = self.max_name_len,
            paid = self.paid,
        )

class Budget:
    """
    Class ``camping.Budget`` represents the budget for a camping trip.
    """

    def __init__(self, *names):
        self._campers = {name: Camper(name) for name in names}

    def total(self):
        return sum(c.paid for c in self._campers.values())

    def people(self):
        return sorted(self._campers)

    def contribute(self, name, amount):
        if name not in self._campers:
            raise LookupError("Name not in budget")
        self._campers[name].pay(amount)

    def individual_share(self):
        return self.total() / len(self._campers)

    def report(self):
        """report displays names and amounts due or owed"""
        share = self.individual_share()
        heading_tpl = 'Total: $ {:.2f}; individual share: $ {:.2f}'
        print(heading_tpl.format(self.total(), share))
        print("-"* 42)
        sorted_campers = sorted(self._campers.values(), key=operator.attrgetter('paid'))
        for camper in sorted_campers:
            balance = f'balance: $ {camper.paid - share:7.2f}'
            print(camper.display(), balance, sep=', ')
