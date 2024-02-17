import dataclasses
import typing as t

from playwright.async_api import Page

from src.utils import extract_number_from_string


@dataclasses.dataclass
class Building:
    id: int
    produces: float | None
    costs: float

    @property
    def html_id(self) -> str:
        return "product" + str(self.id)

    @classmethod
    async def create(cls, page: Page, html_id: str) -> t.Self:
        int_id = int(html_id.removeprefix("product"))

        await (await page.query_selector("#" + html_id)).hover()  # type: ignore[union-attr] # can be None, but not in runtime
        produces = await page.query_selector("#tooltipBuilding > .descriptionBlock > b")

        price = await page.query_selector(f"#productPrice{int_id}")
        if price is None:
            raise ValueError(f"Could not find price for building {int_id}")

        return cls(
            id=int_id,
            produces=extract_number_from_string(await produces.inner_text()) if produces is not None else None,
            costs=extract_number_from_string(await price.inner_text()),
        )
