# UKRegistrationSearch
A script to search for partial license plates querying the DVLA database.

Full blog post is located: https://www.harisqazi.com/osint/transportation/united-kingdom-vehicle-registration-search

## Steps
1. Add API key
2. Comment Test API link
3. Uncomment API link
4. Import `requests` and `strings` if needed
5. Remove print statements if you want a clean JSON output
6. Use `$` for numerical wildcards, and `@` for alphabetical wildcards
7. `python3 license.py`

## Steps for V2
1. Comment Test API link
2. Uncomment API link
3. Import modules using `pip` if needed
4. `python3 licenseV2.py "AA1?AAA"` or `python3 licenseV2.py "AA1?AAA" --api "API_KEY_HERE"`
