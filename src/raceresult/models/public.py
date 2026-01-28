"""Public API models for Raceresult API.

Based on go-model/model.go and go-webapi/api_public.go.
"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class UserInfo(BaseModel):
    """User information.

    Based on go-model/model.go:666-670.
    """

    cust_no: int = Field(default=0, alias="CustNo")
    user_name: str = Field(default="", alias="UserName")
    user_pic: str = Field(default="", alias="UserPic")

    model_config = {"populate_by_name": True}


class UserRight(BaseModel):
    """User right entry.

    Based on go-model/model.go:698-703.
    """

    user_id: int = Field(default=0, alias="UserID")
    user_name: str = Field(default="", alias="UserName")
    user_pic: str = Field(default="", alias="UserPic")
    rights: dict[str, list[str]] = Field(default_factory=dict, alias="Rights")

    model_config = {"populate_by_name": True}

    def has_right(self, right: str) -> bool:
        """Check if user has specific right.

        Based on go-model/model.go:674-696.

        Args:
            right: Right to check (e.g., "data.read")

        Returns:
            True if user has the right
        """
        if not self.rights:
            return False
        if "*" in self.rights:
            return True

        parts = right.split(".", 1)
        if parts[0] not in self.rights:
            return False
        if len(parts) == 1:
            return True

        permissions = self.rights[parts[0]]
        return "*" in permissions or parts[1] in permissions


class OAuthToken(BaseModel):
    """OAuth2 token.

    Based on oauth2.Token structure.
    """

    access_token: str = Field(default="", alias="access_token")
    token_type: str = Field(default="", alias="token_type")
    refresh_token: str = Field(default="", alias="refresh_token")
    expiry: str = Field(default="", alias="expiry")

    model_config = {"populate_by_name": True}
