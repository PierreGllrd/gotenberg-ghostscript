# Gotenberg avec Ghostscript pour Render.com

## 📋 Fichiers

- `Dockerfile` : Dockerfile pour Gotenberg avec Ghostscript installé

## 🚀 Déploiement sur Render.com

### Méthode 1 : Via GitHub (Recommandé)

1. **Créer un repo GitHub** :
   - Allez sur https://github.com/new
   - Nom : `gotenberg-ghostscript` (ou autre)
   - Créez le repo

2. **Pousser ce dossier** :
   ```bash
   cd gotenberg-render
   git init
   git add Dockerfile README.md
   git commit -m "Initial commit: Gotenberg with Ghostscript"
   git branch -M main
   git remote add origin https://github.com/VOTRE_USERNAME/gotenberg-ghostscript.git
   git push -u origin main
   ```

3. **Sur Render.com** :
   - Allez dans votre service Gotenberg
   - Settings → Build & Deploy
   - Connectez votre repo GitHub
   - Render détectera automatiquement le Dockerfile
   - Déployez !

### Méthode 2 : Via Docker Hub (Alternative)

Si vous préférez utiliser Docker Hub :

```bash
# Construire l'image
docker build -t votre-username/gotenberg-ghostscript:latest .

# Pousser sur Docker Hub
docker login
docker push votre-username/gotenberg-ghostscript:latest
```

Puis sur Render.com, dans Settings, changez l'image Docker pour :
```
votre-username/gotenberg-ghostscript:latest
```

## ⚠️ Note importante

Même avec Ghostscript installé, **il n'est pas automatiquement utilisé**.

Les warnings PDF/A-3 sont **non bloquants** :
- ✅ XML Factur-X valide
- ✅ Chorus Pro accepte les factures
- ⚠️ 2 warnings techniques PDF/A-3 (non bloquants)

**Recommandation** : Si Chorus Pro accepte déjà vos factures, vous pouvez ignorer ces warnings !

