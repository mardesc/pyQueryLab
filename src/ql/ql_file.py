"""
ql_file.py

Gestionnaire des fichiers .ql utilisés par pyQueryLab.

Un fichier .ql est physiquement une archive ZIP renommée.
Il contient un ensemble de fichiers et dossiers organisés comme un mini système de fichiers embarqué.

Cette classe encapsule totalement le module zipfile afin que le reste de l'application ne manipule jamais directement ZIP.

Les chemins internes utilisent toujours '/' comme séparateur.

Le point d'entrée du conteneur est le fichier "manifest.json" situé à la racine.

Le manifeste est le fichier central de description d'un fichier .ql : il contient toutes les métadonnées nécessaires pour 
comprendre et exploiter le contenu du conteneur, comme la version du format, les informations générales du projet, les 
connexions, les scripts ou encore les ressources associées. Il joue le rôle de point d'entrée logique du fichier, permettant 
de savoir comment sont structurés et comment interpréter les éléments stockés dans l'archive ZIP

Le manifeste est manipulé, du point de vue des classes utilisatrices, comme un simple dictionnaire Python, éventuellement 
structuré avec des sous-dictionnaires imbriqués selon les besoins. Le format JSON n'intervient jamais directement dans le reste 
de l'application : il constitue uniquement un choix d'implémentation interne à la classe QLFile, utilisé pour la persistance et 
le stockage dans le fichier .ql.

Objectifs :
    - lister le contenu ;
    - lire et écrire des fichiers texte ;
    - créer et supprimer des dossiers ;
    - supprimer des fichiers ;
    - gérer le manifest ;
"""

from pathlib import Path
from tempfile import NamedTemporaryFile
from zipfile import ZIP_DEFLATED # algorithme DEFLATE : algorithme de compression le plus couramment utilisé dans les fichiers ZIP
from zipfile import ZipFile

import json


class QLFile:
    """Gestionnaire d'un conteneur .ql."""

    MANIFEST_FILE = "manifest.json"

    def __init__(self, filename: str):
        """ Ouvre ou crée un fichier .ql."""
        self.filename = Path(filename)

        if not self.filename.exists():
            self._create_archive()

    def _create_archive(self) -> None:
        """ Crée une archive vide avec un manifest minimal. """
        with ZipFile(self.filename, "w", ZIP_DEFLATED):
            pass

        self.save_manifest(
            {
                "format": "pyQueryLab",
                "version": 1
            }
        )

    def exists(self, path: str) -> bool:
        """ Vérifie l'existence d'un chemin. """
        with ZipFile(self.filename) as archive:
            return path in archive.namelist()

    def list_entries(self) -> list[str]:
        """ Retourne tous les chemins présents. """
        with ZipFile(self.filename) as archive:
            return sorted(archive.namelist())

    def list_files(self) -> list[str]:
        """ Retourne uniquement les fichiers. """
        with ZipFile(self.filename) as archive:
            return sorted(
                item
                for item in archive.namelist()
                if not item.endswith("/")
            )

    def list_directories(self) -> list[str]:
        """ Retourne uniquement les dossiers. """
        with ZipFile(self.filename) as archive:
            return sorted(
                item
                for item in archive.namelist()
                if item.endswith("/")
            )

    def read_text(self, path: str) -> str:
        """ Lit un fichier texte UTF-8. """
        with ZipFile(self.filename) as archive:
            return archive.read(path).decode("utf-8")

    def write_text(self, path: str, content: str) -> None:
        """ Crée ou remplace un fichier texte. """
        self.delete_file(path, ignore_missing=True)

        with ZipFile(
            self.filename,
            mode="a",
            compression=ZIP_DEFLATED
        ) as archive:
            archive.writestr(path, content)

    def mkdir(self, path: str) -> None:
        """ Crée un dossier. """
        if not path.endswith("/"):
            path += "/"

        with ZipFile(
            self.filename,
            mode="a",
            compression=ZIP_DEFLATED
        ) as archive:
            archive.writestr(path, "")

    def delete_file(self, path: str, ignore_missing: bool = False) -> None:
        """ Supprime un fichier. """
        if not self.exists(path):
            if ignore_missing:
                return

            raise FileNotFoundError(path)

        self._rebuild( excluded = { path } )

    def delete_directory(self, path: str) -> None:
        """ Supprime un dossier et son contenu. """
        prefix = path.rstrip("/") + "/"

        with ZipFile(self.filename) as archive:

            excluded = {
                name
                for name in archive.namelist()
                if name.startswith(prefix)
            }

        self._rebuild(excluded)

    def load_manifest(self) -> dict:
        """ Charge le manifest JSON. """
        return json.loads( self.read_text( self.MANIFEST_FILE ) )

    def save_manifest(self, data: dict) -> None:
        """ Enregistre le manifest JSON. """
        self.write_text(
            self.MANIFEST_FILE,
            json.dumps(
                data,
                indent=4,
                ensure_ascii=False
            )
        )

    def _rebuild(self, excluded: set[str]) -> None:
        """
        Reconstruit complètement l'archive.
        La méthode _rebuild() est nécessaire parce qu'un fichier ZIP n'est pas conçu pour supprimer ou modifier directement un 
        élément existant. Lorsqu'on ajoute un fichier à une archive ZIP, les nouvelles données sont généralement ajoutées à la 
        fin de l'archive et l'index interne est mis à jour. En revanche, supprimer physiquement une entrée au milieu de l'archive 
        nécessiterait de réorganiser l'ensemble des données stockées. La méthode _rebuild() contourne cette limitation en créant 
        une nouvelle archive temporaire, puis en recopiant un à un tous les fichiers de l'archive d'origine sauf ceux qui doivent 
        être supprimés. Une fois la copie terminée, l'archive temporaire remplace l'archive initiale. 

        Note: NamedTemporaryFile est une fonction du module standard tempfile qui permet de créer un fichier temporaire sur le 
        disque avec un nom réel et unique généré automatiquement par le système d'exploitation. Son nom est accessible via l'attribut 
        name. Dans le cas de la méthode _rebuild(), il sert à construire une nouvelle archive ZIP complète sans risquer de corrompre 
        l'archive d'origine : toutes les données sont d'abord écrites dans ce fichier temporaire, puis, une fois l'opération terminée 
        avec succès, le fichier temporaire remplace l'ancien fichier .ql.
        """
        with NamedTemporaryFile(delete=False) as temp:

            with ZipFile(self.filename) as src:
                with ZipFile(temp.name, "w") as dst:

                    for item in src.infolist():

                        if item.filename in excluded:
                            continue

                        dst.writestr(
                            item,
                            src.read(item.filename)
                        )

            Path(temp.name).replace(
                self.filename
            )
