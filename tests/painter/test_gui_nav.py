import os
import json

from PyQt5 import QtWidgets, QtCore


def make_dummy_image(path):
    # Create a tiny PNG to use as a test image
    from PIL import Image

    img = Image.new("RGBA", (10, 10), (255, 255, 255, 255))
    img.save(path, "PNG")


def test_nav_next_prev_changes_image(qtbot, tmp_path, monkeypatch):
    """Start RootPainter with a small project and assert next/prev change the displayed image"""
    # Create minimal project structure
    sync_dir = tmp_path / "sync"
    datasets = sync_dir / "datasets"
    project_dir = sync_dir / "projects" / "proj1"
    (datasets / "dataset1").mkdir(parents=True)
    project_dir.mkdir(parents=True)

    # create two tiny images
    img1 = datasets / "dataset1" / "img1.png"
    img2 = datasets / "dataset1" / "img2.png"
    make_dummy_image(img1)
    make_dummy_image(img2)

    # create .seg_proj with file_names referencing dataset images
    proj_file = project_dir / "proj1.seg_proj"
    proj_content = {
        "name": "proj1",
        "dataset": "dataset1",
        "original_model_file": "random weights",
        "location": "projects/proj1",
        "file_names": ["img1.png", "img2.png"],
    }
    proj_file.write_text(json.dumps(proj_content))

    # Create annotations/segmentations/messages etc
    (project_dir / "annotations" / "train").mkdir(parents=True)
    (project_dir / "annotations" / "val").mkdir(parents=True)
    (project_dir / "segmentations").mkdir(parents=True)
    (project_dir / "models").mkdir(parents=True)
    (project_dir / "messages").mkdir(parents=True)
    (project_dir / "logs").mkdir(parents=True)

    # Monkeypatch QFileDialog.getExistingDirectory to return our sync_dir
    monkeypatch.setattr(
        QtWidgets.QFileDialog,
        "getExistingDirectory",
        lambda *args, **kwargs: str(sync_dir),
    )

    # Import RootPainter lazily and create instance
    from root_painter.root_painter import RootPainter

    rp = RootPainter(sync_dir)
    qtbot.addWidget(rp)
    rp.show()

    # ensure initial file is img1
    assert os.path.basename(rp.image_path) in ("img1.png", "img1.png")

    label_before = rp.nav_widget.nav_label.text()

    # click next
    qtbot.mouseClick(rp.nav_widget.next_image_button, QtCore.Qt.LeftButton)
    qtbot.wait(200)

    # label should change to indicate new file
    label_after_next = rp.nav_widget.nav_label.text()
    assert label_after_next != label_before

    # click prev
    qtbot.mouseClick(rp.nav_widget.prev_image_button, QtCore.Qt.LeftButton)
    qtbot.wait(200)

    label_after_prev = rp.nav_widget.nav_label.text()
    assert label_after_prev == label_before
