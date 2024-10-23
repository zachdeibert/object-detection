import object_detection
import os
import PySide6.QtCore
import PySide6.QtWidgets
import qdarktheme  # pyright: ignore[reportMissingTypeStubs]
import sys

if __name__ == "__main__":
    app = PySide6.QtWidgets.QApplication(sys.argv)
    qdarktheme.setup_theme("auto")

    app.setApplicationName("object-detection")
    app.setApplicationDisplayName("Object Detection")
    app.setApplicationVersion("0.1.0")
    parser = PySide6.QtCore.QCommandLineParser()
    parser.setApplicationDescription(
        "A script to detect moving objects within a stationary camera feed"
    )
    parser.addHelpOption()
    parser.addVersionOption()

    config_file_option = PySide6.QtCore.QCommandLineOption(
        ("c", "config"),
        "Load a configuration file",
        "config.json",
        os.path.join(__file__, os.pardir, "config", "default.json"),
    )
    parser.addOption(config_file_option)

    parser.process(app)

    config_file = parser.value(config_file_option)
    config = object_detection.config.config(config_file)
    with config:

        window = object_detection.gui.main_window(
            config, list(object_detection.pipeline.create())
        )
        window.showMaximized()
        sys.exit(app.exec())
