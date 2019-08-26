#pragma once

#include <iostream>
#include <map>
#include <string>
#include <vector>


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

using namespace std;

vector<HWND> v;

BOOL CALLBACK enumWindowsProc(
	__in  HWND hWnd,
	__in  LPARAM lParam
) {

	int length = ::GetWindowTextLength(hWnd);
	if (0 == length) return TRUE;

	TCHAR* buffer;
	buffer = new TCHAR[length + 1];
	memset(buffer, 0, (length + 1) * sizeof(TCHAR));

	if (length == 10) {

		TCHAR* buffer2;
		buffer2 = new TCHAR[length + 1];
		memset(buffer2, 0, (length + 1) * sizeof(TCHAR));

		GetWindowText(hWnd, buffer, length + 1);
		tstring windowTitle = tstring(buffer);
		string x = "AltspaceVR";
		bool f = true;
		for (int i = 0; i < length; i++) {
			if (x[i] != buffer[i]) {
				f = false;
				break;
			}
		}

		if (f && length == x.length()) {
			wcout << hWnd << TEXT(": ") << buffer << endl;
			v.push_back(hWnd);
		}

		delete[] buffer;
	}

	return TRUE;
}

int _tmain(int argc, _TCHAR* argv[]) {
	wcout << TEXT("Enumerating Windows...") << endl;
	BOOL enumeratingWindowsSucceeded = ::EnumWindows(enumWindowsProc, NULL);

	for (int j = 0; j < 100; j++) {
		for (int i = 0; i < v.size(); i++) {
			SetForegroundWindow(v[i]);
			PostMessage(v[i], WM_KEYDOWN, 0x57, 0x001C0001);
			Sleep(100);
			//SendMessage(v[i], WM_KEYUP, 0x57, 0x001C0001);
		}
	}
	HWND notepad = FindWindow(_T("Notepad"), NULL);
	HWND edit = FindWindowEx(notepad, NULL, _T("Edit"), NULL);
	SendMessage(edit, WM_SETTEXT, NULL, (LPARAM)_T("hello"));
	return 0;
}