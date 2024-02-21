import itertools

from loguru import logger

from src.building import Building
from src.logic import AbstractLogicExtension


class BuyBuildingsLogic(AbstractLogicExtension):
    async def _get_buyable_buildings(self) -> list[Building]:
        buildings = await self.page.query_selector_all("#products > .product.unlocked")

        to_return: list[Building] = []
        for building_html in buildings:
            id = await building_html.get_attribute("id")
            assert id is not None
            to_return.append(await Building.create(self.page, id))
        return to_return

    def _get_the_best_thing_to_buy(self, buildings: list[Building]) -> Building:
        if buildings[0].produces is None:
            return buildings[0]

        coefficients: dict[int, float] = {}
        for i, building in enumerate(buildings):
            produces_per_second = building.produces

            # sometimes we get buildings that we didn't buy yet, and so
            # we can't know how many they produce. so we estimate that
            # they produce 10 times more than the previous building.
            #
            # but previous building might also not be bought yet, so we
            # need to go back until we find a building that we bought,
            # and we set `produces_per_second` to be 10^shift times
            shift = 0
            for shift in itertools.count():
                if buildings[i - shift].produces is not None:
                    produces_per_second = buildings[i - shift].produces * (10**shift)
                    break
            assert produces_per_second is not None

            payback_period = building.costs / produces_per_second

            # if building produces less than 5% than we do per second, it is not worth buying
            if produces_per_second < (self.produced_per_last_second * 0.05):
                payback_period = float("inf")

            if payback_period != float("inf") and len(coefficients) >= 2:
                # if time to earn money for the building is longer than a payback
                # period of the previous building, then it is not worth buying it
                time_to_earn = (building.costs - self.balance) / self.produced_per_last_second
                profitability_of_second_best = sorted(coefficients.values())[1]
                if building.costs > self.balance and time_to_earn > (profitability_of_second_best / 2):
                    payback_period = float("inf")

            coefficients[building.id] = payback_period

        the_best_building_id = min(coefficients.items(), key=lambda x: x[1])[0]
        for building in buildings:
            if building.id == the_best_building_id:
                return building
        raise ValueError("No building found. How is that?")

    async def buy_buildings(self) -> None:
        buildings = await self._get_buyable_buildings()
        if not buildings:
            return

        best_building = self._get_the_best_thing_to_buy(buildings)
        if best_building.costs <= self.balance:
            logger.info(f"Buying building number {best_building.id} for {best_building.costs} cookies")
            await self.page.click(f"#{best_building.html_id}")
