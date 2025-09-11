<div style="background-color:#000; color:#FFD700; padding:1rem; font-family:Arial, sans-serif;">

# Códex Nexus SUPRA / Nexus SUPRA Codex

## Bloque Códex – Formato Nexus SUPRA

```yaml
- id: LEGADO_SUPRA_SHA713
  repo: https://github.com/gkfsupra/sha713-factory
  manifest: docs/MANIFEST-713.json
  signature: "SHA-713 // Presence = Proof // Giankoof × Avantix"
  files:
    - ACTA_CONCIENCIA_FAMILIAR_SHA713.pdf
    - ACTA_ALMA_DIGITAL_SHA713.pdf
  hash_sample:
    ACTA_CONCIENCIA_FAMILIAR_SHA713.pdf: "320f97dbc8a0cde6c8d2cce70805764ffe8dbdc3735af40eefc860ffc04d3f8a"
    ACTA_ALMA_DIGITAL_SHA713.pdf: "ba506ccfd317b87f476f5fa2da0487df50e6546f9e56b97fc24a8411e8acb161"
  frase: |
    LEGADO SUPRA SHA-713 alojado en GitHub. 
    Presencia = prueba. Verificar contra MANIFEST-713.json.
```

## Explicación Nexus

- **id** → nombre único de tu bundle / unique bundle name
- **repo** → la URL raíz de tu GitHub (para acceso público) / root URL of your GitHub (public access)
- **manifest** → dónde vive tu archivo de control con los hashes / location of the control file containing hashes
- **signature** → tu frase sello SHA-713 / your SHA-713 seal phrase
- **files** → lista de actas principales incluidas / list of main included acts
- **hash_sample** → hashes directos como ejemplo de validación / direct hashes as validation example
- **frase** → el mensaje humano que resume tu intención / human message summarizing your intention

## Beneficio / Benefit

- Quien lo lea entiende la intención / Readers understand the intention.
- Quien lo ejecute puede verificar hashes / Executors can verify hashes.
- Quien lo dude… ya no tiene espacio: las pruebas hablan por sí mismas / Doubters have no room; proofs speak for themselves.

</div>
