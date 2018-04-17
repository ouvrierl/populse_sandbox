import glob
import os.path
import json
import Utils.Utils as utils
import hashlib # To generate the md5 of each scan
from populse_db.DatabaseModel import TAG_ORIGIN_RAW, TAG_TYPE_STRING, TAG_ORIGIN_USER, TAG_TYPE_LIST_INTEGER, TAG_TYPE_LIST_DATE, TAG_TYPE_INTEGER, TAG_TYPE_LIST_DATETIME, TAG_TYPE_LIST_FLOAT, TAG_TYPE_TIME, TAG_TYPE_FLOAT, TAG_TYPE_DATE, TAG_TYPE_DATETIME, TAG_TYPE_LIST_TIME, TAG_TYPE_LIST_STRING
from SoftwareProperties.Config import Config
import datetime
import yaml
from time import time
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QProgressDialog
from datetime import datetime

def getJsonTagsFromFile(file_path, path):
   """
    :return:
    :param file_path: file path of the Json file
    :param path: project path
    :return: a list of the Json tags of the file"""
   json_tags = []
   with open(os.path.join(path, file_path) + ".json") as f:
       for name,value in json.load(f).items():
            json_tags.append([name, value])
   return json_tags


def createProject(name, path, parent_folder):
    """
    Creates a new project
    :param name: project name
    :param path: project path
    :param parent_folder: project folder
    :return: the project object
    """

    # Formating the name to remove spaces et strange characters -> folder name
    recorded_path = os.path.relpath(parent_folder)
    new_path = os.path.join(recorded_path, name)

    # Creating the folder with the folder name that has been formatted
    if not os.path.exists(new_path):
        project_parent_folder = os.makedirs(new_path)
        data_folder = os.makedirs(os.path.join(new_path, 'data'))
        project_path = os.path.join(new_path, name)
        raw_data_folder = os.makedirs(os.path.join(os.path.join(new_path, 'data'), 'raw_data'))
        derived_data_folder = os.makedirs(os.path.join(os.path.join(new_path, 'data'), 'derived_data'))

        #Properties
        os.mkdir(os.path.join(new_path, 'properties'))
        properties = dict(
            name=name,
            date=datetime.now().strftime('%d/%m/%Y %H:%M:%S'),
            sorted_tag='',
            sort_order=''
        )
        with open(os.path.join(new_path, 'properties', 'properties.yml'), 'w', encoding='utf8') as propertyfile:
            yaml.dump(properties, propertyfile, default_flow_style=False, allow_unicode=True)


