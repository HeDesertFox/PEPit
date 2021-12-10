import numpy as np

from PEPit.pep import PEP
from PEPit.functions.convex_lipschitz_function import ConvexLipschitzFunction


def wc_subgd(M, n, gamma, verbose=True):
    """
    Consider the minimization problem

    .. math:: f_\\star \\triangleq \\min_x f(x),

    where :math:`f` is convex and :math:`M`-Lipschitz. This problem is a (possibly non-smooth) minimization problem.

    This code computes a worst-case guarantee for the **subgradient** method. That is, it computes
    the smallest possible :math:`\\tau(n, M, \\gamma)` such that the guarantee

    .. math:: \\min_{0 \leqslant t \leqslant n} f(x_t) - f_\\star \\leqslant \\tau(n, M, \\gamma)  \|x_0 - x_\\star\|

    is valid, where :math:`x_t` is the output of the **subgradient** method after :math:`t\\leqslant n` steps,
    and where :math:`x_\\star` is the minimizer of :math:`f`.

    In short, for given values of :math:`M`, the step-size :math:`\\gamma` and the number of iterations :math:`n`,
    :math:`\\tau(n, M, \\gamma)` is computed as the worst-case value of
    :math:`\\min_{0 \leqslant t \leqslant n} f(x_t) - f_\\star` when  :math:`\\|x_0-x_\\star\\| \\leqslant 1`.

    **Algorithm**:
    For :math:`t\\in \\{0, \\dots, n-1 \\}`

        .. math::
            :nowrap:

            \\begin{eqnarray}
                g_{t} & \\in & \\partial f(x_t) \\\\
                x_{t+1} & = & x_t - \\gamma g_t
            \\end{eqnarray}

    **Theoretical guarantee**:

    The **tight** bound is obtained in [1, Section 3.2.3] and [2, eq (2)],

        .. math:: \\min_{0 \\leqslant t \\leqslant n} f(x_t)- f(x_\\star) \\leqslant \\frac{M}{\\sqrt{n+1}}\|x_0-x_\\star\|.

    **References**:

        `[1] Y. Nesterov, Introductory Lectures on Convex Programming, Volume 1: Basic course (1998).
        <https://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.693.855&rep=rep1&type=pdf>`_

        `[2] S. Boyd, L. Xiao, & A. Mutapcic (2003). Subgradient Methods (Stanford University lecture notes)
        <https://web.stanford.edu/class/ee392o/subgrad_method.pdf>`_

    Args:
        M (float): the Lipschitz parameter.
        n (int): the number of iterations.
        gamma (float): step size.
        verbose (bool, optional): if True, print conclusion.

    Returns:
        tuple: worst_case value, theoretical value

    Example:
        >>> M = 2
        >>> n = 6
        >>> gamma = 1 / (M * np.sqrt(n + 1))
        >>> pepit_tau, theoretical_tau = wc_subgd(M, n, gamma, verbose=True)
        (PEP-it) Setting up the problem: size of the main PSD matrix: 9x9
        (PEP-it) Setting up the problem: performance measure is minimum of 7 element(s)
        (PEP-it) Setting up the problem: initial conditions (1 constraint(s) added)
        (PEP-it) Setting up the problem: interpolation conditions for 1 function(s)
                 function 1 : 64 constraint(s) added
        (PEP-it) Compiling SDP
        (PEP-it) Calling SDP solver
        (PEP-it) Solver status: optimal (solver: SCS); optimal value: 0.755982533173183
        *** Example file: worst-case performance of subgradient method ***
            PEP-it guarantee:		 min_(0 <= t <= n) f(x_t) - f_*  <= 0.755983 ||x_0 - x_*||`
            Theoretical guarantee:	 min_(0 <= t <= n) f(x_t) - f_*  <= 0.755929 ||x_0 - x_*||`
    """

    # Instantiate PEP
    problem = PEP()

    # Declare a convex lipschitz function
    func = problem.declare_function(ConvexLipschitzFunction, param={'M': M})

    # Start by defining its unique optimal point xs = x_* and corresponding function value fs = f_*
    xs = func.stationary_point()
    fs = func.value(xs)

    # Then define the starting point x0 of the algorithm
    x0 = problem.set_initial_point()

    # Set the initial constraint that is the distance between x0 and xs
    problem.set_initial_condition((x0 - xs)**2 <= 1)

    # Run n steps of the subgradient method
    x = x0
    gx, fx = func.oracle(x)

    for _ in range(n):
        problem.set_performance_metric(fx - fs)
        x = x - gamma * gx
        gx, fx = func.oracle(x)

    # Set the performance metric to the function value accuracy
    problem.set_performance_metric(fx - fs)

    # Solve the PEP
    pepit_tau = problem.solve(verbose=verbose)

    # Compute theoretical guarantee (for comparison)
    theoretical_tau = M / np.sqrt(n + 1)

    # Print conclusion if required
    if verbose:
        print('*** Example file: worst-case performance of subgradient method ***')
        print('\tPEP-it guarantee:\t\t min_(0 \leq t \leq n) f(x_i) - f_*  <= {:.6} ||x_0 - x_*||'.format(pepit_tau))
        print('\tTheoretical guarantee:\t min_(0 \leq t \leq n) f(x_i) - f_*  <= {:.6} ||x_0 - x_*||'.format(
            theoretical_tau))

    # Return the worst-case guarantee of the evaluated method (and the reference theoretical value)
    return pepit_tau, theoretical_tau


if __name__ == "__main__":
    M = 2
    n = 6
    gamma = 1 / (M * np.sqrt(n + 1))

    pepit_tau, theoretical_tau  = wc_subgd(M=M, n=n, gamma=gamma, verbose=True)
