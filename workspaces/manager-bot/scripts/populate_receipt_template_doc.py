#!/usr/bin/env python3
"""Populate an already-created Google Doc with a clearly marked receipt template."""
import json, os, subprocess, tempfile, urllib.parse, urllib.request
from urllib.error import HTTPError

DOC_ID = "1vbXaA-o25Dtr4Lp_NE-c_3N59Zv8VeJTfeAdljCSmIY"
ACCOUNT = "vrbs940054@gmail.com"

TEXT = """COPY / TEMPLATE - NOT A VALID RECEIPT
For personal record-keeping or layout reference only

MFG [STORE NAME]
[ADDRESS LINE 1]
[ADDRESS LINE 2]
[TOWN / COUNTY]
[POSTCODE]
Tel : [TELEPHONE]

[DAY DATE YEAR] [TIME]

Store [STORE NO] POS [POS NO]        Trans [TRANS NO]
Op Name: [OPERATOR]

SALE

[ITEM DESCRIPTION]                         £[ITEM PRICE]
-----------------------------------------------
Total                                      £[TOTAL]
-----------------------------------------------
[PAYMENT METHOD]                           £[TOTAL]

[CUSTOMER / ACCOUNT NAME]
VAT No.                         [VAT NUMBER]
VAT Rate       Ex VAT          VAT       Inc. VAT
[RATE]%         £[EX VAT]       £[VAT]      £[INC VAT]
Totals                          £[VAT]      £[TOTAL]

Confirmed minimum customer age: [AGE]

-----------------------------------------------
             CUSTOMER COPY - TEMPLATE
             [PAYMENT TYPE]
             [APPROVAL STATUS]

Receipt no.                                  [RECEIPT NO]
Date/Time                         [DATE] [TIME]
Application name                  [APPLICATION]
AID                               [AID]
Card                              [MASKED CARD]
Auth Code                         [AUTH CODE]
Action code                       [ACTION CODE]
Terminal ID                       [TERMINAL ID]
Transaction number                [TRANSACTION NO]
Merchant ID                       [MERCHANT ID]
STAN/BATCH                        [STAN / BATCH]
CVM                               [CVM]
Amount                            £[AMOUNT] GBP
[CONTACTLESS / PAYMENT NOTE]

-----------------------------------------------
           [BARCODE PLACEHOLDER]
       (do not use as a payment barcode)

Thank You
Please Drive Carefully
[SERVICE / ORDER MESSAGE]
[COSTA / SUPPORT MESSAGE]

Your feedback is important to us
Please contact [CUSTOMER CARE]
Email us: [EMAIL ADDRESS]

Proudly supporting
[BRAND / SUPPORT LINE]

COPY / TEMPLATE - NOT A VALID RECEIPT
"""

def token():
    with tempfile.NamedTemporaryFile(delete=False) as fh:
        path = fh.name
    try:
        subprocess.run(["gog", "auth", "tokens", "export", ACCOUNT, "--out", path, "--overwrite", "--no-input"], check=True, stdout=subprocess.DEVNULL)
        refresh = json.load(open(path, encoding="utf-8"))
    finally:
        try: os.unlink(path)
        except OSError: pass
    creds = json.load(open("/home/vin/.config/gogcli/credentials.json", encoding="utf-8"))
    cfg = creds.get("installed", creds.get("web", creds))
    client_id = cfg["client_id"]; client_secret = [REDACTED_SECRET]"client_secret"]
    payload = urllib.parse.urlencode({"client_id": client_id, "client_secret": client_secret, "refresh_token": refresh["refresh_token"], "grant_type": "refresh_token"}).encode()
    req = urllib.request.Request("https://oauth2.googleapis.com/token", data=payload, method="POST")
    return json.load(urllib.request.urlopen(req))["access_token"]

def main():
    access = token()
    headers = {"Authorization": "Bearer " + access, "Content-Type": "application/json"}
    requests = [
        {"insertText": {"endOfSegmentLocation": {"segmentId": ""}, "text": TEXT}},
        {"updateTextStyle": {"range": {"startIndex": 1, "endIndex": len(TEXT) + 1}, "textStyle": {"weightedFontFamily": {"fontFamily": "Roboto Mono"}, "fontSize": {"magnitude": 8, "unit": "PT"}}, "fields": "weightedFontFamily,fontSize"}},
        {"updateDocumentStyle": {"documentStyle": {"marginTop": {"magnitude": 18, "unit": "PT"}, "marginBottom": {"magnitude": 18, "unit": "PT"}, "marginLeft": {"magnitude": 24, "unit": "PT"}, "marginRight": {"magnitude": 24, "unit": "PT"}, "pageSize": {"width": {"magnitude": 230, "unit": "PT"}, "height": {"magnitude": 760, "unit": "PT"}}}, "fields": "marginTop,marginBottom,marginLeft,marginRight,pageSize"}},
    ]
    body = json.dumps({"requests": requests}).encode()
    req = urllib.request.Request("https://docs.googleapis.com/v1/documents/" + DOC_ID + ":batchUpdate", data=body, headers=headers, method="POST")
    try:
        result = json.load(urllib.request.urlopen(req))
    except HTTPError as exc:
        detail = exc.read().decode("utf-8", "replace")
        raise RuntimeError("Google Docs API rejected the update: " + detail[:1000]) from exc
    print(json.dumps({"documentId": DOC_ID, "insertedCharacters": len(TEXT), "replies": len(result.get("replies", []))}))

if __name__ == "__main__": main()
