// +build linux openbsd freebsd netbsd
// +build webview.backend.gtk4_webkitgtk600

package backend

/*
#cgo CFLAGS: -I${SRCDIR}/../libs/webview/include
#cgo CXXFLAGS: -I${SRCDIR}/../libs/webview/include -DWEBVIEW_STATIC -DWEBVIEW_GTK -std=c++11
#cgo LDFLAGS: -ldl
#cgo pkg-config: gtk4 webkitgtk-6.0

#include "webview.h"
*/
import "C"
