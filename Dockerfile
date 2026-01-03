# Dockerfile pour Gotenberg avec Ghostscript et serveur de post-traitement PDF/A-3
# Ajoute Ghostscript et un serveur HTTP Python pour post-traiter les PDFs

FROM gotenberg/gotenberg:8

# Installer Ghostscript et Python (nécessite les droits root temporairement)
USER root

RUN apt-get update && \
    apt-get install -y ghostscript python3 netcat-openbsd && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Vérifier que Ghostscript est bien installé
RUN gs --version

# Copier les scripts
COPY fix-pdfa3-server.py /usr/local/bin/fix-pdfa3-server.py
COPY post-process.sh /usr/local/bin/post-process.sh
COPY reverse-proxy.py /usr/local/bin/reverse-proxy.py

# Rendre les scripts exécutables
RUN chmod +x /usr/local/bin/fix-pdfa3-server.py && \
    chmod +x /usr/local/bin/post-process.sh && \
    chmod +x /usr/local/bin/reverse-proxy.py

# Créer le script de démarrage qui lance tous les services
RUN echo '#!/bin/bash\n\
set -e\n\
\n\
# Démarrer Gotenberg en arrière-plan (port 3000 interne)\n\
/usr/bin/gotenberg &\n\
GOTENBERG_PID=$!\n\
\n\
# Démarrer le serveur de post-traitement en arrière-plan (port 3001 interne)\n\
/usr/local/bin/fix-pdfa3-server.py &\n\
POST_PROCESS_PID=$!\n\
\n\
# Attendre que les services démarrent\n\
echo "Waiting for services to start..."\n\
for i in {1..10}; do\n\
    if nc -z localhost 3000 && nc -z localhost 3001; then\n\
        echo "All services started"\n\
        break\n\
    fi\n\
    sleep 1\n\
done\n\
\n\
# Démarrer le reverse proxy sur le port principal (PORT ou 3000)\n\
# Le reverse proxy écoute sur le port exposé par Render et route vers les services internes\n\
echo "Starting reverse proxy on port ${PORT:-3000}"\n\
exec /usr/local/bin/reverse-proxy.py' > /usr/local/bin/start.sh && \
    chmod +x /usr/local/bin/start.sh && \
    apt-get update && apt-get install -y netcat-openbsd && apt-get clean && rm -rf /var/lib/apt/lists/*

# Revenir à l'utilisateur gotenberg (sécurité)
USER gotenberg

# Exposer les ports
# 3000 : Gotenberg
# 3001 : Serveur de post-traitement PDF/A-3
EXPOSE 3000 3001

# Commande de démarrage personnalisée
CMD ["/usr/local/bin/start.sh"]
