---
name: pc-muscles-ssh
description: "Brancher un PC Windows comme « muscles » d'un assistant cloud, via SSH sur un réseau privé. Le but premier est simple : installer le pont, puis prouver qu'il fonctionne. La personnalisation (quels jobs, quelles heures, quels garde-fous) vient seulement après, avec l'aide de l'assistant."
---

# PC muscles en SSH — BROUILLON, non publié

> Statut : brouillon à relire et à approuver avant tout autre usage.
> Aucune publication, aucun déploiement, aucune écriture dans une base
> de production, aucune soumission nulle part.
>
> Règle anti-fuite, absolue : ce fichier ne contient AUCUN secret et
> AUCUNE donnée personnelle réelle — pas d'adresse de réseau privé,
> pas d'identifiant de proxy, pas de clé privée, pas de jeton, pas de
> nom d'hôte réel, pas de chemin personnel. Partout, des placeholders
> entre `< >`, à remplacer au moment de l'installation, jamais ici.

## Le but, en une phrase

Le cerveau reste l'assistant cloud : il planifie, rédige les tâches et
vérifie les résultats. Le PC ne fournit que CPU, RAM et disque.
Les commandes passent en SSH sur un réseau privé, jamais par un port
ouvert sur internet, avec une authentification par clé, jamais par
mot de passe.

Ce skill est autonome. Il ne remplace pas un pont vers un agent local
déjà installé sur le PC : si tu veux piloter un agent local, c'est un
autre montage, avec son propre skill. Ici, aucun agent local n'est
requis sur le PC.

## Ordre du skill : d'abord le pont, ensuite le reste

1. **Partie A — installer le pont et prouver qu'il fonctionne.**
   C'est le cœur du skill. Tant que le test final de la partie A ne
   passe pas, on ne passe pas à la partie B.
2. **Partie B — personnaliser, avec l'aide de l'assistant.**
   Seulement après le pont : l'utilisateur choisit ses jobs, ses
   heures, ses garde-fous. Rien de tout ça ne bloque l'installation.

---

# PARTIE A — Installer le pont

## Prérequis

- Un PC Windows, avec un compte administrateur.
- L'utilisateur lui-même, devant le PC, pour les deux gestes que
  personne d'autre ne peut faire à sa place : ouvrir une fenêtre
  élevée, et se connecter au réseau privé dans son navigateur.
- Un assistant cloud capable d'ouvrir une session SSH sortante.
- Le PC doit être allumé et joignable au moment d'un job. Sinon, le
  job attend. On ne « réveille » pas un PC éteint avec ce skill.

## Règles dures de la partie A

- Ne jamais ouvrir le port SSH sur internet (pas de redirection de
  port sur la box/routeur).
- Ne pas toucher au pare-feu au-delà de la règle automatique créée
  par Windows lors de l'installation d'OpenSSH.
- Authentification par clé seulement. Pas de mot de passe pour SSH.
- Une clé dédiée à ce pont, jamais la clé par défaut de l'assistant
  si elle sert déjà à autre chose.
- La clé privée ne sort jamais du côté cloud, ne s'affiche jamais
  dans un fil de discussion, un rapport ou un journal.
- Les adresses du réseau privé ne s'affichent pas dans un fil sauf
  si l'utilisateur le demande explicitement.
- Chaque étape se vérifie avant de passer à la suivante. Un échec
  net vaut mieux qu'une étape « à peu près » passée.

## Étape 1 — Installer OpenSSH Server sur le PC

### Pourquoi l'utilisateur doit le faire lui-même

Installer une capacité Windows exige une fenêtre PowerShell élevée.
Un agent non élevé échoue avec :

```text
The requested operation requires elevation
```

Dans ce cas, l'état reste propre : rien n'est installé, aucun
service n'existe, rien n'écoute sur le port 22. C'est le bon
comportement. Ne pas boucler sur la même fenêtre en espérant un
autre résultat.

### Marche à suivre

L'utilisateur ouvre un Terminal / PowerShell **en tant
qu'administrateur** : clic droit → Exécuter en tant
qu'administrateur, puis Oui à l'invite de contrôle de compte
d'utilisateur (UAC).

Repères d'une fenêtre vraiment élevée :

