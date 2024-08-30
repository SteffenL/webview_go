// +build linux openbsd freebsd netbsd
// +build webview.backend.gtk3_webkitgtk401

package backend

/*
#cgo CFLAGS: -I${SRCDIR}/../libs/webview/include
#cgo CXXFLAGS: -I${SRCDIR}/../libs/webview/include -DWEBVIEW_STATIC -DWEBVIEW_GTK -std=c++11
#cgo LDFLAGS: -ldl
#cgo pkg-config: gtk+-3.0 webkit2gtk-4.1

#include "webview.h"
*/
import "C"
