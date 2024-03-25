import logging
from typing import Dict, List, Tuple, Union
from urllib.request import urlopen

from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


def get_html(url: str):
    page = urlopen(url)
    return page.read().decode("utf-8")


def get_soup(html: str):
    return BeautifulSoup(html, "html.parser")


def get_info_table(soup_obj, internal_url: str = ""):
    infobox = soup_obj.find(id="mw-content-text").find("table", class_="infobox vcard")
    if infobox is None:
        infobox = soup_obj.find(id="mw-content-text").find(
            "table", class_="infobox biography vcard"
        )
        if infobox is None:
            logger.warning(f"cant find info table pf {internal_url}")
        return infobox
    return infobox


def extract_data_from_row(info_piece) -> Union[Tuple[Union[str, None]], None]:
    info_type = info_piece.find("th")
    info_data = info_piece.find("td")

    if info_type is not None and info_data is not None:
        info_type = info_type.text
        info_url_data = None
        if info_data.find("a") is not None:
            info_url_data = [
                q["href"]
                for q in info_data.find_all("a")
                if q["href"].startswith("/wiki")
            ]
            if not info_url_data:
                info_url_data = None
        info_data = info_data.get_text(separator="\n")
        if info_data.startswith("c.\u2009"):
            info_data = info_data[3:]

        return info_type, info_data, info_url_data
    # else return none


def extract_data_from_table(table_obj) -> Dict[str, List[Union[str, None]]]:
    trs = table_obj.find_all("tr")

    data_dict = {}
    for info_piece in trs:
        data = extract_data_from_row(info_piece)
        if data is not None:
            data_dict[data[0]] = [data[1], data[2]]
    return data_dict


def is_url_fit_name(name: str, url: str):
    return name.lower().replace(" ", "_") == url[6:].lower()


def get_full_wiki_url(internal_url: str):
    return "https://en.wikipedia.org" + internal_url
