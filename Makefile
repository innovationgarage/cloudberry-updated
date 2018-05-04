include $(TOPDIR)/rules.mk

PKG_NAME:=updated
PKG_VERSION:=0.1
PKG_RELEASE=$(PKG_SOURCE_VERSION)
PKG_MAINTAINER:=Alexander Alemayhu <alexander@alemayhu.com>
PKG_LICENSE:=GPLv2

include $(INCLUDE_DIR)/package.mk

define Package/updated/default
  CATEGORY:=Network
  SUBMENU:=Download Manager
  TITLE:=Package installer
endef

define Package/updated
  $(Package/updated/default)
  DEPENDS:=+python3
endef

define Package/updated/description
	updated is a user space daemon responsible for installing packages and updating
	them. The project uses UCI for all configuration and the actual package
	management is done by opkg.
endef

define Package/updated/install
	$(CP) ./files/* $(1)/
endef

define Build/Compile
	true
endef

$(eval $(call BuildPackage,updated))
