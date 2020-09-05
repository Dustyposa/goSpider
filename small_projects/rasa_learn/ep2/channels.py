import inspect
import logging
from asyncio import CancelledError
from typing import Text, Callable, Awaitable, List, Dict

from rasa.core.channels import RestInput, UserMessage, CollectingOutputChannel
from rasa.server import get_tracker
from sanic import Blueprint, response
from sanic.request import Request
from sanic.response import HTTPResponse

logger = logging.getLogger(__name__)


class RobotInput(RestInput):

    @classmethod
    def name(cls) -> Text:
        return "rest"

    def blueprint(
            self, on_new_message: Callable[[UserMessage], Awaitable[None]]
    ) -> Blueprint:
        robot_webhook = Blueprint(
            "robot_webhook_{}".format(type(self).__name__),
            inspect.getmodule(self).__name__,
        )

        @robot_webhook.route("/", methods=["GET"])
        async def health(_: Request):
            return response.json({"status": "ok"})

        @robot_webhook.route("/webhook", methods=["POST"])
        async def receive(request: Request) -> HTTPResponse:
            sender_id = await self._extract_sender(request)
            text = self._extract_message(request)
            input_channel = self._extract_input_channel(request)
            metadata = self.get_metadata(request)
            collector = CollectingOutputChannel()
            # noinspection PyBroadException
            try:
                message = UserMessage(
                    text,
                    collector,
                    sender_id,
                    input_channel=input_channel,
                    metadata=metadata,
                )
                await on_new_message(
                    message
                )
            except CancelledError:
                logger.error(
                    "Message handling timed out for "
                    "user message '{}'.".format(text)
                )
            except Exception:
                logger.exception(
                    "An exception occured while handling "
                    "user message '{}'.".format(text)
                )
            return response.json(self.__filter_confidence_below_threshold(
                request=request,
                message=collector.messages,
                sender_id=sender_id
            ))

        return robot_webhook

    def __filter_confidence_below_threshold(
            self,
            request: Request,
            message: List[Dict[str, str]],
            sender_id: str
    ) -> List[Dict[str, str]]:
        tracker = request.app.agent.tracker_store.get_or_create_tracker(sender_id)
        parse_data = tracker.latest_message.parse_data
        response_selector = parse_data.get("response_selector")
        ranking = response_selector["default"]["ranking"]
        if ranking:
            response_msg = [msg["text"] for msg in message]
            kv_ranking = self._turn_to_kv_dict(ranking)
            threshold = 0.80
            del_index = []
            for text in response_msg:
                confidence = kv_ranking.get(text, 1.0)
                if confidence < threshold:
                    del_index.append(text)
            return list(filter(lambda item: item["text"] not in del_index, message))

        return message

    @staticmethod
    def _turn_to_kv_dict(data: List[Dict[str, str]]) -> Dict[str, str]:
        return {item["name"]: item["confidence"] for item in data}
