import re

from scripts.utils import ModManager, get_languages
from settings import language_flags

mod_link = re.compile(r"\[\[([^\].]+)\]\]")


def main(**kwargs):
    for language in get_languages():
        check_json(language)
    print("✅ Tests")


def check_json(language):
    mods = ModManager.get_mod_list(language=language)

    mod_ids_founded = set()
    mod_ids = set(str(mod.id) for mod in mods)
    tp2s = set()
    urls_to_mod = dict()
    nb_warnings = 0

    for mod in mods:
        # check links
        for text in [mod.description] + mod.notes:
            links = mod_link.findall(text)
            for link in links:
                assert link in mod_ids, (
                    f"🔴 {language} {mod.id} : Lien interne vers un mod inexistant → {link}"
                )

        # check id unicity
        assert mod.id not in mod_ids_founded, f"🔴 {language} {mod.id} : ID déjà existant"
        mod_ids_founded.add(mod.id)

        # check urls, warning
        for url in mod.urls:
            if url in urls_to_mod:
                print(
                    f"🟡 {language} Url doublon",
                    f"({url}) → {mod.name} / {urls_to_mod[url]}",
                )
                nb_warnings += 1
            else:
                urls_to_mod[url] = mod.name

        # check tp2
        if mod.tp2 not in ("", "n/a", "non-weidu"):
            tp2_lower = mod.tp2.lower()
            if tp2_lower in tp2s:
                print(f"🟡 {language} TP2 doublon →", mod.tp2)
                nb_warnings += 1
            else:
                tp2s.add(tp2_lower)

        # check languages
        for lang in set(mod.languages) - language_flags.keys():
            print(f"🟡 {language} Langue inconnue →", lang)
            nb_warnings += 1

    if nb_warnings > 0:
        print(f"🟡 {language} {nb_warnings} warnings found")
