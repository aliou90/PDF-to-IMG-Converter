import sys
import os
import fitz  # PyMuPDF
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QTextEdit,
    QFileDialog, QLineEdit, QHBoxLayout
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal

# === Fonction de conversion d'un PDF en images ===
def convert_pdf_to_images(pdf_path, output_folder, log_callback):
    pdf_document = fitz.open(pdf_path)
    pdf_name = os.path.splitext(os.path.basename(pdf_path))[0]

    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)
        pix = page.get_pixmap()
        output_image_path = os.path.join(output_folder, f"{pdf_name}_{page_num + 1}.png")
        pix.save(output_image_path)
        log_callback(f"✅ Page {page_num + 1} → {output_image_path}")
    pdf_document.close()


# === Thread pour exécuter la conversion sans bloquer l'UI ===
class ConverterThread(QThread):
    log_signal = pyqtSignal(str)
    done_signal = pyqtSignal()

    def __init__(self, pdf_directory, output_directory):
        super().__init__()
        self.pdf_directory = pdf_directory
        self.output_directory = output_directory

    def log(self, message):
        self.log_signal.emit(message)

    def run(self):
        os.makedirs(self.output_directory, exist_ok=True)

        for root, _, files in os.walk(self.pdf_directory):
            for file in files:
                if file.lower().endswith('.pdf'):
                    pdf_file_path = os.path.join(root, file)
                    self.log(f"🔄 Conversion de {pdf_file_path}...")

                    relative_path = os.path.relpath(root, self.pdf_directory)
                    output_folder = os.path.join(self.output_directory, relative_path, os.path.splitext(file)[0])
                    os.makedirs(output_folder, exist_ok=True)

                    convert_pdf_to_images(pdf_file_path, output_folder, self.log)

        self.done_signal.emit()


# === Interface principale ===
class PdfToImgApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Convertisseur PDF → Images")
        self.setGeometry(300, 200, 600, 400)

        layout = QVBoxLayout()

        # === Sélection dossier PDF ===
        self.pdf_input = QLineEdit()
        self.pdf_input.setPlaceholderText("Répertoire contenant les PDF")
        btn_browse_pdf = QPushButton("📂 Choisir")
        btn_browse_pdf.clicked.connect(self.browse_pdf_folder)

        h1 = QHBoxLayout()
        h1.addWidget(QLabel("Dossier PDF :"))
        h1.addWidget(self.pdf_input)
        h1.addWidget(btn_browse_pdf)
        layout.addLayout(h1)

        # === Sélection dossier sortie ===
        self.output_input = QLineEdit(os.path.expanduser("~/ConvertionPdfToImg"))
        btn_browse_output = QPushButton("📂 Choisir")
        btn_browse_output.clicked.connect(self.browse_output_folder)

        h2 = QHBoxLayout()
        h2.addWidget(QLabel("Dossier Sortie :"))
        h2.addWidget(self.output_input)
        h2.addWidget(btn_browse_output)
        layout.addLayout(h2)

        # === Bouton de conversion ===
        self.btn_convert = QPushButton("🚀 Lancer la conversion")
        self.btn_convert.clicked.connect(self.start_conversion)
        layout.addWidget(self.btn_convert)

        # === Zone de log ===
        self.log_area = QTextEdit()
        self.log_area.setReadOnly(True)
        self.log_area.setStyleSheet("background: black; color: lime; font-family: monospace;")
        layout.addWidget(self.log_area)

        self.setLayout(layout)

    def browse_pdf_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Sélectionner le dossier PDF")
        if folder:
            self.pdf_input.setText(folder)

    def browse_output_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Sélectionner le dossier de sortie")
        if folder:
            self.output_input.setText(folder)

    def start_conversion(self):
        pdf_dir = self.pdf_input.text().strip()
        output_dir = self.output_input.text().strip()

        if not pdf_dir or not os.path.isdir(pdf_dir):
            self.log("❌ Erreur : Veuillez sélectionner un dossier PDF valide.")
            return

        self.btn_convert.setEnabled(False)
        self.log("🚀 Début de la conversion...")

        self.thread = ConverterThread(pdf_dir, output_dir)
        self.thread.log_signal.connect(self.log)
        self.thread.done_signal.connect(self.conversion_done)
        self.thread.start()

    def log(self, message):
        self.log_area.append(message)
        self.log_area.verticalScrollBar().setValue(self.log_area.verticalScrollBar().maximum())

    def conversion_done(self):
        self.log("✅ Conversion terminée.")
        self.btn_convert.setEnabled(True)


# === Lancer l'application ===
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PdfToImgApp()
    window.show()
    sys.exit(app.exec())
