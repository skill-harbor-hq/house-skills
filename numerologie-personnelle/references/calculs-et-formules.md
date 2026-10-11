# Calculs et formules — Calculations and formulas

**Statut de ce document : c'est LA référence de méthode du skill.** Tous les calculs du profil, des cycles et du journal se font avec ces formules-ci, dans cet ordre, et avec les résultats intermédiaires montrés. Aucun calcul de mémoire, aucun emprunt à une autre variante en cours de route.

**Ce qui est exact ici : l'arithmétique.** Les formules sont publiques, écrites noir sur blanc, et n'importe qui peut les refaire à la main et retomber sur le même résultat. **Ce qui relève de la tradition : les significations** attachées aux nombres (section Associations, plus bas), toujours étiquetées « tradition » et jamais présentées comme des faits.

## 0. La réduction (utilisée partout)

```
réduire(n) :
  tant que n > 9 ET n n'est pas dans {11, 22, 33} :
      n = somme des chiffres de n
  retourner n
```

- Exemples de réduction : 19 → 1 + 9 = 10 → 1 + 0 = **1** · 29 → 2 + 9 = **11** (arrêt, nombre maître) · 39 → 3 + 9 = 12 → 1 + 2 = **3**.
- **Nombres maîtres 11, 22, 33 :** selon la tradition, on ne les réduit pas. La réduction s'arrête dès qu'elle les rencontre, **y compris à une étape intermédiaire** (par exemple un jour de naissance 29 compte pour 11 dans la somme du chemin de vie). C'est une convention de la tradition, assumée et appliquée partout de la même façon dans ce skill.

## 1. Chemin de vie / Life path

### Méthode principale (celle du skill, toujours)

1. Réduire le **mois** de naissance : `m = réduire(mois)`.
2. Réduire le **jour** de naissance : `j = réduire(jour)`.
3. Réduire l'**année** de naissance : `a = réduire(somme des chiffres de l'année)`.
4. Additionner : `total = m + j + a`, puis `chemin de vie = réduire(total)`.

**Justification du choix :** c'est la méthode la plus enseignée dans la tradition contemporaine, et surtout elle rend chaque composante (mois, jour, année) vérifiable séparément et laisse apparaître les nombres maîtres intermédiaires (un jour 29 compte pour 11, pas pour 2). Le skill a besoin d'UNE méthode fixe pour être reproductible : c'est celle-ci, partout, sans exception.

### Variante documentée (jamais utilisée dans un profil du skill)

Variante « somme directe » : additionner tous les chiffres de la date complète d'un coup, puis réduire. Elle peut donner un résultat **différent** (voir l'exemple C : méthode principale 6, variante 33). Quand un utilisateur arrive avec un nombre calculé ailleurs, on nomme l'écart et la méthode probable ; on ne mélange jamais les deux méthodes dans un même profil.

### Exemple A (complet) : naissance le 1990-03-15

- Mois : 3 → **3**
- Jour : 15 → 1 + 5 = **6**
- Année : 1990 → 1 + 9 + 9 + 0 = 19 → 1 + 9 = 10 → 1 + 0 = **1**
- Total : 3 + 6 + 1 = 10 → 1 + 0 = **1**
- **Chemin de vie : 1**

### Exemple B (complet, nombre maître) : naissance le 2003-02-04

- Mois : 2 → **2**
- Jour : 4 → **4**
- Année : 2003 → 2 + 0 + 0 + 3 = **5**
- Total : 2 + 4 + 5 = **11** → arrêt, nombre maître, on ne réduit pas
- **Chemin de vie : 11**

### Exemple C (complet, divergence de variante) : naissance le 1985-12-07

- Mois : 12 → 1 + 2 = **3**
- Jour : 7 → **7**
- Année : 1985 → 1 + 9 + 8 + 5 = 23 → 2 + 3 = **5**
- Total : 3 + 7 + 5 = 15 → 1 + 5 = **6**
- **Chemin de vie (méthode principale) : 6**
- Variante somme directe, pour mémoire : 1 + 2 + 0 + 7 + 1 + 9 + 8 + 5 = 33, nombre maître, donc 33. Les deux méthodes divergent sur cette date ; le skill retient **6** et le dit si on lui présente 33.

## 2. Nombre d'expression / destinée — Expression / destiny number (optionnel)

Uniquement si l'utilisateur fournit son **nom complet de naissance** pour ce calcul. Chaque lettre reçoit sa valeur pythagoricienne, on additionne tout, on réduit.

### Table lettres-chiffres pythagoricienne (complète)

| Valeur | Lettres |
|---|---|
| 1 | A J S |
| 2 | B K T |
| 3 | C L U |
| 4 | D M V |
| 5 | E N W |
| 6 | F O X |
| 7 | G P Y |
| 8 | H Q Z |
| 9 | I R |

- Accents et ligatures : on replie sur la lettre de base (É È Ê → E, Ç → C, À → A, Ï → I, etc.). Espaces, traits d'union et apostrophes sont ignorés. Tout caractère hors A à Z après repliement : demander à l'utilisateur plutôt qu'inventer une valeur.
- Formule : `expression = réduire(somme des valeurs de toutes les lettres du nom complet de naissance)`.

### Exemple E (complet) : « Léa Martin »

- Prénom : L = 3, É → E = 5, A = 1 → sous-total 3 + 5 + 1 = 9
- Nom : M = 4, A = 1, R = 9, T = 2, I = 9, N = 5 → sous-total 4 + 1 + 9 + 2 + 9 + 5 = 30
- Total : 9 + 30 = 39 → 3 + 9 = 12 → 1 + 2 = **3**
- **Nombre d'expression : 3**

## 3. Année personnelle / Personal year

Pour une année civile donnée, à partir de la date de naissance :

1. `j = réduire(jour de naissance)`
2. `m = réduire(mois de naissance)`
3. `a = réduire(somme des chiffres de l'année civile visée)`
4. `année personnelle = réduire(j + m + a)`

Note de tradition : l'année personnelle court, selon les écoles, du 1er janvier ou de l'anniversaire. Le skill utilise l'**année civile** (1er janvier au 31 décembre) pour rester calculable sans ambiguïté, et le dit dans le profil.

## 4. Mois personnel / Personal month

`mois personnel = réduire(année personnelle + numéro du mois civil)`

Le numéro du mois est additionné **tel quel** (octobre = 10), pas pré-réduit : c'est ce qui laisse apparaître un mois personnel 11 quand le calcul le donne (voir l'exemple D).

