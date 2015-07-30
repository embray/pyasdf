# Licensed under a 3-clause BSD style license - see LICENSE.rst
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, unicode_literals, print_function


try:
    import astropy
except ImportError:
    HAS_ASTROPY = False
else:
    HAS_ASTROPY = True

    from astropy.modeling import models
    from astropy import coordinates as coord
    from astropy import units as u

try:
    import gwcs
except ImportError:
    HAS_GWCS = False
else:
    HAS_GWCS = True

    from gwcs import coordinate_frames as cf
    from gwcs import wcs

import pytest

from ....tests import helpers


@pytest.mark.skipif('not HAS_GWCS')
def test_create_wcs(tmpdir):
    m1 = models.Shift(12.4) & models.Shift(-2)
    m2 = models.Scale(2) & models.Scale(-2)
    icrs = cf.CelestialFrame(name='icrs', reference_frame=coord.ICRS())
    det = cf.Frame2D(name='detector', axes_order=(0,1))
    gw1 = wcs.WCS(output_frame='icrs', input_frame='detector', forward_transform=m1)
    gw2 = wcs.WCS(output_frame='icrs', forward_transform=m1)
    gw3 = wcs.WCS(output_frame=icrs, input_frame=det, forward_transform=m1)

    tree = {
        'gw1': gw1,
        'gw2': gw2,
        'gw3': gw3
    }

    helpers.assert_roundtrip_tree(tree, tmpdir)


@pytest.mark.skipif('not HAS_GWCS')
def test_composite_frame(tmpdir):
    icrs = coord.ICRS()
    fk5 = coord.FK5()
    cel1 = cf.CelestialFrame(reference_frame=icrs)
    cel2 = cf.CelestialFrame(reference_frame=fk5)

    spec1 = cf.SpectralFrame(name='freq', unit=[u.Hz,], axes_order=(2,))
    spec2 = cf.SpectralFrame(name='wave', unit=[u.m,], axes_order=(2,))

    comp1 = cf.CompositeFrame([cel1, spec1])
    comp2 = cf.CompositeFrame([cel2, spec2])
    comp = cf.CompositeFrame([comp1, cf.SpectralFrame(axes_order=(3,), unit=(u.m,))])

    tree = {
        'comp1': comp1,
        'comp2': comp2,
        'comp': comp
    }

    helpers.assert_roundtrip_tree(tree, tmpdir)
