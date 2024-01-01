from uuid import UUID


def compare_uuid(uuid: UUID, uuid_compare: UUID) -> bool:
    try:
        return str(uuid).__contains__(str(uuid_compare))
    except Exception as ex:
        return False
