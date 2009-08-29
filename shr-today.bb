DESCRIPTION = "python-elementary and opimd based lock and today screen for the SHR distribution"
HOMEPAGE = "http://wiki.github.com/slyon/today"
SHR_RELEASE ?= "shr"
LICENSE ?= "GPL"
RDEPENDS = "python-elementary python-dbus python-edbus python-ecore"
SECTION = "x11/applications"

PV = "0.0.1-gitr${SRCPV}"
PR = "r0"

inherit setuptools

SRC_URI = "git://github.com/slyon/today.git;protocol=http"
S = "${WORKDIR}/git"

FILES_${PN} += "/etc"
FILES_${PN} += "/usr/share/shr-today"

