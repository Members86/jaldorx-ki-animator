# JALDORX KI-Animator – Architektur

## Ziel

Der iPad-Animator erstellt einen Videoauftrag. Der Auftrag wird später über eine sichere Verbindung an den KAGE-X2-PC geschickt. Dort läuft die Video-KI lokal.

## Datenfluss

iPad / Browser
→ JALDORX KI-Animator
→ sichere Verbindung (später Tailscale)
→ KAGE X2
→ lokaler Job-Server
→ ComfyUI / lokale Video-KI
→ MP4
→ Job-Server
→ iPad

## Auftrag

Ein Auftrag enthält mindestens:

- eindeutige Job-ID
- Produkt
- Produktbild
- Idee / Prompt
- Dauer (5 oder 10 Sekunden)
- Format (9:16, 16:9 oder 1:1)

## Wichtige Vorgabe

Die Videoerzeugung soll lokal auf dem KAGE X2 stattfinden. Es werden keine kostenpflichtigen Cloud-Video-APIs vorausgesetzt.

## Sicherheitsprinzip

Der KAGE X2 wird nicht über einen offenen Internet-Port erreichbar gemacht. Für den späteren Fernzugriff wird eine private Verbindung wie Tailscale verwendet.

## Nächster technischer Schritt

Auf dem KAGE X2 wird ein kleiner lokaler Job-Server eingerichtet. Dieser nimmt Aufträge vom JALDORX-Animator entgegen und startet danach die lokale Video-KI.
