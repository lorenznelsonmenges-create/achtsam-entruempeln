# Projekt-Kontext: Achtsam Entrümpeln

## 1. Das Design-System: "The Curated Sanctuary"
Dieses Projekt folgt strengen Design-Prinzipien, um eine beruhigende, hochwertige Ästhetik ("Editorial Look") zu erzeugen.

* **Farben:**
    * `surface`: #fbf9f3 (Basis-Hintergrund)
    * `primary`: #526447 (Salbeigrün / Akzent)
    * `on-surface`: #31332c (Textfarbe, kein reines Schwarz!)
    * `surface-container-low`: #f5f4ec (Sektionen)
* **Typografie:**
    * Headlines: **Noto Serif** (Klasse: `font-headline`), enges Letter-Spacing.
    * Body: **Manrope** (Klasse: `font-body`).
* **Prinzipien:**
    * **No-Line Rule:** Keine 1px Rahmen. Abgrenzung nur durch Hintergrund-Shifts ("Tonal Layering").
    * **Atemzug-Sektionen:** Viel Whitespace (`py-32 lg:py-48`) mit zentrierten Zitaten.
    * **Logo-Icon:** Das Material-Icon `spa` (Blatt) wird konsistent im Header und in der Side-Nav verwendet.

## 2. Inhaberin: Stefanie Ruf
Alle persönlichen Daten wurden aus dem Lebenslauf (27.03.2025) extrahiert:
* **Name:** Stefanie Ruf
* **Beruf:** Diplom Sozialpädagogin
* **Fokus:** Systemische Mediation, Biografiearbeit, Coaching.
* **Adresse:** Egerländer Str. 9, 65232 Taunusstein
* **Kontakt:** 0177 - 7574529 | steffi_ruf@icloud.com
* **Profilbild:** `images/stefanie-003.jpg` (extrahiert aus PDF).

## 3. Technische Struktur
* **Framework:** HTML5 + Tailwind CSS via CDN (inkl. Custom Config im `<script>` Tag).
* **Dateien:**
    * `index.html`: Startseite mit Hero-Bild (`images/hero-startseite.png`) und großem Logo-Icon.
    * `philosophie.html`: Fokus auf Systematik und Weitergabe (Diakonie/ProJob).
    * `ueber-mich.html`: Profil von Stefanie Ruf mit Qualifikationen.
    * `kontakt.html`: Nicht-scrollbares Split-Layout für Terminanfragen.
    * `impressum.html` & `datenschutz.html`: Rechtlich vorbereitete Seiten.

## 4. Workflow & Status
* Das Projekt ist vollständig in `/home/lorenzm/Projects/Achtsam_entruempeln/` lokalisiert.
* Das Git-Repository ist mit GitHub verknüpft und auf dem Stand des finalen Designs gepusht.
* Veröffentlichung ist via GitHub Pages geplant/aktiviert.

## Gemini Added Memories
- Die 'target/'-Verzeichnisse im Projekt sind aktuell von der Analyse und Suche ausgeschlossen, da sie nur Build-Artefakte enthalten.
- Vor einem Release müssen die 'target/'-Verzeichnisse bereinigt werden (z. B. mit 'cargo clean'), um Altlasten zu entfernen und Speicherplatz zu sparen.
- Die Projektdokumentation muss so erweitert werden, dass ein externer Dienstleister das Programm problemlos über Git auf einem Server deployen kann.
- In der Auftragsverwaltung müssen alle Felder bestehender Aufträge nachträglich bearbeitet werden können.
- Die Auftragserstellung soll optisch (Layout, Styling, Input-Felder) an das Design der Auftragsverwaltung angepasst werden.
- Die E-Mail-Adresse für 'Achtsam Entrümpeln' ist noch nicht final und muss später projektweit korrigiert werden. Aktuell werden Platzhalter wie 'hallo@achtsam-entruempeln.de' oder 'steffi_ruf@icloud.com' verwendet.
- I am running on the user's laptop and do not have direct access to the server.
- The user plans to register the domain and create email accounts for 'Achtsam Entrümpeln' using Hetzner.
