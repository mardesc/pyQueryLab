"""
Fonction :
    - si le chemin fourni est un fichier : affiche les N dernières lignes du fichier ;

    - si le chemin fourni est un dossier : recherche le fichier le plus récemment modifié, puis affiche les N dernières lignes.

Le résultat est retourné sous forme d'un dictionnaire que le runner pourra ensuite afficher en console ou transmettre à une future interface Qt.
"""

from pathlib import Path


def tail_file(filename: Path, line_count: int) -> list[str]:
    """
    Retourne les N dernières lignes d'un fichier texte.
    """

    with open(
        filename,
        mode="r",
        encoding="utf-8",
        errors="replace"
    ) as file:

        lines = file.readlines()

    return [line.rstrip("\n") for line in lines[-line_count:]]


def find_latest_file(directory: Path) -> Path:
    """
    Recherche le fichier le plus récemment modifié dans un dossier.
    """

    files = [
        item
        for item in directory.iterdir()
        if item.is_file()
    ]

    if not files:
        raise FileNotFoundError(
            f"Aucun fichier trouvé dans {directory}"
        )

    return max(
        files,
        key=lambda item: item.stat().st_mtime
    )


def run(path: str, line_count: int = 10) -> dict:
    """
    Point d'entrée appelé par le runner.

    Parametres:
        - path: Nom d'un fichier ou d'un dossier.
        - line_count: Nombre de lignes à retourner.

    Returne : dict : Résultat standardisé.
    """

    # Si path est absolu, target est ce chemin path normalisé (avec séparateurs cohérents et résolution des éléments "." et "..")
    # Sinon, target est le chemin absolu obtenu à partir du répertoire courant et du chemin relatif fourni
    target = Path(path).resolve()

    if not target.exists():
        raise FileNotFoundError(path)

    if target.is_dir():
        logfile = find_latest_file(target)
    else:
        logfile = target

    lines = tail_file(
        logfile,
        line_count
    )

    return {
        "format": "text",
        "title": "Dernières lignes du journal",
        "file": str(logfile),
        "line_count": len(lines),
        "data": "\n".join(lines)
    }
