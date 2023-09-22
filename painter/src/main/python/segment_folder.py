"""
Copyright (C) 2020 Abraham George Smith

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

#pylint: disable=I1101,C0111,W0201,R0903,E0611, R0902, R0914
import os
import time
from PyQt5 import QtWidgets
from PyQt5 import QtCore
import file_utils
from progress_widget import BaseProgressWidget
from instructions import send_instruction
from im_utils import is_image

class SegmentWatchThread(QtCore.QThread):
    """
    Runs another thread.
    """
    progress_change = QtCore.pyqtSignal(int, int)
    done = QtCore.pyqtSignal()

    def __init__(self, segment_dir, total_images):
        super().__init__()
        self.segment_dir = segment_dir
        self.total_images = total_images

    def run(self):
        while True:
            done_fnames = file_utils.ls(self.segment_dir)
            done_fnames = [f for f in done_fnames if is_image(f) or f.endswith('.npz')]
            count = len(done_fnames)
            if count >= self.total_images:
                self.done.emit()
                break
            else:
                self.progress_change.emit(count, self.total_images)
                time.sleep(0.2)


class SegmentProgressWidget(BaseProgressWidget):
    def __init__(self):
        super().__init__('Segmenting dataset')

    def run(self, segment_dir, total_images):
        self.progress_bar.setMaximum(total_images)
        self.watch_thread = SegmentWatchThread(segment_dir, total_images)
        self.watch_thread.progress_change.connect(self.onCountChanged)
        self.watch_thread.done.connect(self.done)
        self.watch_thread.start()

class SegmentFolderWidget(QtWidgets.QWidget):

    submit = QtCore.pyqtSignal()

    def __init__(self, sync_dir, instruction_dir):
        super().__init__()

        self.input_dir = None
        self.output_dir = None
        self.selected_models = []
        self.instruction_dir = instruction_dir
        self.sync_dir = sync_dir
        self.initUI()

    def segment_folder(self):
        selected_models = self.selected_models
        input_dir = self.input_dir
        output_dir = self.output_dir
        all_fnames = file_utils.ls(str(input_dir))
        all_fnames = [f for f in all_fnames if is_image(f)]
        # need to make sure all train photos are copied now.
        content = {
            "model_paths": selected_models,
            "dataset_dir": input_dir,
            "seg_dir": output_dir,
            "file_names": all_fnames,
            "format": self.format_dropdown.currentText()
        }
        send_instruction('segment', content, self.instruction_dir, self.sync_dir)
        self.progress_widget = SegmentProgressWidget()

        self.progress_widget.run(output_dir, len(all_fnames))
        self.progress_widget.show()
        self.close()

    def initUI(self):
        layout = QtWidgets.QVBoxLayout()
        self.setLayout(layout)
        self.setWindowTitle("Segment Folder")

        # Add specify image directory button
        in_dir_label = QtWidgets.QLabel()
        in_dir_label.setText("Input directory: Not yet specified")
        layout.addWidget(in_dir_label)
        self.in_dir_label = in_dir_label

        specify_input_dir_btn = QtWidgets.QPushButton('Specify input directory')
        specify_input_dir_btn.clicked.connect(self.select_input_dir)
        layout.addWidget(specify_input_dir_btn)

        model_label = QtWidgets.QLabel()
        model_label.setText("Model file: Not yet specified")
        layout.addWidget(model_label)
        self.model_label = model_label
        specify_model_btn = QtWidgets.QPushButton('Specify model file')
        specify_model_btn.clicked.connect(self.select_model)
        layout.addWidget(specify_model_btn)


        out_dir_label = QtWidgets.QLabel()
        out_dir_label.setText("Output directory: Not yet specified")
        layout.addWidget(out_dir_label)
        self.out_dir_label = out_dir_label

        self.specify_output_dir_btn = QtWidgets.QPushButton('Specify output directory')
        self.specify_output_dir_btn.clicked.connect(self.select_output_dir)
        self.specify_output_dir_btn.setEnabled(False)
        layout.addWidget(self.specify_output_dir_btn)


        format_label = QtWidgets.QLabel()
        format_label.setText("Segmentation Format: RootPainter Default")
        layout.addWidget(format_label)
        self.format_label = format_label
        self.format_dropdown = QtWidgets.QComboBox()
        self.format_dropdown.addItems(['RootPainter Default (.png)', 'RhizoVision Explorer (.png)'])
        # nobody needs numpy yet
        # self.format_dropdown.addItems(['RootPainter Default (.png)', 'RhizoVision Explorer (.png)', 'Numpy Compressed (.npz)'])
        self.format_dropdown.currentIndexChanged.connect(self.format_selection_change)
        layout.addWidget(self.format_dropdown)

        info_label = QtWidgets.QLabel()
        info_label.setText("Input directory, output directory and model"
                           " must be specified to segment folder.")
        layout.addWidget(info_label)
        self.info_label = info_label

        # Add segment button
        submit_btn = QtWidgets.QPushButton('Segment')
        submit_btn.clicked.connect(self.segment_folder)
        layout.addWidget(submit_btn)
        submit_btn.setEnabled(False)
        self.submit_btn = submit_btn

    def format_selection_change(self, _):
        self.format_label.setText("Segmentation Format: " + self.format_dropdown.currentText())

    def validate(self):
        if not self.input_dir:
            self.info_label.setText("Input directory must be specified to create project")
            self.submit_btn.setEnabled(False)
            return

        if not self.selected_models:
            self.info_label.setText("Starting model must be specified to create project")
            self.submit_btn.setEnabled(False)
            return

        # if models are selected then output can be specified. This is because
        # we want to disable output selection until a model is selected so
        # we can suggest a sensible output folder name based on the selected model
        self.specify_output_dir_btn.setEnabled(True)

        if not self.output_dir:
            self.info_label.setText("Output directory must be specified to create project")
            self.submit_btn.setEnabled(False)
            return

        self.info_label.setText("")
        self.submit_btn.setEnabled(True)

    def try_submit(self):
        self.submit.emit()

    def select_input_dir(self):
        self.input_dialog = QtWidgets.QFileDialog(self)
        self.input_dialog.setFileMode(QtWidgets.QFileDialog.Directory)

        def output_selected():
            self.input_dir = self.input_dialog.selectedFiles()[0]
            self.in_dir_label.setText('Input directory: ' + self.input_dir)
            self.validate()
        self.input_dialog.fileSelected.connect(output_selected)
        self.input_dialog.open()

    def select_output_dir(self):
        self.output_dialog = QtWidgets.QFileDialog(self)
        self.output_dialog.setFileMode(QtWidgets.QFileDialog.Directory)
        def output_selected():
            self.output_dir = self.output_dialog.selectedFiles()[0]
            self.out_dir_label.setText('Output directory: ' + self.output_dir)
            self.validate()
        self.output_dialog.fileSelected.connect(output_selected)
        self.output_dialog.open()

    def get_suggested_output_dir(self, model_file_paths):
        """
        Suggest an output directory path based on the selected models.
        This should both save the user time and encourage sensible (organised?)
        file structure and workflow. 

        They can still overwrite the output dir if they wish.
        """

        # For a model /rp_sync/projects/project_a/models/000004_1685012907.pkl the output folder would be /rp_sync/projects/project_a/results/segmentations_model_4
        model_fpath = model_file_paths[0]
        model_name = os.path.basename(model_fpath)
        project_directory_path = os.path.dirname(model_fpath)
        projects_directory_path = os.path.dirname(project_directory_path)
        if os.path.basename(projects_directory_path) != 'projects':
            # if the model file was not in a models dir in a project in the projects folder then do not suggest an ouput location.
            return None 
        results_dir = os.path.join(project_directory_path, 'results')
        model_fnames = [os.path.splitext(m)[0] for m in model_



If multiple models are selected, the output folder would be /rp_sync/projects/project_a/results/segmentations_model_4_5_6_7_8
If the model has been renamed by the user i.e it is not 000004_1685012907.pkl but user_model_name.pkl then we include the user-specified name(s) verbatim.
        


        return 

    def select_model(self):
        options = QtWidgets.QFileDialog.Options()
        file_paths, _ = QtWidgets.QFileDialog.getOpenFileNames(self,
                                                               "Specify model file", "",
                                                               "Pickle Files (*.pkl)",
                                                               options=options)
        if file_paths:
            file_paths = [os.path.abspath(f) for f in file_paths]
            if len(file_paths) == 1:
                self.model_label.setText('Model file: ' + file_paths[0])
            else:
                self.model_label.setText(f'{len(file_paths)} model files selected')
            self.selected_models = file_paths

            # if there is not yet a specified output directory. Then at this point
            # we will suggest one based on the model name.
            if self.output_dir is None:
                self.output_dir = self.get_suggested_output_dir(file_paths)

            self.validate()
