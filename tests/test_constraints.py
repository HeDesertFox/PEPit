import unittest

from PEPit.pep import PEP
from PEPit.point import Point
from PEPit.expression import Expression
from PEPit.constraint import Constraint
from PEPit.function import Function

from PEPit.functions.smooth_strongly_convex_function import SmoothStronglyConvexFunction


class TestConstraints(unittest.TestCase):

    def setUp(self):

        # smooth-strongly convex gradient descent set up
        self.L = 1.
        self.mu = 0.1
        self.gamma = 1 / self.L

        # Instantiate PEP
        self.problem = PEP()

        # Declare a strongly convex smooth function
        self.func = self.problem.declare_function(SmoothStronglyConvexFunction, param={'L': self.L, 'mu': self.mu})

        # Start by defining its unique optimal point xs = x_* and corresponding function value fs = f_*
        self.xs = self.func.stationary_point()

        # Then define the starting point x0 of the algorithm
        self.x0 = self.problem.set_initial_point()

        # Set the initial constraint that is the distance between x0 and x^*
        self.problem.set_initial_condition((self.x0 - self.xs) ** 2 <= 1)

        # Run n steps of the GD method
        self.x1 = self.x0 - self.gamma * self.func.gradient(self.x0)

        # Set the performance metric to the function values accuracy
        self.problem.set_performance_metric((self.x1 - self.xs) ** 2)

        self.solution = self.problem.solve(verbose=False)

    def test_is_instance(self):

        self.assertIsInstance(self.func, Function)
        self.assertIsInstance(self.func, SmoothStronglyConvexFunction)
        self.assertIsInstance(self.xs, Point)
        self.assertIsInstance(self.x0, Point)
        self.assertIsInstance(self.x1, Point)
        for i in range(len(self.problem.list_of_conditions)):
            self.assertIsInstance(self.problem.list_of_conditions[i], Constraint)
            self.assertIsInstance(self.problem.list_of_conditions[i].expression, Expression)
        for i in range(len(self.func.list_of_constraints)):
            self.assertIsInstance(self.func.list_of_constraints[i], Constraint)
            self.assertIsInstance(self.func.list_of_constraints[i].expression, Expression)

    def test_counter(self):

        self.assertIs(self.func.counter, 0)
        self.assertIs(self.xs.counter, 0)
        self.assertIs(self.x0.counter, 1)
        self.assertIs(self.x1.counter, None)

        # conditions are first added as Constraint in PEP
        for i in range(len(self.problem.list_of_conditions)):
            self.assertIs(self.problem.list_of_conditions[i].counter, i)

        # class constraints are added after initial conditions in PEP
        for i in range(len(self.func.list_of_constraints)):
            self.assertIs(self.func.list_of_constraints[i].counter, i + len(self.problem.list_of_conditions))

    def test_equality_inequality(self):

        for i in range(len(self.func.list_of_constraints)):
            self.assertIsInstance(self.func.list_of_constraints[i].equality_or_inequality, str)
            self.assertIn(self.func.list_of_constraints[i].equality_or_inequality, {'equality', 'inequality'})

        for i in range(len(self.problem.list_of_conditions)):
            self.assertIsInstance(self.problem.list_of_conditions[i].equality_or_inequality, str)
            self.assertIn(self.problem.list_of_conditions[i].equality_or_inequality, {'equality', 'inequality'})

    def test_dual_variable_value(self):

        for i in range(len(self.func.list_of_constraints)):
            self.assertIsInstance(self.func.list_of_constraints[i].dual_variable_value, float)

        for i in range(len(self.problem.list_of_conditions)):
            self.assertIsInstance(self.problem.list_of_conditions[i].dual_variable_value, float)

    def tearDown(self):

        Point.counter = 0
        Expression.counter = 0
        Function.counter = 0