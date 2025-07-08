from symbol import Symbol, s

# Define the symbols
Financial_Instrument = s.Financial_Instrument
Stock = s.Stock
Bond = s.Bond
Exchange = s.Exchange
Corporation = s.Corporation
Country = s.Country

# Establish relationships
Financial_Instrument.relate(Stock, how="has type")
Financial_Instrument.relate(Bond, how="has type")
Stock.relate(Exchange, how="traded on")
Bond.relate(Corporation, how="issued by")
Exchange.relate(Country, how="located in")
Corporation.relate(Country, how="located in")

# Generate the Mermaid diagram source
mermaid_source = Financial_Instrument.to_mmd()

# Print the Mermaid diagram source
print(mermaid_source)
