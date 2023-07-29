# 커스텀 커맨드는 <app_name>/management/<command_name>.py 경로에 있어야 한다
from typing import List

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.management import BaseCommand, CommandError
from django.core.mail import send_mail
from django.core.validators import validate_email


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("receiver", nargs="+", type=str, help="이메일 수신자 주소")

    def handle(self, *args, **options):
        subject = "장고를 활용한 이메일 발송"  # TODO: 템플릿 시스템을 통해 문자열 완성하기
        content = "메시지 내용입니다."  # TODO: 템플릿 시스템을 통해 문자열 완성하기
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
