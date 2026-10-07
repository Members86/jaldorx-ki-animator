# JALDORX KI-Animator – lokaler Job-Server

Der Ordner enthält die lokalen Server-Bausteine für den späteren **KAGE X2**.

## Start

Auf dem KAGE X2 reicht später zunächst:

```bash
python3 server/app.py
```

Standardmäßig läuft der Server auf:

```
http://127.0.0.1:8765
```

## Endpunkte

- `GET /health` – prüft, ob der Server läuft
- `GET /jobs` – listet Aufträge
- `GET /jobs/<id>` – zeigt einen Auftrag
- `POST /jobs` – nimmt einen Videoauftrag an

## Auftrag

```json
{
  "product": "EIGENES PRODUKT",
  "idea": "Mach was Gutes",
  "duration": "10",
  "format": "9:16",
  "image": null
}
```

## Video-KI

`engine.py` ist die interne Adapter-Schicht für die spätere **JALDORX LOCAL AI**.

Dort wird auf dem KAGE X2 ein lokales Video-Modell angeschlossen. Die Benutzeroberfläche bleibt dabei JALDORX; der eigentliche KI-Motor läuft unsichtbar im Hintergrund.

Die konkrete Modellentscheidung (z. B. Wan oder LTX) treffen wir erst, wenn der KAGE X2 da ist und wir VRAM, Geschwindigkeit und Bildqualität auf der echten Hardware testen können.

## Wichtig

Noch wird kein echtes MP4 erzeugt. Der Server nimmt Aufträge entgegen und ist für die lokale Video-KI vorbereitet.

Der Server ist absichtlich standardmäßig nur lokal gebunden. Die spätere Fernverbindung vom iPad wird über ein privates Netzwerk wie Tailscale abgesichert – nicht über einen offenen Router-Port.
