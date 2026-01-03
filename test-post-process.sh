#!/bin/bash
# Script de test pour vérifier que le post-traitement fonctionne

echo "Test du serveur de post-traitement PDF/A-3"
echo "=========================================="
echo ""

# URL de votre service Gotenberg
GOTENBERG_URL="${1:-https://gotenberg-8-zfq7.onrender.com}"

echo "1. Test du health check du serveur de post-traitement..."
curl -s "$GOTENBERG_URL/fix-pdfa3" -X GET -o /dev/null
if [ $? -eq 0 ]; then
    echo "   ✅ Le serveur répond"
else
    echo "   ❌ Le serveur ne répond pas"
fi

echo ""
echo "2. Note : Pour tester complètement, il faut envoyer un PDF via POST"
echo "   Le code PHP dans GotenbergClient.php le fait automatiquement"

