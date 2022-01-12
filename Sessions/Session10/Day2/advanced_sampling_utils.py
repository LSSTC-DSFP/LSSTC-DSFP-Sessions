# -*- coding: utf-8 -*-

from __future__ import division, print_function

__all__ = [
    "setup_plotting",
    "test_emcee_functions",
    "test_dynesty_functions",
    "test_pymc3_model",
    "Angle",
]

import sys
import traceback
from itertools import product

import numpy as np
import matplotlib.pyplot as plt

import theano
import theano.tensor as tt

import pymc3 as pm
import pymc3.distributions.transforms as tr
from pymc3.distributions import generate_samples

import emcee

if not emcee.__version__.startswith("3"):
    raise ImportError(
        "For emcee, version 3.0 or greater is needed. "
        "You can install that using: "
        "'pip install emcee==3.0rc2'"
    )


def setup_plotting():
    plt.style.use("default")
    plt.rcParams["savefig.dpi"] = 100
    plt.rcParams["figure.dpi"] = 100
    plt.rcParams["font.size"] = 16
    plt.rcParams["font.family"] = "sans-serif"
    plt.rcParams["font.sans-serif"] = ["Liberation Sans"]
    plt.rcParams["mathtext.fontset"] = "custom"


def emcee_loglike_ref(params, x, y):
    bperp, theta, logs = params
    m = np.tan(theta)
    b = bperp / np.cos(theta)
    model = m * x + b
    return -0.5 * np.sum((y - model) ** 2 / np.exp(2 * logs) + 2 * logs)


def dynesty_prior_transform_ref(u):
    bperp = -10 + 20 * u[0]
    theta = -0.5 * np.pi + np.pi * u[1]
    logs = -10 + 20 * u[2]
    return np.array([bperp, theta, logs])


def test_emcee_get_params(emcee_get_params_impl):
    for m, b, logs in product(
        [-3.5, 5.0, 0.0], [-9.7, 0.0, 1e-4, 5.0], [0.5, -2.0, 5.0]
    ):
        theta = np.arctan(m)
        bperp = b * np.cos(theta)
        mtest, btest, logstest = emcee_get_params_impl(
            np.array([bperp, theta, logs])
        )
        if not np.allclose(m, mtest):
            raise ValueError("Incorrect m calculation")
        if not np.allclose(b, btest):
            raise ValueError("Incorrect b calculation")
        if not np.allclose(logs, logstest):
            raise ValueError("Incorrect logs calculation")


def test_emcee_logprior(emcee_logprior_impl):
    ref = emcee_logprior_impl(np.zeros(3))
    for i, name in enumerate(["bperp", "theta", "logs"]):
        coord = np.zeros(3)
        for delta in [0.1, -1.05]:
            coord[i] = delta
            val = emcee_logprior_impl(coord)
            if not np.allclose(ref, val):
                raise ValueError("Incorrect logprior for {0}".format(name))
        for delta in [11.1, -15.05]:
            coord[i] = delta
            val = emcee_logprior_impl(coord)
            if not (np.isinf(val) and val < 0):
                raise ValueError(
                    (
                        "logprior for {0} should return -np.inf "
                        "outside of bounds"
                    ).format(name)
                )
    val = emcee_logprior_impl(np.array([12.0, 0.5 * np.pi + 0.1, -11.6]))
    if not (np.isinf(val) and val < 0):
        raise ValueError("logprior should return -np.inf outside of bounds")


def test_emcee_loglike(emcee_loglike_impl, x, y):
    ref_zero = emcee_loglike_ref(np.zeros(3), x, y)
    impl_zero = emcee_loglike_impl(np.zeros(3))
    for m, b, logs in product(
        [-3.5, 5.0, 0.0], [-9.7, 0.0, 1e-4, 5.0], [0.5, -2.0, 5.0]
    ):
        theta = np.arctan(m)
        bperp = b * np.cos(theta)
        coords = np.array([bperp, theta, logs])
        ref_val = emcee_loglike_ref(coords, x, y)
        impl_val = emcee_loglike_impl(coords)
        if not (
            np.isfinite(impl_val)
            and np.allclose(ref_val - ref_zero, impl_val - impl_zero)
        ):
            raise ValueError(
                "Incorrect loglike for parameters: {0}".format(coords)
            )


