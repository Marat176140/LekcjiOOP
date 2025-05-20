import sys
import os
import json
import shutil
import subprocess
from datetime import datetime
from pathlib import Path
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit,
    QPushButton, QFileDialog, QTextEdit
)

class GeneratorKluczy(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Generator kluczy SSH")
        self.uklad = QVBoxLayout()

        self.pole_email = QLineEdit()
        self.pole_alias = QLineEdit()
        self.pole_host = QLineEdit()

        self.uklad.addWidget(QLabel("Email:"))
        self.uklad.addWidget(self.pole_email)
        self.uklad.addWidget(QLabel("Alias:"))
        self.uklad.addWidget(self.pole_alias)
        self.uklad.addWidget(QLabel("Host:"))
        self.uklad.addWidget(self.pole_host)

        self.przycisk_generuj = QPushButton("Generuj klucz")
        self.przycisk_generuj.clicked.connect(self.generuj_klucz)
        self.uklad.addWidget(self.przycisk_generuj)

        self.przycisk_pokaz_konfig = QPushButton("Pokaż konfigurację")
        self.przycisk_pokaz_konfig.clicked.connect(self.pokaz_konfig)
        self.uklad.addWidget(self.przycisk_pokaz_konfig)

        self.przycisk_pokaz_json = QPushButton("Pokaż plik JSON")
        self.przycisk_pokaz_json.clicked.connect(self.pokaz_json)
        self.uklad.addWidget(self.przycisk_pokaz_json)

        self.przycisk_kopiuj = QPushButton("Eksportuj folder z kluczami")
        self.przycisk_kopiuj.clicked.connect(self.kopiuj_folder)
        self.uklad.addWidget(self.przycisk_kopiuj)

        self.wyjscie = QTextEdit()
        self.wyjscie.setReadOnly(True)
        self.uklad.addWidget(self.wyjscie)

        self.setLayout(self.uklad)

        self.folder_kluczy = Path("moje_klucze")
        self.sciezka_konfig = self.folder_kluczy / "konfiguracja.txt"
        self.sciezka_json = self.folder_kluczy / "klucze.json"
        self.folder_kluczy.mkdir(exist_ok=True)

    def generuj_klucz(self):
        email = self.pole_email.text().strip()
        alias = self.pole_alias.text().strip()
        host = self.pole_host.text().strip()

        if not all([email, alias, host]):
            self.wyjscie.setText("Wpisz wszystkie dane: email, alias i host")
            return

        nazwa_klucza = f"klucz_ed25519_{alias}"
        sciezka_klucza = self.folder_kluczy / nazwa_klucza

        if sciezka_klucza.exists():
            self.wyjscie.setText(f"Klucz '{nazwa_klucza}' już istnieje.")
            return

        polecenie = [
            "ssh-keygen", "-t", "ed25519", "-C", email,
            "-f", str(sciezka_klucza), "-N", ""
        ]
        try:
            subprocess.run(polecenie, check=True)
        except subprocess.CalledProcessError:
            self.wyjscie.setText("Błąd podczas generowania klucza")
            return

        linia_konfig = (
            f"Host {alias}\n"
            f"    HostName {host}\n"
            f"    User git\n"
            f"    IdentityFile {sciezka_klucza}\n\n"
        )
        with open(self.sciezka_konfig, "a") as plik_konfig:
            plik_konfig.write(linia_konfig)

        dane = []
        if self.sciezka_json.exists():
            with open(self.sciezka_json, "r") as f:
                dane = json.load(f)

        dane.append({
            "nazwa": nazwa_klucza,
            "email": email,
            "host": host,
            "sciezka": str(sciezka_klucza),
            "data": datetime.now().isoformat()
        })
        with open(self.sciezka_json, "w") as f:
            json.dump(dane, f, indent=4)

        self.wyjscie.setText(f"Klucz '{nazwa_klucza}' został wygenerowany")

    def pokaz_konfig(self):
        if self.sciezka_konfig.exists():
            with open(self.sciezka_konfig, "r") as f:
                zawartosc = f.read()
            self.wyjscie.setText(zawartosc)
        else:
            self.wyjscie.setText("Brak pliku konfiguracyjnego")

    def pokaz_json(self):
        if self.sciezka_json.exists():
            with open(self.sciezka_json, "r") as f:
                zawartosc = f.read()

            self.wyjscie.setText(zawartosc)
        else:
                self.wyjscie.setText("Brak pliku JSON")

    def kopiuj_folder(self):
        folder_docelowy = QFileDialog.getExistingDirectory(self, "Wybierz folder docelowy")
        if folder_docelowy:
            try:
                cel = Path(folder_docelowy) / "moje_klucze_export"
                if cel.exists():
                    shutil.rmtree(cel)
                shutil.copytree(self.folder_kluczy, cel)
                self.wyjscie.setText(f"Folder skopiowany do: {cel}")
            except Exception as e:
                self.wyjscie.setText(f"Błąd podczas kopiowania: {e}")
        else:
            self.wyjscie.setText("Operacja anulowana")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    okno = GeneratorKluczy()
    okno.show()
    sys.exit(app.exec_())
