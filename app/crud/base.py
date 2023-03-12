from bson import ObjectId
from typing import Any, List
from pymongo.collection import Collection


class CRUD:
    """
    These methods are used to perform CRUD operations on a collection
    Note that no validation is performed on the data, it is assumed that the data is valid
    """
    @staticmethod
    def read_one(collection: Collection, _id: Any) -> dict or None:
        """
        :return: The object if found, None otherwise
        """
        return collection.find_one({"_id": _id})

    @staticmethod
    def read_all(collection: Collection, *, skip: int = 0, limit: int = 100) -> List[dict]:
        """
        :return: list of objects
        """
        if skip < 0:
            skip = 0

        if limit < 0:
            limit = 100

        return list(collection.find(skip=skip,
                                    limit=limit))

    @staticmethod
    def create(collection: Collection, *, obj_in: dict) -> dict:
        """
        :return: The created object
        """
        obj_in["_id"] = str(ObjectId())
        obj_in = collection.insert_one(obj_in)
        created_obj_id = obj_in.inserted_id

        return collection.find_one({"_id": created_obj_id})

    @staticmethod
    def update(collection: Collection, *, _id: Any, obj_in: dict) -> dict or None:
        """
        :return: The updated object if updated, None otherwise
        """
        update_feedback = collection.update_one(filter={"_id": _id},
                                                update={"$set": obj_in})

        if update_feedback.modified_count == 1:
            return collection.find_one({"_id": _id})

        return None

    @staticmethod
    def delete(collection: Collection, *, _id: Any) -> dict or None:
        """
        :return: The deleted object if deleted, None otherwise
        """
        deleted_obj = collection.find_one({"_id": _id})
        delete_feedback = collection.delete_one({"_id": _id})

        if delete_feedback.deleted_count == 1:
            return deleted_obj

        return None