def test_emcee_logprob(emcee_logprob_impl, x, y):
    ref_zero = emcee_loglike_ref(np.zeros(3), x, y)
    impl_zero = emcee_logprob_impl(np.zeros(3))
    for m, b, logs in product(
        [-3.5, 5.0, 0.0], [-9.7, 0.0, 1e-4, 5.0], [0.5, -2.0, 5.0]
    ):
        theta = np.arctan(m)
        bperp = b * np.cos(theta)
        coords = np.array([bperp, theta, logs])
        ref_val = emcee_loglike_ref(coords, x, y)
        impl_val = emcee_logprob_impl(coords)
        if not (
            np.isfinite(impl_val)
            and np.allclose(ref_val - ref_zero, impl_val - impl_zero)
        ):
            raise ValueError(
                "Incorrect logprob for parameters: {0}".format(coords)
            )

    impl_val = emcee_logprob_impl(np.array([-12.0, 0.1, 5.6]))
    if not (np.isinf(impl_val) and impl_val < 0):
        raise ValueError("logprob should return -np.inf outside of bounds")


def test_dynesty_prior_transform(dynesty_prior_transform_impl):
    for u in product(
        np.linspace(0, 1, 5), np.linspace(0, 1, 10), np.linspace(0, 1, 12)
    ):
        ref = dynesty_prior_transform_ref(np.array(u))
        impl = dynesty_prior_transform_impl(np.array(u))
        if not np.allclose(ref, impl):
            raise ValueError(
                "Invalid prior_transform for coordinates: {0}".format(u)
            )


def test_function(name, test_func, *args):
    sys.stderr.write("Testing '{0}'... ".format(name))
    try:
        test_func(*args)
    except Exception:
        sys.stderr.write("FAILED with the following error:\n")
        traceback.print_exc()
    else:
        sys.stderr.write("PASSED! :)\n")


def test_emcee_functions(
    emcee_get_params_impl,
    emcee_logprior_impl,
    emcee_loglike_impl,
    emcee_logprob_impl,
    x,
    y,
):
    test_function(
        "emcee_get_params", test_emcee_get_params, emcee_get_params_impl
    )
    test_function("emcee_logprior", test_emcee_logprior, emcee_logprior_impl)
    test_function(
        "emcee_loglike", test_emcee_loglike, emcee_loglike_impl, x, y
    )
    test_function(
        "emcee_logprob", test_emcee_logprob, emcee_logprob_impl, x, y
    )


def test_dynesty_functions(
    dynesty_get_params_impl,
    dynesty_prior_transform_impl,
    dynesty_loglike_impl,
    x,
    y,
):
    test_function(
        "dynesty_get_params", test_emcee_get_params, dynesty_get_params_impl
    )
    test_function(
        "dynesty_prior_transform",
        test_dynesty_prior_transform,
        dynesty_prior_transform_impl,
    )
    test_function(
        "dynesty_loglike", test_emcee_loglike, dynesty_loglike_impl, x, y
    )


def get_args_for_theano_function(point=None, model=None):
    model = pm.modelcontext(model)
    if point is None:
        point = model.test_point
    return [point[k.name] for k in model.vars]


def get_theano_function_for_var(var, model=None, **kwargs):
    model = pm.modelcontext(model)
    kwargs["on_unused_input"] = kwargs.get("on_unused_input", "ignore")
    return theano.function(model.vars, var, **kwargs)


