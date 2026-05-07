Commandes basiques GIT BASH
/////////////////
GIT
/////////////////
git
> infos et index des commandes/utilisation des commandes

/////////////////
CHANGE DIRECTORY CD
/////////////////
Ex à partir de :  /c/repo/python

Poursuivre en relatif : 
cd bubble/
> /c/repo/python/bubble

Remonter en relatif
cd ..
> /c/repo

En absolu (pour repo non partageable)
cd /c/repo/python


//////////////////////
LS (pas git)
/////////////////////

ls
 > liste les dossiers contenus
ls -a
> montre tout (même dossiers cachés)

ls -1
> avec leurs infos (droits, auteurice, date..)

-rw-r--r-- = readwrite read read (droits d'admin sur le dossier/fichier)

//////////////////////
CLEAR SCREEN
/////////////////////
clear

//////////////////////
COmmencer REPO
/////////////////////

git init
> génère dossier caché .git, nécéssaire, à déplacer avec le reste le cas échéant. A supp pour revenir à l'état de dossier classique
> Pas de repo dans un repo

//////////////////////
Git STATUS Etat des fichiers inclus/exclus..
/////////////////////

git status

//////////////////////
INCLURE add
/////////////////////

git add <Fichier>
> inclure fichier

git add *_variant*.py 
> inclure whatever_variantwhatever
git add .
> inclure tout

git add Assets/ *png
> inclure les .png du dossier Assets 

//////////////////////
EXCLURE add
/////////////////////


//////////////////////
COMMIT commentaire engageant (= balisage)
/////////////////////
Pas de commit possible sans add, il faut qqch à commenter

git commit -m "<Message>"
git commit -a -m "<Message>" 
> ajoute un add (mais seulement des fichiers déjà connus de git !)

//////////////////////
DIFF
/////////////////////

git diff 
> montrer status, sur seulement ce qui a changé
git diff <File>

//////////////////////
RESTORE
/////////////////////

git restore <File>
> restore possible jusqu'au dernier commit

git restore --staged <File>
> 

//////////////////////
QUIT
/////////////////////

Q
> je sais plus mais "quitter"

//////////////////////
STAGES
/////////////////////

git staged 
> Jsais plus

//////////////////////
LOG
/////////////////////

git log
> Les commits

git log -6
> Les 6 derniers logs

git log --oneline


////////////////////
MEMO de création lien remote
////////////////////

Attention, il faut au moins un commit pour le setupstream !

j.patard@UNITY-11 MINGW64 /c/Repo/Python/Cassebrique (main)
$ git remote add origin https://github.com/Julule/break_out.git
> lien pris du repo sur github

j.patard@UNITY-11 MINGW64 /c/Repo/Python/Cassebrique (main)
$ git remote -v
origin  https://github.com/Julule/break_out.git (fetch)
origin  https://github.com/Julule/break_out.git (push)

j.patard@UNITY-11 MINGW64 /c/Repo/Python/Cassebrique (main)
$ git push -u origin main
Enumerating objects: 3, done.
Counting objects: 100% (3/3), done.
Delta compression using up to 28 threads
Compressing objects: 100% (2/2), done.
Writing objects: 100% (3/3), 1.93 KiB | 1.93 MiB/s, done.
Total 3 (delta 0), reused 0 (delta 0), pack-reused 0 (from 0)
To https://github.com/Julule/break_out.git
 * [new branch]      main -> main
branch 'main' set up to track 'origin/main'.

////////////////////
REMOTE
////////////////////

$ git remote -v
> c'est l'emplacement du repo lié sur github
origin  https://github.com/Julule/Superprog.git (fetch)
origin  https://github.com/Julule/Superprog.git (push)

$ git remote remove origin
> permet, après un clone, de couper le lien pour pouvoir push/pull dessus


////////////////////
PUSH PULL
////////////////////
Après une modification :
$ git add <Fichier>
$ git commit message
$ git push 

$ git pull
> Récupérer / en début de session

$ git push
> Téléverser en fin de session/pour partager

////////////////////
CLONE repo (pré-créé sur github)
////////////////////

j.patard@UNITY-11 MINGW64 /c/Repo/ATHOME
$ git clone https://github.com/Julule/Superprog.git AT_HOME_EXEMPLE(nom du dossier home)
> pas besoin de origin truc

////////////////////
BRANCH
////////////////////

$ git branch other_branch
> créer une branche

$ git switch other_branch
> on se trouve maintenant à other_branch (ce qui est indiqué entre parenthèses après le chemin de loc)

$ git merge 
$ git merge origin/other_branch
> copie des commits de other_branch sur branche de loc

$ git push --set-upstream origin other_branch
> push la branche la première fois

$ git branch -d other_branch
> supprimer la branche
$ git push -d other_branch
> push la suppression

$ git branch -a
> voir les branches

$ git config --global user.name "Jul"
$ git config --global user.email "julie@mail.mail"
> changer nom/email en global (pour tous les repos du pc)

$ git config --local user.name "Jul"
> changer en local

////////////////////
Fichier GIT IGNORE
////////////////////

C'est un ficher avec l'ext .gitignore, qui sert à dire à git d'ignorer certains fichiers (notamment les fichiers spécifiques VS, que git pige pas)

On peut le faire à la main, mais sinon, il est auto généré si on créé le repo depuis visual code

Il existe des templates basique en ligne, voir marque pages c#


















