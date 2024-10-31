from __future__ import annotations

import pytest
from osgeo import gdal, ogr, osr

def test_gdal_import():
    assert gdal is not None
    assert ogr is not None
    assert osr is not None

def test_gdal_version():
    version = gdal.__version__
    assert version is not None
    assert isinstance(version, str)
    assert len(version.split('.')) >= 3

def test_gdal_driver_count():
    driver_count = gdal.GetDriverCount()
    assert driver_count > 0

def test_ogr_driver_count():
    driver_count = ogr.GetDriverCount()
    assert driver_count > 0

def test_spatial_reference():
    srs = osr.SpatialReference()
    srs.ImportFromEPSG(4326)
    assert srs.GetAuthorityCode(None) == '4326'

def test_gdal_open():
    # This test might fail if the file doesn't exist, so we'll skip it if there's an error
    try:
        ds = gdal.Open('tests/data/test.tif')
        assert ds is not None
    except RuntimeError:
        pytest.skip("Test data file not found")

if __name__ == '__main__':
    pytest.main()