- le titre de la fenêtre affiche « Administrateur » ;
- l'UAC a demandé un Oui à l'ouverture ;
- l'invite se trouve dans un chemin système, par exemple
  `C:\Windows\system32`.

Sans ces deux premiers signes, la fenêtre n'est pas élevée :
fermer, rouvrir correctement, puis seulement coller les commandes.

Commandes, dans l'ordre, dans la fenêtre élevée :

```powershell
Get-WindowsCapability -Online | Where-Object Name -like 'OpenSSH.Server*'
```

```powershell
Add-WindowsCapability -Online -Name OpenSSH.Server~~~~0.0.1.0
```

```powershell
Start-Service sshd
```

```powershell
Set-Service -Name sshd -StartupType Automatic
```

Vérifications (elles fonctionnent ensuite sans élévation) :

```powershell
Get-Service sshd
```

```powershell
Get-Service sshd | Select-Object Name, Status, StartType
```

```powershell
netstat -ano | findstr ":22"
```

### Critère de réussite de l'étape 1

- L'installation de la capacité retourne `Online: True` et
  `RestartNeeded: False`.
- Le service `sshd` est `Running`.
- Quelque chose écoute sur le port 22.
- Le type de démarrage vaut `Automatic`, vérifié avec la
  commande `Select-Object` ci-dessus — une commande
  `Set-Service` passée sans erreur ne suffit pas comme preuve.

### Friction connue : la deuxième tentative identique

Si une première tentative a échoué avec « requires elevation »,
une deuxième tentative dans la même fenêtre donne le même échec.
Ce n'est pas la commande qui est fausse, c'est la fenêtre qui
n'est toujours pas élevée. Changer de fenêtre, pas de commande.

## Étape 2 — Relier les deux côtés par un réseau privé

### Principe

Les deux machines rejoignent le même réseau privé. Aucun port SSH
n'est ouvert sur internet. C'est le réseau privé qui rend le PC
joignable par l'assistant, pas une exposition publique.

### Côté assistant cloud

Installer / activer le client du réseau privé, puis vérifier
l'état de connexion. À ce stade, il est normal de ne voir aucun
autre appareil : le PC n'a pas encore rejoint.

### Côté PC

L'utilisateur installe le client du réseau privé sur le PC,
depuis le site officiel du fournisseur de ce réseau, puis
se connecte lui-même dans son navigateur (connexion SSO). Un agent
ne peut pas faire cette connexion à sa place.

Les deux machines doivent être sur le même réseau privé (même
compte, même réseau) : sinon, la visibilité mutuelle de l'étape
suivante ne se produira jamais, même si chaque côté semble
« connecté » de son bord.

L'utilisateur relève ensuite, sur le PC, l'adresse privée du PC
et l'état de connexion, sans les coller dans un fil sauf s'il le
demande.

### Critère de réussite de l'étape 2 : visibilité mutuelle

- Le statut côté cloud liste le PC.
- Le statut côté PC liste l'assistant cloud.
- Les deux bords se voient. C'est la seule preuve qui compte.

Précision technique : le réseau privé transporte du TCP. Un test
de type ping ne prouve rien ici : seul un test TCP/SSH compte.

## Étape 3 — Clé dédiée, configuration, droits stricts

### 3a. Générer une clé dédiée, côté cloud

```bash
ssh-keygen -t ed25519 -f <chemin-vers-cle-dediee> -N ""
```

- Type : `ed25519`.
- Sans passphrase : c'est un choix délibéré pour un usage sans
  surveillance. Il n'est acceptable que parce que la clé est
  dédiée à ce seul pont, et révocable en une ligne (voir
  « Révocation »).
- Permissions de la clé privée : lecture par le propriétaire
  seulement.
- Ne jamais toucher à une paire de clés existante qui sert déjà
  à autre chose.
- La clé publique seule voyage vers le PC. La clé privée ne
  voyage jamais.

### 3b. Installer la clé publique côté PC

Dans une fenêtre élevée, l'utilisateur place la clé publique
dans le fichier des administrateurs :

```text
C:\ProgramData\ssh\administrators_authorized_keys
```

Ce fichier est celui du compte administrateur. Une clé placée
ailleurs (par exemple dans le fichier utilisateur classique)
ne donnera pas l'accès administrateur attendu.

### 3c. Droits stricts, avec les parenthèses quotées

