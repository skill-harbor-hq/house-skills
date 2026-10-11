# Dates et protocole / Dates and protocol: Mercury retrograde 2026-2027

Source unique des dates de ce skill: extrait fidele, ligne par ligne, de la section Retrogrades du calendrier `references/calendar-2026-2027.md` du skill Journal Celeste (calendrier verifie entre deux sources ephemerides a sa creation). Aucune date inventee, aucune date ajoutee. Si une periode n'est pas dans la table ci-dessous, elle n'est pas annoncee.

Note de couverture: le calendrier source donne les retrogrades de Mercure pour 2026 et 2027 au complet (3 periodes par annee, le rythme habituel de Mercure). Aucun trou signale dans la source pour Mercure 2026-2027. Au-dela du 31 decembre 2027, la table s'arrete: le dire clairement plutot que de deviner, et proposer de prolonger la table a partir d'un calendrier ephemeride verifie entre deux sources.

Retrograde motion is apparent motion: Mercury never actually reverses; from Earth it only looks like it moves backwards for a few weeks because Earth overtakes it on its own orbit. La retrogradation est un mouvement apparent: Mercure ne recule jamais vraiment; vu de la Terre, il semble reculer pendant quelques semaines parce que la Terre le depasse sur son orbite.

## Table des retrogrades de Mercure 2026

| Debut (retrograde from) | Fin (direct again) | Signe (sign) |
|---|---|---|
| Feb 26, 2026 | Mar 20, 2026 | Pisces |
| Jun 29, 2026 | Jul 23, 2026 | Cancer |
| Oct 24, 2026 | Nov 13, 2026 | Scorpio |

## Table des retrogrades de Mercure 2027

| Debut (retrograde from) | Fin (direct again) | Signe (sign) |
|---|---|---|
| Feb 9, 2027 | Mar 3, 2027 | Pisces -> Aquarius |
| Jun 10, 2027 | Jul 4, 2027 | Cancer -> Gemini |
| Oct 7, 2027 | Oct 28, 2027 | Scorpio -> Libra |

Lecture de la table: une date D est "en retrograde" si Debut <= D <= Fin pour l'une des lignes. Le jour du debut et le jour de la fin comptent comme dans la periode (convention du calendrier source, qui donne la periode du premier au dernier jour).

## Fonction "retrograde oui / non"

1. Prendre la date du jour (ou la date demandee).
2. La comparer aux 6 lignes ci-dessus, bornes incluses.
3. Oui: repondre oui, avec la periode complete et le signe. Non: repondre non, avec la prochaine periode a venir (ou preciser que la derniere periode couverte est passee si la date depasse la table).

## Alertes

Le skill n'a aucun canal push propre. Deux modes, selon le profil:

1. **Controle de session (defaut).** Au debut d'une conversation, si la date du jour tombe a J-3 d'un debut de periode, ou le jour meme du debut (J-0), et que les alertes sont activees dans le profil, surfacer l'alerte une seule fois.
2. **Controle planifie (seulement avec consentement explicite).** L'assistant peut configurer une verification recurrente avec l'outil de planification de son hote. Consentement par utilisateur, revocable, jamais presume a l'installation.

Format d'alerte (3 lignes + 1 question), ton calme, jamais anxiogene:

```
Mercure retrograde: [date de debut] au [date de fin], en [signe].
Mouvement apparent seulement: Mercure ne recule pas vraiment.
Lentille de la tradition: revoir, relire, prevoir une marge, verifier deux fois.
Tu veux ouvrir le mini-journal pour cette periode?
```

EN equivalent, same shape. Une alerte par declencheur (J-3, puis J-0); si l'utilisateur l'ignore, elle ne se repete pas. Une periode de journal ne s'ouvre que si l'utilisateur dit oui.

## Mini-journal: protocole

Fichier local de l'utilisateur: `~/mercure-retrograde/journal.md` (dossier au choix de l'utilisateur). Une seule periode a la fois.

### Ouverture (a J-0 ou quand l'utilisateur accepte l'alerte)

```markdown
## Mercure retrograde: [debut] au [fin] - signe: [signe] - statut: ouvert
**A observer (mots de l'utilisateur):** ...
### Entrees
```

### Entree en 30 secondes

L'utilisateur dicte librement. L'assistant extrait seulement: la date, une note d'humeur si elle est donnee, et une ligne de fait dans les mots de l'utilisateur. Relire l'entree telle qu'enregistree. Jamais d'interpretation pendant la periode, sauf demande explicite.

```markdown
- [YYYY-MM-DD] humeur [n/10 si donnee] - [une ligne, mots de l'utilisateur]
```

### Bilan de fin de periode

1. Declencheur: la periode est terminee (date de fin passee) ou l'utilisateur demande le bilan.
2. Relire les entrees du fichier, les resumer en 2 ou 3 lignes sans ajouter de sens.
3. Poser la seule question de verdict: "Ton verdict: ca a resonne, pas resonne, ou entre les deux?" / "Your verdict: resonated, did not resonate, or in between?"
4. Ecrire le verdict et un resume d'une ligne (mots de l'utilisateur de preference) dans `journal.md`, marquer la periode fermee:

```markdown
### Bilan
**Relecture de l'assistant:** [2 ou 3 lignes, faits seulement]
**Verdict de l'utilisateur:** resonne | pas resonne | entre les deux - [ses mots si donnes]
```

5. Apres le bilan, le skill se met en pause: aucun suivi, aucune statistique au-dela de cette periode. Une nouvelle periode ne s'ouvre qu'a la demande de l'utilisateur.
