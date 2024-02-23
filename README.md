# Compat-Man
A config based compatibility tool manager to install and update your compatibility tools

config.conf will be looked for in
* XDG_CONFIG_HOME/compatman
* ~/.config/compatman

In that order

# Usage
````
# list all compatability tools defined in config.conf
compatman list
````
```
# Sync (download / update) all compatability tools defined in config.conf
compatman sync
# Alternativly input a specific compatability tool with -c to only sync perticular tools
compatman sync -c <First-Tool-Name> -c <Second-Tool-Name>
```

# Config File

````
[<Custom-Name-For-Tool>]
type=<Desired-Tool-To-Install>
path=<Path-To-Tools-Desired-Location>
version=<Version-To-Install>
````

once a config has been made then the tool will be installed to **{path}/{Name-For-Tool}**
as many configs as you need can be put into config.conf

| variable | possible values                      | Description                                                                                       |
|----------|--------------------------------------|---------------------------------------------------------------------------------------------------|
| type     | proton-ge                            | The type of compatibility tool to install                                                         |
| path     | ~/.steam/steam/compatibilitytools.d/ | The location for the tool to be installed                                                         |
| version  | GitHub_tag_name, latest              | The version of the tool to install as defined by tag name or the latest to get the newest version |

[ProtonGE](https://github.com/GloriousEggroll/proton-ge-custom) - GitHub