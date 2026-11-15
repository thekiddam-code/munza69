"""Extract installed Shell icons to bounded PNGs; never download replacement app logos."""
import ctypes,struct,zlib
from ctypes import wintypes as W

def png(width,height,rgba):
 def chunk(kind,data):return struct.pack('!I',len(data))+kind+data+struct.pack('!I',zlib.crc32(kind+data)&0xffffffff)
 rows=b''.join(b'\0'+rgba[y*width*4:(y+1)*width*4] for y in range(height))
 return b'\x89PNG\r\n\x1a\n'+chunk(b'IHDR',struct.pack('!2I5B',width,height,8,6,0,0,0))+chunk(b'IDAT',zlib.compress(rows))+chunk(b'IEND',b'')

def installed_icon(path,app_id=None):
 if not hasattr(ctypes,'WinDLL'):return None
 shell=ctypes.WinDLL('shell32',use_last_error=True);user=ctypes.WinDLL('user32');gdi=ctypes.WinDLL('gdi32');ole=ctypes.WinDLL('ole32')
 class Info(ctypes.Structure):_fields_=[('hIcon',W.HANDLE),('iIcon',ctypes.c_int),('attributes',W.DWORD),('displayName',W.WCHAR*260),('typeName',W.WCHAR*80)]
 class Header(ctypes.Structure):_fields_=[('size',W.DWORD),('width',W.LONG),('height',W.LONG),('planes',W.WORD),('bitCount',W.WORD),('compression',W.DWORD),('sizeImage',W.DWORD),('xppm',W.LONG),('yppm',W.LONG),('used',W.DWORD),('important',W.DWORD)]
 class Bitmap(ctypes.Structure):_fields_=[('header',Header),('color',W.DWORD*3)]
 shell.SHGetFileInfoW.argtypes=[W.LPCVOID,W.DWORD,ctypes.POINTER(Info),W.UINT,W.UINT];shell.SHGetFileInfoW.restype=ctypes.c_size_t
 shell.SHParseDisplayName.argtypes=[W.LPCWSTR,W.LPVOID,ctypes.POINTER(W.LPVOID),W.DWORD,ctypes.POINTER(W.DWORD)];shell.SHParseDisplayName.restype=ctypes.c_long
 user.GetDC.argtypes=[W.HWND];user.GetDC.restype=W.HDC;user.ReleaseDC.argtypes=[W.HWND,W.HDC]
 user.DrawIconEx.argtypes=[W.HDC,ctypes.c_int,ctypes.c_int,W.HANDLE,ctypes.c_int,ctypes.c_int,W.UINT,W.HBRUSH,W.UINT]
 user.DestroyIcon.argtypes=[W.HANDLE]
 gdi.CreateCompatibleDC.argtypes=[W.HDC];gdi.CreateCompatibleDC.restype=W.HDC;gdi.DeleteDC.argtypes=[W.HDC]
 gdi.CreateDIBSection.argtypes=[W.HDC,ctypes.POINTER(Bitmap),W.UINT,ctypes.POINTER(W.LPVOID),W.HANDLE,W.DWORD];gdi.CreateDIBSection.restype=W.HBITMAP
 gdi.SelectObject.argtypes=[W.HDC,W.HANDLE];gdi.SelectObject.restype=W.HANDLE;gdi.DeleteObject.argtypes=[W.HANDLE]
 ole.CoTaskMemFree.argtypes=[W.LPVOID]
 ole.CoInitializeEx.argtypes=[W.LPVOID,W.DWORD];ole.CoInitializeEx.restype=ctypes.c_long
 initialized=ole.CoInitializeEx(None,2)>=0
 info=Info();pidl=W.LPVOID();dc=None;mem=None;bitmap=None;old=None
 try:
  flags=0x100 # SHGFI_ICON, large icon
  if app_id:
   if shell.SHParseDisplayName('shell:AppsFolder\\'+app_id,None,ctypes.byref(pidl),0,None)<0:return None
   arg=pidl;flags|=8
  else:arg=ctypes.cast(ctypes.c_wchar_p(str(path)),W.LPCVOID)
  if not shell.SHGetFileInfoW(arg,0,ctypes.byref(info),ctypes.sizeof(info),flags) or not info.hIcon:return None
  size=48;dc=user.GetDC(None);mem=gdi.CreateCompatibleDC(dc);bits=W.LPVOID();bi=Bitmap();bi.header=Header(ctypes.sizeof(Header),size,-size,1,32,0,0,0,0,0,0);bitmap=gdi.CreateDIBSection(dc,ctypes.byref(bi),0,ctypes.byref(bits),None,0)
  if not mem or not bitmap or not bits:return None
  old=gdi.SelectObject(mem,bitmap);ctypes.memset(bits,0,size*size*4)
  if not user.DrawIconEx(mem,0,0,info.hIcon,size,size,0,None,3):return None
  raw=ctypes.string_at(bits,size*size*4);rgba=bytearray(len(raw));alpha=any(raw[3::4])
  for i in range(0,len(raw),4):
   b,g,r,a=raw[i:i+4];a=a if alpha else (255 if b or g or r else 0)
   # Windows DIB color channels are premultiplied by alpha.
   rgba[i:i+4]=bytes((min(255,round(r*255/a)) if a else 0,min(255,round(g*255/a)) if a else 0,min(255,round(b*255/a)) if a else 0,a))
  return png(size,size,bytes(rgba))
 finally:
  if old and mem:gdi.SelectObject(mem,old)
  if bitmap:gdi.DeleteObject(bitmap)
  if mem:gdi.DeleteDC(mem)
  if dc:user.ReleaseDC(None,dc)
  if info.hIcon:user.DestroyIcon(info.hIcon)
  if pidl:ole.CoTaskMemFree(pidl)
  if initialized:ole.CoUninitialize()
