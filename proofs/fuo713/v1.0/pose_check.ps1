$file = "robot_movement.log"
Write-Host ">> SHA-256:"
Get-FileHash -Path $file -Algorithm SHA256
if (Test-Path "Giankoof_GPG.asc") {
  Write-Host ">> GPG verify:"
  gpg --verify Giankoof_GPG.asc $file
} else {
  Write-Host ">> No signature found (Giankoof_GPG.asc)."
}
