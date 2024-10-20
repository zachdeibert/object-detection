import object_detection
import PySide6.QtCore
import PySide6.QtWidgets
import sys

if __name__ == "__main__":
    app = PySide6.QtWidgets.QApplication(sys.argv)

    app.setApplicationName("object-detection")
    app.setApplicationDisplayName("Object Detection")
    app.setApplicationVersion("0.1.0")
    parser = PySide6.QtCore.QCommandLineParser()
    parser.setApplicationDescription(
        "A script to detect moving objects within a stationary camera feed"
    )
    parser.addHelpOption()
    parser.addVersionOption()
    parser.process(app)

    window = object_detection.gui.MainWindow()
    window.showMaximized()
    sys.exit(app.exec())