## 5. Jour personnel / Personal day

`jour personnel = réduire(mois personnel + numéro du jour du mois)`

Même convention : le jour est additionné tel quel (le 10 = 10), puis on réduit, avec arrêt sur 11, 22 ou 33.

### Exemple D (complet, cycles) : née le 1990-03-15 (exemple A), cycles au 2026-10-10

- Année personnelle 2026 : jour de naissance 15 → 6 ; mois de naissance 3 → 3 ; année civile 2026 → 2 + 0 + 2 + 6 = 10 → 1 ; total 6 + 3 + 1 = 10 → **1**. Année personnelle : **1**
- Mois personnel, octobre 2026 : 1 + 10 = **11** → arrêt, nombre maître. Mois personnel : **11**
- Jour personnel, le 10 octobre 2026 : 11 + 10 = 21 → 2 + 1 = **3**. Jour personnel : **3**

## Associations traditionnelles (tradition, pas des faits)

**Étiquette permanente :** ce qui suit est ce que la tradition numérologique associe à chaque nombre. Ce ne sont ni des traits prouvés, ni des prévisions. Le skill cite la ligne, puis laisse l'utilisateur juger dans son journal.

| Nombre | Association traditionnelle (un trait, une ligne) |
|---|---|
| 1 | Tradition : élan, autonomie, commencement |
| 2 | Tradition : relation, patience, diplomatie |
| 3 | Tradition : expression, créativité, parole |
| 4 | Tradition : structure, travail, stabilité |
| 5 | Tradition : mouvement, changement, liberté |
| 6 | Tradition : responsabilité, foyer, soin |
| 7 | Tradition : introspection, étude, recul |
| 8 | Tradition : matière, pouvoir, réalisation |
| 9 | Tradition : accomplissement, don, clôture |
| 11 | Tradition : intuition, sensibilité, inspiration (nombre maître) |
| 22 | Tradition : construction à grande échelle, « maître bâtisseur » (nombre maître) |
| 33 | Tradition : service, transmission, « maître enseignant » (nombre maître) |

Appliquées aux cycles, les mêmes lignes se lisent en thème de période selon la tradition : une année personnelle 1 serait un thème de commencement, une année 9 un thème de clôture, et ainsi de suite. Toujours « selon la tradition », jamais « cette année sera ».
