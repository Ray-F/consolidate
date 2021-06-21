import copy
from typing import List

from bson import ObjectId

from main.domain.common.repository import Repository
from main.domain.model.user import User
from main.infrastructure.mongo_service import MongoService
from main.infrastructure.repository.account_repository import AccountRepository
from main.infrastructure.repository.entity_mapper import UserEntityMapper


class UserRepository(Repository):

    def __init__(self,
                 mongo_service: MongoService,
                 account_repository: AccountRepository):
        self.__user_collection = mongo_service.collection("users")
        self.__user_mapper = UserEntityMapper()
        self.__account_repository = account_repository

    def list(self) -> List[User]:
        pipeline = [{
            "$lookup": {
                "from": "accounts",
                "localField": "account_ids",
                "foreignField": "_id",
                "as": "accounts"
            }
        }]

        dbo_list = self.__user_collection.aggregate(pipeline)
        return [self.__user_mapper.to_domain_model(dbo) for dbo in dbo_list]

    def save(self, user: User) -> User:
        dbo = self.__user_mapper.from_domain_model(user)

        # Save all accounts to the DB
        [self.__account_repository.save(account) for account in user.accounts]

        if user.id:
            result = self.__user_collection.update_one({'_id': ObjectId(user.id)}, {'$set': dbo}, upsert=True)
            return user

        # If no user ID exists
        else:
            result = self.__user_collection.insert_one(dbo)

            # Copying to prevent modifying the previous user object
            new_user = copy.deepcopy(user)
            new_user.id = result.inserted_id
            return new_user
