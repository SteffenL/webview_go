// +build darwin
// +build webview.backend.cocoa_webkit

package backend

/*
#cgo CFLAGS: -I${SRCDIR}/../libs/webview/include
#cgo CXXFLAGS: -I${SRCDIR}/../libs/webview/include -DWEBVIEW_STATIC -DWEBVIEW_COCOA -std=c++11
#cgo LDFLAGS: -framework WebKit -ldl

#include "webview.h"
*/
import "C"
