################################################################################
#
# pika
#
################################################################################

PIKA_VERSION = 1.2.0
PIKA_SOURCE = pika-$(PIKA_VERSION).tar.gz
PIKA_SITE = https://files.pythonhosted.org/packages/fc/89/26d3054216d869901dd461f3de1f5b35802bcc3834d1831ebf62ad16ac1e
PIKA_LICENSE = BSD
PIKA_LICENSE_FILES = LICENSE
PIKA_SETUP_TYPE = distutils

$(eval $(python-package))
