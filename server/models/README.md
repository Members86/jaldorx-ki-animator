# JALDORX LOCAL AI – Modellplan

## Erste Testkandidatur: Wan 2.1 T2V 1.3B

Der erste lokale Testmotor soll **Wan 2.1 T2V 1.3B** sein.

Warum:
- offizieller Wan-2.1-Code unterstützt Text-to-Video
- der Hersteller nennt ca. 8,19 GB VRAM für T2V-1.3B
- 480p ist die empfohlene Auflösung für das 1.3B-Modell
- damit passt der erste Test grundsätzlich zur geplanten RTX 5070 Ti mit 16 GB VRAM

Quelle:
https://github.com/Wan-Video/Wan2.1

## Noch nicht fest verdrahtet

Wir installieren das Modell erst auf dem KAGE X2 und testen dort:
1. startet es stabil?
2. wie viel VRAM wird tatsächlich benötigt?
3. wie schnell ist ein 5-Sekunden-Clip?
4. wie gut funktionieren Produktbilder?
5. wie gut funktionieren unsere 9:16-Werbeclips?

Erst danach wird der Motor dauerhaft in server/engine.py eingebunden.

## Ziel

Der Benutzer sieht weiterhin ausschließlich:

**JALDORX KI-Animator**

Das Modell läuft intern auf dem KAGE X2. Keine Cloud-API und keine separate Benutzeroberfläche als Voraussetzung.
