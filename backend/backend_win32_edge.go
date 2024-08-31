// +build windows
// +build webview.backend.win32_edge

package backend

/*
#cgo CFLAGS: -I${SRCDIR}/../libs/webview/include
#cgo CXXFLAGS: -I${SRCDIR}/../libs/webview/include -I${SRCDIR}/../libs/mswebview2/include -DWEBVIEW_STATIC -DWEBVIEW_EDGE -std=c++14
#cgo LDFLAGS: -static -ladvapi32 -lole32 -lshell32 -lshlwapi -luser32 -lversion

#include "webview.h"
*/
import "C"
