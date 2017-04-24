from abc import ABCMeta, abstractproperty

import six

from eventsourcing.domain.model.events import EventWithEntityID, EventWithEntityVersion, EventWithTimestamp


class AbstractSnapshop(six.with_metaclass(ABCMeta)):
    @abstractproperty
    def topic(self):
        """
        Path to the class of the snapshotted entity.
        """

    @abstractproperty
    def state(self):
        """
        State of the snapshotted entity.
        """

    @abstractproperty
    def entity_id(self):
        """
        ID of the snapshotted entity.
        """

    @abstractproperty
    def originator_version(self):
        """
        Version of the last event applied to the entity.
        """


class Snapshot(EventWithTimestamp, EventWithEntityVersion, EventWithEntityID, AbstractSnapshop):
    def __init__(self, entity_id, originator_version, topic, state):
        super(Snapshot, self).__init__(
            entity_id=entity_id,
            originator_version=originator_version,
            topic=topic,
            state=state,
        )

    @property
    def topic(self):
        """
        Path to the class of the snapshotted entity.
        """
        return self.__dict__['topic']

    @property
    def state(self):
        """
        State of the snapshotted entity.
        """
        return self.__dict__['state']
