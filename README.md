# Graphql_Extractor
- This Tool will help you format a burp result for graphql sitemap data into beautiful JSON. it is helpful when introspection is OFF and burp listed the fields on sitemap.
- To Use this tool
1. Goto Burpsuite -> Find the `/graphql` (or the specific endpoint)
2. right Click and do `save selected item`
3. Save it on your Computer.
4. Finally, You can run the tool now `python3 graphql_extractor.py burp_save`

 - It will save the extracted data on new text file you can access it with jq or any json processing tool.
