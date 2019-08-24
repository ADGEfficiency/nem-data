
---


- plot the flow through interconnector versus the loss factor

[Design of the NEM](http://www.ceem.unsw.edu.au/sites/default/files/event/documents/ceem-nemdesign.pdf)

Bidding -> predispatch -> PASA

Unregulated inconnectors are allowed
- Murrary (SA to Vic)
- Directlink (QLD to NSW)

page 9 has diagram of the interconnectors

16 regions

Constrained on generator cannot set price

Effect of interconnector losses on the spot market
- different loss factors for generators and consumers
- difference is given to network service providers


[AN INTRODUCTION TO AUSTRALIA’S NATIONAL ELECTRICITY MARKET](http://www.abc.net.au/mediawatch/transcripts/1234_aemo2.pdf)

[Regions and Marginal Loss factors - 2016/17](https://www.aemo.com.au/-/media/Files/Electricity/NEM/Security_and_Reliability/Loss_Factors_and_Regional_Boundaries/2016/REVISED-V3--FINAL-Regional-Boundaries-and-Marginal-Loss-Factors-for-the-201617-Financial-Year.pdf)

---

Two sets of transmission losses
1. interconnector losses - dynamically set on a 5 min basis, depends on flow, `PUBLIC_PRICE_REVISION_DISPATCH` (not in archive) `PUBLIC_DVD_TRANSMISSIONLOSSFACTOR` (in archive)
2. DUID losses - set every 12 months, annual average of estimated HH losses for generator and consumers - `PUBLIC_DVD_DUIDETAILSUMMARY`

Inteconnector flows - to determine how to apply the loss factor
- `PUBLIC_DVD_INTERCONNECTOR`

Two sets of joins
1. DUID with region - to find interconnector loss
2. DUID with DUID losses (edited) 

---


