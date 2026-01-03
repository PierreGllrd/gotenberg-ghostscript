# Dockerfile pour Gotenberg avec Ghostscript sur Render.com
# Ce Dockerfile ajoute Ghostscript à l'image Gotenberg officielle
# pour permettre le post-traitement PDF/A-3

FROM gotenberg/gotenberg:8

# Installer Ghostscript (nécessite les droits root temporairement)
USER root

RUN apt-get update && \
    apt-get install -y ghostscript && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Vérifier que Ghostscript est bien installé
RUN gs --version

# Revenir à l'utilisateur gotenberg (sécurité)
USER gotenberg

# Note : Pour utiliser Ghostscript, vous devrez soit :
# 1. Créer un endpoint custom dans Gotenberg (complexe)
# 2. Accepter les warnings PDF/A-3 (recommandé - ils sont non bloquants)
# 3. Modifier le code PHP pour appeler Ghostscript via SSH/API

