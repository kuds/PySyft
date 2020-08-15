from typing import List
from enum import Enum

from ...common.service.auth import service_auth
from ..... import serialize, deserialize
from ....common import UID
from .....proto.core.node.domain.service.get_all_requests_message_pb2 import (
    GetAllRequestsMessage as GetAllRequestsMessage_PB,
)
from .....proto.core.node.domain.service.get_all_requests_message_pb2 import (
    GetAllRequestsResponseMessage as GetAllRequestsResponseMessage_PB,
)
from .request_message import RequestMessage
from typing import Optional
from ....io.address import Address
from ....common.message import ImmediateSyftMessageWithoutReply
from ....common.message import ImmediateSyftMessageWithReply
from ...common.service.node_service import ImmediateNodeServiceWithoutReply
from .....decorators import syft_decorator
from ...abstract.node import AbstractNode
from nacl.signing import VerifyKey
from google.protobuf.reflection import GeneratedProtocolMessageType


class GetAllRequestsMessage(ImmediateSyftMessageWithReply):
    def __init__(
        self, address: Address, reply_to: Address, msg_id: Optional[UID] = None
    ):
        super().__init__(address=address, msg_id=msg_id, reply_to=reply_to)

    @syft_decorator(typechecking=True)
    def _object2proto(self) -> GetAllRequestsMessage_PB:
        """Returns a protobuf serialization of self.

        As a requirement of all objects which inherit from Serializable,
        this method transforms the current object into the corresponding
        Protobuf object so that it can be further serialized.

        :return: returns a protobuf object
        :rtype: GetAllRequestsMessage_PB

        .. note::
            This method is purely an internal method. Please use object.serialize() or one of
            the other public serialization methods if you wish to serialize an
            object.
        """
        return GetAllRequestsMessage_PB(
            msg_id=self.id.serialize(),
            address=self.address.serialize(),
            reply_to=self.reply_to.serialize(),
        )

    @staticmethod
    def _proto2object(proto: GetAllRequestsMessage_PB) -> "GetAllRequestsMessage":
        """Creates a ReprMessage from a protobuf

        As a requirement of all objects which inherit from Serializable,
        this method transforms a protobuf object into an instance of this class.

        :return: returns an instance of ReprMessage
        :rtype: ReprMessage

        .. note::
            This method is purely an internal method. Please use syft.deserialize()
            if you wish to deserialize an object.
        """

        return GetAllRequestsMessage(
            msg_id=deserialize(blob=proto.msg_id),
            address=deserialize(blob=proto.address),
            reply_to=deserialize(blob=proto.reply_to),
        )

    @staticmethod
    def get_protobuf_schema() -> GeneratedProtocolMessageType:
        """ Return the type of protobuf object which stores a class of this type

        As a part of serializatoin and deserialization, we need the ability to
        lookup the protobuf object type directly from the object type. This
        static method allows us to do this.

        Importantly, this method is also used to create the reverse lookup ability within
        the metaclass of Serializable. In the metaclass, it calls this method and then
        it takes whatever type is returned from this method and adds an attribute to it
        with the type of this class attached to it. See the MetaSerializable class for details.

        :return: the type of protobuf object which corresponds to this class.
        :rtype: GeneratedProtocolMessageType

        """

        return GetAllRequestsMessage_PB


class GetAllRequestsResponseMessage(ImmediateSyftMessageWithoutReply):
    def __init__(
        self,
        requests: List[RequestMessage],
        address: Address,
        msg_id: Optional[UID] = None,
    ):
        super().__init__(address=address, msg_id=msg_id)
        self.requests = requests

    @syft_decorator(typechecking=True)
    def _object2proto(self) -> GetAllRequestsResponseMessage_PB:
        """Returns a protobuf serialization of self.

        As a requirement of all objects which inherit from Serializable,
        this method transforms the current object into the corresponding
        Protobuf object so that it can be further serialized.

        :return: returns a protobuf object
        :rtype: ReprMessage_PB

        .. note::
            This method is purely an internal method. Please use object.serialize() or one of
            the other public serialization methods if you wish to serialize an
            object.
        """
        return GetAllRequestsResponseMessage_PB(
            msg_id=self.id.serialize(),
            address=self.address.serialize(),
            requests=list(map(lambda x: x.serialize(), self.requests)),
        )

    @staticmethod
    def _proto2object(
        proto: GetAllRequestsResponseMessage_PB,
    ) -> "GetAllRequestsResponseMessage":
        """Creates a GetAllRequestsResponseMessage from a protobuf

        As a requirement of all objects which inherit from Serializable,
        this method transforms a protobuf object into an instance of this class.

        :return: returns an instance of GetAllRequestsResponseMessage
        :rtype: GetAllRequestsResponseMessage

        .. note::
            This method is purely an internal method. Please use syft.deserialize()
            if you wish to deserialize an object.
        """

        return GetAllRequestsResponseMessage(
            msg_id=deserialize(blob=proto.msg_id),
            address=deserialize(blob=proto.address),
            requests=[deserialize(blob=x) for x in proto.requests],
        )

    @staticmethod
    def get_protobuf_schema() -> GeneratedProtocolMessageType:
        """ Return the type of protobuf object which stores a class of this type

        As a part of serializatoin and deserialization, we need the ability to
        lookup the protobuf object type directly from the object type. This
        static method allows us to do this.

        Importantly, this method is also used to create the reverse lookup ability within
        the metaclass of Serializable. In the metaclass, it calls this method and then
        it takes whatever type is returned from this method and adds an attribute to it
        with the type of this class attached to it. See the MetaSerializable class for details.

        :return: the type of protobuf object which corresponds to this class.
        :rtype: GeneratedProtocolMessageType

        """

        return GetAllRequestsResponseMessage_PB


class GetAllRequestsService(ImmediateNodeServiceWithoutReply):
    @staticmethod
    @syft_decorator(typechecking=True)
    def message_handler_types() -> List[type]:
        return [GetAllRequestsMessage]

    @staticmethod
    @syft_decorator(typechecking=True)
    @service_auth(root_only=True)
    def process(
        node: AbstractNode, msg: GetAllRequestsMessage, verify_key: VerifyKey
    ) -> GetAllRequestsResponseMessage:
        return GetAllRequestsResponseMessage(
            requests=node.requests, address=msg.reply_to
        )
