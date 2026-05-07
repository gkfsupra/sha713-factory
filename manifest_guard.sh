#!/bin/bash
echo "𓂀 INICIANDO VIGILANCIA DE MANIFIESTO..."
COUNT=$(ls -1 | grep -i "manifest-713.json" | wc -l)
if [ $COUNT -gt 1 ]; then
    echo "❌ ALERTA: COLISIÓN DETECTADA. Múltiples versiones encontradas."
    ls | grep -i "manifest-713.json"
    exit 1
else
    echo "✅ COHERENCIA TOTAL: Un solo vector de identidad detectado."
fi
