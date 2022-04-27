##############################################################
#
# AESD-SENSEHATLIVE
#
##############################################################

# Repository version
AESD_SENSEHATLIVE_VERSION = 0a865bc8b498524b8af1194db1cd8a7a9a4bc581

# Note: Be sure to reference the *ssh* repository URL here (not https) to work properly
# with ssh keys and the automated build/test system.
# Your site should start with git@github.com:
AESD_SENSEHATLIVE_SITE = git@github.com:cu-ecen-aeld/final-project-kejo1166.git
AESD_SENSEHATLIVE_SITE_METHOD = git
AESD_SENSEHATLIVE_GIT_SUBMODULES = YES


define AESD_SENSEHATLIVE_INSTALL_TARGET_CMDS
	mkdir -p $(TARGET_DIR)/opt/aesd-sensehatlive/
	cp -rf $(@D)/aesd-sensehatlive/* $(TARGET_DIR)/opt/aesd-sensehatlive/
	chmod -R 755 $(TARGET_DIR)/opt/aesd-sensehatlive
endef

$(eval $(generic-package))
