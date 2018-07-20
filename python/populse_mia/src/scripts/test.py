import os

# Working from the scripts directory
from PyQt5.QtCore import QPoint, Qt
from PyQt5.QtGui import QKeySequence

from populse_db.database import FIELD_TYPE_INTEGER

os.chdir(os.path.dirname(os.path.realpath(__file__)))

import unittest

from PyQt5.QtTest import QTest
from PyQt5.QtWidgets import QApplication
from Project.Project import Project, COLLECTION_CURRENT, COLLECTION_INITIAL, COLLECTION_BRICK, TAG_ORIGIN_USER, TAG_FILENAME, TAG_CHECKSUM, TAG_TYPE, TAG_BRICKS, TAG_EXP_TYPE
from MainWindow.Main_Window import Main_Window
from SoftwareProperties.Config import Config

class TestMIADataBrowser(unittest.TestCase):

    def setUp(self):
        """
        Called before each test
        """

        self.app = QApplication([])
        self.project = Project(None, True)
        self.imageViewer = Main_Window(self.project, test=True)
        print(self._testMethodName)

    def tearDown(self):
        """
        Called after each test
        """

        self.imageViewer.project.unsaveModifications()
        self.imageViewer.close()

    def test_unnamed_project_software_opening(self):
        """
        Tests unnamed project creation at software opening
        """

        self.assertIsInstance(self.project, Project)
        self.assertEqual(self.imageViewer.project.getName(), "Unnamed project")
        tags = self.imageViewer.project.session.get_fields_names(COLLECTION_CURRENT)
        self.assertEqual(len(tags), 5)
        self.assertTrue(TAG_CHECKSUM in tags)
        self.assertTrue(TAG_FILENAME in tags)
        self.assertTrue(TAG_TYPE in tags)
        self.assertTrue(TAG_EXP_TYPE in tags)
        self.assertTrue(TAG_BRICKS in tags)
        self.assertEqual(self.imageViewer.project.session.get_documents_names(COLLECTION_CURRENT), [])
        self.assertEqual(self.imageViewer.project.session.get_documents_names(COLLECTION_INITIAL), [])
        collections = self.imageViewer.project.session.get_collections_names()
        self.assertEqual(len(collections), 3)
        self.assertTrue(COLLECTION_INITIAL in collections)
        self.assertTrue(COLLECTION_CURRENT in collections)
        self.assertTrue(COLLECTION_BRICK in collections)
        self.assertEqual(self.imageViewer.windowTitle(), "MIA - Multiparametric Image Analysis - Unnamed project")

    def test_projects_removed_from_current_projects(self):
        """
        Tests that the projects are removed from the list of current projects
        """

        config = Config()
        projects = config.get_opened_projects()
        self.assertEqual(len(projects), 1)
        self.assertTrue(self.imageViewer.project.folder in projects)

    def test_open_project(self):
        """
        Tests project opening
        """

        self.imageViewer.switch_project("project_8", "project_8", "project_8")
        self.assertEqual(self.imageViewer.project.getName(), "project_8")
        self.assertEqual(self.imageViewer.windowTitle(), "MIA - Multiparametric Image Analysis - project_8")
        documents = self.imageViewer.project.session.get_documents_names(COLLECTION_CURRENT)
        self.assertEqual(len(documents), 8)
        self.assertTrue("data/raw_data/Guerbet-C6-2014-Rat-K52-Tube27-2014-02-14_10-23-17-02-G1_Guerbet_Anat-RARE__pvm_-00-02-20.000.nii" in documents)
        self.assertTrue("data/raw_data/Guerbet-C6-2014-Rat-K52-Tube27-2014-02-14_10-23-17-04-G3_Guerbet_MDEFT-MDEFT__pvm_-00-09-40.800.nii" in documents)
        self.assertTrue("data/raw_data/Guerbet-C6-2014-Rat-K52-Tube27-2014-02-14_10-23-17-05-G4_Guerbet_T1SE_800-RARE__pvm_-00-01-42.400.nii" in documents)
        self.assertTrue("data/raw_data/Guerbet-C6-2014-Rat-K52-Tube27-2014-02-14_10-23-17-06-G4_Guerbet_T1SE_800-RARE__pvm_-00-01-42.400.nii" in documents)
        self.assertTrue("data/raw_data/Guerbet-C6-2014-Rat-K52-Tube27-2014-02-14_10-23-17-08-G4_Guerbet_T1SE_800-RARE__pvm_-00-01-42.400.nii" in documents)
        self.assertTrue("data/raw_data/Guerbet-C6-2014-Rat-K52-Tube27-2014-02-14_10-23-17-09-G4_Guerbet_T1SE_800-RARE__pvm_-00-01-42.400.nii" in documents)
        self.assertTrue("data/raw_data/Guerbet-C6-2014-Rat-K52-Tube27-2014-02-14_10-23-17-10-G3_Guerbet_MDEFT-MDEFT__pvm_-00-09-40.800.nii" in documents)
        self.assertTrue("data/raw_data/Guerbet-C6-2014-Rat-K52-Tube27-2014-02-14_10-23-17-11-G4_Guerbet_T1SE_800-RARE__pvm_-00-01-42.400.nii" in documents)
        documents = self.imageViewer.project.session.get_documents_names(COLLECTION_INITIAL)
        self.assertEqual(len(documents), 8)
        self.assertTrue("data/raw_data/Guerbet-C6-2014-Rat-K52-Tube27-2014-02-14_10-23-17-02-G1_Guerbet_Anat-RARE__pvm_-00-02-20.000.nii" in documents)
        self.assertTrue("data/raw_data/Guerbet-C6-2014-Rat-K52-Tube27-2014-02-14_10-23-17-04-G3_Guerbet_MDEFT-MDEFT__pvm_-00-09-40.800.nii" in documents)
        self.assertTrue("data/raw_data/Guerbet-C6-2014-Rat-K52-Tube27-2014-02-14_10-23-17-05-G4_Guerbet_T1SE_800-RARE__pvm_-00-01-42.400.nii" in documents)
        self.assertTrue("data/raw_data/Guerbet-C6-2014-Rat-K52-Tube27-2014-02-14_10-23-17-06-G4_Guerbet_T1SE_800-RARE__pvm_-00-01-42.400.nii" in documents)
        self.assertTrue("data/raw_data/Guerbet-C6-2014-Rat-K52-Tube27-2014-02-14_10-23-17-08-G4_Guerbet_T1SE_800-RARE__pvm_-00-01-42.400.nii" in documents)
        self.assertTrue("data/raw_data/Guerbet-C6-2014-Rat-K52-Tube27-2014-02-14_10-23-17-09-G4_Guerbet_T1SE_800-RARE__pvm_-00-01-42.400.nii" in documents)
        self.assertTrue("data/raw_data/Guerbet-C6-2014-Rat-K52-Tube27-2014-02-14_10-23-17-10-G3_Guerbet_MDEFT-MDEFT__pvm_-00-09-40.800.nii" in documents)
        self.assertTrue("data/raw_data/Guerbet-C6-2014-Rat-K52-Tube27-2014-02-14_10-23-17-11-G4_Guerbet_T1SE_800-RARE__pvm_-00-01-42.400.nii" in documents)

    def test_add_tag(self):
        """
        Tests the pop up adding a tag
        """

        # Testing without tag name
        self.imageViewer.data_browser.add_tag_action.trigger()
        add_tag = self.imageViewer.data_browser.pop_up_add_tag
        QTest.mouseClick(add_tag.push_button_ok, Qt.LeftButton)
        self.assertEqual(add_tag.msg.text(), "The tag name cannot be empty")

        # Testing with tag name already existing
        self.imageViewer.data_browser.add_tag_action.trigger()
        add_tag = self.imageViewer.data_browser.pop_up_add_tag
        add_tag.text_edit_tag_name.setText("Type")
        QTest.mouseClick(add_tag.push_button_ok, Qt.LeftButton)
        self.assertEqual(add_tag.msg.text(), "This tag name already exists")

        # Testing with wrong type
        self.imageViewer.data_browser.add_tag_action.trigger()
        add_tag = self.imageViewer.data_browser.pop_up_add_tag
        add_tag.text_edit_tag_name.setText("Test")
        add_tag.combo_box_type.setCurrentText(FIELD_TYPE_INTEGER)
        add_tag.type = FIELD_TYPE_INTEGER
        add_tag.text_edit_default_value.setText("Should be integer")
        QTest.mouseClick(add_tag.push_button_ok, Qt.LeftButton)
        self.assertEqual(add_tag.msg.text(), "Invalid default value")

        self.imageViewer.data_browser.add_tag_action.trigger()
        add_tag = self.imageViewer.data_browser.pop_up_add_tag
        add_tag.text_edit_tag_name.setText("Test")
        QTest.mouseClick(add_tag.push_button_ok, Qt.LeftButton)
        self.assertTrue("Test" in self.imageViewer.project.session.get_fields_names(COLLECTION_CURRENT))
        self.assertTrue("Test" in self.imageViewer.project.session.get_fields_names(COLLECTION_INITIAL))

    def test_clone_tag(self):
        """
        Tests the pop up cloning a tag
        """

        # Testing without new tag name
        self.imageViewer.data_browser.clone_tag_action.trigger()
        clone_tag = self.imageViewer.data_browser.pop_up_clone_tag
        QTest.mouseClick(clone_tag.push_button_ok, Qt.LeftButton)
        self.assertEqual(clone_tag.msg.text(), "The tag name can't be empty")

        # Testing without any tag selected to clone
        self.imageViewer.data_browser.clone_tag_action.trigger()
        clone_tag = self.imageViewer.data_browser.pop_up_clone_tag
        clone_tag.line_edit_new_tag_name.setText("Test")
        QTest.mouseClick(clone_tag.push_button_ok, Qt.LeftButton)
        self.assertEqual(clone_tag.msg.text(), "The tag to clone must be selected")

        # Testing with tag name already existing
        self.imageViewer.data_browser.clone_tag_action.trigger()
        clone_tag = self.imageViewer.data_browser.pop_up_clone_tag
        clone_tag.line_edit_new_tag_name.setText("Type")
        QTest.mouseClick(clone_tag.push_button_ok, Qt.LeftButton)
        self.assertEqual(clone_tag.msg.text(), "This tag name already exists")

        self.imageViewer.data_browser.clone_tag_action.trigger()
        clone_tag = self.imageViewer.data_browser.pop_up_clone_tag
        clone_tag.line_edit_new_tag_name.setText("Test")
        clone_tag.list_widget_tags.setCurrentRow(0) # Bricks tag selected
        QTest.mouseClick(clone_tag.push_button_ok, Qt.LeftButton)
        self.assertTrue("Test" in self.imageViewer.project.session.get_fields_names(COLLECTION_CURRENT))
        self.assertTrue("Test" in self.imageViewer.project.session.get_fields_names(COLLECTION_INITIAL))
        test_row = self.imageViewer.project.session.get_field(COLLECTION_CURRENT, "Test")
        filename_row = self.imageViewer.project.session.get_field(COLLECTION_CURRENT, TAG_BRICKS)
        self.assertEqual(test_row.description, filename_row.description)
        self.assertEqual(test_row.unit, filename_row.unit)
        self.assertEqual(test_row.default_value, filename_row.default_value)
        self.assertEqual(test_row.type, filename_row.type)
        self.assertEqual(test_row.origin, TAG_ORIGIN_USER)
        self.assertEqual(test_row.visibility, True)
        test_row = self.imageViewer.project.session.get_field(COLLECTION_INITIAL, "Test")
        filename_row = self.imageViewer.project.session.get_field(COLLECTION_INITIAL, TAG_BRICKS)
        self.assertEqual(test_row.description, filename_row.description)
        self.assertEqual(test_row.unit, filename_row.unit)
        self.assertEqual(test_row.default_value, filename_row.default_value)
        self.assertEqual(test_row.type, filename_row.type)
        self.assertEqual(test_row.origin, TAG_ORIGIN_USER)
        self.assertEqual(test_row.visibility, True)

    def test_remove_tag(self):
        """
        Tests the popup removing user tags
        """

        # Adding a tag
        self.imageViewer.data_browser.add_tag_action.trigger()
        add_tag = self.imageViewer.data_browser.pop_up_add_tag
        add_tag.text_edit_tag_name.setText("Test")
        QTest.mouseClick(add_tag.push_button_ok, Qt.LeftButton)

        old_tags_current = self.imageViewer.project.session.get_fields_names(COLLECTION_CURRENT)
        old_tags_initial = self.imageViewer.project.session.get_fields_names(COLLECTION_INITIAL)
        self.imageViewer.data_browser.remove_tag_action.trigger()
        remove_tag = self.imageViewer.data_browser.pop_up_remove_tag
        QTest.mouseClick(remove_tag.push_button_ok, Qt.LeftButton)
        new_tags_current = self.imageViewer.project.session.get_fields_names(COLLECTION_CURRENT)
        new_tags_initial = self.imageViewer.project.session.get_fields_names(COLLECTION_INITIAL)
        self.assertTrue(old_tags_current == new_tags_current)
        self.assertTrue(old_tags_initial == new_tags_initial)

        old_tags_current = self.imageViewer.project.session.get_fields_names(COLLECTION_CURRENT)
        old_tags_initial = self.imageViewer.project.session.get_fields_names(COLLECTION_INITIAL)
        self.assertTrue("Test" in old_tags_current)
        self.assertTrue("Test" in old_tags_initial)
        self.imageViewer.data_browser.remove_tag_action.trigger()
        remove_tag = self.imageViewer.data_browser.pop_up_remove_tag
        remove_tag.list_widget_tags.setCurrentRow(0) # Test tag selected
        QTest.mouseClick(remove_tag.push_button_ok, Qt.LeftButton)
        new_tags_current = self.imageViewer.project.session.get_fields_names(COLLECTION_CURRENT)
        new_tags_initial = self.imageViewer.project.session.get_fields_names(COLLECTION_INITIAL)
        self.assertTrue("Test" not in new_tags_current)
        self.assertTrue("Test" not in new_tags_initial)

    def test_visualized_tags(self):
        """
        Tests the popup modifying the visualized tags
        """

        # Testing default tags visibility
        visibles = self.imageViewer.project.session.get_visibles()
        self.assertEqual(len(visibles), 4)
        self.assertTrue(TAG_FILENAME in visibles)
        self.assertTrue(TAG_BRICKS in visibles)
        self.assertTrue(TAG_TYPE in visibles)
        self.assertTrue(TAG_EXP_TYPE in visibles)

        # Testing columns displayed in the databrowser
        self.assertEqual(self.imageViewer.data_browser.table_data.columnCount(), 4)
        columns_displayed = []
        for column in range (0, self.imageViewer.data_browser.table_data.columnCount()):
            tag_displayed = self.imageViewer.data_browser.table_data.horizontalHeaderItem(column).text()
            if not self.imageViewer.data_browser.table_data.isColumnHidden(column):
                columns_displayed.append(tag_displayed)
        self.assertEqual(sorted(visibles), sorted(columns_displayed))

        # Testing that FileName tag is the first column
        self.assertEqual(self.imageViewer.data_browser.table_data.horizontalHeaderItem(0).text(), TAG_FILENAME)

        # Trying to set the visibles tags
        QTest.mouseClick(self.imageViewer.data_browser.visualized_tags_button, Qt.LeftButton)
        settings = self.imageViewer.data_browser.table_data.pop_up

        # Testing that checksum tag isn't displayed
        settings.tab_tags.search_bar.setText(TAG_CHECKSUM)
        self.assertEqual(settings.tab_tags.list_widget_tags.count(), 0)

        # Testing that FileName is not displayed in the list of visible tags
        settings.tab_tags.search_bar.setText("")
        visibles_tags = []
        for row in range (0, settings.tab_tags.list_widget_selected_tags.count()):
            item = settings.tab_tags.list_widget_selected_tags.item(row).text()
            visibles_tags.append(item)
        self.assertEqual(len(visibles_tags), 3)
        self.assertTrue(TAG_BRICKS in visibles_tags)
        self.assertTrue(TAG_EXP_TYPE in visibles_tags)
        self.assertTrue(TAG_TYPE in visibles_tags)

        # Testing when hiding a tag
        settings.tab_tags.list_widget_selected_tags.item(0).setSelected(True) # Bricks tag selected
        QTest.mouseClick(settings.tab_tags.push_button_unselect_tag, Qt.LeftButton)
        visibles_tags = []
        for row in range(0, settings.tab_tags.list_widget_selected_tags.count()):
            item = settings.tab_tags.list_widget_selected_tags.item(row).text()
            visibles_tags.append(item)
        self.assertEqual(len(visibles_tags), 2)
        self.assertTrue(TAG_TYPE in visibles_tags)
        self.assertTrue(TAG_EXP_TYPE in visibles_tags)
        QTest.mouseClick(settings.push_button_ok, Qt.LeftButton)

        new_visibles = self.imageViewer.project.session.get_visibles()
        self.assertEqual(len(new_visibles), 3)
        self.assertTrue(TAG_FILENAME in new_visibles)
        self.assertTrue(TAG_EXP_TYPE in new_visibles)
        self.assertTrue(TAG_TYPE in new_visibles)

        columns_displayed = []
        for column in range(0, self.imageViewer.data_browser.table_data.columnCount()):
            item = self.imageViewer.data_browser.table_data.horizontalHeaderItem(column)
            if not self.imageViewer.data_browser.table_data.isColumnHidden(column):
                columns_displayed.append(item.text())
        self.assertEqual(len(columns_displayed), 3)
        self.assertTrue(TAG_FILENAME in columns_displayed)
        self.assertTrue(TAG_EXP_TYPE in columns_displayed)
        self.assertTrue(TAG_TYPE in columns_displayed)

        # Testing when showing a new tag
        QTest.mouseClick(self.imageViewer.data_browser.visualized_tags_button, Qt.LeftButton)
        settings = self.imageViewer.data_browser.table_data.pop_up
        settings.tab_tags.search_bar.setText(TAG_BRICKS)
        settings.tab_tags.list_widget_tags.item(0).setSelected(True)
        QTest.mouseClick(settings.tab_tags.push_button_select_tag, Qt.LeftButton)
        QTest.mouseClick(settings.push_button_ok, Qt.LeftButton)

        new_visibles = self.imageViewer.project.session.get_visibles()
        self.assertEqual(len(new_visibles), 4)
        self.assertTrue(TAG_FILENAME in new_visibles)
        self.assertTrue(TAG_EXP_TYPE in new_visibles)
        self.assertTrue(TAG_TYPE in new_visibles)
        self.assertTrue(TAG_BRICKS in new_visibles)

        columns_displayed = []
        for column in range(0, self.imageViewer.data_browser.table_data.columnCount()):
            item = self.imageViewer.data_browser.table_data.horizontalHeaderItem(column)
            if not self.imageViewer.data_browser.table_data.isColumnHidden(column):
                columns_displayed.append(item.text())
        self.assertEqual(len(columns_displayed), 4)
        self.assertTrue(TAG_FILENAME in columns_displayed)
        self.assertTrue(TAG_EXP_TYPE in columns_displayed)
        self.assertTrue(TAG_TYPE in columns_displayed)
        self.assertTrue(TAG_BRICKS in columns_displayed)

    def test_rapid_search(self):
        """
        Tests the rapid search bar
        """

        self.imageViewer.switch_project("project_8", "project_8", "project_8")

        # Checking that the 8 scans are shown in the databrowser
        self.assertEqual(self.imageViewer.data_browser.table_data.rowCount(), 8)
        scans_displayed = []
        for row in range(0, self.imageViewer.data_browser.table_data.rowCount()):
            item = self.imageViewer.data_browser.table_data.item(row, 0)
            scan_name = item.text()
            if not self.imageViewer.data_browser.table_data.isRowHidden(row):
                scans_displayed.append(scan_name)
        self.assertEqual(len(scans_displayed), 8)
        self.assertTrue("data/raw_data/Guerbet-C6-2014-Rat-K52-Tube27-2014-02-14_10-23-17-02-G1_Guerbet_Anat-RARE__pvm_-00-02-20.000.nii" in scans_displayed)
        self.assertTrue("data/raw_data/Guerbet-C6-2014-Rat-K52-Tube27-2014-02-14_10-23-17-04-G3_Guerbet_MDEFT-MDEFT__pvm_-00-09-40.800.nii" in scans_displayed)
        self.assertTrue("data/raw_data/Guerbet-C6-2014-Rat-K52-Tube27-2014-02-14_10-23-17-05-G4_Guerbet_T1SE_800-RARE__pvm_-00-01-42.400.nii" in scans_displayed)
        self.assertTrue("data/raw_data/Guerbet-C6-2014-Rat-K52-Tube27-2014-02-14_10-23-17-06-G4_Guerbet_T1SE_800-RARE__pvm_-00-01-42.400.nii" in scans_displayed)
        self.assertTrue("data/raw_data/Guerbet-C6-2014-Rat-K52-Tube27-2014-02-14_10-23-17-08-G4_Guerbet_T1SE_800-RARE__pvm_-00-01-42.400.nii" in scans_displayed)
        self.assertTrue("data/raw_data/Guerbet-C6-2014-Rat-K52-Tube27-2014-02-14_10-23-17-09-G4_Guerbet_T1SE_800-RARE__pvm_-00-01-42.400.nii" in scans_displayed)
        self.assertTrue("data/raw_data/Guerbet-C6-2014-Rat-K52-Tube27-2014-02-14_10-23-17-10-G3_Guerbet_MDEFT-MDEFT__pvm_-00-09-40.800.nii" in scans_displayed)
        self.assertTrue("data/raw_data/Guerbet-C6-2014-Rat-K52-Tube27-2014-02-14_10-23-17-11-G4_Guerbet_T1SE_800-RARE__pvm_-00-01-42.400.nii" in scans_displayed)

        # Testing G1 rapid search
        self.imageViewer.data_browser.search_bar.setText("G1")
        scans_displayed = []
        for row in range(0, self.imageViewer.data_browser.table_data.rowCount()):
            item = self.imageViewer.data_browser.table_data.item(row, 0)
            scan_name = item.text()
            if not self.imageViewer.data_browser.table_data.isRowHidden(row):
                scans_displayed.append(scan_name)
        self.assertEqual(len(scans_displayed), 1)
        self.assertTrue("data/raw_data/Guerbet-C6-2014-Rat-K52-Tube27-2014-02-14_10-23-17-02-G1_Guerbet_Anat-RARE__pvm_-00-02-20.000.nii" in scans_displayed)

        # Testing that all the scans are back when clicking on the cross
        QTest.mouseClick(self.imageViewer.data_browser.button_cross, Qt.LeftButton)

        scans_displayed = []
        for row in range(0, self.imageViewer.data_browser.table_data.rowCount()):
            item = self.imageViewer.data_browser.table_data.item(row, 0)
            scan_name = item.text()
            if not self.imageViewer.data_browser.table_data.isRowHidden(row):
                scans_displayed.append(scan_name)
        self.assertEqual(len(scans_displayed), 8)
        self.assertTrue("data/raw_data/Guerbet-C6-2014-Rat-K52-Tube27-2014-02-14_10-23-17-02-G1_Guerbet_Anat-RARE__pvm_-00-02-20.000.nii" in scans_displayed)
        self.assertTrue("data/raw_data/Guerbet-C6-2014-Rat-K52-Tube27-2014-02-14_10-23-17-04-G3_Guerbet_MDEFT-MDEFT__pvm_-00-09-40.800.nii" in scans_displayed)
        self.assertTrue("data/raw_data/Guerbet-C6-2014-Rat-K52-Tube27-2014-02-14_10-23-17-05-G4_Guerbet_T1SE_800-RARE__pvm_-00-01-42.400.nii" in scans_displayed)
        self.assertTrue("data/raw_data/Guerbet-C6-2014-Rat-K52-Tube27-2014-02-14_10-23-17-06-G4_Guerbet_T1SE_800-RARE__pvm_-00-01-42.400.nii" in scans_displayed)
        self.assertTrue("data/raw_data/Guerbet-C6-2014-Rat-K52-Tube27-2014-02-14_10-23-17-08-G4_Guerbet_T1SE_800-RARE__pvm_-00-01-42.400.nii" in scans_displayed)
        self.assertTrue("data/raw_data/Guerbet-C6-2014-Rat-K52-Tube27-2014-02-14_10-23-17-09-G4_Guerbet_T1SE_800-RARE__pvm_-00-01-42.400.nii" in scans_displayed)
        self.assertTrue("data/raw_data/Guerbet-C6-2014-Rat-K52-Tube27-2014-02-14_10-23-17-10-G3_Guerbet_MDEFT-MDEFT__pvm_-00-09-40.800.nii" in scans_displayed)
        self.assertTrue("data/raw_data/Guerbet-C6-2014-Rat-K52-Tube27-2014-02-14_10-23-17-11-G4_Guerbet_T1SE_800-RARE__pvm_-00-01-42.400.nii" in scans_displayed)

        # Testing not defined values
        QTest.mouseClick(self.imageViewer.data_browser.button_cross, Qt.LeftButton)
        self.imageViewer.data_browser.search_bar.setText("*Not Defined*")
        scans_displayed = []
        for row in range(0, self.imageViewer.data_browser.table_data.rowCount()):
            item = self.imageViewer.data_browser.table_data.item(row, 0)
            scan_name = item.text()
            if not self.imageViewer.data_browser.table_data.isRowHidden(row):
                scans_displayed.append(scan_name)
        self.assertEqual(scans_displayed, ["data/raw_data/Guerbet-C6-2014-Rat-K52-Tube27-2014-02-14_10-23-17-11-G4_Guerbet_T1SE_800-RARE__pvm_-00-01-42.400.nii"])

    def test_advanced_search(self):
        """
        Tests the advanced search widget
        """

        self.imageViewer.switch_project("project_8", "project_8", "project_8")

        scans_displayed = []
        for row in range(0, self.imageViewer.data_browser.table_data.rowCount()):
            item = self.imageViewer.data_browser.table_data.item(row, 0)
            scan_name = item.text()
            if not self.imageViewer.data_browser.table_data.isRowHidden(row):
                scans_displayed.append(scan_name)
        self.assertEqual(len(scans_displayed), 8)
        self.assertTrue("data/raw_data/Guerbet-C6-2014-Rat-K52-Tube27-2014-02-14_10-23-17-02-G1_Guerbet_Anat-RARE__pvm_-00-02-20.000.nii" in scans_displayed)
        self.assertTrue("data/raw_data/Guerbet-C6-2014-Rat-K52-Tube27-2014-02-14_10-23-17-04-G3_Guerbet_MDEFT-MDEFT__pvm_-00-09-40.800.nii" in scans_displayed)
        self.assertTrue("data/raw_data/Guerbet-C6-2014-Rat-K52-Tube27-2014-02-14_10-23-17-05-G4_Guerbet_T1SE_800-RARE__pvm_-00-01-42.400.nii" in scans_displayed)
        self.assertTrue("data/raw_data/Guerbet-C6-2014-Rat-K52-Tube27-2014-02-14_10-23-17-06-G4_Guerbet_T1SE_800-RARE__pvm_-00-01-42.400.nii" in scans_displayed)
        self.assertTrue("data/raw_data/Guerbet-C6-2014-Rat-K52-Tube27-2014-02-14_10-23-17-08-G4_Guerbet_T1SE_800-RARE__pvm_-00-01-42.400.nii" in scans_displayed)
        self.assertTrue("data/raw_data/Guerbet-C6-2014-Rat-K52-Tube27-2014-02-14_10-23-17-09-G4_Guerbet_T1SE_800-RARE__pvm_-00-01-42.400.nii" in scans_displayed)
        self.assertTrue("data/raw_data/Guerbet-C6-2014-Rat-K52-Tube27-2014-02-14_10-23-17-10-G3_Guerbet_MDEFT-MDEFT__pvm_-00-09-40.800.nii" in scans_displayed)
        self.assertTrue("data/raw_data/Guerbet-C6-2014-Rat-K52-Tube27-2014-02-14_10-23-17-11-G4_Guerbet_T1SE_800-RARE__pvm_-00-01-42.400.nii" in scans_displayed)

        QTest.mouseClick(self.imageViewer.data_browser.advanced_search_button, Qt.LeftButton)
        field = self.imageViewer.data_browser.advanced_search.rows[0][2]
        condition = self.imageViewer.data_browser.advanced_search.rows[0][3]
        value = self.imageViewer.data_browser.advanced_search.rows[0][4]
        field_filename_index = field.findText(TAG_FILENAME)
        field.setCurrentIndex(field_filename_index)
        condition_contains_index = condition.findText("CONTAINS")
        condition.setCurrentIndex(condition_contains_index)
        value.setText("G1")
        QTest.mouseClick(self.imageViewer.data_browser.advanced_search.search, Qt.LeftButton)

        # Testing that only one scan is display with the filter applied
        scans_displayed = []
        for row in range(0, self.imageViewer.data_browser.table_data.rowCount()):
            item = self.imageViewer.data_browser.table_data.item(row, 0)
            scan_name = item.text()
            if not self.imageViewer.data_browser.table_data.isRowHidden(row):
                scans_displayed.append(scan_name)
        self.assertEqual(len(scans_displayed), 1)
        self.assertTrue("data/raw_data/Guerbet-C6-2014-Rat-K52-Tube27-2014-02-14_10-23-17-02-G1_Guerbet_Anat-RARE__pvm_-00-02-20.000.nii" in scans_displayed)

        # Testing that every scan is back when clicking again on advanced search
        QTest.mouseClick(self.imageViewer.data_browser.advanced_search_button, Qt.LeftButton)
        scans_displayed = []
        for row in range(0, self.imageViewer.data_browser.table_data.rowCount()):
            item = self.imageViewer.data_browser.table_data.item(row, 0)
            scan_name = item.text()
            if not self.imageViewer.data_browser.table_data.isRowHidden(row):
                scans_displayed.append(scan_name)
        self.assertEqual(len(scans_displayed), 8)
        self.assertTrue("data/raw_data/Guerbet-C6-2014-Rat-K52-Tube27-2014-02-14_10-23-17-02-G1_Guerbet_Anat-RARE__pvm_-00-02-20.000.nii" in scans_displayed)
        self.assertTrue("data/raw_data/Guerbet-C6-2014-Rat-K52-Tube27-2014-02-14_10-23-17-04-G3_Guerbet_MDEFT-MDEFT__pvm_-00-09-40.800.nii" in scans_displayed)
        self.assertTrue("data/raw_data/Guerbet-C6-2014-Rat-K52-Tube27-2014-02-14_10-23-17-05-G4_Guerbet_T1SE_800-RARE__pvm_-00-01-42.400.nii" in scans_displayed)
        self.assertTrue("data/raw_data/Guerbet-C6-2014-Rat-K52-Tube27-2014-02-14_10-23-17-06-G4_Guerbet_T1SE_800-RARE__pvm_-00-01-42.400.nii" in scans_displayed)
        self.assertTrue("data/raw_data/Guerbet-C6-2014-Rat-K52-Tube27-2014-02-14_10-23-17-08-G4_Guerbet_T1SE_800-RARE__pvm_-00-01-42.400.nii" in scans_displayed)
        self.assertTrue("data/raw_data/Guerbet-C6-2014-Rat-K52-Tube27-2014-02-14_10-23-17-09-G4_Guerbet_T1SE_800-RARE__pvm_-00-01-42.400.nii" in scans_displayed)
        self.assertTrue("data/raw_data/Guerbet-C6-2014-Rat-K52-Tube27-2014-02-14_10-23-17-10-G3_Guerbet_MDEFT-MDEFT__pvm_-00-09-40.800.nii" in scans_displayed)
        self.assertTrue("data/raw_data/Guerbet-C6-2014-Rat-K52-Tube27-2014-02-14_10-23-17-11-G4_Guerbet_T1SE_800-RARE__pvm_-00-01-42.400.nii" in scans_displayed)

    def test_remove_scan(self):
        """
        Tests scans removal in the databrowser
        """

        self.imageViewer.switch_project("project_8", "project_8", "project_8")

        scans_displayed = []
        for row in range(0, self.imageViewer.data_browser.table_data.rowCount()):
            item = self.imageViewer.data_browser.table_data.item(row, 0)
            scan_name = item.text()
            if not self.imageViewer.data_browser.table_data.isRowHidden(row):
                scans_displayed.append(scan_name)
        self.assertEqual(len(scans_displayed), 8)
        self.assertTrue("data/raw_data/Guerbet-C6-2014-Rat-K52-Tube27-2014-02-14_10-23-17-02-G1_Guerbet_Anat-RARE__pvm_-00-02-20.000.nii" in scans_displayed)
        self.assertTrue("data/raw_data/Guerbet-C6-2014-Rat-K52-Tube27-2014-02-14_10-23-17-04-G3_Guerbet_MDEFT-MDEFT__pvm_-00-09-40.800.nii" in scans_displayed)
        self.assertTrue("data/raw_data/Guerbet-C6-2014-Rat-K52-Tube27-2014-02-14_10-23-17-05-G4_Guerbet_T1SE_800-RARE__pvm_-00-01-42.400.nii" in scans_displayed)
        self.assertTrue("data/raw_data/Guerbet-C6-2014-Rat-K52-Tube27-2014-02-14_10-23-17-06-G4_Guerbet_T1SE_800-RARE__pvm_-00-01-42.400.nii" in scans_displayed)
        self.assertTrue("data/raw_data/Guerbet-C6-2014-Rat-K52-Tube27-2014-02-14_10-23-17-08-G4_Guerbet_T1SE_800-RARE__pvm_-00-01-42.400.nii" in scans_displayed)
        self.assertTrue("data/raw_data/Guerbet-C6-2014-Rat-K52-Tube27-2014-02-14_10-23-17-09-G4_Guerbet_T1SE_800-RARE__pvm_-00-01-42.400.nii" in scans_displayed)
        self.assertTrue("data/raw_data/Guerbet-C6-2014-Rat-K52-Tube27-2014-02-14_10-23-17-10-G3_Guerbet_MDEFT-MDEFT__pvm_-00-09-40.800.nii" in scans_displayed)
        self.assertTrue("data/raw_data/Guerbet-C6-2014-Rat-K52-Tube27-2014-02-14_10-23-17-11-G4_Guerbet_T1SE_800-RARE__pvm_-00-01-42.400.nii" in scans_displayed)

        # Trying to remove a scan
        self.imageViewer.data_browser.table_data.selectRow(0)
        self.imageViewer.data_browser.table_data.remove_scan()

        scans_displayed = []
        for row in range(0, self.imageViewer.data_browser.table_data.rowCount()):
            item = self.imageViewer.data_browser.table_data.item(row, 0)
            scan_name = item.text()
            if not self.imageViewer.data_browser.table_data.isRowHidden(row):
                scans_displayed.append(scan_name)
        self.assertEqual(len(scans_displayed), 7)
        self.assertTrue("data/raw_data/Guerbet-C6-2014-Rat-K52-Tube27-2014-02-14_10-23-17-04-G3_Guerbet_MDEFT-MDEFT__pvm_-00-09-40.800.nii" in scans_displayed)
        self.assertTrue("data/raw_data/Guerbet-C6-2014-Rat-K52-Tube27-2014-02-14_10-23-17-05-G4_Guerbet_T1SE_800-RARE__pvm_-00-01-42.400.nii" in scans_displayed)
        self.assertTrue("data/raw_data/Guerbet-C6-2014-Rat-K52-Tube27-2014-02-14_10-23-17-06-G4_Guerbet_T1SE_800-RARE__pvm_-00-01-42.400.nii" in scans_displayed)
        self.assertTrue("data/raw_data/Guerbet-C6-2014-Rat-K52-Tube27-2014-02-14_10-23-17-08-G4_Guerbet_T1SE_800-RARE__pvm_-00-01-42.400.nii" in scans_displayed)
        self.assertTrue("data/raw_data/Guerbet-C6-2014-Rat-K52-Tube27-2014-02-14_10-23-17-09-G4_Guerbet_T1SE_800-RARE__pvm_-00-01-42.400.nii" in scans_displayed)
        self.assertTrue("data/raw_data/Guerbet-C6-2014-Rat-K52-Tube27-2014-02-14_10-23-17-10-G3_Guerbet_MDEFT-MDEFT__pvm_-00-09-40.800.nii" in scans_displayed)
        self.assertTrue("data/raw_data/Guerbet-C6-2014-Rat-K52-Tube27-2014-02-14_10-23-17-11-G4_Guerbet_T1SE_800-RARE__pvm_-00-01-42.400.nii" in scans_displayed)

    def test_set_value(self):
        """
        Tests the values modifications
        """

        self.imageViewer.switch_project("project_8", "project_8", "project_8")

        value = float(self.imageViewer.project.session.get_value(COLLECTION_CURRENT, "data/raw_data/Guerbet-C6-2014-Rat-K52-Tube27-2014-02-14_10-23-17-02-G1_Guerbet_Anat-RARE__pvm_-00-02-20.000.nii", "BandWidth"))
        value_initial = float(self.imageViewer.project.session.get_value(COLLECTION_INITIAL, "data/raw_data/Guerbet-C6-2014-Rat-K52-Tube27-2014-02-14_10-23-17-02-G1_Guerbet_Anat-RARE__pvm_-00-02-20.000.nii", "BandWidth"))
        bandwidth_column  = self.imageViewer.data_browser.table_data.get_tag_column("BandWidth")
        item = self.imageViewer.data_browser.table_data.item(0, bandwidth_column)
        G1_bandwidth_databrowser = float(item.text())
        self.assertEqual(value, float(50000))
        self.assertEqual(value, G1_bandwidth_databrowser)
        self.assertEqual(value, value_initial)

        item.setSelected(True)
        item.setText("25000")

        value = float(self.imageViewer.project.session.get_value(COLLECTION_CURRENT,
                                                                              "data/raw_data/Guerbet-C6-2014-Rat-K52-Tube27-2014-02-14_10-23-17-02-G1_Guerbet_Anat-RARE__pvm_-00-02-20.000.nii",
                                                                              "BandWidth"))
        value_initial = float(self.imageViewer.project.session.get_value(COLLECTION_INITIAL,
                                                                 "data/raw_data/Guerbet-C6-2014-Rat-K52-Tube27-2014-02-14_10-23-17-02-G1_Guerbet_Anat-RARE__pvm_-00-02-20.000.nii",
                                                                 "BandWidth"))
        item = self.imageViewer.data_browser.table_data.item(0, bandwidth_column)
        G1_bandwidth_databrowser = float(item.text())
        self.assertEqual(value, float(25000))
        self.assertEqual(value, G1_bandwidth_databrowser)
        self.assertEqual(value_initial, float(50000))

    def test_reset_cell(self):
        """
        Tests the method resetting the selected cells
        """

        self.imageViewer.switch_project("project_8", "project_8", "project_8")

        bandwidth_column = self.imageViewer.data_browser.table_data.get_tag_column("BandWidth")

        value = float(self.imageViewer.project.session.get_value(COLLECTION_CURRENT,
                                                                              "data/raw_data/Guerbet-C6-2014-Rat-K52-Tube27-2014-02-14_10-23-17-02-G1_Guerbet_Anat-RARE__pvm_-00-02-20.000.nii",
                                                                              "BandWidth"))
        value_initial = float(self.imageViewer.project.session.get_value(COLLECTION_INITIAL,
                                                                 "data/raw_data/Guerbet-C6-2014-Rat-K52-Tube27-2014-02-14_10-23-17-02-G1_Guerbet_Anat-RARE__pvm_-00-02-20.000.nii",
                                                                 "BandWidth"))
        item = self.imageViewer.data_browser.table_data.item(0, bandwidth_column)
        databrowser = float(item.text())
        self.assertEqual(value, float(50000))
        self.assertEqual(value, databrowser)
        self.assertEqual(value, value_initial)
        item.setSelected(True)

        item.setText("25000")

        value = float(self.imageViewer.project.session.get_value(COLLECTION_CURRENT,
                                                                              "data/raw_data/Guerbet-C6-2014-Rat-K52-Tube27-2014-02-14_10-23-17-02-G1_Guerbet_Anat-RARE__pvm_-00-02-20.000.nii",
                                                                              "BandWidth"))
        value_initial = float(self.imageViewer.project.session.get_value(COLLECTION_INITIAL,
                                                                 "data/raw_data/Guerbet-C6-2014-Rat-K52-Tube27-2014-02-14_10-23-17-02-G1_Guerbet_Anat-RARE__pvm_-00-02-20.000.nii",
                                                                 "BandWidth"))
        item = self.imageViewer.data_browser.table_data.item(0, bandwidth_column)
        databrowser = float(item.text())
        self.assertEqual(value, float(25000))
        self.assertEqual(value, databrowser)
        self.assertEqual(value_initial, float(50000))

        self.imageViewer.data_browser.table_data.itemChanged.disconnect()
        self.imageViewer.data_browser.table_data.reset_cell()
        self.imageViewer.data_browser.table_data.itemChanged.connect(
        self.imageViewer.data_browser.table_data.change_cell_color)

        value = float(self.imageViewer.project.session.get_value(COLLECTION_CURRENT,
                                                                              "data/raw_data/Guerbet-C6-2014-Rat-K52-Tube27-2014-02-14_10-23-17-02-G1_Guerbet_Anat-RARE__pvm_-00-02-20.000.nii",
                                                                              "BandWidth"))
        value_initial = float(self.imageViewer.project.session.get_value(COLLECTION_INITIAL,
                                                                 "data/raw_data/Guerbet-C6-2014-Rat-K52-Tube27-2014-02-14_10-23-17-02-G1_Guerbet_Anat-RARE__pvm_-00-02-20.000.nii",
                                                                 "BandWidth"))
        item = self.imageViewer.data_browser.table_data.item(0, bandwidth_column)
        databrowser = float(item.text())
        self.assertEqual(value, float(50000))
        self.assertEqual(value, databrowser)
        self.assertEqual(value, value_initial)

    def test_reset_column(self):
        """
        Tests the method resetting the columns selected
        """

        self.imageViewer.switch_project("project_8", "project_8", "project_8")

        bandwidth_column = self.imageViewer.data_browser.table_data.get_tag_column("BandWidth")

        value = float(self.imageViewer.project.session.get_value(COLLECTION_CURRENT,
                                                                              "data/raw_data/Guerbet-C6-2014-Rat-K52-Tube27-2014-02-14_10-23-17-02-G1_Guerbet_Anat-RARE__pvm_-00-02-20.000.nii",
                                                                              "BandWidth"))
        value_initial = float(self.imageViewer.project.session.get_value(COLLECTION_INITIAL,
                                                                 "data/raw_data/Guerbet-C6-2014-Rat-K52-Tube27-2014-02-14_10-23-17-02-G1_Guerbet_Anat-RARE__pvm_-00-02-20.000.nii",
                                                                 "BandWidth"))
        item = self.imageViewer.data_browser.table_data.item(0, bandwidth_column)
        databrowser = float(item.text())
        self.assertEqual(value, float(50000))
        self.assertEqual(value, databrowser)
        self.assertEqual(value, value_initial)
        item.setSelected(True)

        value = float(self.imageViewer.project.session.get_value(COLLECTION_CURRENT,
                                                                              "data/raw_data/Guerbet-C6-2014-Rat-K52-Tube27-2014-02-14_10-23-17-04-G3_Guerbet_MDEFT-MDEFT__pvm_-00-09-40.800.nii",
                                                                              "BandWidth"))
        value_initial = float(self.imageViewer.project.session.get_value(COLLECTION_INITIAL,
                                                                 "data/raw_data/Guerbet-C6-2014-Rat-K52-Tube27-2014-02-14_10-23-17-04-G3_Guerbet_MDEFT-MDEFT__pvm_-00-09-40.800.nii",
                                                                 "BandWidth"))
        item = self.imageViewer.data_browser.table_data.item(1, bandwidth_column)
        databrowser = float(item.text())
        self.assertEqual(value, float(25000))
        self.assertEqual(value, databrowser)
        self.assertEqual(value, value_initial)
        item.setSelected(True)

        item.setText("70000")

        value = float(self.imageViewer.project.session.get_value(COLLECTION_CURRENT,
                                                                              "data/raw_data/Guerbet-C6-2014-Rat-K52-Tube27-2014-02-14_10-23-17-02-G1_Guerbet_Anat-RARE__pvm_-00-02-20.000.nii",
                                                                              "BandWidth"))
        value_initial = float(self.imageViewer.project.session.get_value(COLLECTION_INITIAL,
                                                                 "data/raw_data/Guerbet-C6-2014-Rat-K52-Tube27-2014-02-14_10-23-17-02-G1_Guerbet_Anat-RARE__pvm_-00-02-20.000.nii",
                                                                 "BandWidth"))
        item = self.imageViewer.data_browser.table_data.item(0, bandwidth_column)
        databrowser = float(item.text())
        self.assertEqual(value, float(70000))
        self.assertEqual(value, databrowser)
        self.assertEqual(value_initial, float(50000))

        value = float(self.imageViewer.project.session.get_value(COLLECTION_CURRENT,
                                                                              "data/raw_data/Guerbet-C6-2014-Rat-K52-Tube27-2014-02-14_10-23-17-04-G3_Guerbet_MDEFT-MDEFT__pvm_-00-09-40.800.nii",
                                                                              "BandWidth"))
        value_initial = float(self.imageViewer.project.session.get_value(COLLECTION_INITIAL,
                                                                 "data/raw_data/Guerbet-C6-2014-Rat-K52-Tube27-2014-02-14_10-23-17-04-G3_Guerbet_MDEFT-MDEFT__pvm_-00-09-40.800.nii",
                                                                 "BandWidth"))
        item = self.imageViewer.data_browser.table_data.item(1, bandwidth_column)
        databrowser = float(item.text())
        self.assertEqual(value, float(70000))
        self.assertEqual(value, databrowser)
        self.assertEqual(value_initial, float(25000))

        self.imageViewer.data_browser.table_data.itemChanged.disconnect()
        self.imageViewer.data_browser.table_data.reset_column()
        self.imageViewer.data_browser.table_data.itemChanged.connect(self.imageViewer.data_browser.table_data.change_cell_color)

        value = float(self.imageViewer.project.session.get_value(COLLECTION_CURRENT,
                                                                              "data/raw_data/Guerbet-C6-2014-Rat-K52-Tube27-2014-02-14_10-23-17-02-G1_Guerbet_Anat-RARE__pvm_-00-02-20.000.nii",
                                                                              "BandWidth"))
        value_initial = float(self.imageViewer.project.session.get_value(COLLECTION_INITIAL,
                                                                 "data/raw_data/Guerbet-C6-2014-Rat-K52-Tube27-2014-02-14_10-23-17-02-G1_Guerbet_Anat-RARE__pvm_-00-02-20.000.nii",
                                                                 "BandWidth"))
        item = self.imageViewer.data_browser.table_data.item(0, bandwidth_column)
        databrowser = float(item.text())
        self.assertEqual(value, float(50000))
        self.assertEqual(value, databrowser)
        self.assertEqual(value, value_initial)

        value = float(self.imageViewer.project.session.get_value(COLLECTION_CURRENT,
                                                                              "data/raw_data/Guerbet-C6-2014-Rat-K52-Tube27-2014-02-14_10-23-17-04-G3_Guerbet_MDEFT-MDEFT__pvm_-00-09-40.800.nii",
                                                                              "BandWidth"))
        value_initial = float(self.imageViewer.project.session.get_value(COLLECTION_INITIAL,
                                                                 "data/raw_data/Guerbet-C6-2014-Rat-K52-Tube27-2014-02-14_10-23-17-04-G3_Guerbet_MDEFT-MDEFT__pvm_-00-09-40.800.nii",
                                                                 "BandWidth"))
        item = self.imageViewer.data_browser.table_data.item(1, bandwidth_column)
        databrowser = float(item.text())
        self.assertEqual(value, float(25000))
        self.assertEqual(value, databrowser)
        self.assertEqual(value, value_initial)

    def test_reset_row(self):
        """
        Tests row reset
        """

        self.imageViewer.switch_project("project_8", "project_8", "project_8")

        bw_column = self.imageViewer.data_browser.table_data.get_tag_column("BandWidth")

        bw_item = self.imageViewer.data_browser.table_data.item(0, bw_column)
        old_bw = bw_item.text()
        self.assertEqual(int(old_bw), 50000)

        bw_item.setSelected(True)
        bw_item.setText("25000")
        set_item = self.imageViewer.data_browser.table_data.item(0, bw_column)
        set_bw = set_item.text()
        self.assertEqual(int(set_bw), 25000)

        self.imageViewer.data_browser.table_data.clearSelection()

        item = self.imageViewer.data_browser.table_data.item(0, 0)
        item.setSelected(True)
        self.imageViewer.data_browser.table_data.itemChanged.disconnect()
        self.imageViewer.data_browser.table_data.reset_row()
        self.imageViewer.data_browser.table_data.itemChanged.connect(
            self.imageViewer.data_browser.table_data.change_cell_color)

        bw_item = self.imageViewer.data_browser.table_data.item(0, bw_column)
        new_bw = bw_item.text()
        self.assertEqual(int(new_bw), 50000)

    def test_add_path(self):
        """
        Tests the popup to add a path
        """

        QTest.mouseClick(self.imageViewer.data_browser.addRowLabel, Qt.LeftButton)
        add_path = self.imageViewer.data_browser.table_data.pop_up_add_path

        QTest.mouseClick(add_path.ok_button, Qt.LeftButton)
        self.assertEqual(add_path.msg.text(), "Invalid arguments")

        add_path.file_line_edit.setText(os.path.join(".", "test_not_existing.py"))
        add_path.type_line_edit.setText("Python")
        QTest.mouseClick(add_path.ok_button, Qt.LeftButton)
        self.assertEqual(add_path.msg.text(), "Invalid arguments")

        add_path.file_line_edit.setText(os.path.join(".", "test.py"))
        add_path.type_line_edit.setText("Python")
        QTest.mouseClick(add_path.ok_button, Qt.LeftButton)

        self.assertEqual(self.imageViewer.project.session.get_documents_names(COLLECTION_CURRENT), ['data/downloaded_data/test.py'])
        self.assertEqual(self.imageViewer.project.session.get_documents_names(COLLECTION_INITIAL), ['data/downloaded_data/test.py'])
        self.assertEqual(self.imageViewer.data_browser.table_data.rowCount(), 1)
        self.assertEqual(self.imageViewer.data_browser.table_data.item(0, 0).text(), 'data/downloaded_data/test.py')

    def test_send_documents_to_pipeline(self):
        """
        Tests the popup sending the documents to the pipeline manager
        """

        self.imageViewer.switch_project("project_8", "project_8", "project_8")

        # Checking that the pipeline manager has an empty list at the beginning
        self.assertEqual(self.imageViewer.pipeline_manager.scan_list, [])

        # Sending the selection (all scans), but closing the popup
        QTest.mouseClick(self.imageViewer.data_browser.send_documents_to_pipeline_button, Qt.LeftButton)
        send_popup = self.imageViewer.data_browser.show_selection
        send_popup.close()

        # Checking that the list is stil empty
        self.assertEqual(self.imageViewer.pipeline_manager.scan_list, [])

        # Sending the selection (all scans)
        QTest.mouseClick(self.imageViewer.data_browser.send_documents_to_pipeline_button, Qt.LeftButton)
        send_popup = self.imageViewer.data_browser.show_selection
        send_popup.ok_clicked()

        # Checking that all scans have been sent to the pipeline manager
        scans = self.imageViewer.pipeline_manager.scan_list
        self.assertEqual(len(scans), 8)
        self.assertTrue("data/raw_data/Guerbet-C6-2014-Rat-K52-Tube27-2014-02-14_10-23-17-02-G1_Guerbet_Anat-RARE__pvm_-00-02-20.000.nii" in scans)
        self.assertTrue("data/raw_data/Guerbet-C6-2014-Rat-K52-Tube27-2014-02-14_10-23-17-04-G3_Guerbet_MDEFT-MDEFT__pvm_-00-09-40.800.nii" in scans)
        self.assertTrue("data/raw_data/Guerbet-C6-2014-Rat-K52-Tube27-2014-02-14_10-23-17-05-G4_Guerbet_T1SE_800-RARE__pvm_-00-01-42.400.nii" in scans)
        self.assertTrue("data/raw_data/Guerbet-C6-2014-Rat-K52-Tube27-2014-02-14_10-23-17-06-G4_Guerbet_T1SE_800-RARE__pvm_-00-01-42.400.nii" in scans)
        self.assertTrue("data/raw_data/Guerbet-C6-2014-Rat-K52-Tube27-2014-02-14_10-23-17-08-G4_Guerbet_T1SE_800-RARE__pvm_-00-01-42.400.nii" in scans)
        self.assertTrue("data/raw_data/Guerbet-C6-2014-Rat-K52-Tube27-2014-02-14_10-23-17-09-G4_Guerbet_T1SE_800-RARE__pvm_-00-01-42.400.nii" in scans)
        self.assertTrue("data/raw_data/Guerbet-C6-2014-Rat-K52-Tube27-2014-02-14_10-23-17-10-G3_Guerbet_MDEFT-MDEFT__pvm_-00-09-40.800.nii" in scans)
        self.assertTrue("data/raw_data/Guerbet-C6-2014-Rat-K52-Tube27-2014-02-14_10-23-17-11-G4_Guerbet_T1SE_800-RARE__pvm_-00-01-42.400.nii" in scans)

        # Selecting the first 2 scans
        item1 = self.imageViewer.data_browser.table_data.item(0, 0)
        item1.setSelected(True)
        scan1 = item1.text()
        item2 = self.imageViewer.data_browser.table_data.item(1, 0)
        scan2 = item2.text()
        item2.setSelected(True)

        # Sending the selection (first 2 scans)
        QTest.mouseClick(self.imageViewer.data_browser.send_documents_to_pipeline_button, Qt.LeftButton)
        send_popup = self.imageViewer.data_browser.show_selection
        send_popup.ok_clicked()

        # Checking that the first 2 scans have been sent to the pipeline manager
        scans = self.imageViewer.pipeline_manager.scan_list
        self.assertEqual(len(scans), 2)
        self.assertTrue(scan1 in scans)
        self.assertTrue(scan2 in scans)

        # Testing with the rapid search
        self.imageViewer.data_browser.table_data.clearSelection()
        self.imageViewer.data_browser.search_bar.setText("G3")

        # Sending the selection (G3 scans)
        QTest.mouseClick(self.imageViewer.data_browser.send_documents_to_pipeline_button, Qt.LeftButton)
        send_popup = self.imageViewer.data_browser.show_selection
        send_popup.ok_clicked()

        # Checking that G3 scans have been sent to the pipeline manager
        scans = self.imageViewer.pipeline_manager.scan_list
        self.assertEqual(len(scans), 2)
        self.assertTrue(
            "data/raw_data/Guerbet-C6-2014-Rat-K52-Tube27-2014-02-14_10-23-17-04-G3_Guerbet_MDEFT-MDEFT__pvm_-00-09-40.800.nii" in scans)
        self.assertTrue(
            "data/raw_data/Guerbet-C6-2014-Rat-K52-Tube27-2014-02-14_10-23-17-10-G3_Guerbet_MDEFT-MDEFT__pvm_-00-09-40.800.nii" in scans)

    def test_sort(self):
        """
        Tests the sorting in the databrowser
        """

        self.imageViewer.switch_project("project_8", "project_8", "project_8")

        mixed_bandwidths = []
        for row in range(0, self.imageViewer.data_browser.table_data.rowCount()):
            bandwidth_column = self.imageViewer.data_browser.table_data.get_tag_column("BandWidth")
            item = self.imageViewer.data_browser.table_data.item(row, bandwidth_column)
            scan_name = item.text()
            if not self.imageViewer.data_browser.table_data.isRowHidden(row):
                mixed_bandwidths.append(scan_name)

        self.imageViewer.data_browser.table_data.horizontalHeader().setSortIndicator(bandwidth_column, 0)

        up_bandwidths = []
        for row in range(0, self.imageViewer.data_browser.table_data.rowCount()):
            bandwidth_column = self.imageViewer.data_browser.table_data.get_tag_column("BandWidth")
            item = self.imageViewer.data_browser.table_data.item(row, bandwidth_column)
            scan_name = item.text()
            if not self.imageViewer.data_browser.table_data.isRowHidden(row):
                up_bandwidths.append(scan_name)

        self.assertNotEqual(mixed_bandwidths, up_bandwidths)
        self.assertEqual(sorted(mixed_bandwidths), up_bandwidths)

        self.imageViewer.data_browser.table_data.horizontalHeader().setSortIndicator(bandwidth_column, 1)

        down_bandwidths = []
        for row in range(0, self.imageViewer.data_browser.table_data.rowCount()):
            bandwidth_column = self.imageViewer.data_browser.table_data.get_tag_column("BandWidth")
            item = self.imageViewer.data_browser.table_data.item(row, bandwidth_column)
            scan_name = item.text()
            if not self.imageViewer.data_browser.table_data.isRowHidden(row):
                down_bandwidths.append(scan_name)

        self.assertNotEqual(mixed_bandwidths, down_bandwidths)
        self.assertEqual(sorted(mixed_bandwidths, reverse=True), down_bandwidths)

    def test_set_list_values(self):
        """
        Tests the setting of list values in the databrowser
        """

        self.imageViewer.switch_project("project_8", "project_8", "project_8")

        fov_column = self.imageViewer.data_browser.table_data.get_tag_column("FOV")
        fov_item = self.imageViewer.data_browser.table_data.item(0, fov_column)

    def test_mia_preferences(self):
        """
        Tests the MIA preferences popup
        """

        config = Config()
        old_auto_save = config.isAutoSave()
        self.assertEqual(old_auto_save, "no")

        # Auto save activated
        self.imageViewer.action_software_preferences.trigger()
        properties = self.imageViewer.pop_up_preferences
        properties.tab_widget.setCurrentIndex(1)
        properties.save_checkbox.setChecked(True)
        QTest.mouseClick(properties.push_button_ok, Qt.LeftButton)

        config = Config()
        new_auto_save = config.isAutoSave()
        self.assertEqual(new_auto_save, "yes")

        # Auto save disabled again
        self.imageViewer.action_software_preferences.trigger()
        properties = self.imageViewer.pop_up_preferences
        properties.tab_widget.setCurrentIndex(1)
        properties.save_checkbox.setChecked(False)
        QTest.mouseClick(properties.push_button_ok, Qt.LeftButton)
        config = Config()
        reput_auto_save = config.isAutoSave()
        self.assertEqual(reput_auto_save, "no")

    def test_undo_redo_databrowser(self):
        """
        Tests the databrowser undo/redo
        """

        self.imageViewer.switch_project("project_8", "project_8", "project_8")

        self.assertEqual(self.imageViewer.project.undos, [])
        self.assertEqual(self.imageViewer.project.redos, [])

        # Testing sort undo/redo
        bw_column = self.imageViewer.data_browser.table_data.get_tag_column("BandWidth")
        bw_item = self.imageViewer.data_browser.table_data.item(0, bw_column)
        bw_old = bw_item.text()
        self.assertEqual(int(bw_old), 50000)
        bw_item.setSelected(True)
        bw_item.setText("0")
        self.assertEqual(self.imageViewer.project.undos, [['modified_values', [['data/raw_data/Guerbet-C6-2014-Rat-K52-Tube27-2014-02-14_10-23-17-02-G1_Guerbet_Anat-RARE__pvm_-00-02-20.000.nii', 'BandWidth', 50000.0, 0.0]]]])
        self.assertEqual(self.imageViewer.project.redos, [])
        bw_item = self.imageViewer.data_browser.table_data.item(0, bw_column)
        bw_set = bw_item.text()
        self.assertEqual(int(bw_set), 0)
        self.imageViewer.action_undo.trigger()
        bw_item = self.imageViewer.data_browser.table_data.item(0, bw_column)
        bw_undo = bw_item.text()
        self.assertEqual(int(bw_undo), 50000)
        self.assertEqual(self.imageViewer.project.redos, [['modified_values', [[
                                                                                   'data/raw_data/Guerbet-C6-2014-Rat-K52-Tube27-2014-02-14_10-23-17-02-G1_Guerbet_Anat-RARE__pvm_-00-02-20.000.nii',
                                                                                   'BandWidth', 50000.0, 0.0]]]])
        self.assertEqual(self.imageViewer.project.undos, [])
        self.imageViewer.action_redo.trigger()
        self.assertEqual(self.imageViewer.project.undos, [['modified_values', [[
                                                                                   'data/raw_data/Guerbet-C6-2014-Rat-K52-Tube27-2014-02-14_10-23-17-02-G1_Guerbet_Anat-RARE__pvm_-00-02-20.000.nii',
                                                                                   'BandWidth', 50000.0, 0.0]]]])
        self.assertEqual(self.imageViewer.project.redos, [])
        bw_item = self.imageViewer.data_browser.table_data.item(0, bw_column)
        bw_redo = bw_item.text()
        self.assertEqual(int(bw_redo), 0)

if __name__ == '__main__':
    unittest.main()