Toujours dans une fenêtre élevée, appliquer des droits stricts
avec les identifiants système indépendants de la langue de
Windows. **Les parenthèses doivent être quotées**, sinon
PowerShell les interprète et la commande échoue.

Forme à utiliser (guillemets autour de chaque droit complet) :

```powershell
icacls "C:\ProgramData\ssh\administrators_authorized_keys" /inheritance:r /grant "NT AUTHORITY\SYSTEM:(F)" /grant "BUILTIN\Administrators:(F)"
```

Vérifier ensuite que les droits appliqués sont bien :

- `BUILTIN\Administrators:(F)`
- `NT AUTHORITY\SYSTEM:(F)`

Commande d'affichage des droits, dans la même fenêtre élevée :

```powershell
icacls "C:\ProgramData\ssh\administrators_authorized_keys"
```

#### Friction connue : icacls non quoté

Symptôme : PowerShell signale que `(F)` est interprété comme
un terme, avec une erreur de commande introuvable, et les
droits stricts ne sont PAS appliqués — alors que tout le reste
du collage peut sembler vert.

Fix : reposer la commande avec chaque droit complet entre
guillemets, comme ci-dessus, puis revérifier les droits.
Ne pas considérer l'étape comme faite tant que les droits
vérifiés ne correspondent pas.

### 3d. Configuration SSH : clé oui, mot de passe non

Sauvegarder d'abord le fichier de configuration, puis modifier :

```powershell
Copy-Item "C:\ProgramData\ssh\sshd_config" "C:\ProgramData\ssh\sshd_config.bak"
```

Fichier à modifier :

```text
C:\ProgramData\ssh\sshd_config
```

Valeurs à obtenir :

```text
PubkeyAuthentication yes
PasswordAuthentication no
```

Puis redémarrer le service :

```powershell
Restart-Service sshd
```

Vérifier après redémarrage que le service est toujours
`Running` et que les deux valeurs sont bien celles ci-dessus.

## Étape 4 — Premier test : une commande simple, et rien d'autre

### Commande

