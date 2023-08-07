from typing import Optional

import strawberry

from gql_types import Character, Power, CharacterRole
from gql_types import CharacterInput, PowerInput, SetCharacterPowersInput, SetCharacterEnemiesInput
from repositories import get_character_repository, get_power_repository


@strawberry.type
class Query:
    @strawberry.field
    def character(self, id:strawberry.ID)->Optional[Character]:
        character_repo = get_character_repository()
        return character_repo.get(int(id))

    @strawberry.field
    def allCharacters(self)->list[Character]:
        character_repo = get_character_repository()
        return character_repo.get_all()

    @strawberry.field
    def power(self, id:strawberry.ID)->Optional[Power]:
        power_repo = get_power_repository()
        return power_repo.get(int(id))

    @strawberry.field
    def allPowers(self)->list[Power]:
        power_repo = get_power_repository()
        return power_repo.get_all()

@strawberry.type
class Mutation:
    @strawberry.mutation
    def addCharacter(self, input:CharacterInput)->int:
        character_repo = get_character_repository()
        return character_repo.save(
            input.name,
            input.role.value,
            input.realName,
            input.powerIds,
            input.enemyIds,
        )

    @strawberry.mutation
    def addPower(self, input:PowerInput)->int:
        power_repo = get_power_repository()
        return power_repo.save(input.name, input.userIds)

    @strawberry.mutation
    def setCharacterPowers(self, input:SetCharacterPowersInput)->bool:
        character_repo = get_character_repository()
        return character_repo.set_character_powers(input.characterId,
                                                        input.powerIds)

    @strawberry.mutation
    def setCharacterEnemies(self, input:SetCharacterEnemiesInput)->bool:
        character_repo = get_character_repository()
        return character_repo.set_character_enemies(input.characterId,
                                                        input.enemyIds)

    @strawberry.mutation
    def changeCharacterRole(self, id:strawberry.ID, role:CharacterRole)->bool:
        character_repo = get_character_repository()
        return character_repo.change_cahracter_role(id, role.value)

    @strawberry.mutation
    def deleteCharacter(self, id:strawberry.ID)->bool:
        character_repo = get_character_repository()
        return character_repo.delete(id)

    @strawberry.mutation
    def deletePower(self, id:strawberry.ID)->bool:
        power_repo = get_power_repository()
        return power_repo.delete(id)

schema = strawberry.Schema(query=Query, mutation=Mutation)
