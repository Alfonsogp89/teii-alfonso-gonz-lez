# Tecnologías Específicas en Ingeniería Informática • Configuración de `git`

- [Tecnologías Específicas en Ingeniería Informática • Configuración de `git`](#tecnologías-específicas-en-ingeniería-informática--configuración-de-git)
  - [Instalación de `git`](#instalación-de-git)
  - [Configuración de `git`](#configuración-de-git)
  - [Referencias](#referencias)

___

## Instalación de `git`

Instalación de `git` en Linux:

```bash
$ sudo apt-get -y install git
```

En MacOS `git` está instalado por defecto.

Para comprobar que `git` está instalado:

```bash
$ git version
git version 2.34.1
```

## Configuración de `git`

La herramienta `git` se puede configurar con ámbito de sistema, usuario o global
y repositorio. En nuestro caso, asumiremos que la configuración es la misma para
todos los repositorios del usuario.

:warning: Usa tu nombre y apellido(s), y tu dirección de correo electrónico de
la UMU.

<!-- markdownlint-disable MD013 -->
```bash
$ git config --global user.name "Nombre Apellido1 [Apellido2]"
$ git config --global user.email "alumno@um.es"
$ git config --global core.autocrlf input
$ git config --global core.editor "vim"            # Alternativa: nano
$ git config --global push.default matching        # Alternativa: simple
$ git config --global color.ui auto
$ git config --global alias.mlog    "log --graph --date-order --date=short --pretty=format:'%C(auto)%h%d %C(reset)%s %C(bold blue)%ce %C(reset)%C(green)%cr (%cd)'"
$ git config --global alias.mlogall "mlog --all"
$ git config --global init.defaultBranch main
```
<!-- markdownlint-enable MD013 -->

La configuración actual se puede consultar con `git config`:

<!-- markdownlint-disable MD013 -->
```bash
$ git config --global --list
user.name=Nombre Apellido1 [Apellido2]
user.email=alumno@um.es
color.ui=auto
core.autocrlf=input
core.editor=vim
push.default=matching
alias.mlog=log --graph --date-order --date=short --pretty=format:'%C(auto)%h%d %C(reset)%s %C(bold blue)%ce %C(reset)%C(green)%cr (%cd)'
alias.mlogall=mlog --all
default.Branch=main
```
<!-- markdownlint-enable MD013 -->

La configuración se almacena en el archivo `$HOME/.gitconfig`:

<!-- markdownlint-disable MD013 -->
```bash
$ cat $HOME/.gitconfig
[user]
    name = Nombre Apellido1 [Apellido2]
    email = alumno@um.es
[color]
    ui = auto
[core]
  autocrlf = input
  editor = vim
[push]
  default = matching
[alias]
  mlog = log --graph --date-order --date=short --pretty=format:'%C(auto)%h%d %C(reset)%s %C(bold blue)%ce %C(reset)%C(green)%cr (%cd)'
  mlogall = mlog --all
[init]
  default.Branch = main
```
<!-- markdownlint-enable MD013 -->

:pushpin: En la máquina virtual de la asignatura, el archivo
`$HOME/.gitconfig` es un enlace simbólico a `$HOME/TEII/.gitconfig`, dónde el
directorio `TEII` es una carpeta compartida con el *host*.

## Referencias

- [git-scm.com • Pro Git Book by Scott Chacon and Ben Straub](https://www.git-scm.com/book/en/v2)
  - [1.5 Getting Started - Installing Git](https://www.git-scm.com/book/en/v2/Getting-Started-Installing-Git)
  - [8.1 Customizing Git - Git Configuration](https://www.git-scm.com/book/en/v2/Customizing-Git-Git-Configuration)
