class DomainModel:
    """
    A domain entity that should encapsulate the core business logic (alongside a `DomainService`).
    """


class ValueObject:
    """
    A domain data entity used to store data in the application, and is never persisted. Always re-constructable
    from persisted data (usually encapsulated by a `DomainModel`).
    """


class Dto:
    """
    A data transfer object (DTO).

    Must have JSON serializable fields (i.e. of mostly primitive types).
    """
