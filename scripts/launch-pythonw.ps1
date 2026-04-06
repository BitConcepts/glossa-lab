# launch-pythonw.ps1
# Launches pythonw.exe with the given module and args.
# CreateNoWindow=true (kernel flag) + pythonw.exe (GUI subsystem) = zero console window.
# Writes PID to PidFile and returns immediately.
#
# Called from setup-os.cmd with no quoting issues since paths are passed as params.
param(
    [Parameter(Mandatory)][string]$Pythonw,   # full path to pythonw.exe
    [Parameter(Mandatory)][string]$Module,    # module name (after -m)
    [string[]]$ExtraArgs   = @(),             # additional argv
    [Parameter(Mandatory)][string]$WorkDir,   # working directory
    [string]  $PyPath      = "",              # PYTHONPATH to inject
    [Parameter(Mandatory)][string]$PidFile    # file to write PID into
)

$psi = [System.Diagnostics.ProcessStartInfo]::new($Pythonw)
$psi.Arguments        = ((@("-m", $Module) + $ExtraArgs) | ForEach-Object { $_ }) -join " "
$psi.WorkingDirectory = $WorkDir
$psi.UseShellExecute  = $false
$psi.CreateNoWindow   = $true

if ($PyPath -ne "") {
    $psi.EnvironmentVariables["PYTHONPATH"] = $PyPath
}

$proc = [System.Diagnostics.Process]::Start($psi)
if ($null -eq $proc) { Write-Error "Process.Start returned null"; exit 1 }

$proc.Id | Set-Content -Encoding ASCII -Path $PidFile
Write-Host $proc.Id