Côté cloud, avec la clé dédiée, en mode sans interaction
(pas d'invite de mot de passe, pas de question interactive) :

```bash
ssh -i <chemin-vers-cle-dediee> -o BatchMode=yes <utilisateur>@<PC-reseau-prive> hostname
```

- `<utilisateur>` : le compte administrateur du PC.
- `<PC-reseau-prive>` : l'adresse privée du PC sur le réseau
  privé, jamais une adresse publique.
- Si l'environnement cloud impose un proxy de sortie pour
  joindre le réseau privé, l'adapter à cet environnement. Règle
  dure, quel que soit le proxy : n'utiliser que hôte et port
  nus, sans identifiants dans l'hôte. Exemple générique, à
  adapter à ton proxy, pas une commande universelle :

```bash
ssh -o ProxyCommand="nc -X connect -x <proxy-hote>:<proxy-port> %h %p" -i <chemin-vers-cle-dediee> -o BatchMode=yes <utilisateur>@<PC-reseau-prive> hostname
```

### Friction possible : première clé d'hôte inconnue — procédure vérifiée (2026-10-25)

En mode sans interaction, une première connexion vers un hôte
jamais vu peut échouer sur la vérification de la clé d'hôte,
sans que ce soit un problème de clé, de réseau ou de droits.
Ne pas « cliquer oui » en interactif pour faire passer le
test : une acceptation sans comparaison ne prouve rien.
Procédure vérifiée, en trois temps, sans jamais désactiver
la vérification de la clé d'hôte par habitude :

1. **Lire l'empreinte locale, sur le PC.** Dans une fenêtre
   PowerShell, l'utilisateur lit l'empreinte de la clé d'hôte
   du PC, par exemple pour la clé ed25519 :

```powershell
ssh-keygen -lf C:\ProgramData\ssh\ssh_host_ed25519_key.pub
```

Si ce fichier n'existe pas, essayer la clé RSA du même
dossier. Le résultat est une ligne avec une empreinte, pas
une clé privée : cette empreinte peut être partagée avec
l'assistant sans risque, une clé privée, jamais.

2. **Récupérer l'empreinte présentée, côté cloud, sans
   l'enregistrer.** Une connexion en mode verbeux, avec un
   fichier de clés connues jetable et sans enregistrement,
   affiche l'empreinte que le PC présente réellement, avant
   toute décision d'enregistrement. Ne pas compter sur
   `ssh-keyscan` avec des options de proxy : dans certaines
   versions, ses options de type `-o` / `-O` ne sont pas
   supportées du tout.

3. **Comparer, puis seulement enregistrer si les deux
   empreintes sont identiques, caractère par caractère.**
   Si elles diffèrent, on n'enregistre rien et on cherche
   pourquoi avant de continuer. Si elles correspondent,
   enregistrer avec une acceptation pour nouvel hôte
   seulement, puis **retester avec les réglages par défaut,
   sans option spéciale** : c'est le retest par défaut qui
   prouve que l'enregistrement est au bon endroit, pas le
   test qui a servi à enregistrer.

### Friction vérifiée : une entrée pour l'adresse ne suffit pas

La vérification se fait sous le nom exact qui sera utilisé
ensuite. Une clé déjà enregistrée pour l'adresse du PC ne
satisfait pas une connexion faite par son nom d'hôte : la
vérification par nom a échoué alors que la clé était déjà
présente pour l'adresse. Enregistrer sous le nom d'hôte
exact, puis retester avec ce même nom.

### Friction vérifiée : ne pas supposer où ssh range ses clés connues

Sur une machine cloud, le dossier personnel vu par
l'interpréteur et le dossier de base du compte qui exécute
ssh peuvent être deux endroits différents, et ssh lit le
fichier de clés connues de son compte, pas forcément celui
qu'on voit en tapant `~`. Ne pas conclure « aucune clé
connue enregistrée » à partir d'un seul dossier, et ne pas
spécifier un fichier de clés connues au hasard : vérifier
quel fichier ssh lit par défaut, enregistrer là, puis
retester par défaut.

### Distinction à garder : PC occupé n'est pas PC inaccessible

Un backup ou un gros traitement en cours peut ralentir le
PC, mais il n'efface pas les clés connues et ne change pas
l'empreinte de sa clé d'hôte. Si l'erreur est une
vérification de clé d'hôte, c'est un problème de confiance,
pas de charge. À l'inverse, un PC lent ou difficile à
joindre pendant un backup n'est pas, à lui seul, une preuve
de problème de clé. Ne pas mélanger les deux diagnostics,
et ne pas lancer de gros job sur un PC déjà occupé par un
backup sans l'accord de l'utilisateur.

### Friction connue : identifiants dans l'hôte du proxy

Symptôme : échec de résolution DNS (par exemple une erreur
de type `getaddrinfo`).

Cause : des identifiants ont été glissés dans le nom d'hôte
du proxy. Le proxy ne les attend pas là.

Fix : retirer toute information d'identification de l'hôte,
ne garder que hôte et port nus, puis relancer le test.
Ne jamais afficher d'identifiants de proxy dans un fil.

Note : la première connexion à travers certains proxys peut
déclencher une demande d'approbation à l'utilisateur. Sans
cette approbation, la connexion attend. C'est normal, ce
n'est pas un échec du pont.

### Critère de réussite de la partie A

Le test est réussi si, et seulement si, toutes ces conditions
sont réunies :

- la commande renvoie le nom du PC ;
- le code de sortie vaut `0` ;
- l'authentification s'est faite par clé, sans mot de passe ;
- le mode sans interaction n'a posé aucune question.

À ce moment-là, et seulement à ce moment-là, le pont
fonctionne. On peut passer à la partie B.

## Exemple de première tâche : un test en bac à sable

Après le test `hostname`, la première tâche utile est un test
en bac à sable, dans un dossier de test séparé — jamais dans
un dossier de production ou un dossier de travail réel.

Exemple vérifié lors de la construction de ce skill : le test
d'un skill de consignes pures (aucun script, aucun outil,
aucun compte à connecter).

Vérifications faites pour ce type de test :

- clonage / copie dans le dossier de test : OK ;
- structure attendue présente : fichier principal du skill
  à la racine, fichiers de référence non vides, liens résolus ;
- zéro fichier exécutable ou outil en dehors des fichiers
  inertes fournis par l'outil de version lui-même ;
- rien à exécuter : un skill de consignes pures ne s'exécute pas.

