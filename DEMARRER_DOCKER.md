# 🐳 Démarrer Docker Desktop

## ❌ Erreur rencontrée

```
ERROR: error during connect: this error may indicate that the docker daemon is not running
```

Cela signifie que **Docker Desktop n'est pas démarré**.

## ✅ Solution : Démarrer Docker Desktop

### Étape 1 : Vérifier que Docker Desktop est installé

1. **Cherchez "Docker Desktop"** dans le menu Démarrer de Windows
2. Si vous ne le trouvez pas, téléchargez-le : https://www.docker.com/products/docker-desktop

### Étape 2 : Démarrer Docker Desktop

1. **Lancez Docker Desktop** depuis le menu Démarrer
2. **Attendez** que Docker démarre (icône dans la barre des tâches)
3. L'icône Docker doit être **verte** (pas orange/rouge)

### Étape 3 : Vérifier que Docker fonctionne

Dans PowerShell, testez :
```bash
docker --version
```

Vous devriez voir quelque chose comme :
```
Docker version 24.0.0, build ...
```

### Étape 4 : Relancer la commande build

Une fois Docker Desktop démarré, relancez :
```bash
docker build -t PierreGaillard/gotenberg-ghostscript:latest .
```

---

## 🚀 Alternative : GitHub Actions (Plus simple - Pas besoin de Docker local)

Si vous préférez ne pas utiliser Docker Desktop, utilisez **GitHub Actions** qui construit l'image automatiquement dans le cloud.

Voir : `RENDER_COM_IMAGE_DOCKER_HUB.md` → Option B

