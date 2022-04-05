################################################################################
#
# sense-emu
#
################################################################################

SENSE_EMU_VERSION = 1.1
SENSE_EMU_SOURCE = sense-emu-$(SENSE_EMU_VERSION).tar.gz
SENSE_EMU_SITE = https://files.pythonhosted.org/packages/e5/b1/a8d1fd5c78f7b265b2271bf8d134404ccdf56b2b34f218c3d40c04cdd15a
SENSE_EMU_SETUP_TYPE = setuptools
SENSE_EMU_LICENSE = BSD
SENSE_EMU_LICENSE_FILES = LICENSE

$(eval $(python-package))
