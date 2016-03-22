{
  "id": "0005",
  "items": {
    "Segment7": "0004"
  },
  "rules": {
    "PATH_TO_RULES_FILE": "C:/Programmierung/Repos/Python/TinkerforgeRedHab/openHabProfiles/test.rules",
    "rules": [
      "rule \"Weather Station LCD Backlight\" when Item TF_Button0 changed then if (TF_LCD_Backlight.state == ON) sendCommand(TF_LCD_Backlight, OFF) else sendCommand(TF_LCD_Backlight, ON) end"
    ]
  }
}