class Constraint(object):
    """
    A :class:`Constraint` encodes either an equality or an inequality between two :class:`Expression` objects.

    A :class:`Constraint` must be understood either as
    `self.expression` = 0 or `self.expression` :math:`\\leqslant` 0
    depending on the value of `self.equality_or_inequality`.

    Attributes:
        expression (Expression): The :class:`Expression` that is compared to 0.
        equality_or_inequality (str): "equality" or "inequality". Encodes the type of constraint.
        dual_variable_value (float): the associated dual variable at optimal point of the solved PEP.
                                     Set to None before evaluation via the :class:`PEP` solving method PEP.solve.
        counter (int): counts the :class:`Constraint` objects.

    A :class:`Constraint` results from a comparison between two :class:`Expression` objects.

    Example:
        >>> from PEPit import Expression
        >>> expr1 = Expression()
        >>> expr2 = Expression()
        >>> inequality1 = expr1 <= expr2
        >>> inequality2 = expr1 >= expr2
        >>> equality = expr1 == expr2

    """
    # Class counter.
    # It counts the number of generated constraints
    counter = 0

    def __init__(self, expression, equality_or_inequality):
        """
        :class:`Constraint` objects can also be instantiated via the following arguments.

        Args:
            expression (Expression): an object of class Expression
            equality_or_inequality (str): either 'equality' or 'inequality'.

        Instantiating the :class:`Constraint` objects of the first example can be done by

        Example:
            >>> from PEPit import Expression
            >>> expr1 = Expression()
            >>> expr2 = Expression()
            >>> inequality1 = Constraint(expression=expr1-expr2, equality_or_inequality="inequality")
            >>> inequality2 = Constraint(expression=expr2-expr1, equality_or_inequality="inequality")
            >>> equality = Constraint(expression=expr1-expr2, equality_or_inequality="equality")

        Raises:
            AssertionError: if provided `equality_or_inequality` argument is neither "equality" nor "inequality".

        """

        # Update the counter
        self.counter = Constraint.counter
        Constraint.counter += 1

        # Store the underlying expression
        self.expression = expression

        # Verify that 'equality_or_inequality' is well defined and store its value
        assert equality_or_inequality in {'equality', 'inequality'}
        self.equality_or_inequality = equality_or_inequality

        # After solving the PEP, one can find the value of the underlying expression in self.expression.value.
        # Moreover, the associated dual variable value must be stored in self.dual_variable_value.
        self.dual_variable_value = None