Écart à signaler, sans l'effacer : lors de ce test, le nombre
de lignes du fichier principal différait entre une mesure du
matin et la mesure du soir. Contenu vérifié conforme à l'usage,
mais à re-vérifier à la source avant toute publication ou
réutilisation. Une différence de comptage n'est pas une preuve
de corruption, mais ce n'est pas non plus une preuve
d'identité : on revérifie, on ne suppose pas.

## Leçon de quoting entre les couches

Une commande qui fonctionne dans un terminal local ne traverse
pas forcément intacte les couches SSH puis interpréteur distant.

Règle pratique, vérifiée lors de la construction de ce skill :

- Les variables propres à un interpréteur (par exemple les
  variables automatiques PowerShell) ne traversent pas les
  couches SSH / interpréteur distant. Ne pas compter dessus.
- Préférer des commandes simples, natives de l'interpréteur
  distant, par exemple des comptages avec l'outil de recherche
  texte de l'invite de commandes plutôt qu'une construction
  PowerShell complexe passée par SSH.
- En cas de résultat vide ou étrange, simplifier la commande
  d'abord, avant de conclure que la donnée est absente.

## Inventaire à relever avant un gros job

Avant de confier un gros traitement au PC, relever et noter :

- présence et version de l'outil de version (git) ;
- présence et version de Python et de ses bibliothèques utiles ;
- présence et version de Node ;
- présence d'un outil de téléchargement en ligne de commande ;
- présence des navigateurs installés ;
- espace disque libre ;
- joignabilité du site ou du service cible depuis le PC,
  si le job en a besoin.

Cet inventaire est une grille, pas une liste d'exigences :
chaque job n'a besoin que d'une partie de la grille, et les
versions attendues dépendent du job. Aucun compte ni mot de
passe n'est requis pour un job en lecture seule sur un site
public.

## Journal des frictions

Pendant l'installation, et ensuite à chaque accrochage, noter
une entrée datée par accrochage :

- étape ;
- erreur exacte ;
- fix essayé ;
- résultat.

Ce journal est la matière première des futures versions de ce
skill : la plupart des frictions arrivent du côté PC, invisibles
pour le cerveau cloud. Les confirmations nettes méritent aussi
une ligne, courte.

## Test à froid de ce brouillon — ce qui est prouvé, ce qui ne l'est pas

Test à froid fait le soir de la rédaction, sans toucher au PC
et sans rien publier : relecture du brouillon, commande par
commande, contre les notes de l'installation réelle.

- Prouvé par l'installation réelle : le pont lui-même fonctionne
  (premier test réussi, puis première tâche en bac à sable).
- Non prouvé par ce test à froid : qu'un étranger, avec ce seul
  fichier et sans notre historique, reproduise le pont du premier
  coup sur un PC neuf. C'est le vrai test du skill, et il reste
  à faire sur un PC neuf ou réinitialisé, pas sur le PC déjà
  branché.
- Points reconstruits, pas recopiés verbatim de la soirée
  d'installation : la forme complète de la commande de droits,
  la commande de sauvegarde du fichier de configuration, la
  commande de vérification du type de démarrage, et l'exemple
  générique de proxy. Ils sont cohérents avec le résultat
  vérifié ce soir-là, mais ils doivent être confirmés sur un
  PC neuf avant de présenter ce skill comme final.

---

# PARTIE B — Personnaliser, avec l'aide de l'assistant

Cette partie ne commence qu'après le critère de réussite de la
partie A. Elle est optionnelle : le pont fonctionne déjà sans
elle. Son but est d'aider l'utilisateur à mettre ses propres
choses, sans lui imposer les choix de quelqu'un d'autre.

## Comment l'assistant aide

L'assistant pose des questions simples, une à la fois, puis
remplit le gabarit ci-dessous avec les réponses de
l'utilisateur. L'utilisateur valide le gabarit rempli avant
qu'il ne serve. Si une réponse change plus tard, on met à
jour le gabarit, on ne garde pas l'ancienne version active
en parallèle.

## Gabarit à remplir (placeholders, pas des règles)

