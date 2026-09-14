"""
Desktop notification support for encoding completion.
Uses PowerShell's NotifyIcon on Windows; silently no-ops on failure.
"""
import subprocess


def notify_complete(size_mb: float, target_mb: float) -> None:
    """Show a Windows system-tray balloon tip when encoding finishes."""
    msg = f"Conversion complete!  {size_mb:.2f} MB / {target_mb:.1f} MB target"
    ps_script = (
        "Add-Type -AssemblyName System.Windows.Forms;"
        "$n=New-Object System.Windows.Forms.NotifyIcon;"
        "$n.Icon=[System.Drawing.SystemIcons]::Information;"
        "$n.Visible=$true;"
        f"$n.ShowBalloonTip(5000,'pyWebmConverter','{msg}',"
        "[System.Windows.Forms.ToolTipIcon]::None);"
        "Start-Sleep -Seconds 6;"
        "$n.Dispose()"
    )
    try:
        subprocess.Popen(  # pylint: disable=consider-using-with
            ["powershell", "-WindowStyle", "Hidden", "-Command", ps_script],
            creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    except (FileNotFoundError, OSError):
        pass
