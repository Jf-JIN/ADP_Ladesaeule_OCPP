const lang_pkg_de = {
    // 登录页面
    "text_login_title": "Willkommen bei der Anmeldung",
    "text_login": "Anmeldung",
    "user_login": "Benutzeranmeldung",
    "admin_login": "Administratoranmeldung",
    "username": "Benutzername",
    "password": "Passwort",

    // 主页
    "text_home": "Home",
    "text_console": "Information",
    "text_image": "Daten",
    "text_manual_input": "Manuale Eingabe",
    "text_current_time": "Akutelle Zeit",
    "text_rasberry_pi_system": "Information über Rasberry Pi System",
    "text_optimisation_system": "Optimisation System Information",
    "text_GPIO": "Hardware Information",

    // 用户界面
    "welcome_title": "OCPP Charge Station",
    "welcome_text": "Herzlich Willkommen bei der Nutzung der OCPP-Ladesäule, einer Ladestationssoftware, die auf dem OCPP-Protokoll basiert.",
    "Testen_btn": "Testen",
    "charge_mode_label": "Lademodus:",
    "direct_charge": "Einfaches Laden",
    "select_dynamic": "Dynamische Anpassung",
    "select_shortest_time": "Minimale Ladezeit",
    "select_least_cost": "Minimale Ladekosten",
    "charge_power_label": "Ladeenergie:",
    "departure_time_label": "Geschätzte Abfahrtszeit",
    "save_settings": "Abgeben und speichern",
    "charge_now": "Jetzt laden",
    "home_current_current": "Aktueller Strom",
    "home_current_voltage": "Aktuelle Spannung",
    "home_charged_energy": "Geladene Menge",
    "home_left_time": "Verbleibende Zeit",
    "home_charging_status": "Lade-Status",
    "stop": "STOP",
    // 手动输入
    "system_operation_question_title": "Systembetrieb",
    "system_operation_question": "Möchten Sie das System neu starten oder herunterfahren?",
    "system_operation_reboot_text": "Neustart",
    "system_operation_shutdown_text": "Herunterfahren",
    "system_operation_cancel_text": "Abbrechen",
    "reboot_question": "Möchten Sie das System wirklich neu starten?",
    "shutdown_question": 'Möchten Sie das System wirklich herunterfahren?<br>Das Programm wird beendet!<br>Wenn Sie es erneut starten möchten, verwenden Sie bitte JupyterLab unter:<br><a href="http://raspberrypi.local:8888/lab" target="_blank">http://respberrypi.local:8888/lab</a>',
    "shutdown_question_2": 'Bitte bestätigen Sie erneut das Herunterfahren des Systems.<br>Wenn Sie es erneut starten möchten, verwenden Sie bitte JupyterLab unter:<br><a href="http://raspberrypi.local:8888/lab" target="_blank">http://respberrypi.local:8888/lab</a>',
    "shutdown_message": 'Das System wird jetzt heruntergefahren.<br>Wenn Sie es erneut starten möchten, verwenden Sie bitte JupyterLab unter:<br><a href="http://raspberrypi.local:8888/lab" target="_blank">http://respberrypi.local:8888/lab</a>',
    "implement": "Implementieren",
    "manual_stop": "STOP",
    "label_manual_target_energy": "Zielenergie(Wh)",
    "manual_depart_time_label": "Geschätzte Abfahrtszeit",
    "drop_zone": "Ziehen Sie die Datei zum Hochladen oder klicken Sie, um die Datei auszuwählen",
    "lb_btn_manual_input": "Bitte laden Sie die Datei hoch",
    "file_name": "<Keine Datei>",
    "btn_clear_csv": "CSV-Datei löschen",
    "btn_create_example_csv": "Beispiel-CSV-Datei erstellen",
    // 词条
    "csv_file_error": "CSV-Datei ist falsch, bitte überprüfen Sie das Dateiformat",
    "no_file_selected": "<Keine Datei>",
    "success": "Erfolg",
    "error": "Fehler",
    "warning": "Warning",
    "info": "Info",
    "TE_not_num": "Bitte geben Sie eine gültige Zahl ein. Ziel-Energie ist jetzt keine Zahl.",
    "TE_not_positive": "Bitte geben Sie eine gültige Zahl ein. Ziel-Energie ist jetzt keine positive Zahl.",
    "time_in_past": "Die ausgewählte Zeit kann nicht in der Vergangenheit liegen. Bitte wählen Sie eine gültige Zeit aus.",
    // 表格
    "evse_data": "EVSE Daten",
    "register_address": "Registeradresse",
    "function_code": "Funktionscode",
    "register_value": "Registerwert",
    "status": "Status",
    "isError": "Fehler vorhanden",
    "exception_code": "Ausnahmecode",
    "dev_id": "Geräte ID",
    "transaction_id": "TransaktionsID",
    "bits": "Bits",
    "address": "Adresse",
    "Shelly_data": "Shelly Daten",
    "phase": "Phase",
    "power": "Leistung",
    "pf": "Leistungsfaktor",
    "current": "Strom",
    "voltage": "Spannung",
    "is_valid": "Gültig",
    "total": "Gesamt",
    "charged_energy": "Geladene Energie",
    "Shelly_is_valid": "Shelly ist gültig",
    "register_description": "Registerbeschreibung",
    "reg_description": {
        "1000": "[R/W] Tatsächlich konfigurierte Stromstärke",
        "1001": "[R] Tatsächlich ausgegebene Stromstärke",
        "1002": "[R] Fahrzeugstatus",
        "1003": "[R] PP-Strombegrenzung",
        "1004": "[R/W] Befehl(ein/ausschalten)",
        "1006": "[R] EVSE-Status",
        "1008": "[R] Fehler-Zeitüberschreitung",
        "1009": "[R] Selbsttest-Zeitüberschreitung",
        "2000": "[R/W] Standardstromwert",
        "2001": "[R/W] Slave-Adresse",
        "2002": "[R/W] Minimale Stromstärke",
    },
    "light_description": {
        "title_status": "Status der Kontrollleuchte",
        "title_description": "Beschreibung",
        "title_meaning": "Bedeutung",
        "status_ready": "Dauerlicht",
        "description_ready": "Ständig eingeschaltet",
        "meaning_ready": "Nicht am Laden, Gerät ist bereit",
        "status_prepare": "Blinkt 0,1s an / 0,1s aus",
        "description_prepare": "Schnelles Blinken",
        "meaning_prepare": "Bereitet Ladevorgang vor",
        "status_charging": "Blinkt 1s an / 1s aus",
        "description_charging": "Blinkt einmal pro Sekunde",
        "meaning_charging": "Wird geladen",
        "status_evse_shelly_error": "0,2s an - 0,2s aus - 0,2s an - 2s aus",
        "description_evse_shelly_error": "Fehlermuster",
        "meaning_evse_shelly_error": "Ladefehler oder Systemstörung"
    },
}