def _test_pymc3_model(pymc3_model, x, y):
    named_vars = pymc3_model.named_vars

    for name in ["bperp", "theta", "logs"]:
        if name not in named_vars:
            raise ValueError("Variable {0} missing from model".format(name))
        if name + "_interval__" not in named_vars:
            raise ValueError(
                "Variable {0} should be a pm.Uniform distribution".format(name)
            )

    for name in ["m", "b"]:
        if name not in named_vars:
            raise ValueError(
                "pm.Deterministic variable {0} missing from model".format(name)
            )

    observed = []
    for k, v in named_vars.items():
        if isinstance(v, pm.model.ObservedRV):
            observed.append((k, v))
    if len(observed) != 1:
        raise ValueError(
            "There should be exactly one observed variable, not {0}".format(
                len(observed)
            )
        )

    with pm.Model() as pymc3_model_ref:
        bperp = pm.Uniform("bperp", lower=-10, upper=10)
        theta = pm.Uniform("theta", lower=-0.5 * np.pi, upper=0.5 * np.pi)
        logs = pm.Uniform("logs", lower=-10, upper=10)
        m = pm.Deterministic("m", pm.math.tan(theta))
        b = pm.Deterministic("b", bperp / pm.math.cos(theta))
        model = m * x + b
        pm.Normal("loglike", mu=model, sd=pm.math.exp(logs), observed=y)

    varlist_ref = pymc3_model_ref.unobserved_RVs
    names_ref = [v.name for v in varlist_ref]
    func_ref = get_theano_function_for_var(varlist_ref, model=pymc3_model_ref)

    varlist_impl = pymc3_model.unobserved_RVs
    names_impl = [v.name for v in varlist_impl]
    func_impl = get_theano_function_for_var(varlist_impl, model=pymc3_model)

    for vec in product(
        np.linspace(-100, 100, 5),
        np.linspace(-100, 100, 10),
        np.linspace(-100, 100, 12),
    ):
        args_ref = get_args_for_theano_function(
            {
                "bperp_interval__": vec[0],
                "theta_interval__": vec[1],
                "logs_interval__": vec[2],
            },
            model=pymc3_model_ref,
        )
        args_impl = get_args_for_theano_function(
            {
                "bperp_interval__": vec[0],
                "theta_interval__": vec[1],
                "logs_interval__": vec[2],
            },
            model=pymc3_model,
        )
        ref = dict(zip(names_ref, func_ref(*args_ref)))
        impl = dict(zip(names_impl, func_impl(*args_impl)))
        for k, v in ref.items():
            if k not in impl:
                raise ValueError("Parameter {0} not in model".format(k))
            if not np.allclose(v, impl[k]):
                raise ValueError(
                    "Invalid calculation of parameter {0}".format(k)
                )


def test_pymc3_model(pymc3_model, x, y):
    test_function("pymc3_model", _test_pymc3_model, pymc3_model, x, y)


class AngleTransform(tr.Transform):
    """Reference: exoplanet.dfm.io"""

    name = "angle"

    def __init__(self, *args, **kwargs):
        self.regularized = kwargs.pop("regularized", 10.0)
        super(AngleTransform, self).__init__(*args, **kwargs)

    def backward(self, y):
        return tt.arctan2(y[0], y[1])

    def forward(self, x):
        return tt.concatenate(
            (tt.shape_padleft(tt.sin(x)), tt.shape_padleft(tt.cos(x))), axis=0
        )

    def forward_val(self, x, point=None):
        return np.array([np.sin(x), np.cos(x)])

    def jacobian_det(self, y):
        sm = tt.sum(tt.square(y), axis=0)
        if self.regularized is not None:
            return self.regularized * tt.log(sm) - 0.5 * sm
        return -0.5 * sm


class Angle(pm.Continuous):
    """An angle constrained to be in the range -pi to pi

    The actual sampling is performed in the two dimensional vector space
    ``(sin(theta), cos(theta))`` so that the sampler doesn't see a
    discontinuity at pi.

    """

    def __init__(self, *args, **kwargs):
        transform = kwargs.pop("transform", None)
        if transform is None:
            if "regularized" in kwargs:
                transform = AngleTransform(
                    regularized=kwargs.pop("regularized")
                )
            else:
                transform = AngleTransform()
        kwargs["transform"] = transform

        shape = kwargs.get("shape", None)
        if shape is None:
            testval = 0.0
        else:
            testval = np.zeros(shape)
        kwargs["testval"] = kwargs.pop("testval", testval)
        super(Angle, self).__init__(*args, **kwargs)

    def _random(self, size=None):
        return np.random.uniform(-np.pi, np.pi, size)

    def random(self, point=None, size=None):
        return generate_samples(
            self._random,
            dist_shape=self.shape,
            broadcast_shape=self.shape,
            size=size,
        )

    def logp(self, value):
        return tt.zeros_like(tt.as_tensor_variable(value))
