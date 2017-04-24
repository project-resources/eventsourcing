import uuid

from eventsourcing.domain.model.entity import AbstractEntityRepository, TimestampedVersionedEntity, AttributeChanged, Created, \
    Discarded, attribute, entity_mutator, singledispatch
from eventsourcing.domain.model.events import TimestampedVersionedEntityEvent, publish


class Example(TimestampedVersionedEntity):
    """
    An example event sourced domain model entity.
    """

    class Created(Created):
        pass

    class AttributeChanged(AttributeChanged):
        pass

    class Discarded(Discarded):
        pass

    class Heartbeat(TimestampedVersionedEntityEvent):
        pass

    def __init__(self, foo='', a='', b='', **kwargs):
        super(Example, self).__init__(**kwargs)
        self._foo = foo
        self._a = a
        self._b = b
        self._count_heartbeats = 0

    @attribute
    def foo(self):
        """An example attribute."""

    @attribute
    def a(self):
        """An example attribute."""

    @attribute
    def b(self):
        """Another example attribute."""

    def beat_heart(self, number_of_beats=1):
        self._assert_not_discarded()
        events = []
        while number_of_beats > 0:
            event = self.Heartbeat(entity_id=self._id, originator_version=self._version)
            events.append(event)
            self._apply(event)
            number_of_beats -= 1
        publish(events)

    def count_heartbeats(self):
        return self._count_heartbeats

    @staticmethod
    def _mutator(event, initial):
        return example_mutator(event, initial)


@singledispatch
def example_mutator(event, initial):
    return entity_mutator(event, initial)


@example_mutator.register(Example.Heartbeat)
def heartbeat_mutator(event, self):
    self._validate_originator(event)
    assert isinstance(self, Example), self
    self._count_heartbeats += 1
    self._increment_version()
    return self


class AbstractExampleRepository(AbstractEntityRepository):
    pass


def create_new_example(foo='', a='', b=''):
    """
    Factory method for example entities.

    :rtype: Example
    """
    entity_id = uuid.uuid4()
    event = Example.Created(entity_id=entity_id, foo=foo, a=a, b=b)
    entity = Example.mutate(event=event)
    publish(event=event)
    return entity
