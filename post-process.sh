#!/bin/bash
# Script de post-traitement PDF/A-3 avec Ghostscript
# Appelé depuis le code PHP pour corriger les PDFs

INPUT_PDF="$1"
OUTPUT_PDF="$2"

if [ -z "$INPUT_PDF" ] || [ -z "$OUTPUT_PDF" ]; then
    echo "Usage: post-process.sh input.pdf output.pdf" >&2
    exit 1
fi

# Convertir en PDF/A-3 strict avec Ghostscript
gs -dPDFA=3 -dBATCH -dNOPAUSE -dNOOUTERSAVE \
    -sColorConversionStrategy=RGB \
    -sOutputFile="$OUTPUT_PDF" \
    -sDEVICE=pdfwrite \
    -dPDFACompatibilityPolicy=1 \
    -dUseCIEColor=true \
    "$INPUT_PDF" > /dev/null 2>&1

if [ $? -eq 0 ] && [ -f "$OUTPUT_PDF" ]; then
    echo "OK"
    exit 0
else
    echo "ERROR"
    exit 1
fi

