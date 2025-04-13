from dataclasses import dataclass
from typing import Type, Optional

from sqlalchemy.ext.asyncio import AsyncSession

import models
from schemes import Settings


@dataclass
class Repository:
    settings: Settings
    db_session: AsyncSession
    model: Type[Optional[models]]
