# pre-fixlist
A tool for managing prefix lists

- At configurable intervals, expand as-macros from relevant Internet registries
- Store every "fetch" of data in persistent storage, enabling diff between points in time
- Define rulesets to programatically allow or deny objects in prefix lists. 
  - More than X percent growth between two runs
  - Your own prefixes/asn(s) in customer macro
  - Google/tier ones/root-servers/etc in customer macro
- Provide a REST API to
  - Fetch expanded data 
  - Add new as-macros to be polled from registries
