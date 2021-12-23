import unittest

import PEPit.examples.unconstrained_convex_minimization.proximal_point as ref_ppa
import PEPit.examples.composite_convex_minimization.proximal_gradient as ref_pgd

from tests.additional_complexified_examples_tests.proximal_gradient import wc_pgd
from tests.additional_complexified_examples_tests.proximal_point import wc_ppa


class TestExamples(unittest.TestCase):

    def setUp(self):
        self.n = 6
        self.mu = .1
        self.L = 1

        self.verbose = False

    def test_PGD_modified(self):
        L, mu, gamma, n = 1, 0.1, 1, 2

        wc, theory = wc_pgd(L, mu, gamma, n, verbose=self.verbose)
        self.assertAlmostEqual(wc, theory, delta=10 ** -3 * theory)

    def test_PGD_vs_PGD_modified(self):
        L, mu, gamma, n = 1, 0.1, 1, 2

        wc_modified, theory = wc_pgd(L, mu, gamma, n, verbose=self.verbose)
        wc, theory = ref_pgd.wc_proximal_gradient(L, mu, gamma, n, verbose=self.verbose)
        self.assertAlmostEqual(wc_modified, wc, delta=10 ** -3 * theory)

    def test_PPA_modified(self):
        n, gamma = 2, 1

        wc, theory = wc_ppa(n, gamma, verbose=self.verbose)
        self.assertAlmostEqual(wc, theory, delta=10 ** -3 * theory)

    def test_PPA_vs_PPA_modified(self):
        n, gamma = 2, 1

        wc_modified, theory = wc_ppa(n, gamma, verbose=self.verbose)
        wc, theory = ref_ppa.wc_proximal_point(n, gamma, verbose=self.verbose)
        self.assertAlmostEqual(wc_modified, wc, delta=10 ** -3 * theory)