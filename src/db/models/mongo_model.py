from pydantic import BaseModel


class MongoModel(BaseModel):
    @classmethod
    def from_mongo(cls, data: dict):
        if not data:
            return data
        return cls(**dict(data))

    def mongo(self, **kwargs):
        exclude_unset = kwargs.pop('exclude_unset', True)
        by_alias = kwargs.pop('by_alias', True)

        parsed = self.dict(
          exclude_unset=exclude_unset,
          by_alias=by_alias,
          **kwargs,
        )

        return parsed
