# 커스텀 커맨드는 <app_name>/management/<command_name>.py 경로에 있어야 한다
from typing import List

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.management import BaseCommand, CommandError
from django.core.mail import send_mail
from django.core.validators import validate_email
from django.template.loader import render_to_string


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("receiver", nargs="+", type=str, help="이메일 수신자 주소")

    def handle(self, *args, **options):
        # 템플릿 내에서 참조할 수 있는 값들을 context data 라고 한다
        subject = render_to_string("app/hello_email_subject.txt")
        content = render_to_string("app/hello_email_content.txt", {"event_name": "안녕"})
        sender_emil = settings.DEFAULT_FROM_EMAIL
        receiver_email_list: List[str] = options["receiver"]

        try:
            for email in receiver_email_list:
                validate_email(email)
        except ValidationError as e:
            raise CommandError(e.message)
        # management command 구현에서는 명령 오류가 발생하였을 때, commanderror를 발생시킨다.
        send_mail(
            subject,
            content,
            sender_emil,
            receiver_email_list,
            fail_silently=False,
        )
