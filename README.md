# Token Discord Scraper

## Description
Ce script permet d'extraire des informations depuis un compte Discord à l'aide d'un token d'authentification. Il récupère diverses données telles que :

- Les informations de l'utilisateur
- La liste des serveurs et des amis
- Les connexions et sessions actives
- Les messages privés et de serveurs
- Les informations de facturation et abonnements Nitro

**⚠️ Ce script est à des fins éducatives uniquement. L'utilisation non autorisée d'un token Discord viole les conditions d'utilisation de Discord et peut entraîner un bannissement du compte concerné.**

---

## Installation
### Prérequis
- Python 3.x
- `requests`

### Installation des dépendances
```bash
pip install requests
```

### Configuration
Modifie la variable `TOKEN` dans le script avec le token du compte Discord concerné :
```python
TOKEN = "TON_TOKEN_ICI"
```

---

## Utilisation
1. Exécute le script en ligne de commande :
```bash
python script.py
```
2. Saisis le nom du dossier où seront stockées les données JSON.
3. Le script récupérera les informations et les enregistrera sous forme de fichiers JSON dans le dossier spécifié.

---

## Avertissement ⚠️
L'extraction de données sans autorisation peut être considérée comme une violation des conditions d'utilisation de Discord. **Ce projet est uniquement destiné à un usage éducatif et personnel.**

L'auteur ne sera en aucun cas responsable d'un usage illégal de ce script.

---

## Licence
MIT License

