def replaceMonth(date):
    date = date.lower()
    monthsByLanguage = {
        "en": ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
               "November", "December"],
        "fr": ["janvier", "février", "mars", "avril", "mai", "juin", "juillet", "août", "septembre", "octobre",
               "novembre", "décembre"],
        "nl": ["januari", "februari", "maart", "april", "mei", "juni", "juli", "augustus", "september", "oktober", "november", "december"],
        "de": ["Januar", "Februar", "März", "April", "Mai", "Juni", "Juli", "August", "September", "Oktober", "November", "Dezember"],
        "it": ["gennaio", "febbraio", "marzo", "aprile", "maggio", "giugno", "luglio", "agosto", "settembre", "ottobre",
               "novembre", "dicembre"],
        "es": ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"],
        "tr": ["Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran", "Temmuz", "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık"]
    }

    for language, months in monthsByLanguage.items():
        for index, month in enumerate(months):
            if " " + month.lower() + " " in date:
                date = date.replace(" "+month.lower()+" ", " "+monthsByLanguage["en"][index].lower()+" ")
    return date.strip()