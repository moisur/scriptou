@echo off
CLS
ECHO =======================================================
ECHO    Lancement de l'Analyseur de Transcription YouTube
ECHO =======================================================
ECHO.

REM --- Configuration ---
SET PROJECT_DIR=C:\Users\jean-\Desktop\TRANSCRIPT
SET VENV_ACTIVATE_SCRIPT_PATH=%PROJECT_DIR%\venv\Scripts\activate.bat
SET PYTHON_IN_VENV=%PROJECT_DIR%\venv\Scripts\python.exe
SET FLASK_APP_FILE=app.py
SET BROWSER_URL=http://127.0.0.1:5001
SET SERVER_START_TIMEOUT=5
REM --- Fin Configuration ---

ECHO Repertoire du projet: %PROJECT_DIR%

REM Vérifications (on les garde, elles sont utiles)
IF NOT EXIST "%PROJECT_DIR%" (ECHO ERREUR: Repertoire projet '%PROJECT_DIR%' non trouve.& GOTO EndScriptWithError)
IF NOT EXIST "%VENV_ACTIVATE_SCRIPT_PATH%" (ECHO ERREUR: Script activation venv '%VENV_ACTIVATE_SCRIPT_PATH%' non trouve.& GOTO EndScriptWithError)
IF NOT EXIST "%PYTHON_IN_VENV%" (ECHO ERREUR: Python dans venv '%PYTHON_IN_VENV%' non trouve.& GOTO EndScriptWithError)
IF NOT EXIST "%PROJECT_DIR%\%FLASK_APP_FILE%" (ECHO ERREUR: Fichier Flask app '%PROJECT_DIR%\%FLASK_APP_FILE%' non trouve.& GOTO EndScriptWithError)
ECHO Toutes les verifications de fichiers sont OK.
ECHO.

ECHO Lancement du serveur Flask en arriere-plan...
REM La commande clé:
REM On utilise START pour lancer une nouvelle fenêtre.
REM Le titre de la fenêtre sera "TranscriptAppServer".
REM /D définit le répertoire de travail pour la nouvelle commande.
REM CMD /C exécute la commande entre guillemets puis se termine.
REM A l'intérieur de CMD /C:
REM   1. On appelle le script d'activation du venv.
REM   2. ET (&&) si l'activation réussit, on lance python app.py.
REM      On utilise %PYTHON_IN_VENV% pour être sûr d'utiliser le python du venv.
START "TranscriptAppServer" /D "%PROJECT_DIR%" /MIN CMD /C "CALL "%VENV_ACTIVATE_SCRIPT_PATH%" && "%PYTHON_IN_VENV%" "%FLASK_APP_FILE%""

ECHO Serveur Flask en cours de lancement (dans une fenetre separee)...
ECHO Attente de %SERVER_START_TIMEOUT% secondes pour que le serveur demarre...
TIMEOUT /T %SERVER_START_TIMEOUT% /NOBREAK > NUL

ECHO Ouverture de l'application dans le navigateur: %BROWSER_URL%
START "" "%BROWSER_URL%"

GOTO EndScriptNormal

:EndScriptWithError
ECHO.
ECHO --- SCRIPT INTERROMPU A CAUSE D'UNE ERREUR ---
PAUSE
EXIT /B 1

:EndScriptNormal
ECHO.
ECHO =====================================================================
ECHO L'application devrait etre ouverte dans votre navigateur.
ECHO Le serveur Flask tourne dans une fenetre separee nommee "TranscriptAppServer".
ECHO Pour arreter l'application, fermez cette fenetre de serveur.
ECHO =====================================================================
ECHO (Cette fenetre va se fermer automatiquement dans 10 secondes)
TIMEOUT /T 10 > NUL
EXIT /B 0
