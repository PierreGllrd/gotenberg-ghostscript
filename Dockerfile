# Dockerfile pour Gotenberg avec Ghostscript et serveur de post-traitement PDF/A-3
# Ajoute Ghostscript et un serveur HTTP Python pour post-traiter les PDFs

FROM gotenberg/gotenberg:8

# Installer Ghostscript et Python (nécessite les droits root temporairement)
USER root

RUN apt-get update && \
    apt-get install -y ghostscript python3 && \
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
# Démarrer Gotenberg en arrière-plan (port 3000)\n\
/usr/bin/gotenberg &\n\
\n\
# Démarrer le serveur de post-traitement en arrière-plan (port 3001)\n\
/usr/local/bin/fix-pdfa3-server.py &\n\
\n\
# Attendre que les services démarrent\n\
sleep 3\n\
\n\
# Démarrer le reverse proxy sur le port principal (PORT ou 3000)\n\
exec /usr/local/bin/reverse-proxy.py' > /usr/local/bin/start.sh && \
    chmod +x /usr/local/bin/start.sh

# Revenir à l'utilisateur gotenberg (sécurité)
USER gotenberg

# Exposer les ports
# 3000 : Gotenberg
# 3001 : Serveur de post-traitement PDF/A-3
EXPOSE 3000 3001

# Commande de démarrage personnalisée
CMD ["/usr/local/bin/start.sh"]
