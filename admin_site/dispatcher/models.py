from django.db import models


class House(models.Model):
    name = models.CharField("Название дома", max_length=200)
    chat_id = models.BigIntegerField("Telegram chat_id", blank=True, null=True)

    class Meta:
        verbose_name = "Дом"
        verbose_name_plural = "Дома"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Request(models.Model):
    STATUS_ACCEPTED = "accepted"
    STATUS_IN_PROGRESS = "in_progress"
    STATUS_NEED_INFO = "need_info"
    STATUS_DONE = "done"
    STATUS_REJECTED = "rejected"

    STATUS_CHOICES = [
        (STATUS_ACCEPTED, "Принято"),
        (STATUS_IN_PROGRESS, "В работе"),
        (STATUS_NEED_INFO, "Нужна информация"),
        (STATUS_DONE, "Выполнено"),
        (STATUS_REJECTED, "Отклонено"),
    ]

    TYPE_EMERGENCY = "emergency"
    TYPE_COMPLAINT = "complaint"
    TYPE_REQUEST = "request"
    TYPE_QUESTION = "question"
    TYPE_PROPOSAL = "proposal"

    TYPE_CHOICES = [
        (TYPE_EMERGENCY, "Авария"),
        (TYPE_COMPLAINT, "Жалоба"),
        (TYPE_REQUEST, "Заявка"),
        (TYPE_QUESTION, "Вопрос"),
        (TYPE_PROPOSAL, "Предложение"),
    ]

    SENTIMENT_NEGATIVE = "negative"
    SENTIMENT_NEUTRAL = "neutral"
    SENTIMENT_POSITIVE = "positive"

    SENTIMENT_CHOICES = [
        (SENTIMENT_NEGATIVE, "Негативная"),
        (SENTIMENT_NEUTRAL, "Нейтральная"),
        (SENTIMENT_POSITIVE, "Позитивная"),
    ]

    number = models.AutoField("Номер обращения", primary_key=True)
    status = models.CharField(
        "Статус", max_length=20, choices=STATUS_CHOICES, default=STATUS_ACCEPTED
    )
    type = models.CharField("Тип", max_length=20, choices=TYPE_CHOICES)
    house = models.ForeignKey(
        House, on_delete=models.CASCADE, verbose_name="Дом", related_name="requests"
    )
    entrance = models.CharField("Подъезд", max_length=10, blank=True, default="")
    apartment = models.CharField("Квартира", max_length=10, blank=True, default="")
    text = models.TextField("Текст обращения")
    media = models.URLField("Медиа", blank=True, default="")
    contact = models.CharField("Контакт", max_length=200, blank=True, default="")
    sentiment = models.CharField(
        "Тональность", max_length=20, choices=SENTIMENT_CHOICES, default=SENTIMENT_NEUTRAL
    )
    summary = models.CharField("Суть", max_length=500, blank=True, default="")
    comment_to_resident = models.TextField("Комментарий жителю", blank=True, default="")
    internal_comment = models.TextField("Внутренний комментарий", blank=True, default="")
    resident_tg_id = models.BigIntegerField("TG ID жителя", blank=True, null=True)
    message_id = models.IntegerField("TG message_id", blank=True, null=True)
    chat_id = models.BigIntegerField("TG chat_id", blank=True, null=True)
    created_at = models.DateTimeField("Создано", auto_now_add=True)
    updated_at = models.DateTimeField("Обновлено", auto_now=True)

    class Meta:
        verbose_name = "Обращение"
        verbose_name_plural = "Обращения"
        ordering = ["-created_at"]

    def __str__(self):
        return f"#{self.number} — {self.get_type_display()} ({self.get_status_display()})"
