# JALDORX KI-Animator – lokaler Job-Server

Der Ordner enthält den ersten echten Server-Baustein für den späteren **KAGE X2**.

## Start

Auf dem KAGE X2 reicht später zunächst:

```bash
python3 server/app.py
```

Der Server läuft standardmäßig nur auf:

```
http://127.0.0.1:8765
```

## Endpunkte

- `GET /health` – prüft, ob der Server läuft
- `GET /jobs` – listet Aufträge
- `GET /jobs/<id>` – zeigt einen Auftrag
- `POST /jobs` – nimmt einen neuen Videoauftrag an

## Auftrag

Beispiel:

```json
{
  "product": "EIGENES PRODUKT",
  "idea": "Mach was Gutes",
  "duration": "10",
  "format": "9:16",
  "image": null
}
```

## Wichtig

Das ist zunächst **nur die Auftragszentrale**. Noch keine Video-KI.

Der nächste Baustein wird die Verbindung dieses Servers mit **ComfyUI** und der später ausgewählten lokalen Video-KI.

Der Server ist absichtlich standardmäßig nur lokal gebunden. Die spätere Fernverbindung vom iPad wird über ein privates Netzwerk wie Tailscale abgesichert – nicht über einen offenen Router-Port.
