# Windows

## Modify Windows 11 Right-click Context Menu

In Windows 11, run the following command in Command Prompt (Terminal) to apply the Windows 10 classic context menu style :

```bash
# modify
reg.exe add “HKCU\Software\Classes\CLSID\{86ca1aa0-34aa-4e8b-a509-50c905bae2a2}\InprocServer32” /f

# recover
reg.exe delete “HKCU\Software\Classes\CLSID\{86ca1aa0-34aa-4e8b-a509-50c905bae2a2}” /f
```
