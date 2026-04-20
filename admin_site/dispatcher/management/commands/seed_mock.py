from django.core.management.base import BaseCommand
from dispatcher.models import House, Request


HOUSES = [
    {"name": "Левобережье, дом 10", "chat_id": -1001111111111},
    {"name": "Левобережье, дом 15", "chat_id": -1002222222222},
    {"name": "Правобережье, дом 21", "chat_id": -1003333333333},
]

MOCK_REQUESTS = [
    {
        "type": Request.TYPE_EMERGENCY,
        "text": "В подвале течет вода, срочно посмотрите!",
        "sentiment": Request.SENTIMENT_NEGATIVE,
        "summary": "Течь воды в подвале",
        "house_idx": 0,
        "entrance": "1",
        "apartment": "",
        "contact": "@ivan_resident",
        "status": Request.STATUS_ACCEPTED,
        "resident_tg_id": 100001,
    },
    {
        "type": Request.TYPE_COMPLAINT,
        "text": "Уже третий день нет горячей воды, когда починят?",
        "sentiment": Request.SENTIMENT_NEGATIVE,
        "summary": "Нет горячей воды 3 дня",
        "house_idx": 0,
        "entrance": "2",
        "apartment": "45",
        "contact": "@maria_smith",
        "status": Request.STATUS_IN_PROGRESS,
        "resident_tg_id": 100002,
    },
    {
        "type": Request.TYPE_REQUEST,
        "text": "Пожалуйста, замените лампочку в подъезде номер 3, на этаже 5 темно.",
        "sentiment": Request.SENTIMENT_NEUTRAL,
        "summary": "Замена лампочки в подъезде",
        "house_idx": 1,
        "entrance": "3",
        "apartment": "",
        "contact": "@petr_n",
        "status": Request.STATUS_ACCEPTED,
        "resident_tg_id": 100003,
    },
    {
        "type": Request.TYPE_QUESTION,
        "text": "Подскажите, когда плановое отключение отопления?",
        "sentiment": Request.SENTIMENT_NEUTRAL,
        "summary": "Вопрос про отключение отопления",
        "house_idx": 2,
        "entrance": "",
        "apartment": "",
        "contact": "@anna_q",
        "status": Request.STATUS_NEED_INFO,
        "resident_tg_id": 100004,
    },
    {
        "type": Request.TYPE_COMPLAINT,
        "text": "Соседи сверху шумят после 23:00, невозможно спать!",
        "sentiment": Request.SENTIMENT_NEGATIVE,
        "summary": "Шум от соседей ночью",
        "house_idx": 0,
        "entrance": "1",
        "apartment": "12",
        "contact": "@sleepy_resident",
        "status": Request.STATUS_IN_PROGRESS,
        "resident_tg_id": 100005,
    },
    {
        "type": Request.TYPE_EMERGENCY,
        "text": "Запах газа в подъезде! Срочно вызовите службу!",
        "sentiment": Request.SENTIMENT_NEGATIVE,
        "summary": "Запах газа в подъезде",
        "house_idx": 1,
        "entrance": "2",
        "apartment": "",
        "contact": "@worried_mom",
        "status": Request.STATUS_DONE,
        "comment_to_resident": "Аварийная служба выехала, утечка устранена.",
        "resident_tg_id": 100006,
    },
    {
        "type": Request.TYPE_PROPOSAL,
        "text": "Предлагаю установить детскую площадку во дворе дома 21.",
        "sentiment": Request.SENTIMENT_POSITIVE,
        "summary": "Предложение установить детскую площадку",
        "house_idx": 2,
        "entrance": "",
        "apartment": "",
        "contact": "@active_citizen",
        "status": Request.STATUS_ACCEPTED,
        "resident_tg_id": 100007,
    },
    {
        "type": Request.TYPE_REQUEST,
        "text": "Нужен доступ к подвалу для проверки счетчиков, квартира 78.",
        "sentiment": Request.SENTIMENT_NEUTRAL,
        "summary": "Доступ в подвал для счетчиков",
        "house_idx": 1,
        "entrance": "4",
        "apartment": "78",
        "contact": "@homeowner_78",
        "status": Request.STATUS_ACCEPTED,
        "resident_tg_id": 100008,
    },
    {
        "type": Request.TYPE_COMPLAINT,
        "text": "Мусоропровод забит, мусор на этажах уже неделю!",
        "sentiment": Request.SENTIMENT_NEGATIVE,
        "summary": "Забит мусоропровод",
        "house_idx": 2,
        "entrance": "1",
        "apartment": "",
        "contact": "@angry_resident",
        "status": Request.STATUS_ACCEPTED,
        "resident_tg_id": 100009,
    },
    {
        "type": Request.TYPE_QUESTION,
        "text": "Куда обращаться по поводу протечки крыши?",
        "sentiment": Request.SENTIMENT_NEUTRAL,
        "summary": "Вопрос про протечку крыши",
        "house_idx": 0,
        "entrance": "",
        "apartment": "5",
        "contact": "@roof_problem",
        "status": Request.STATUS_IN_PROGRESS,
        "resident_tg_id": 100010,
    },
    {
        "type": Request.TYPE_REQUEST,
        "text": "Просьба озеленить территорию возле дома, очень голый двор.",
        "sentiment": Request.SENTIMENT_NEUTRAL,
        "summary": "Озеленение двора",
        "house_idx": 2,
        "entrance": "",
        "apartment": "",
        "contact": "@green_thumb",
        "status": Request.STATUS_REJECTED,
        "comment_to_resident": "Озеленение запланировано на следующий сезон.",
        "internal_comment": "Бюджет на этот год исчерпан",
        "resident_tg_id": 100011,
    },
    {
        "type": Request.TYPE_EMERGENCY,
        "text": "Обрушение штукатурки в подъезде! Чуть не ударило ребенка!",
        "sentiment": Request.SENTIMENT_NEGATIVE,
        "summary": "Обрушение штукатурки",
        "house_idx": 1,
        "entrance": "1",
        "apartment": "",
        "contact": "@scared_parent",
        "status": Request.STATUS_IN_PROGRESS,
        "resident_tg_id": 100012,
    },
    {
        "type": Request.TYPE_COMPLAINT,
        "text": "Лифт снова сломан, пожилые люди не могут подняться на 9 этаж.",
        "sentiment": Request.SENTIMENT_NEGATIVE,
        "summary": "Сломан лифт",
        "house_idx": 0,
        "entrance": "2",
        "apartment": "",
        "contact": "@elderly_help",
        "status": Request.STATUS_NEED_INFO,
        "resident_tg_id": 100013,
    },
    {
        "type": Request.TYPE_REQUEST,
        "text": "Прошу выдать ключи от почтовых ящиков, мы новые жильцы кв. 33.",
        "sentiment": Request.SENTIMENT_NEUTRAL,
        "summary": "Ключи от почтовых ящиков",
        "house_idx": 1,
        "entrance": "3",
        "apartment": "33",
        "contact": "@new_settler",
        "status": Request.STATUS_DONE,
        "comment_to_resident": "Ключи переданы специалистом на месте.",
        "resident_tg_id": 100014,
    },
    {
        "type": Request.TYPE_COMPLAINT,
        "text": "Домофон не работает уже 2 недели, вход свободный!",
        "sentiment": Request.SENTIMENT_NEGATIVE,
        "summary": "Не работает домофон",
        "house_idx": 2,
        "entrance": "2",
        "apartment": "",
        "contact": "@security_concern",
        "status": Request.STATUS_ACCEPTED,
        "resident_tg_id": 100015,
    },
    {
        "type": Request.TYPE_REQUEST,
        "text": "Хотим организовать собрание жильцов, подскажите как.",
        "sentiment": Request.SENTIMENT_POSITIVE,
        "summary": "Организация собрания жильцов",
        "house_idx": 0,
        "entrance": "",
        "apartment": "",
        "contact": "@community_org",
        "status": Request.STATUS_DONE,
        "comment_to_resident": "Собрание назначено на 15 мая в 19:00, холл 1 подъезда.",
        "resident_tg_id": 100016,
    },
]


class Command(BaseCommand):
    help = "Заполнение БД мок-данными для демо"

    def handle(self, *args, **options):
        if Request.objects.exists():
            self.stdout.write(self.style.WARNING("Данные уже существуют, пропускаем seed."))
            return

        houses = []
        for h in HOUSES:
            house = House.objects.create(name=h["name"], chat_id=h["chat_id"])
            houses.append(house)
            self.stdout.write(f"  Дом: {house.name}")

        for data in MOCK_REQUESTS:
            data_copy = dict(data)
            data_copy["house"] = houses[data_copy.pop("house_idx")]
            Request.objects.create(**data_copy)

        self.stdout.write(self.style.SUCCESS(f"Создано {len(MOCK_REQUESTS)} обращений"))
