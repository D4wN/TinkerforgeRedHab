{
    "id": "0041",
    "items": {
        "lamp01": "ON",
        "Segment7": "0041",
        "TF_LCD": "TFNUM<00>Hallo TinkerForge"
    },
    "rules": {
        "PATH_TO_RULES_FILE": "/etc/openhab/configurations/rules/labor.rules",
        "rules": [
            "rule \"TFDemo\" when Item Distance received update then sendCommand(Segment7, \"\"+Distance.state)) end"
        ]
    }
}

