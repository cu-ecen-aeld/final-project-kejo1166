################################################################################
#
# rtimulib
#
################################################################################

RTIMULIB_VERSION = 7.2.1
RTIMULIB_SOURCE = RTIMULib-$(RTIMULIB_VERSION).tar.gz
RTIMULIB_SITE = https://files.pythonhosted.org/packages/86/78/562816a251259f387b1f27388ced9a6a0758b70944d64f4f622c30e47b21
RTIMULIB_LICENSE = Apache License
RTIMULIB_LICENSE_FILES = LICENSE
RTIMULIB_SETUP_TYPE = setuptools

$(eval $(python-package))
