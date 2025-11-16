# 📄 PDF-to-IMG Converter

Un convertisseur **PDF vers images** simple et rapide, développé en Python (PyQt5).
Ce projet a été conçu pour offrir une interface graphique intuitive permettant de convertir chaque page d’un PDF en image (PNG/JPG) en un clic.

---

## 🖥️ Présentation

Ce projet est celui que nous avons construit ensemble dans le chat.
Il permet de :

* Sélectionner un fichier **PDF**
* Convertir chaque page en image (PNG ou JPG)
* Enregistrer les images dans un dossier dédié
* Visualiser l’avancement et les logs en direct
* Utiliser une interface fluide basée sur **PyQt5**

---

## 🖼️ Capture d’écran

```
assets/screenshots/screenshot1.png
```

*(Assure-toi que le fichier existe réellement dans ton repo GitHub.)*

---

## 🚀 Fonctionnalités

* Convertit toutes les pages d’un PDF en images
* Support PNG et JPG
* Interface graphique simple (PyQt5)
* Gestion propre des répertoires de sortie
* Logs intégrés pour suivre la progression
* Rapidité et stabilité

---

## 🛠️ Technologies utilisées

* **Python 3**
* **PyQt5**
* **pdf2image**
* **Pillow**

---

## 📦 Installation

Clonez le projet :

```bash
git clone git@github.com:aliou90/PDF-to-IMG-Converter.git
cd PDF-to-IMG-Converter
```

Installez les dépendances :

```bash
pip install PyQt5 PyQt5-sip PyQt5-Qt5 pdf2image pillow
```

(puis, si nécessaire : `pip freeze > requirements.txt`)

---

## ▶️ Utilisation

Lancez l’application :

```bash
python app.py
```

---

## 📁 Structure du projet (exemple)

```
PDF-to-IMG-Converter/
│
├── assets/
│   └── screenshots/
│       └── screenshot1.png
│
├── main.py
├── modules/
│   └── converter.py
├── requirements.txt
└── README.md
```

---

## 👤 Auteur

**Aliou Mbengue**
GitHub : [@aliou90](https://github.com/aliou90)


