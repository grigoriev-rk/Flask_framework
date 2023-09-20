from pydantic import BaseModel, validator
from typing import Optional


class CreateAds(BaseModel):
    title: str
    description: str
    owner: str

    # @validator('title check')
    # def title_check(cls, value):
    #     black_list = ['drugs', 'weapons', 'fakenotes', 'carding', 'explosive', 'precursor']
    #     if title or description in black_list:
    #         raise ValueError('Invalid advertisement type!')
    #     return value