def read_log(project):

    """ From the log export file of the import software, the data base (here the current project) is loaded with
    the tags"""

    begin = time()

    raw_data_folder = os.path.relpath(os.path.join(project.folder, 'data', 'raw_data'))

    # Checking all the export logs from MRIManager and taking the most recent
    list_logs = glob.glob(os.path.join(raw_data_folder, "logExport*.json"))
    log_to_read = max(list_logs, key=os.path.getctime)

    with open(log_to_read, "r", encoding="utf-8") as file:
        list_dict_log = json.load(file)

    # For history
    historyMaker = []
    historyMaker.append("add_scans")
    scans_added = []
    values_added = []
    tags_set = []

    # Default tags stored
    config = Config()
    default_tags = config.getDefaultTags()
    tags_to_remove = ["Dataset data file", "Dataset header file"] # List of tags to remove

    # Progressbar
    len_log = len(list_dict_log)
    ui_progressbar = QProgressDialog("Reading exported files", "Cancel", 0, len_log)
    ui_progressbar.setWindowModality(Qt.WindowModal)
    ui_progressbar.setWindowTitle("")
    idx = 0
    for dict_log in list_dict_log:

        # Progressbar
        idx += 1
        ui_progressbar.setValue(idx)
        if ui_progressbar.wasCanceled():
            break

        if dict_log['StatusExport'] == "Export ok":
            file_name = dict_log['NameFile']
            path_name = raw_data_folder
            with open(os.path.join(path_name, file_name) + ".nii", 'rb') as scan_file:
                data = scan_file.read()
                original_md5 = hashlib.md5(data).hexdigest()

            project.database.add_scan(file_name, original_md5) # Scan added to the Database
            scans_added.append([file_name, original_md5]) # Scan added to history

            # We create the tag FileName
            project.database.add_value(file_name, "FileName", file_name, None) # FileName tag added
            values_added.append([file_name, "FileName", file_name, None])

            # For each tag in each scan
            for tag in getJsonTagsFromFile(file_name, path_name): # For each tag of the scan

                # We do the tag only if it's not in the tags to remove
                if tag[0] not in tags_to_remove:
                    properties = tag[1]
                    unit = None
                    format = ''
                    tag_type = TAG_TYPE_STRING
                    description = None
                    if isinstance(properties, dict):
                        value = properties['value']
                        unit = properties['units']
                        if unit == "":
                            unit = None
                        format = properties['format']
                        tag_type = properties['type']
                        if tag_type == "":
                            tag_type = TAG_TYPE_STRING
                        description = properties['description']
                        if description == "":
                            description = None
                    else:
                        value = properties[0]

                    tag_name = tag[0]

                    # Creating date types
                    if format is not None and format != "":
                        format = format.replace("yyyy", "%Y")
                        format = format.replace("MM", "%m")
                        format = format.replace("dd", "%d")
                        format = format.replace("HH", "%H")
                        format = format.replace("mm", "%M")
                        format = format.replace("ss", "%S")
                        format = format.replace("SSS", "%f")
                        if "%Y" in format and "%m" in format and "%d" in format and "%H" in format and "%M" in format and "%S" in format:
                            tag_type = TAG_TYPE_DATETIME
                        elif "%Y" in format and "%m" in format and "%d" in format:
                            tag_type = TAG_TYPE_DATE
                        elif "%H" in format and "%M" in format and "%S" in format:
                            tag_type = TAG_TYPE_TIME

                    if tag_name != "Json_Version":
                        # Preparing value and type
                        if len(value) is 1:
                            value = value[0]
                        else:
                            if tag_type == TAG_TYPE_STRING:
                                tag_type = TAG_TYPE_LIST_STRING
                            elif tag_type == TAG_TYPE_INTEGER:
                                tag_type = TAG_TYPE_LIST_INTEGER
                            elif tag_type == TAG_TYPE_FLOAT:
                                tag_type = TAG_TYPE_LIST_FLOAT
                            elif tag_type == TAG_TYPE_DATE:
                                tag_type = TAG_TYPE_LIST_DATE
                            elif tag_type == TAG_TYPE_DATETIME:
                                tag_type = TAG_TYPE_LIST_DATETIME
                            elif tag_type == TAG_TYPE_TIME:
                                tag_type = TAG_TYPE_LIST_TIME
                            value_prepared = []
                            for value_single in value:
                                value_prepared.append(value_single[0])
                            value = value_prepared

                    if tag_type == TAG_TYPE_DATETIME or tag_type == TAG_TYPE_DATE or tag_type == TAG_TYPE_TIME:
                        if value is not None and value != "":
                            value = datetime.strptime(value, format)
                            if tag_type == TAG_TYPE_TIME:
                                value = value.time()
                            elif tag_type == TAG_TYPE_DATE:
                                value = value.date()

                    # TODO time lists

                    # Tag updated in database
                    database_tag = project.database.get_tag(tag_name)
                    if database_tag is None:
                        # Adding the tag as it's not in the database yet
                        if tag_name in default_tags:
                            project.database.add_tag(tag_name, True, TAG_ORIGIN_RAW, tag_type, unit, None,
                                                     description)
                        else:
                            project.database.add_tag(tag_name, False, TAG_ORIGIN_RAW, tag_type, unit, None,
                                                     description)
                    elif tag_name not in tags_set:
                        tags_set.append(tag_name)
                        # The tag is updated as it's already in the database
                        project.database.set_tag_origin(tag_name, TAG_ORIGIN_RAW)
                        if tag_name in default_tags:
                            project.database.set_tag_visibility(tag_name, True)
                        else:
                            project.database.set_tag_visibility(tag_name, False)
                        project.database.set_tag_description(tag_name, description)
                        project.database.set_tag_type(tag_name, tag_type)
                        project.database.set_tag_unit(tag_name, unit)

                    # The value is accepted if it's not empty or null
                    if value is not None and value != "":
                        project.database.add_value(file_name, tag_name, value, value) # Value added to the Database
                        values_added.append([file_name, tag_name, value, value]) # Value added to history

    ui_progressbar.close()

    # Missing values added thanks to default values
    for tag in project.database.get_tags():
        if tag.origin == TAG_ORIGIN_USER:
            for scan in scans_added:
                if tag.default_value is not None and project.database.get_current_value(scan[0], tag.name) is None:
                    project.database.add_value(scan[0], tag.name, tag.default_value, None)
                    values_added.append([scan[0], tag.namee, tag.default_value, None])  # Value added to history

    # For history
    historyMaker.append(scans_added)
    historyMaker.append(values_added)
    project.undos.append(historyMaker)
    project.redos.clear()

    print("read_log time: " + str(time() - begin))

def verify_scans(project, path):
    # Returning the files that are problematic
    return_list = []
    for scan in project.database.get_scans():

        file_name = scan.name
        path_name = os.path.relpath(os.path.join(path, 'data', 'raw_data'))

        if os.path.exists(os.path.join(path_name, file_name) + ".nii"):
            # If the file exists, we do the checksum
            with open(os.path.join(path_name, file_name) + ".nii", 'rb') as scan_file:
                data = scan_file.read()
                actual_md5 = hashlib.md5(data).hexdigest()

            if actual_md5 != scan.checksum:
                return_list.append(file_name)

        else:
            # Otherwise, we directly add the file in the list
            return_list.append(file_name)

    return return_list


def save_project(database):
    database.saveModifications()