#pragma once

#include "targetver.h"


#include <iostream>
#include <map>
#include <string>

namespace std {
#if defined _UNICODE || defined UNICODE
	typedef wstring tstring;
#else
	typedef string tstring;
#endif
}

#include <stdio.h>
#include <tchar.h>
#include <Windows.h>
#include <psapi.h>