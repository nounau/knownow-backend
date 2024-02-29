# services.py
from app.models import mailTemplate


class mailTemplateService:
    mailTemplate = mailTemplate.MailTemplate()

    def addMailTemplate(self, data):
        return self.mailTemplate.create(data)

    def getMailTemplateByType(self, mailType):
        return self.mailTemplate.find_by_mailType(mailType)