from pytgcalls import PyTgCalls, filters as cfilters
from pytgcalls.types import MediaStream, ChatUpdate

from ahmedyad.config import UBCall
from ahmedyad.queues import QUEUE, clear_queue, get_queue, pop_an_item


async def skip_current_song(chat_id):
    if chat_id in QUEUE:
        chat_queue = get_queue(chat_id)
        if len(chat_queue) == 1:
            await UBCall.leave_call(chat_id)
            clear_queue(chat_id)
            return 1
        else:
            songname = chat_queue[1][0]
            url = chat_queue[1][1]
            link = chat_queue[1][2]
            stream_type = chat_queue[1][3]
            await UBCall.play(
                chat_id,
                url,
            )

            pop_an_item(chat_id)
            return [songname, link, stream_type]
    else:
        return 0


async def skip_item(chat_id, h):
    if chat_id in QUEUE:
        chat_queue = get_queue(chat_id)
        try:
            x = int(h)
            songname = chat_queue[x][0]
            chat_queue.pop(x)
            return songname
        except (ValueError, IndexError):
            return 0
    else:
        return 0


@UBCall.on_update(cfilters.stream_end)
async def on_end_handler(client, update):
    chat_id = update.chat_id
    await skip_current_song(chat_id)


@UBCall.on_update(cfilters.chat_update(ChatUpdate.Status.CLOSED_VOICE_CHAT))
async def close_handler(client: PyTgCalls, chat_id: int):
    if chat_id in QUEUE:
        clear_queue(chat_id)


@UBCall.on_update(cfilters.chat_update(ChatUpdate.Status.LEFT_CALL))
async def kicked_handler(client, update):
    if update.chat_id in QUEUE:
        clear_queue(update.chat_id)
