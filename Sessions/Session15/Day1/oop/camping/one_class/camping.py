"""
Class ``camping.Budget`` represents the budget for a camping trip.
"""

class Budget:

    def __init__(self, *names):
        self._campers = {name:0.0 for name in names}

    def total(self):
        return sum(self._campers.values())

    def people(self):
        return sorted(self._campers)

    def contribute(self, name, amount):
        if name not in self._campers:
            raise LookupError("Person not in budget")
        self._campers[name] += amount

    def individual_share(self):
        return self.total() / len(self._campers)

    def balances(self):
        share = self.individual_share()
        result = []
        for name in self.people():
            paid = self._campers[name]
            result.append((paid - share, name, paid))
        return result

    def report(self):
        """report displays names and amounts due or owed"""
        heading_tpl = 'Total: $ {:.2f}; individual share: $ {:.2f}'
        print(heading_tpl.format(self.total(), self.individual_share())) 
        print("-"* 42)
        name_len = max(len(name) for name in self._campers)
        for balance, name, paid in sorted(self.balances()):
            print(f"{name:>{name_len}} paid ${paid:6.2f}, balance: $ {balance:6.2f}")
