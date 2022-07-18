======================
Camping Budget Example
======================

Class ``camping.Camper`` represents a contributor to the budget of a camping trip.

    >>> from camping import Camper
    >>> a = Camper('Anna')
    >>> a.pay(33)
    >>> a.display()
    'Anna paid $  33.00'

A camper can be created with an initial balance:

    >>> c = Camper('Charlie', 9)

The ``.display()`` method right-justifies the names taking into account the
longest name so far, so that multiple calls show aligned columns:

    >>> for camper in [a, c]:
    ...     print(camper.display())
       Anna paid $  33.00
    Charlie paid $   9.00


Class ``camping.Budget`` represents the budget for a camping trip
in which campers who pitched in more than average need to be
reimbursed by the others.

    >>> from camping import Budget
    >>> b = Budget('Debbie', 'Ann', 'Bob', 'Charlie')
    >>> b.total()
    0.0
    >>> b.people()
    ['Ann', 'Bob', 'Charlie', 'Debbie']
    >>> b.contribute("Bob", 50.00)
    >>> b.contribute("Debbie", 40.00)
    >>> b.contribute("Ann", 10.00)
    >>> b.total()
    100.0

The ``report`` method lists who should receive or pay, and the
respective amounts.

    >>> b.report()
    Total: $ 100.00; individual share: $ 25.00
    ------------------------------------------
    Charlie paid $   0.00, balance: $  -25.00
        Ann paid $  10.00, balance: $  -15.00
     Debbie paid $  40.00, balance: $   15.00
        Bob paid $  50.00, balance: $   25.00



-------------
Running tests
-------------

To run these doctests on **bash** use this command line::

    $ python3 -m doctest README.rst


--------
Exercise
--------

.. tip:: To practice TDD with doctests, this is a good option to run the tests::

    $ python3 -m doctest README.rst -f


1. Allow adding contributors later
----------------------------------

As implemented, ``camping.Budget`` does not allow adding contributor names after the budget is created.
Implement a method to allow adding a contributor with an optional contribution.

An alternative to such a method would be to change the ``contribute`` method,
removing the code that tests whether the contributor's name is found in ``self._campers``.
This would be simpler, but is there a drawback to this approach? Discuss.
