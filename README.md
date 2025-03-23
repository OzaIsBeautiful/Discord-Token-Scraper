# Discord Token Scraper

## Description
Ce script permet d'extraire diverses données d'un compte Discord en utilisant son token d'authentification. Il récupère des informations comme les amis, les serveurs, les messages privés et les transactions.

⚠️ **Attention** : L'utilisation de ce script pour accéder aux données d'un compte sans l'autorisation du propriétaire est strictement interdite par les conditions d'utilisation de Discord et peut entraîner un bannissement du compte ou des conséquences légales.

## Prérequis
- Python 3
- Bibliothèque `requests`

## Installation
```bash
pip install requests
```

## Utilisation
1. Récupérer le token de session Discord.
2. Remplacer `TON_TOKEN_ICI` dans le script par le token récupéré.
3. Exécuter le script :
   ```bash
   python script.py
   ```
4. Suivre les instructions pour stocker les fichiers JSON des données extraites.

## Problèmes courants
### Erreur 401: Unauthorized
- Assurez-vous que le token utilisé est valide et actif.
- Vérifiez que la session Discord est bien connectée sur l'appareil utilisé.
- Discord peut invalider un token s'il est utilisé depuis un autre appareil/IP.
- Essayer d'utiliser le même User-Agent que celui du navigateur pour éviter d'être bloqué.

### Erreur 404: Not Found
- Le token peut être invalide ou expiré.
- L'API peut avoir changé ou la requête est mal formatée.

## Avertissement
L'utilisation de ce script peut entraîner des risques pour votre compte. Discord peut révoquer votre token ou suspendre votre compte en cas d'abus. Ce projet est uniquement à des fins éducatives.

