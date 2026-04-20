import logging

logger = logging.getLogger(__name__)


def notify_resident(request_obj):
    """
    STUB: уведомление жителю при смене статуса.
    В продакшене — отправка в личку Telegram-бота.
    Сейчас — логирование в консоль.
    """
    msg = (
        f"[STUB NOTIFY] Жителю {request_obj.contact} (tg_id={request_obj.resident_tg_id}):\n"
        f"Обращение #{request_obj.number}\n"
        f"Новый статус: {request_obj.get_status_display()}\n"
        f"Комментарий: {request_obj.comment_to_resident or '—'}"
    )
    logger.info(msg)
    print(msg)


def create_request_from_classification(
    category, house_id, text, sender_name="", sentiment="neutral", summary="", chat_id=None, message_id=None, resident_tg_id=None
):
    """
    Авто-создание обращения из классифицированного сообщения бота.
    Категории бота → тип обращения:
      Аварийный сигнал → Авария
      Жалоба → Жалоба
      Заявка / просьба → Заявка
      Вопрос → Вопрос
      Предложение → Предложение
      Информационное / Благодарность / Шум → не создают обращение (return None)
    """
    from dispatcher.models import Request, House

    CATEGORY_MAP = {
        "Аварийный сигнал": Request.TYPE_EMERGENCY,
        "Жалоба": Request.TYPE_COMPLAINT,
        "Заявка / просьба": Request.TYPE_REQUEST,
        "Вопрос": Request.TYPE_QUESTION,
        "Предложение": Request.TYPE_PROPOSAL,
    }

    request_type = CATEGORY_MAP.get(category)
    if request_type is None:
        return None

    house = House.objects.get(pk=house_id)
    sentiment_map = {
        "Негативная": Request.SENTIMENT_NEGATIVE,
        "Нейтральная": Request.SENTIMENT_NEUTRAL,
        "Позитивная": Request.SENTIMENT_POSITIVE,
    }
    sentiment_val = sentiment_map.get(sentiment, Request.SENTIMENT_NEUTRAL)

    req = Request.objects.create(
        type=request_type,
        house=house,
        text=text,
        contact=sender_name,
        sentiment=sentiment_val,
        summary=summary,
        chat_id=chat_id,
        message_id=message_id,
        resident_tg_id=resident_tg_id,
    )
    logger.info(f"Auto-created request #{req.number} from category '{category}'")
    return req
