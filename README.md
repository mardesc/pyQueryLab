# pyQueryLab

Projet personnel développé sur temps personnel autour de l’exploration, de l’analyse et de la valorisation de données. Application de bureau basée sur Qt (PySide6) et conçue autour d’une interface multi-onglets supportant Oracle, SQL Server, PostgreSQL, MySQL et SQLite, avec exports CSV/Excel/Word/PDF, exécution Python, graphiques et reporting. Stack : SQLAlchemy, NumPy, pandas, Matplotlib, Seaborn, WeasyPrint, PyInstaller

# Important

pyQueryLab is provided "as is", without warranty of any kind.

This software is experimental and intended for educational, personal and exploratory purposes.

The author assumes no responsibility or liability for any direct, indirect, incidental, consequential or other damages arising from the use, modification, distribution or inability to use this software.

Use of this software is entirely at the user's own risk.

This software is not intended for production, safety-critical or regulated environments.

# Licence

Ce projet est distribué sous licence MIT.

Voir le fichier LICENSE.

# Présentation

Le projet vise à construire progressivement un environnement de travail modulaire permettant :
- l’exploration SQL,
- l’analyse exploratoire et la valorisation de données,
- l’expérimentation autour de pandas / numpy,
- le rendu tabulaire et HTML,
- et, à terme, une interface graphique basée sur Qt.

## Version Python recommandée

Python 3.13.x (version cible actuelle)

---

# SGBD pris en charge

Le projet a vocation à fonctionner avec plusieurs systèmes de gestion de bases de données relationnelles, notamment :
- Oracle Database,
- PostgreSQL,
- SQLite,
- SQL Server,
- MySQL.

Le support initial est principalement développé et testé autour d’Oracle Database et SQLite.

L’architecture repose principalement sur SQLAlchemy afin de limiter les dépendances spécifiques à chaque moteur et favoriser une approche multi-SGBD cohérente.

---

# Statut

🚧 Prototype / développement initial

# État actuel

Projet en phase initiale de conception, prototypage et expérimentation.

Les premières versions visent principalement :
- la gestion des connexions,
- l’exécution et le rendu de requêtes SQL,
- le rendu structuré des résultats,
- une architecture modulaire et testable en ligne de commande.

L’interface graphique viendra dans un second temps.

---

# Objectifs du projet

- Exploration SQL multi-SGBD
- Analyse exploratoire et valorisation de données
- Expérimentation autour de pandas
- Architecture modulaire
- Projet pédagogique et évolutif
- Terrain d’apprentissage et de prototypage

---

# Technologies envisagées

## Base de données / SQL

- SQLAlchemy
- Oracle Database
- PostgreSQL
- SQLite
- SQL Server
- MySQL

## Analyse de données

- pandas
- numpy

## Visualisation

- matplotlib
- seaborn

## Reporting / export

- WeasyPrint

## Interface graphique (future)

- PySide6 / Qt

## Distribution

- PyInstaller

---

# Philosophie du projet

`pyQueryLab` est avant tout :
- un projet hobby,
- un terrain d’expérimentation,
- un support d’apprentissage,
- et un laboratoire technique personnel.

Le développement est volontairement progressif :
1. moteur SQL en ligne de commande
2. gestion structurée des résultats
3. intégration data-science
4. rendu HTML
5. graphiques et visualisation
6. exports CSV / Excel / Word / PDF
7. interface graphique multi-onglets
8. génération d’exécutables

L’objectif n’est pas de reproduire intégralement des outils existants, mais d’expérimenter des idées autour de l’exploration SQL, de la manipulation de données et de la visualisation légère.

Le projet est développé progressivement à titre personnel et sans engagement de calendrier ou de support.

