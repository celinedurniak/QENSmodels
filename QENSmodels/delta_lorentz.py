import numpy as np
import QENSmodels


def sqwDeltaLorentz(w, q, scale=1.0, center=0.0, A0=0.0, hwhm=1.0):
    r"""
    Model corresponding to a delta representing a fraction p of
    fixed atoms and a Lorentzian corresponding to a Brownian
    Translational diffusion model for the remaining (1 - p) atoms.

    Model = A0*delta + (1-A0)*Lorentz(Gamma)

    Parameters
    ----------
    w: float, list or :class:`~numpy:numpy.ndarray`
        energy transfer (in ps)

    q: float, list or :class:`~numpy:numpy.ndarray`
        momentum transfer (non-fitting, in 1/Angstrom)

    scale: float
        scale factor. Default to 1.

    center: float
        peak center. Default to 0.

    A0: float, list or :class:`~numpy:numpy.ndarray` of the same size as q
        amplitude of the delta function. Default to 0.

    hwhm: float, list or :class:`~numpy:numpy.ndarray` of the same size as q
        half width half maximum. Default to 1.

    Return
    ------
    :class:`~numpy:numpy.ndarray`
        output array


    Examples
    --------
    >>> QENSmodels.sqwDeltaLorentz([1, 2, 3], 0.1)
    array([ 0.15915494,  0.06366198,  0.03183099])


    Notes
    -----
    The `sqwDeltaLorentz` is expressed as

    .. math::

        S(q, \omega) &= A_0 \delta(\omega, \text{scale}, \text{center}) \\
        &+ (1 - A_0) \text{Lorentzian}(\omega, \text{scale}, \text{center}, \text{hwhm})

    """
    w = np.asarray(w, dtype=np.float32)

    # Input validation
    q = np.asarray(q, dtype=np.float32)

    # Create output array
    sqw = np.zeros((q.size, w.size))

    # Model
    if q.size > 1:
        for i in range(q.size):
            sqw[i, :] = A0[i] * QENSmodels.delta(w, scale, center)
            sqw[i, :] += (1-A0[i]) * QENSmodels.lorentzian(w, scale, center, hwhm[i])
    else:
        sqw[0, :] = A0 * QENSmodels.delta(w, scale, center)
        sqw[0, :] += (1-A0) * QENSmodels.lorentzian(w, scale, center, hwhm)

    # For Bumps use (needed for final plotting)
    # Using a 'Curve' in bumps for each Q --> needs vector array
    if q.size == 1:
        sqw = np.reshape(sqw, w.size)

    return sqw
