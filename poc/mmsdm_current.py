from bs4 import BeautifulSoup
import requests
from pathlib import Path
from nemdata.interfaces import scrape_url, unzip_file
import pandas as pd

if __name__ == "__main__":
    #  https://nemweb.com.au/Reports/Current/Public_Prices/PUBLIC_PRICES_202101220000_20210123040554.zip
    #  just going to do a one time scrape of what is in current
    reports = {"public-prices": "Public_Prices"}

    header = {"user-agent": "Adam Green, adam.green@adgefficiency.com"}
    url = "https://nemweb.com.au/Reports/Current/Public_Prices/"
    res = requests.get(url, headers=header)
    soup = BeautifulSoup(res.text)
    links = soup.findAll("a")
    prefix = "https://nemweb.com.au"
    #  first link is link to parent directory
    fldr = Path.cwd() / "public-prices" / "raw"
    fldr.mkdir(exist_ok=True, parents=True)
    dfs = []
    for li in links[1:]:
        url = Path(prefix + li["href"])
        fi = fldr / url.name
        url = str(url).replace(":/", "://")
        scrape_url(url, fi)
        unzip_file(fi, fldr)

    #  now the cleaning
    #  these files have repeated header columns (gives Parser Errors) lines

    clean = []
    n_headers = 0
    fi = fi.with_suffix(".CSV")
    fis = [f for f in fldr.iterdir() if f.suffix == ".CSV"]
    print(f" processing {len(fis)} files")
    for n, fi in enumerate(fis):
        lines = []
        for line in pd.read_csv(
            str(fi),
            chunksize=1,
            #  first row is summary, different schema
            skiprows=1,
            #  this makes the second row the header
            header=0,
            #  make the line with C, I, D the index
            index_col=0,
        ):
            if line.index == "D":
                lines.append(line)

        lines = pd.concat(lines, axis=0)
        fldr = Path.cwd() / "public-prices" / "clean-csvs"
        fldr.mkdir(exist_ok=True)
        lines.to_csv(fldr / fi.name)
        print(f"lines :{lines.shape}, n: {n}")
        clean.append(lines)

    clean = pd.concat(clean, axis=0)
    clean.to_csv(fldr / "public-prices.csv")
    print(f"clean :{clean.shape}")

    """
    ran in console
    clean = pd.read_csv('./public-prices/clean-csvs/public-prices.csv')
    mask = clean['DREGION'] == 'TREGION'
    subset = clean.loc[mask, :]
    subset.to_csv('./public-prices/tregion.csv')
    """
