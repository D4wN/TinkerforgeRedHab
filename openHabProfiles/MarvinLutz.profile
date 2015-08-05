{
  "id": "0815",
  "items": {
    "lamp01": "ON",
    "TF_Segment7": "0814",
    "TF_LCD": "TFNUM<00>Hallo: Marvin"
  },
  "rules": {
    "PATH_TO_RULES_FILE": "/etc/openhab/configurations/rules/demo.rules",
    "rules": [
      "rule \"Weather Station LCD Backlight\" when Item TF_Button0 changed then if (TF_LCD_Backlight.state == ON) sendCommand(TF_LCD_Backlight, OFF) else sendCommand(TF_LCD_Backlight, ON) end"
    ]
  }
}