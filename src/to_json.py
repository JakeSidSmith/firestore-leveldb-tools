import os
import json
import sys
# import google sdks
from google.appengine.api.files import records
from google.appengine.datastore import entity_pb
from google.appengine.api import datastore

cwd = os.getcwd()
# repo_root = os.path.dirname(os.path.realpath(__file__))


if len(sys.argv) < 2:
    sys.exit("No firestore backup folder specified")

if len(sys.argv) < 3:
    sys.exit("No outfile specified")

backup = sys.argv[1]
out_file = sys.argv[2]

if not out_file.endswith(".json"):
    sys.exit("Outfile should have .json extension")

# command-line arguments
backup_folder = os.path.join(cwd, os.path.normpath(backup))
out_path = os.path.join(cwd, os.path.normpath(out_file))


def get_collection_in_json_tree_for_proto_entity(json_tree, entity_proto):
    result = json_tree
    for element in entity_proto.key().path().element_list():
        next_key = None
        if element.has_type():
            next_key = element.type()
        elif element.has_name():
            next_key = element.name()
        # elif element.has_id(): next_key = element.id()

        if next_key is not None:
            if next_key not in result:
                result[next_key] = {}
            result = result[next_key]
    return result


# def get_collection_of_proto_entity(entity_proto):
#     # reverse path-elements, so we always get last collection
#     for element in entity_proto.key().path().element_list():
#         if element.has_type():
#             return element.type()


def get_key_of_proto_entity(entity_proto):
    # reverse path-elements, so we always get last key
    for element in reversed(entity_proto.key().path().element_list()):
        if element.has_name():
            return element.name()
        # if element.has_id(): return element.id()


def get_value_of_proto_entity(entity_proto):
    return datastore.Entity.FromPb(entity_proto)


def json_serialize_func(obj):
    import calendar
    import datetime

    if isinstance(obj, datetime.datetime):
        if obj.utcoffset() is not None:
            obj = obj - obj.utcoffset()
        millis = int(
            calendar.timegm(obj.timetuple()) * 1000 +
            obj.microsecond / 1000
        )
        return millis
    # raise TypeError('Not sure how to serialize %s' % (obj,))
    return str(obj)


def init():
    json_tree = {}
    items = []

    for filename in os.listdir(backup_folder):
        if not filename.startswith("output-"):
            continue
        print("Reading from:" + filename)

        in_path = os.path.join(backup_folder, filename)
        raw = open(in_path, 'rb')
        reader = records.RecordsReader(raw)
        for record_index, record in enumerate(reader):
            entity_proto = entity_pb.EntityProto(contents=record)

            # collection = GetCollectionOfProtoEntity(entity_proto)
            collection_in_json_tree = get_collection_in_json_tree_for_proto_entity(
                json_tree, entity_proto)
            key = get_key_of_proto_entity(entity_proto)
            entity = get_value_of_proto_entity(entity_proto)

            collection_in_json_tree[key] = entity
            # also add to flat list, so we know the total item count
            items.append(entity)

            print("Parsing document #" + str(len(items)))

    out = open(out_path, 'w')
    out.write(json.dumps(json_tree, default=json_serialize_func,
                         encoding='latin-1', indent=2))
    out.close()
    print("JSON file written to: " + out_path)


init()
