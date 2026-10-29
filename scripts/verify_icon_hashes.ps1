# verify_icon_hashes.ps1 — Spec 080 FR-005 tray icon verification.
#
# Computes the SHA-256 of the two packaged tray icon assets with the
# .NET SHA-256 implementation (System.Security.Cryptography) and
# compares against the pins passed in by setup-os.cmd install.
#
# Why not Get-FileHash: that cmdlet arrives via module autoloading
# (Microsoft.PowerShell.Utility), which is NOT guaranteed in every
# context the installer runs in. On 2026-10-28 the Syncyard runner's
# `powershell -NoProfile -Command` child threw
# CommandNotFoundException for Get-FileHash, and the old batch check
# then misreported that hashing failure as a hash "mismatch" and
# refused a good install. The .NET implementation is part of the
# runtime PowerShell itself loads, so it exists wherever
# powershell.exe runs at all.
#
# The comparison is case-insensitive (-ieq): a SHA-256 pin is a hex
# digest, and hex letter case carries no information. Pins in
# setup-os.cmd are uppercase; .NET's converter emits uppercase too,
# but the check must not depend on either side's casing.
#
# Exit codes: 0 = both assets verified; 2 = hashing itself failed
# (reported as a hashing failure, never as a mismatch); 3 = an asset
# is missing; 4 = digest mismatch. Any nonzero exit refuses the
# install, loudly.

param(
    [Parameter(Mandatory = $true)][string]$IcoPath,
    [Parameter(Mandatory = $true)][string]$IcoSha256,
    [Parameter(Mandatory = $true)][string]$PngPath,
    [Parameter(Mandatory = $true)][string]$PngSha256
)

function Get-Sha256Hex([string]$Path) {
    $sha = [System.Security.Cryptography.SHA256]::Create()
    try {
        $stream = [System.IO.File]::OpenRead($Path)
        try {
            $hash = $sha.ComputeHash($stream)
        } finally {
            $stream.Dispose()
        }
    } finally {
        $sha.Dispose()
    }
    return ([System.BitConverter]::ToString($hash) -replace '-', '')
}

function Test-IconAsset([string]$Path, [string]$Expected) {
    if (-not (Test-Path -LiteralPath $Path)) {
        Write-Host "[ERROR] Tray icon asset missing: $Path"
        exit 3
    }
    try {
        $actual = Get-Sha256Hex $Path
    } catch {
        Write-Host "[ERROR] Could not compute SHA-256 for $Path : $($_.Exception.Message)"
        Write-Host "        This is a hashing failure, not a hash mismatch."
        exit 2
    }
    if ($actual -ieq $Expected) {
        Write-Host "[OK] Tray icon verified: $Path"
        return
    }
    Write-Host "[ERROR] Tray icon hash mismatch: $Path"
    Write-Host "        Expected SHA-256 $Expected"
    Write-Host "        Actual   SHA-256 $actual"
    Write-Host "        Refusing to install."
    exit 4
}

Test-IconAsset $IcoPath $IcoSha256
Test-IconAsset $PngPath $PngSha256
exit 0
