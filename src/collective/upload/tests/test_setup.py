# -*- coding: utf-8 -*-

import unittest2 as unittest

from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles

from plone.browserlayer.utils import registered_layers

from collective.upload.config import PROJECTNAME
from collective.upload.testing import INTEGRATION_TESTING


class InstallTest(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']

    def test_installed(self):
        qi = getattr(self.portal, 'portal_quickinstaller')
        self.assertTrue(qi.isProductInstalled(PROJECTNAME))

    def test_browserlayer_installed(self):
        layers = [l.getName() for l in registered_layers()]
        self.assertTrue('IUploadBrowserLayer' in layers)


class UninstallTest(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.qi = self.portal['portal_quickinstaller']

    def test_product_is_installed(self):
        """ Validate that our products GS profile has been run and the product
            installed
        """
        pid = 'collective.upload'
        installed = [p['id'] for p in self.qi.listInstalledProducts()]
        self.assertTrue(pid in installed,
                        'package appears not to have been installed')

    def test_uninstalled(self):
        self.qi.uninstallProducts(products=[PROJECTNAME])
        self.assertFalse(self.qi.isProductInstalled(PROJECTNAME))

    def test_browserlayer_uninstalled(self):
        self.qi.uninstallProducts(products=[PROJECTNAME])
        layers = [l.getName() for l in registered_layers()]
        self.assertFalse('IUploadBrowserLayer' in layers)
