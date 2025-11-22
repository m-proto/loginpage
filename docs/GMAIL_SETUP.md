# Configuration Gmail pour l'envoi d'emails

⚠️ **OBLIGATOIRE** : L'application envoie TOUJOURS des emails réels. Tu DOIS configurer Gmail SMTP.

---

## Étape 1 : Activer la validation en 2 étapes

1. Va sur **https://myaccount.google.com/security**
2. Cherche "Validation en deux étapes" (ou "2-Step Verification")
3. Clique sur **"Activer"** si ce n'est pas déjà fait
4. Suis les instructions pour configurer (SMS ou autre méthode)

⚠️ **Important :** La validation en 2 étapes est OBLIGATOIRE pour créer un App Password !

---

## Étape 2 : Créer un App Password

1. Retourne sur **https://myaccount.google.com/security**
2. Cherche "Mots de passe des applications" (ou "App Passwords")
   - Si tu ne le vois pas, c'est que la validation en 2 étapes n'est pas activée
3. Clique dessus
4. Sélectionne :
   - **Application** : "Autre (nom personnalisé)"
   - **Nom** : "LogPages API" (ou ce que tu veux)
5. Clique sur **"Générer"**
6. Google va afficher un mot de passe comme : `abcd efgh ijkl mnop`
7. **COPIE CE MOT DE PASSE** (tu ne pourras plus le voir après !)

---

## Étape 3 : Configurer le fichier .env

Ouvre le fichier `.env` à la racine du projet et modifie ces lignes :

```bash
# Email Settings (Gmail SMTP)
SMTP_EMAIL=ba.mouhamed1895@gmail.com
SMTP_PASSWORD=abcdefghijklmnop  # ← Colle ton App Password ici (SANS espaces - 16 caractères)
```

⚠️ **Important :** Enlève TOUS les espaces du mot de passe !

Exemple :
- ❌ `abcd efgh ijkl mnop` (MAUVAIS - avec espaces)
- ✅ `abcdefghijklmnop` (BON - sans espaces)

---

## Étape 4 : Tester

Une fois configuré :

```bash
# Lance le backend
python main.py
```

Puis teste le login avec ton email `ba.mouhamed1895@gmail.com` - tu devrais recevoir un vrai email !

---

## Dépannage

### Erreur : "Username and Password not accepted"

- Vérifie que la validation en 2 étapes est activée
- Vérifie que tu utilises bien l'**App Password**, pas ton mot de passe Gmail normal
- Enlève tous les espaces de l'App Password

### Erreur : "SMTP Authentication Error"

- Vérifie que `SMTP_EMAIL` correspond bien à ton adresse Gmail
- Vérifie que l'App Password est correct

### L'email n'arrive pas

- Vérifie dans les **SPAMS** !
- Attends quelques minutes (parfois un délai)
- Vérifie que `SMTP_EMAIL` et `SMTP_PASSWORD` sont corrects dans le .env

---

## Sécurité

⚠️ **IMPORTANT :**

- Ne partage JAMAIS ton App Password
- Ne commit JAMAIS le fichier `.env` sur Git (il est dans `.gitignore`)
- Si tu penses que ton App Password a été compromis, révoque-le sur Google et crée-en un nouveau