```text
Jobs autorisés sur le PC : <liste, ou « aucun pour l'instant »>
Jobs explicitement non décidés : <liste, ou « aucun »>
Jobs à rediscuter plus tard : <liste, ou « aucun »>
Heures interdites : <plage, ou « aucune »>
Rapport après chaque job : <oui / non>
Publication ou déploiement : <toujours avec un go explicite /
  autre règle choisie par l'utilisateur>
Arrêt : <ce qui se passe quand l'utilisateur dit stop>
Comptes et mots de passe : <jamais via le pont / autre règle
  choisie par l'utilisateur>
Condition PC : <allumé et joignable requis, sinon le job attend>
Déclencheurs de délégation : <plus vite sur le PC / VM saturée /
  autre, ou « aucun »>
```

Recommandations par défaut de ce skill (l'utilisateur peut
les resserrer, et ne devrait les assouplir qu'en connaissance
de cause) :

- un rapport après chaque job ;
- rien de publié ni de déployé sans un go explicite pour ce
  geste précis ;
- un « stop » arrête tout net, dans le même tour ;
- jamais de comptes ni de mots de passe de l'utilisateur via
  le pont ;
- un job ne part que si le PC est allumé et joignable, sinon
  il attend.

Le menu n'est pas un blanc-seing : autoriser une catégorie
de jobs n'autorise pas chaque job de cette catégorie à
publier, déployer, écrire hors de son périmètre ou toucher
à un compte. Chaque publication et chaque déploiement gardent
leur propre go.

## Exemple rempli — les choix d'un premier utilisateur, pas la règle du skill

> Ce qui suit est un EXEMPLE, pour montrer à quoi ressemble
> un gabarit rempli. Ce ne sont pas les règles de ce skill,
> et un autre utilisateur n'a aucune raison de les reprendre
> telles quelles.

```text
Jobs autorisés : builds et tests de site, tests d'installation
  de skills, gros traitements (encodage, images en masse,
  gros scripts).
Jobs explicitement non décidés : pilotage direct d'un modèle
  local sur le PC.
Jobs à rediscuter plus tard : sauvegardes et archives locales
  vers le disque du PC.
Heures interdites : la nuit (choix personnel de cet utilisateur).
Rapport après chaque job : oui.
Publication ou déploiement : toujours avec un go explicite.
Arrêt : stop = arrêt net, dans le même tour.
Comptes et mots de passe : jamais via le pont.
Condition PC : allumé et joignable requis, sinon le job attend.
Déclencheurs de délégation : déléguer quand c'est plus vite
  sur le PC, et aussi quand la machine cloud est saturée
  (ressources basses, gros job déjà en cours), même si le
  gain brut est modeste, pour la délester.
```

## Révocation et arrêt définitif

Pour couper l'accès du pont, dans l'ordre :

1. Sur le PC, retirer la ligne de la clé dédiée du fichier
   des administrateurs.
2. Redémarrer le service SSH du PC.
3. Côté cloud, supprimer la paire de clés dédiée.
4. Vérifier qu'une nouvelle tentative de connexion échoue.

La révocation ne dépend d'aucun autre système : supprimer la
ligne suffit à couper l'accès, même si la clé privée existait
encore quelque part.

## Checklist de fin

Le montage est terminé quand toutes ces cases sont vraies :

- [ ] OpenSSH installé, service en marche, écoute sur le port
      22 vérifiée, démarrage automatique confirmé.
- [ ] Réseau privé rejoint des deux bords, visibilité mutuelle
      vérifiée.
- [ ] Clé dédiée générée, clé publique installée, droits
      stricts vérifiés, mot de passe désactivé vérifié.
- [ ] Premier test réussi : commande simple, code de sortie
      `0`, authentification par clé.
- [ ] Une première tâche en bac à sable réussie, dans un
      dossier de test séparé.
- [ ] Gabarit de la partie B rempli par l'utilisateur, ou
      explicitement reporté à plus tard (pas laissé vide
      par oubli).
- [ ] Procédure de révocation connue et testable.

---

## Ce que ce skill ne fait pas

- Il n'ouvre aucun port sur internet.
- Il n'installe aucun agent local sur le PC.
- Il ne gère ni comptes, ni mots de passe, ni secrets.
- Il ne publie ni ne déploie rien par lui-même.
- Il ne transforme pas un choix personnel d'un utilisateur
  (menu, heures interdites, déclencheurs) en règle pour
  les autres utilisateurs.
