# Active l'environnement virtuel Python
.\.venv\Scripts\Activate.ps1

# Met à jour le fichier requirements.txt
python -m pip freeze > requirements.txt

Write-Host "requirements.txt mis à jour."
