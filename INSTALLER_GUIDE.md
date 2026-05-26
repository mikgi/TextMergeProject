# Windows Installer Guide

## 1) Build the app folder (`.exe`)

```powershell
.\build_exe.ps1
```

Output:

- `dist\TextMergeApp\TextMergeApp.exe`

## 2) Build installer (`.exe`)

Install **Inno Setup 6** first, then open `installer.iss` and click **Build**.

Or via command line (default path):

```powershell
& "C:\Program Files (x86)\Inno Setup 6\ISCC.exe" .\installer.iss
```

Output:

- `dist\TextMergeInstaller.exe`

## Notes

- This project uses one-folder packaging (safer for fonts/resources).
- If SmartScreen warns on first run, choose **More info** -> **Run anyway**.
