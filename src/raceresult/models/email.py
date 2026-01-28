"""Email template models for Raceresult API.

Based on go-model/emailtemplate/emailtemplate.go, preview.go, attachment.go.
"""

from __future__ import annotations

from enum import IntEnum

from pydantic import BaseModel, Field


class TemplateType(IntEnum):
    """Type of email template.

    Based on go-model/emailtemplate/emailtemplate.go:30-38.
    """

    SINGLE = 0
    GROUP = 1
    SMS = 2
    WEB_SERVICE = 3
    GROUP_BY_ID = 4


class AttachmentType(IntEnum):
    """Type of attachment.

    Based on go-model/emailtemplate/attachment.go:16-23.
    """

    FILE = 0
    CERTIFICATE = 1
    URL = 2
    UNSENT_INVOICE = 3


class AttachmentSendForType(IntEnum):
    """When to send attachment in group emails.

    Based on go-model/emailtemplate/attachment.go:25-31.
    """

    LAST = 0
    FIRST = 1
    ALL = 2
    ANY = 3


class HTTPHeader(BaseModel):
    """HTTP header for web service templates.

    Based on go-model/emailtemplate/emailtemplate.go:3-6.
    """

    name: str = Field(default="", alias="Name")
    value: str = Field(default="", alias="Value")

    model_config = {"populate_by_name": True}


class Attachment(BaseModel):
    """Email attachment configuration.

    Based on go-model/emailtemplate/attachment.go:8-14.
    """

    type: AttachmentType = Field(default=AttachmentType.FILE, alias="Type")
    name: str = Field(default="", alias="Name")
    label: str = Field(default="", alias="Label")
    filter: str = Field(default="", alias="Filter")
    send_for: AttachmentSendForType = Field(default=AttachmentSendForType.LAST, alias="SendFor")

    model_config = {"populate_by_name": True}


class EmailTemplate(BaseModel):
    """Email template definition.

    Based on go-model/emailtemplate/emailtemplate.go:8-28.
    """

    name: str = Field(default="", alias="Name")
    type: TemplateType = Field(default=TemplateType.SINGLE, alias="Type")
    sender: str = Field(default="", alias="Sender")
    sender_name: str = Field(default="", alias="SenderName")
    reply_to: str = Field(default="", alias="ReplyTo")
    cc: str = Field(default="", alias="CC")
    bcc: str = Field(default="", alias="BCC")
    receiver_field: str = Field(default="", alias="ReceiverField")
    html: bool = Field(default=False, alias="HTML")
    method: str = Field(default="", alias="Method")
    subject: str = Field(default="", alias="Subject")
    text: str = Field(default="", alias="Text")
    header: str = Field(default="", alias="Header")
    footer: str = Field(default="", alias="Footer")
    default_filter: str = Field(default="", alias="DefaultFilter")
    set_custom_field_after_sending: str = Field(default="", alias="SetCustomFieldAfterSending")
    save_result_in: str = Field(default="", alias="SaveResultIn")
    attachments: list[Attachment] = Field(default_factory=list, alias="Attachments")
    http_headers: list[HTTPHeader] = Field(default_factory=list, alias="HTTPHeaders")

    model_config = {"populate_by_name": True}


class PreviewAttachment(BaseModel):
    """Preview attachment info.

    Based on go-model/emailtemplate/preview.go:24-30.
    """

    type: AttachmentType = Field(default=AttachmentType.FILE, alias="Type")
    name: str = Field(default="", alias="Name")
    label: str = Field(default="", alias="Label")
    bib: int = Field(default=0, alias="Bib")
    pid: int = Field(default=0, alias="PID")

    model_config = {"populate_by_name": True}


class Preview(BaseModel):
    """Email preview result.

    Based on go-model/emailtemplate/preview.go:3-22.
    """

    type: TemplateType = Field(default=TemplateType.SINGLE, alias="Type")
    bibs: list[int] = Field(default_factory=list, alias="Bibs")
    pids: list[int] = Field(default_factory=list, alias="PIDs")
    sender: str | None = Field(default=None, alias="Sender")
    sender_name: str | None = Field(default=None, alias="SenderName")
    reply_to: str | None = Field(default=None, alias="ReplyTo")
    cc: str | None = Field(default=None, alias="CC")
    bcc: str | None = Field(default=None, alias="BCC")
    cell_phone: str | None = Field(default=None, alias="CellPhone")
    email: str | None = Field(default=None, alias="Email")
    subject: str | None = Field(default=None, alias="Subject")
    text: str | None = Field(default=None, alias="Text")
    html: bool = Field(default=False, alias="HTML")
    url: str | None = Field(default=None, alias="URL")
    method: str | None = Field(default=None, alias="Method")
    attachments: list[PreviewAttachment] = Field(default_factory=list, alias="Attachments")
    http_headers: list[HTTPHeader] = Field(default_factory=list, alias="HTTPHeaders")
    errors: list[str] = Field(default_factory=list, alias="Errors")

    model_config = {"populate_by_name": True}
