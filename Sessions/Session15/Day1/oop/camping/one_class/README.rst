======================
Camping Budget Example
======================

Class ``camping.Budget`` represents the budget for a camping trip
in which the people who pitched in more than average need to be
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
    Charlie paid $  0.00, balance: $ -25.00
        Ann paid $ 10.00, balance: $ -15.00
     Debbie paid $ 40.00, balance: $  15.00
        Bob paid $ 50.00, balance: $  25.00


The data used by ``report`` is computed by the `balances` method:

    >>> b.balances()
    [(-15.0, 'Ann', 10.0), (25.0, 'Bob', 50.0), (-25.0, 'Charlie', 0.0), (15.0, 'Debbie', 40.0)]


-------------
Running tests
-------------

To run these doctests on **bash** use this command line::

    $ python3 -m doctest README.rst


--------
Exercise
--------

.. tip:: To practice TDD with doctests, this is a good option to run the tests::

    $ python3 -m doctest README.rst -o REPORT_ONLY_FIRST_FAILURE


1. Allow adding contributors later
----------------------------------

As implemented, ``camping.Budget`` does not allow adding contributor names after the budget is created.
Implement a method to allow adding a contributor with an optional contribution.

An alternative to such a method would be to change the ``contribute`` method,
removing the code that tests whether the contributor's name is found in ``_contributions``.
This would be simpler, but is there a drawback to this approach? Discuss.
