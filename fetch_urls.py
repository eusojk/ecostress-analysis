import requests
from bs4 import BeautifulSoup

ECOSTRESS_ROOT_URL_DAAC = "https://e4ftl01.cr.usgs.gov/ECOSTRESS"
ECOSTRESS_ROOT_URL_APPEEARS = "https://appeears.earthdatacloud.nasa.gov/api/product"


# see https://ecostress.jpl.nasa.gov/data/science-data-products-summary-table
ECOSTRESS_PRODUCTS = ["ECO1BRAD.001", "ECO1BATT.001", "ECO1BMAPRAD.001", "ECO1BGEO.001", "ECO2LSTE.001", "ECO2CLD.001",
                      "ECO3ETPTJPL.001", "ECO3ANCQA.001", "ECO3ETALEXIU.001", "ECO4ESIPTJPL.001", "ECO4ESIALEXIU.001",
                      "ECO4WUE.001"]

OUTPUT_FILE = "urls.txt"
FILE_TYPE = ".h5"
PRODUCT_ID = "ECO3ETPTJPL.001"
LAYER_ID = "EVAPOTRANSPIRATION_PT_JPL_ETsoil"

def is_product_valid(product_id):
    return product_id in ECOSTRESS_PRODUCTS

def print_invalid_error(product_id):
    print(
            f"'{product_id}' is not a valid ECOSTRESS products. \nPlease visit: https://ecostress.jpl.nasa.gov/data/science-data-products-summary-table. \nAborting...\n")

def check_product_id(product_id):
    if not is_product_valid(product_id):
        print_invalid_error(product_id)
        exit()
    return

def fetch_from_daac(product_id, year=2020, month=1, day=1):

    check_product_id(product_id)
    month = str(month).zfill(2)
    day = str(day).zfill(2)
    url = f"{ECOSTRESS_ROOT_URL_DAAC}/{product_id}/{year}.{month}.{day}/"

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

    print(f"Links to {product_id} stored in {OUTPUT_FILE}.")


def fetch_from_appeears(product_id, layer, year=2020, month=1, day=1):
    check_product_id(product_id)

    params = {'pretty': True}
    url = f"{ECOSTRESS_ROOT_URL_APPEEARS}/{product_id}"
    response = requests.get(url, params=params)
    product_response = response.json()

    print(product_response[layer])
    print(type(product_response))

# fetch_from_daac(PRODUCT_ID)
fetch_from_appeears(PRODUCT_ID, LAYER_ID)


