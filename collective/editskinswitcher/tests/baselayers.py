from Products.PloneTestCase import PloneTestCase as ptc
from Testing import ZopeTestCase as ztc
from Products.PloneTestCase.layer import onsetup
from Products.Five import fiveconfigure
from Products.Five import zcml

@onsetup
def setup_product():
    """Set up the package and its dependencies.

    The @onsetup decorator causes the execution of this body to be
    deferred until the setup of the Plone site testing layer. We could
    have created our own layer, but this is the easiest way for Plone
    integration tests.
    """
    # Load the ZCML configuration for the example.tests package.
    # This can of course use <include /> to include other packages.

    fiveconfigure.debug_mode = True

    import collective.editskinswitcher
    zcml.load_config('configure.zcml', collective.editskinswitcher)
    zcml.load_config('testing-layers.zcml', collective.editskinswitcher)
    fiveconfigure.debug_mode = False

    # fix important, we avoid an error on setupPloneSite


    # We need to tell the testing framework that these products
    # should be available. This can't happen until after we have loaded
    # the ZCML. Thus, we do it here. Note the use of installPackage()
    # instead of installProduct().
    # This is *only* necessary for packages outside the Products.*
    # namespace which are also declared as Zope 2 products, using
    # <five:registerPackage /> in ZCML.

    # We may also need to load dependencies, e.g.:
    #   ztc.installPackage('borg.localrole')

    ztc.installPackage('collective.editskinswitcher')

# The order here is important: We first call the (deferred) function
# which installs the products we need for this product. Then, we let
# PloneTestCase set up this product on installation.

setup_product()
ptc.setupPloneSite(products=['collective.editskinswitcher'], extension_profiles=['collective.editskinswitcher:testing'])


class LayersTestCase(ptc.PloneTestCase):
    """Class for functional test cases with different layers.
    """

