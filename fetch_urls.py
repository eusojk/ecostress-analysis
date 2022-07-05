import requests
from bs4 import BeautifulSoup

ECOSTRESS_ROOT_URL = "https://e4ftl01.cr.usgs.gov/ECOSTRESS"

# see https://ecostress.jpl.nasa.gov/data/science-data-products-summary-table
ECOSTRESS_PRODUCTS = ["ECO1BRAD.001", "ECO1BATT.001", "ECO1BMAPRAD.001", "ECO1BGEO.001", "ECO2LSTE.001", "ECO2CLD.001", "ECO3ETPTJPL.001", "ECO3ANCQA.001", "ECO3ETALEXIU.001", "ECO4ESIPTJPL.001", "ECO4ESIALEXIU.001", "ECO4WUE.001"]

OUTPUT_FILE = "urls.txt"
FILE_TYPE = ".h5"

def fetch(product, year=2020, month=1, day=1):

    if product not in ECOSTRESS_PRODUCTS:
        print(f"{product} is not a valid ECOSTRESS valid. Please visit: https://ecostress.jpl.nasa.gov/data/science-data-products-summary-table")
        return

    month = str(month).zfill(2)
    day = str(day).zfill(2)
    url = f"{ECOSTRESS_ROOT_URL}/{product}/{year}.{month}.{day}/"

    try:
        request = requests.get(url)
        found = BeautifulSoup(request.text, 'html.parser')
    except Exception as e:
        print(f"Exception/error occured: {e}. Aborting...")
        return

    list_found = found.find_all('a')
    if len(list_found) == 0:
        print(f"No product links found at {url}. Aborting....")
        return

    print(f"Searching products' links from: {url}")
    with open(OUTPUT_FILE, 'w') as f:
        for e in list_found:
            link = e.get('href')
            if link.endswith(FILE_TYPE):
                sub_url = f"{url}{link}"
                f.write(sub_url)
                f.write('\n')

    print(f"Links to {product} stored in {OUTPUT_FILE}.")


fetch("ECO3ETPTJPL.001")
