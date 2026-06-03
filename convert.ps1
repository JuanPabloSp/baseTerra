param (
    [string]$LabName
)

if ([string]::IsNullOrEmpty($LabName)) {
    Write-Host "Uso: .\convert.ps1 Lab01 (o Lab02)" -ForegroundColor Red
    exit 1
}

Write-Host "Procesando $LabName..." -ForegroundColor Cyan

$uvPath = "$env:USERPROFILE\.local\bin\uv.exe"

# Ejecutar conversión
& $uvPath run c:\Proyectos\.agents\skills\doc-converter-and-pdf-reader\scripts\convert.py "c:\Proyectos\$LabName\trabajo.md" "c:\Proyectos\$LabName\trabajo.docx"

if ($LASTEXITCODE -ne 0) {
    Write-Host "Error durante la conversión de $LabName" -ForegroundColor Red
    exit $LASTEXITCODE
}

# Crear copia .doc
Copy-Item -Path "c:\Proyectos\$LabName\trabajo.docx" -Destination "c:\Proyectos\$LabName\trabajo.doc" -Force

# Re-generar ZIP excluyendo .terraform
Get-ChildItem -Path "c:\Proyectos\$LabName" -Exclude .terraform | Compress-Archive -DestinationPath "c:\Proyectos\${LabName}.zip" -Force

Write-Host "¡Conversión y empaquetado de $LabName completado con éxito!" -ForegroundColor Green
